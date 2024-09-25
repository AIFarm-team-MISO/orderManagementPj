import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def close_popup_if_exists(driver, close_button_selector, timeout=5):
    try:
        print("스마트스토어센터 공지팝업")

        # 팝업 닫기 버튼을 찾아서 JavaScript로 강제 클릭
        popup_close_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, close_button_selector))
        )
        driver.execute_script("arguments[0].click();", popup_close_button) #자바스크립트로 되어 있는경우 팝업을 강제로 닫을 수 있다.

    

        print("팝업닫기 완료")

    except NoSuchElementException:
        print("팝업이 없습니다.")
    except Exception as e:
        print(f"팝업을 닫는 중 오류 발생: {e}")

