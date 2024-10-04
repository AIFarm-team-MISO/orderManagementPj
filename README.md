# 쇼핑몰 주문 및 송장 관리 자동화 시스템 (orderManagementPj)

## 프로젝트 개요
이 프로젝트는 **쇼핑몰 주문 처리와 송장 발송 과정을 자동화**하는 시스템입니다. 
여러 쇼핑몰에서 발생한 주문을 자동으로 크롤링하여 **데이터베이스(DB)**에 저장하고, 
도매 사이트로부터 송장을 수집한 후, 쇼핑몰에 **자동으로 발송 처리**를 합니다. 
이 시스템은 **수작업의 비효율성을 개선**하고 **정확성을 높여** 
작업 시간을 크게 단축하는 것을 목표로 합니다.

프로젝트는 **Python**과 **Django 프레임워크**를 기반으로 설계되어, **빠른 개발 및 유지보수**가 용이하며
Django의 **ORM(Object-Relational Mapping)**을 통해 데이터베이스 처리 작업이 간편하며, 
**모듈화된 코드 구조**로 확장성과 재사용성을 극대화하였습니다. 
또한, **AWS EC2 우분투 서버**를 활용하여 시스템의 **안정성**과 **확장성**을 확보하고, 
클라우드 기반으로 어디서든 접근 가능한 환경을 구축하였습니다. 
AWS를 통한 서버 관리로 **자동화 작업**을 주기적으로 실행하고, 
대용량 트래픽 처리 및 보안성을 강화할 수 있는 클라우드 환경을 구축했습니다.

이 프로젝트는 **효율적인 백엔드 관리**와 **유지보수 용이성**을 염두에 두어 
실시간 주문 및 발송 관리의 자동화 시스템을 성공적으로 구현한 MVP입니다.


## 프로젝트 플로우
- 스마트스토어 자동 로그인 및 주문 데이터 다운로드
Selenium을 사용해 스마트스토어에 자동으로 로그인
배송페이지로 이동하여 배송 준비 상태의 주문 내역을 엑셀 파일로 다운로드 

- 엑셀 파일 비밀번호 해제 및 데이터 처리
다운로드한 엑셀 파일의 비밀번호를 자동으로 해제하고 데이터를 추출

- MySQL 데이터베이스 저장 및 웹 페이지에서 조회
추출한 데이터를 Django 모델로 변환하여 MySQL 데이터베이스에 저장

## 향후 개발예정 기능
- 도매 사이트로부터 송장데이터 취합 및 쇼핑몰 발송처리
도매 사이트에서 주문 건의 송장을 조회하고, 송장을 스마트스토어에 자동 입력하여 발송처리.

- 자동화 주기 실행
모든 작업은 30분 간격으로 자동화되어 주기적으로 실행.

- 연동 쇼핑몰 추가
현재 스마트스토어 외 오픈마켓 추가 예정

## 프로젝트 파일 구조 
orderManagementPj/
│
├── manage.py                   # Django 프로젝트 관리 명령어 파일
├── order_management/            # 메인 애플리케이션 폴더
│   ├── __init__.py              # 패키지 초기화 파일
│   ├── crawling/                # 데이터 크롤링을 위한 모듈
│   │   └── __init__.py
│   │   └── selenium_driver.py   # Selenium 크롬 드라이버 설정
│   │   ├── smartstore/          # 스마트스토어 관련 모듈
│   │       └── __init__.py
│   │       └── login.py         # 로그인 관련 기능
│   │       └── shipmentpage_handle.py # 배송 페이지 처리
│   │       └── page_navigation.py    # 페이지 이동 처리
│   ├── data_handle/             # 데이터 관리(엑셀, DB) 관련 모듈
│   │   └── __init__.py
│   │   ├── migrations/          # Django 마이그레이션 파일
│   │       └── __init__.py
│   │       └── 0001_initial.py  # 첫 마이그레이션 파일
│   │   └── orderlist_handle.py  # 엑셀 파일을 처리하고 DB 저장
│   │   └── models.py            # 데이터베이스 모델 정의
│   ├── web/                     # 웹 관련 모듈 (템플릿 및 정적 파일 포함)
│   │   └── __init__.py
│   │   └── views.py             # 웹 페이지의 비즈니스 로직 처리
│   │   └── urls.py              # URL 라우팅
│   │   ├── templates/           # HTML 템플릿 파일
│   │       └── web_handle/
│   │           └── order_list.html  # 주문 리스트 웹 페이지 템플릿
│   │   ├── static/              # 정적 파일(CSS, JS) 폴더
│   │       └── css/
│   │           └── style.css    # CSS 파일
│   │       └── js/
│   │           └── script.js    # 자바스크립트 파일
├── test/                        # 테스트 코드 폴더
│   └── __init__.py
│   └── test_login.py            # 로그인 테스트
│   └── test_data_handle.py       # 데이터 처리 테스트
├── doc/                         # 프로젝트 문서 폴더
│── config.ini                   # 환경 설정 파일 (로컬)
│── config_server.ini            # 환경 설정 파일 (서버)
│── main.py                      # 메인 실행 파일
└── requirements.txt             # 프로젝트 의존성 패키지 목록


