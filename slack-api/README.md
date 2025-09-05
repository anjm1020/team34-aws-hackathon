# Slack Bot

## 설치 및 실행

1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate
```

2. 패키지 설치
```bash
pip install -r requirements.txt
```

3. 환경변수 설정
`.env` 파일에 Slack Bot Token과 Signing Secret을 설정하세요.

4. 봇 실행
```bash
python src/bot.py
```