# order_management/page_navigation.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def go_to_shipping_management(driver, timeout=10):
    try:
        # "배송준비" 의 숫자 링크 클릭 (ui-sref를 사용한 요소)
        shipping_management_link = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.text-number[data-nclicks-code='orddel.wait']"))
        )
        print("배송준비 링크를 클릭합니다.")
        shipping_management_link.click()

        # 페이지 로딩 대기
        WebDriverWait(driver, timeout).until(
            EC.title_contains("배송준비")
        )
        print("배송준비 페이지로 전환되었습니다.")
        
    except NoSuchElementException:
        print("배송준비 링크를 찾을 수 없습니다.")
    except TimeoutException:
        print("페이지 로딩 시간 초과")
    except Exception as e:
        print(f"배송준비 페이지로 이동 중 오류 발생: {e}")
