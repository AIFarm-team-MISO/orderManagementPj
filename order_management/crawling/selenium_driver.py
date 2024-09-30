from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os


'''
크롬 드라이버 초기화 및 셋팅

'''
def create_driver(driver_path, download_dir=None, headless=True):
    chrome_options = Options()
    
    print('다운로드 폴더 : ', download_dir)

    # 기본 다운로드 경로 설정
    if download_dir:
        prefs = {
            "download.default_directory": download_dir, #파일을 다운로드할 기본 경로를 지정
            "download.prompt_for_download": False, #다운로드 시 경로를 묻는 팝업을 비활성화
            "download.directory_upgrade": False, #다운로드 경로를 덮어쓰기 허용
            "safebrowsing.enabled": True #안전하지 않은 파일을 다운로드할 때 경고를 방지
        }
        chrome_options.add_experimental_option("prefs", prefs)

    # 로그 파일 경로 설정
    log_dir = "F:/orderManagementPj/logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "chromedriver.log")

    # 헤드리스 모드(브라우저 창을 열지 않고 실행) 설정 (필요한 경우)
    if headless:
        chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--window-size=1920x1080')
        # chrome_options.add_argument('--remote-debugging-port=9222')  # 추가: 디버깅 포트 설정
        # chrome_options.add_argument('--incognito')  # 브라우저를 시크릿 모드로 실행
        # chrome_options.add_argument('--disable-cache')  # 캐시를 비활성화
        # chrome_options.add_argument('--log-level=ALL')  # 로그 레벨을 설정하여 모든 로그 기록
    
    
        log_dir = "F:/orderManagementPj/logs"  # 로그 파일을 저장할 디렉터리 설정
        os.makedirs(log_dir, exist_ok=True)  # 디렉터리가 없으면 생성

        log_path = os.path.join(log_dir, "chromedriver.log")

    # WebDriver 서비스 생성
    
    service = Service(executable_path=driver_path, log_path=log_path)
    
    # WebDriver 생성
    driver = webdriver.Chrome(service=service, options=chrome_options)

    if headless:
            driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
                "width": 1600,
                "height": 900,
                "deviceScaleFactor": 0,
                "mobile": False
            })
            driver.execute_cdp_cmd('Network.enable', {})
            driver.execute_cdp_cmd('Page.enable', {})
            driver.execute_cdp_cmd('Security.enable', {})

    driver.set_window_size(1600, 900)
    
    return driver