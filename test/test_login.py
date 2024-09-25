'''
    프로젝트의 각모듈을 실행하며 테스트 하기 위한 유닛테스트 코드

'''
import sys
import os
import time

# 모듈 임포트를 위한 경로 추가(order_management의 경로를 명시)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from order_management.config_loader import load_config, load_env
from order_management.selenium_driver import create_driver
from order_management.login import login_to_smartstore
from order_management.popup_handler import close_popup_if_exists
from order_management.page_navigation import go_to_shipping_management
from order_management.shipmentpage_handle import download_excel_with_password 
# from order_management.orderlist_handle import decrypt_excel

class TestSmartStoreLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('--------크롤링 환경설정--------')
        # 설정과 환경 변수 로드
        cls.config = load_config()
        cls.naver_id, cls.naver_pw , cls.excel_pw, cls.excel_download_url = load_env()

        # 드라이버 설정
        driver_path = cls.config['selenium']['driver_path']
        cls.base_url = cls.config['selenium']['base_url']
        cls.driver = create_driver(driver_path, cls.excel_download_url, headless=False)
        cls.driver.set_window_size(1600, 900)  # 창 크기를 설정

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

        
        # 설정파일 로드 (엑셀다운로드 저장위치, 엑셀저장 비밀번호)
        download_path = self.config['path']['download_path']     
        excel_pw = self.excel_pw

        # 엑셀다운로드 클릭 및 저장
        download_excel_with_password(self.driver, excel_pw, download_path)

        # 페이지 로딩 대기
        time.sleep(10)     








        

    @classmethod
    def tearDownClass(cls):
        print('종료프로세스')
        # 테스트 후 드라이버 종료
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()

    # 각각의 함수만 따로 테스트해볼경우 
    # suite = unittest.TestSuite()
    # suite.addTest(TestSmartStoreLogin('test_login')) 
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
