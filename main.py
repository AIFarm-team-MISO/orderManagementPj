from order_management.config_loader import load_config, load_env
from order_management.selenium_driver import create_driver
from order_management.login import login_to_smartstore
from order_management.popup_handler import close_popup_if_exists
from order_management.page_navigation import go_to_shipping_management

'''
    프로젝트의 각모듈의 테스트가 끝난후 배포될 메인 실행 페이지
    이후 모듈테스트가 끝난후 작성 예정
'''
def main():
    # 설정 로드
    config = load_config()
    naver_id, naver_pw = load_env()

    # 드라이버 설정
    driver_path = config['selenium']['driver_path']
    base_url = config['selenium']['base_url']
    driver = create_driver(driver_path, headless=False)

    try:
        # 로그인
        login_to_smartstore(driver, base_url, naver_id, naver_pw)

        # 팝업 닫기
        close_popup_if_exists(driver)

        # 배송준비 페이지로 이동
        go_to_shipping_management(driver)

        # 이후 작업 수행...
        print("프로그램이 정상적으로 실행 완료!")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
