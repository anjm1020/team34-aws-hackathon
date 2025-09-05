# Step 2: 개발 환경 설정 가이드

## 1. 프로젝트 디렉토리 구조 생성

### 1.1 기본 디렉토리 생성
```
slack-bot/
├── src/
│   └── bot.py (또는 bot.js)
├── .env
├── requirements.txt (Python) 또는 package.json (Node.js)
└── README.md
```

### 1.2 디렉토리 생성 명령어
```bash
mkdir -p src
touch src/bot.py
touch .env
touch requirements.txt
```

## 2. 개발 언어 선택 및 패키지 설치

### 2.1 Python 사용 시
```bash
# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 필요한 패키지 설치
pip install slack-sdk python-dotenv
```

**requirements.txt 내용:**
```
slack-sdk==3.26.2
python-dotenv==1.0.0
```

### 2.2 Node.js 사용 시
```bash
# package.json 초기화
npm init -y

# 필요한 패키지 설치
npm install @slack/bolt-js dotenv
```

**package.json 주요 의존성:**
```json
{
  "dependencies": {
    "@slack/bolt-js": "^3.17.1",
    "dotenv": "^16.3.1"
  }
}
```

## 3. 환경변수 파일 설정

### 3.1 .env 파일 생성
```bash
# .env 파일 내용
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
```

### 3.2 .gitignore 파일 생성
```bash
# .gitignore 내용
.env
venv/
node_modules/
__pycache__/
*.pyc
.DS_Store
```

## 4. 기본 프로젝트 파일 생성

### 4.1 Python용 기본 구조 (src/bot.py)
```python
import os
from dotenv import load_dotenv
from slack_sdk import WebClient

# 환경변수 로드
load_dotenv()

# Slack 클라이언트 초기화
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

def main():
    print("Slack Bot 시작...")

if __name__ == "__main__":
    main()
```

### 4.2 Node.js용 기본 구조 (src/bot.js)
```javascript
require('dotenv').config();
const { App } = require('@slack/bolt-js');

// Slack 앱 초기화
const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET
});

async function main() {
  console.log('Slack Bot 시작...');
}

main();
```

## 5. 개발 도구 설정 (선택사항)

### 5.1 Python 개발 도구
```bash
pip install black flake8  # 코드 포맷팅 및 린팅
```

### 5.2 Node.js 개발 도구
```bash
npm install --save-dev nodemon  # 자동 재시작
```

## 6. 완료 확인사항
- [ ] 프로젝트 디렉토리 구조 생성 완료
- [ ] 필요한 패키지 설치 완료
- [ ] .env 파일 생성 및 토큰 설정 완료
- [ ] .gitignore 파일 생성 완료
- [ ] 기본 봇 파일 생성 완료

## 다음 단계
Step 3: 기본 봇 코드 구현으로 진행