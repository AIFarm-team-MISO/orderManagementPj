import time

from order_management.config_loader import load_config, load_smartstorelogin_env
from order_management.crawling.selenium_driver import create_driver
from order_management.crawling.smartstore.login import login_to_smartstore
from order_management.crawling.popup_handler import close_popup_if_exists
from order_management.crawling.smartstore.page_navigation import go_to_shipping_management
from order_management.crawling.smartstore.shipmentpage_handle import download_excel_with_password

'''
    프로젝트의 각모듈의 테스트가 끝난후 배포될 메인 실행 페이지
    이후 모듈테스트가 끝난후 작성 예정
'''
def main():

    # 설정과 환경 변수 로드
    config = load_config()
    naver_id, naver_pw , excel_pw, excel_download_url = load_smartstorelogin_env()

    # 드라이버 설정
    driver_path = config['selenium']['driver_path']
    base_url = config['selenium']['base_url']
    driver = create_driver(driver_path, headless=False)
    driver.set_window_size(1600, 900)  # 창 크기를 설정

    try:
        # 로그인
        login_to_smartstore(driver, base_url, naver_id, naver_pw)

        # 팝업 닫기
        close_popup_if_exists(driver)

        # 배송준비 페이지로 이동
        go_to_shipping_management(driver)

        # 배송준비페이지의 팝업 닫기
        close_popup_if_exists(driver, "button.close")

        
        # 설정파일 로드 (엑셀다운로드 저장위치, 엑셀저장 비밀번호)
        download_path = config['path']['download_path']     
        excel_pw = excel_pw

        # 엑셀 파일 다운로드 및 저장
        download_excel_with_password(driver, excel_pw, download_path)

        # 페이지 로딩 대기
        time.sleep(10)  




    except Exception as e:
        print(f"에러가 발생했습니다: {e}")
    finally:
        driver.quit()  # WebDriver를 반드시 종료

if __name__ == "__main__":
    main()
