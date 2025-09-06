# LinkedIn 프로필 처리 시스템

## 설치 방법

```bash
# 패키지 설치
pip3 install -r requirements.txt

# .env 파일 생성 (linkedin-scraper-mcp/.env 참고)
cp linkedin-scraper-mcp/.env.example .env
# .env 파일에 LinkedIn 계정 정보와 DB 정보 입력
```

## 실행 방법

```bash
# 1단계: 엑셀 → JSON 변환
python3 -c "
from excel_to_json import excel_to_json
excel_to_json('~/Downloads/networking.xlsx')
"

# 2단계: LinkedIn 스크래핑 + JSON 생성
python3 process_members.py

# 3단계: 아이스브레이킹 API + DB 업로드
python3 add_icebreaking.py
```

## 디렉토리 구조

```
linkedin/
├── excel_to_json.py
├── process_members.py
├── add_icebreaking.py
├── requirements.txt
├── .env
├── converted_json/
├── result/
└── linkedin-scraper-mcp/
    ├── main.py
    ├── postgres_config.py
    └── .env
```