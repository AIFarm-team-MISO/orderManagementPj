import time
import pandas as pd
import os
import django

# Django 설정 파일을 지정
os.environ['DJANGO_SETTINGS_MODULE'] = 'order_management.settings'

# Django 설정을 로드
django.setup()

from order_management.config_loader import load_config
from order_management.crawling.selenium_driver import create_driver
from order_management.crawling.smartstore.login import login_to_smartstore
from order_management.crawling.popup_handler import close_popup_if_exists
from order_management.crawling.smartstore.page_navigation import go_to_shipping_management
from order_management.crawling.smartstore.shipmentpage_handle import download_excel_with_password
from order_management.config_loader import get_latest_file
from order_management.data_handle.orderlist_handle import decrypt_excel
from order_management.data_handle.models import Order

'''
    프로젝트의 각모듈의 테스트가 끝난후 배포될 메인 실행 페이지
    이후 모듈테스트가 끝난후 작성 예정
'''


def data_Handle():
        """
            엑셀 파일의 데이터를 처리하고, DB에 데이터를 저장 
        """

        # 설정과 환경 변수 로드
        config, timeout = load_config()  # config와 timeout을 각각 클래스 변수에 할당

        # 엑셀 설정 정보 
        excel_download_url = config['excel']['excel_download_url']  
        excel_password = config['excel']['excel_password']

        print('-- 데이터 테스트 시작 --')

        #다운로드 된 폴더의 가장 최신파일의 경로를 가져온다.        
        latest_file_path = get_latest_file(excel_download_url)
    
        # 데이터 전처리 : 엑셀 파일에서 필요한 열만 선택
        columns_to_extract = ["상품주문번호", "판매자 상품코드", "수취인명", "수취인연락처1", "상품명"]

        df = decrypt_excel(latest_file_path, excel_password, columns_to_extract)

        # 긴 문자열도 모두 표시하도록 설정 변경
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_columns', None)  # 모든 열 표시
        pd.set_option('display.max_rows', None)  # 모든 행 표시

        # 데이터프레임의 첫 몇 줄을 출력하여 제대로 읽혔는지 확인
        if df is not None and not df.empty:
            print('가져온 엑셀의 내용----------- : \n', df.head())
            # 데이터를 나중에 DB에 저장하기 위해 클래스 변수에 저장
        else:
            print("데이터프레임을 생성하는 데 실패했거나 데이터가 없습니다.")



        # 데이터프레임의 첫 몇 줄을 출력하여 제대로 읽혔는지 확인
        if df is not None and not df.empty:
            print('DB에 저장할 엑셀의 내용----------- : \n', df.head())

            # 데이터베이스에 저장된 항목 수를 추적하기 위한 카운터
            saved_count = 0
            skipped_count = 0

            # 데이터베이스에 저장
            for idx, (_, row) in enumerate(df.iterrows(), start=1):
                # 주문번호로 기존 데이터가 있는지 확인 후 저장
                if not Order.objects.filter(order_number=str(row["상품주문번호"]).strip()).exists():
                    order = Order(
                        order_number=row["상품주문번호"],
                        Product_code=row["판매자 상품코드"],
                        customer_name=row["수취인명"],
                        customer_phone=row["수취인연락처1"],
                        product_name=row["상품명"]

                    )
                    order.save()
                    saved_count += 1
                    print(f"{idx}. 주문번호 {row['상품주문번호']}가 성공적으로 데이터베이스에 저장되었습니다.")
                else:
                    skipped_count += 1
                    print(f"{idx}. 주문번호 {row['상품주문번호']}는 이미 데이터베이스에 존재합니다. 저장하지 않습니다.")

            # 최종 결과 출력
            print(f"\n총 {saved_count}개의 데이터가 데이터베이스에 저장되었습니다.")
            print(f"{skipped_count}개의 데이터는 이미 존재하여 저장되지 않았습니다.")

        else:
            print("데이터프레임이 비어 있거나 존재하지 않습니다.")

def main():
    try:
        # 설정과 환경 변수 로드
        config, timeout = load_config()  # config와 timeout을 각각 클래스 변수에 할당

        # 드라이버 설정
        driver_path = config['selenium']['driver_path']

        # 경로 설정
        base_url = config['selenium']['base_url']

        # 스마트스토어 접속 정보
        naver_id = config['smartstore']['naver_id']
        naver_pw = config['smartstore']['naver_pw']

        # 엑셀 설정 정보 
        excel_download_url = config['excel']['excel_download_url']  
        excel_pw = config['excel']['excel_password']

        # timeout
        timeout = config['selenium']['timeout']

        print('driver_path : ', driver_path)
        print('cls.base_url : ', base_url)
        print('cls.excel_download_url : ', excel_download_url)
        print('cls.naver_id : ', naver_id)
        print('cls.naver_pw : ', naver_pw)
        print('timeout : ', timeout)

        # WebDriver 생성
        driver = create_driver(driver_path, excel_download_url, headless=True)

        # 로그인
        login_to_smartstore(driver, base_url, naver_id, naver_pw, timeout)
        print('--------- 로그인 완료 ------------')

        # 팝업 닫기
        close_popup_if_exists(driver, "button.close", timeout)
        print('--------- 팝업 닫기 완료 ------------')

        # 배송준비 페이지로 이동
        go_to_shipping_management(driver, timeout)
        print('--------- 배송준비 페이지로 이동 완료 ------------')

        # 배송준비 페이지의 팝업 닫기
        close_popup_if_exists(driver, "button.close", timeout)
        print('--------- 배송준비 페이지의 팝업 닫기 완료 ------------')

        # 엑셀 파일 다운로드 및 저장
        download_excel_with_password(driver, excel_pw, excel_download_url, timeout)
        print('--------- 엑셀 파일 다운로드 및 저장 완료 ------------')

        # 페이지 로딩 대기
        time.sleep(10)


        data_Handle()


    except Exception as e:
        print(f"에러가 발생했습니다: {e}")
    finally:
        driver.quit()  # WebDriver 종료


if __name__ == "__main__":
    main()
