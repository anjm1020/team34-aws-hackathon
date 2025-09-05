# Step 1: Slack Bot 생성 가이드

## 1. Slack App 생성

### 1.1 Slack API 사이트 접속
- https://api.slack.com/apps 접속
- "Create New App" 버튼 클릭

### 1.2 앱 생성 방법 선택
- "From scratch" 선택
- App Name 입력 (예: "My Bot")
- 워크스페이스 선택
- "Create App" 클릭

## 2. Bot 기본 설정

### 2.1 OAuth & Permissions 설정
- 좌측 메뉴에서 "OAuth & Permissions" 클릭
- "Scopes" 섹션으로 스크롤
- "Bot Token Scopes"에서 다음 권한 추가:
  - `chat:write` - 메시지 전송
  - `channels:read` - 채널 정보 읽기
  - `users:read` - 사용자 정보 읽기

### 2.2 Bot Token 설치
- 페이지 상단 "Install to Workspace" 클릭
- 권한 확인 후 "Allow" 클릭
- "Bot User OAuth Token" 복사 (xoxb-로 시작)

## 3. Bot 사용자 설정

### 3.1 App Home 설정
- 좌측 메뉴에서 "App Home" 클릭
- "Your App's Presence in Slack" 섹션에서:
  - Display Name 설정
  - Default Username 설정

## 4. 토큰 보안 관리

### 4.1 환경변수 준비
- Bot User OAuth Token을 안전하게 보관
- 코드에 직접 하드코딩하지 말고 환경변수 사용 예정

## 5. 완료 확인사항
- [x] Slack App 생성 완료
- [x] Bot Token Scopes 권한 설정 완료
- [x] Bot User OAuth Token 발급 완료
- [x] 토큰을 안전한 곳에 저장 완료

## 다음 단계
Step 2: 개발 환경 설정으로 진행