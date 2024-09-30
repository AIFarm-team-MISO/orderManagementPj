import sys
import os
import unittest
import django

# 모듈 임포트를 위한 경로 추가(order_management의 경로를 명시)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Django 설정 파일을 지정
os.environ['DJANGO_SETTINGS_MODULE'] = 'order_management.settings'

# Django 설정을 로드
django.setup()

from order_management.config_loader import load_config
from order_management.data_handle.orderlist_handle import decrypt_excel
from order_management.config_loader import get_latest_file
import pandas as pd
from order_management.data_handle.models import Order


'''
    -- 할일 --
    데이터베이스 설계 및 테이블생성 - 완료
    데이터베이스 데이터 저장
    웹 페이지에서 데이터 표시
    스마트폰 접근을 위한 최적화
    
'''
class TestDataHandle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('-- 테스트 시작 --')
        
        # 설정과 환경 변수 로드
        cls.config, cls.timeout = load_config()  # config와 timeout을 각각 클래스 변수에 할당

        # 엑셀 설정 정보 
        cls.excel_download_url = cls.config['excel']['excel_download_url']  
        cls.excel_password = cls.config['excel']['excel_password']
    

    # 다운로드된 배송준비 엑셀파일 처리 
    def test_01_excelRead(self):
        print('-------- 배송준비 엑셀파일 처리시작-------- ')

        #다운로드 된 폴더의 가장 최신파일의 경로를 가져온다.        
        latest_file_path = get_latest_file(self.excel_download_url)
    
        # 데이터 전처리 : 엑셀 파일에서 필요한 열만 선택
        columns_to_extract = ["상품주문번호", "판매자 상품코드", "수취인명", "수취인연락처1", "상품명"]

        df = decrypt_excel(latest_file_path, self.excel_password, columns_to_extract)

        # 긴 문자열도 모두 표시하도록 설정 변경
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_columns', None)  # 모든 열 표시
        pd.set_option('display.max_rows', None)  # 모든 행 표시

        # 데이터프레임의 첫 몇 줄을 출력하여 제대로 읽혔는지 확인
        if df is not None and not df.empty:
            print('가져온 엑셀의 내용----------- : \n', df.head())
            # 데이터를 나중에 DB에 저장하기 위해 클래스 변수에 저장
            self.__class__.df = df
        else:
            self.fail("데이터프레임을 생성하는 데 실패했거나 데이터가 없습니다.")

        # TODO: 같은 사람이 여러 개의 묶음을 주문한 경우를 판별하는 플래그 필드 추가
        # TODO: 데이터 입력시간등 주문이 발생한 날짜도 db에 저장해야할듯 

        

    def test_02_DBSave(self):  
        # 데이터프레임의 첫 몇 줄을 출력하여 제대로 읽혔는지 확인
        if self.__class__.df is not None and not self.__class__.df.empty:
            print('DB에 저장할 엑셀의 내용----------- : \n', self.__class__.df.head())

            # 데이터베이스에 저장된 항목 수를 추적하기 위한 카운터
            saved_count = 0
            skipped_count = 0

            # 데이터베이스에 저장
            for idx, (_, row) in enumerate(self.__class__.df.iterrows(), start=1):
                # 주문번호로 기존 데이터가 있는지 확인 후 저장
                if not Order.objects.filter(order_number=row["상품주문번호"]).exists():
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
            self.fail("데이터프레임이 비어 있거나 존재하지 않습니다.")


    @classmethod
    def tearDownClass(cls):
        print('-- 테스트 종료 --')
        
if __name__ == "__main__":
    unittest.main()

    # 각각의 함수만 따로 테스트해볼경우 
    # suite = unittest.TestSuite()
    # suite.addTest(TestDataHandle('test_02_DBSave')) 
    # runner = unittest.TextTestRunner()
    # runner.run(suite)