import sys
import os
import time

# 모듈 임포트를 위한 경로 추가(order_management의 경로를 명시)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from order_management.config_loader import load_config
from order_management.crawling.selenium_driver import create_driver
from order_management.crawling.smartstore.login import login_to_smartstore
from order_management.crawling.popup_handler import close_popup_if_exists
from order_management.crawling.smartstore.page_navigation import go_to_shipping_management
from order_management.crawling.smartstore.shipmentpage_handle import download_excel_with_password 

'''
    스마트스토어의 로그인 및 배송예정 리스트 엑셀 다운로드

    현재 헤드리스 모드일때 창이 켜지는 문제가 있지만 테스트모두 통과 되었음.
    그러면 설정파일을 시스템에 따라 다르게 읽히는 부분만 추가해서 서버에서 테스트 해보자. 
    


'''
class TestSmartStoreLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('-- 테스트시작 --')
        print('--------크롤링 환경설정--------')
        # 설정과 환경 변수 로드
        cls.config = load_config()

        # 드라이버 설정
        driver_path = cls.config['selenium']['driver_path']

        # 접속 경로설정 
        cls.base_url = cls.config['selenium']['base_url']

        # 스마트스토어 접속 정보
        cls.naver_id = cls.config['smartstore']['naver_id']
        cls.naver_pw = cls.config['smartstore']['naver_pw']

        # 엑셀비밀번호 
        cls.excel_download_url= cls.config['excel']['excel_download_url']
        cls.excel_pw = cls.config['excel']['excel_password']

        print('driver_path : ', driver_path)
        print('cls.base_url : ', cls.base_url)
        print('cls.excel_download_url : ', cls.excel_download_url)
        print('cls.naver_id : ', cls.naver_id)
        print('cls.naver_pw : ', cls.naver_pw)

        cls.driver = create_driver(driver_path, cls.excel_download_url, headless=True)

    # 스마트스토어센터 로그인
    def test_01_login(self):
        print('-------- 로긴테스트시작-------- ')
        
        # 로그인 테스트 실행
        login_to_smartstore(self.driver, self.base_url, self.naver_id, self.naver_pw)

        # 로그인 후 페이지 타이틀이나 URL 등을 확인
        self.assertIn("네이버 스마트스토어센터", self.driver.title)

    # 스마트스토어센터 공지팝업 닫기
    def test_02_popup_handle(self):
        print('-------- 메인페이지 팝업처리 시작-------- ')

        close_popup_if_exists(self.driver, "button.close")
         
    # 배송준비 숫자를 클릭해서 배송준비페이지로 이동
    def test_03_page_navi(self):
        print('-------- 배송관리 페이지이동 시작-------- ')

        go_to_shipping_management(self.driver)
         
    # 배송준비페이지의 팝업 닫기 및 배송준비 주문건 다운로드
    def test_04_shipmentlist_handle(self):
        print('-------- 배송관리 페이지 처리시작-------- ')

        # 배송준비페이지의 팝업 닫기
        close_popup_if_exists(self.driver, "button.close")

    

        # 엑셀다운로드 클릭 및 저장
        download_excel_with_password(self.driver, self.excel_pw, self.excel_download_url)

        # 페이지 로딩 대기
        time.sleep(10)     
          

    @classmethod
    def tearDownClass(cls):
        print('-- 테스트 종료 --')
        # 테스트 후 드라이버 종료
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()

    # 각각의 함수만 따로 테스트해볼경우 
    # suite = unittest.TestSuite()
    # suite.addTest(TestSmartStoreLogin('test_orderlist_handle')) 
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
