from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def create_driver(driver_path, download_dir=None, headless=False):
    chrome_options = Options()
    
    # 기본 다운로드 경로 설정
    if download_dir:
        prefs = {
            "download.default_directory": download_dir, #파일을 다운로드할 기본 경로를 지정
            "download.prompt_for_download": False, #다운로드 시 경로를 묻는 팝업을 비활성화
            "download.directory_upgrade": False, #다운로드 경로를 덮어쓰기 허용
            "safebrowsing.enabled": True #안전하지 않은 파일을 다운로드할 때 경고를 방지
        }
        chrome_options.add_experimental_option("prefs", prefs)

    # 헤드리스 모드 설정 (필요한 경우)
    if headless:
        chrome_options.add_argument("--headless")  # 브라우저 창을 열지 않고 실행
    
    # WebDriver 서비스 생성
    service = Service(executable_path=driver_path)
    
    # WebDriver 생성
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver