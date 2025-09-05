import os

from dotenv import load_dotenv
from slack_sdk import WebClient

# 환경변수 로드
load_dotenv()

# Slack 클라이언트 초기화
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def main():
    print("Slack Bot 시작...")

    # API 연결 테스트
    try:
        response = client.auth_test()
        print(f"✅ Slack 연결 성공! Bot: {response['user']}")

        # 워크스페이스 멤버 목록 확인
        users = client.users_list()
        print("\n현재 워크스페이스 멤버들:")
        for user in users["members"]:
            if not user.get("deleted", False) and not user.get("is_bot", False):
                print(f"- {user['real_name']} (@{user['name']}) - ID: {user['id']}")

    except Exception as e:
        print(f"❌ 오류: {e}")


def send_dm_test(user_id):
    """특정 사용자에게 DM 전송 테스트"""
    try:
        response = client.chat_postMessage(
            channel=user_id, text="테스트 메시지입니다! 🚀 DM 전송이 성공했습니다."
        )
        print(f"✅ DM 전송 성공! 메시지 ID: {response['ts']}")
    except Exception as e:
        print(f"❌ DM 전송 실패: {e}")


if __name__ == "__main__":
    main()

    # DM 테스트 실행
    user_id = "U09DCP3CU92"  # Jaemin Jung
    send_dm_test(user_id)