## 주요 기능 및 특징
- 자동화된 주문 처리
스마트스토어에서 수작업 없이 자동으로 주문 데이터를 수집하고, 엑셀 파일을 다운로드한 후 비밀번호를 해제하여 데이터를 추출.

- 보안 강화
엑셀 파일에 설정된 비밀번호를 자동으로 해제하여 
개인정보 보호를 유지하고, 고객 정보(이름, 연락처, 주소 등)를 안전하게 처리하여 외부 노출을 방지

- 데이터베이스 연동 및 반응형 웹 페이지 
Django 프레임워크를 통해 MySQL 데이터베이스에 주문 데이터를 저장하고, 이를 웹 페이지에서 조회 가능.
반응형으로 제작되어 PC와 모바일에서도 원활한 데이터 접근이 가능.

- AWS 서버 배포 및 안정성 
AWS EC2 우분투 서버에 배포하여 외부에서도 웹 페이지와 데이터베이스에 안정적으로 접근할 수 있으며, 
클라우드 환경을 통해 서버 확장성과 보안이 보장됨.

## 기술 스택
- **프로그래밍 언어**: Python
- **웹 프레임워크**: Django
- **데이터베이스**: MySQL
- **웹 크롤링 및 자동화**: Selenium
- **서버 배포**: AWS Ubuntu, Nginx
- **버전 관리**: Git, GitHub
- **원격 서버 관리**: PuTTY, VNC

## 프로젝트설치 및 실행 방법
- 로컬 환경에서 실행하는 방법
1. Git_hub 리포지토리를 클론합니다.
    git clone https://github.com/AIFarm-team-MISO/orderManagementPj.git

2. 가상 환경을 생성하고 활성화합니다.
    python -m venv myenv
    source myenv/bin/activate  # Windows에서는 myenv\Scripts\activate

3. 필요한 패키지를 설치합니다.
    pip install -r requirements.txt

4. 데이터베이스 설치후 설정을 완료하고 마이그레이션을 실행합니다
    python manage.py makemigrations
    python manage.py migrate

5. 테스크 코드 및 메인코드 실행 
테스트 코드는 각각의 테스트를 실행함으로서 각가의 모듈의 테스트가 가능합니다. 
메인코드 는 프로젝트의 모든 모듈이 실행됩니다. 

    python main.py                             # 메인코드
    python3 -m unittest test.test_login        # 테스트코드1 : 스마트스토어 로그인 및 배송리스트 엑셀파일 다운로드
    python3 -m unittest test.test_data_handle  # 테스트코드2 : 엑셀파일 데이터 추출 및 DB저장

    *** 헤드리스 모드를 off 로 코드에서 변경후 실행하면 테스트코드1의 브라우저의 흐름이 확인됩니다. 
    # WebDriver 생성
    driver = create_driver(driver_path, excel_download_url, headless=False)

6. 웹페이지 확인
    python manage.py runserver       #Django서버 실행
    http://127.0.0.1:8000/ 로 접속   #웹브라우저에서 실행

- 서버 환경에서 실행하는 방법
1. 원격접속를 이용한 서버접속 및 실행 (RealVNC Viewer 설치 후 실행)
    connect : 3.39.6.220:5901
    pw : 3886

2. 테스크 코드 및 메인코드 실행 
    python3 main.py                            #메인코드
    python3 -m unittest test.test_login        #스마트스토어 로그인 및 배송리스트 엑셀파일 다운로드
    python3 -m unittest test.test_data_handle  #엑셀파일 데이터 추출 및 DB저장

3. 웹페이지 확인
웹브라우저에서 http://3.39.6.220/ 로 접속


### 테스트 사전 요구 사항
- Python 3.x
- MySQL
- Git
- VNC Viewer

## 시연 영상 및 스크린샷
아래의 링크로 시연영상 및 스크린샷 확인이 가능
https://drive.google.com/drive/folders/1Dnj0V_STk4qp_d6Dxbs8WYTAshFUFgOD?usp=drive_link


## 작성자 정보 및 연락처
이름: 최진호
이메일: sevenstar15@naver.com
GitHub: https://github.com/AIFarm-team-MISO

