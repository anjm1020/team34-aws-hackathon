import os
import json

from dotenv import load_dotenv
from slack_sdk import WebClient

# 환경변수 로드
load_dotenv()

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def main():
    print("Slack Bot 시작...")

    # API 연결 테스트
    try:
        response = client.auth_test()
        print(f"✅ Slack 연결 성공! Bot: {response['user']}")

        # 워크스페이스 멤버 목록 확인
        users = client.users_list()
        
        # JSON 파일로 저장
        with open('people.json', 'w', encoding='utf-8') as f:
            json.dump(users.data, f, ensure_ascii=False, indent=2)
        print("✅ people.json 파일로 저장 완료!")

    except Exception as e:
        print(f"❌ 오류: {e}")


def send_dm(user_id, content):
    """특정 사용자에게 DM 전송 테스트"""
    try:
        response = client.chat_postMessage(channel=user_id, text=content)
        print(f"✅ DM 전송 성공! 메시지 ID: {response['ts']}")
    except Exception as e:
        print(f"❌ DM 전송 실패: {e}")


if __name__ == "__main__":
    main()
