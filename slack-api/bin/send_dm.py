import json
import os

from dotenv import load_dotenv
from slack_sdk import WebClient

# 환경변수 로드
load_dotenv()

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def main():
    print("Slack Bot 시작...")

    # people.json 파일이 존재하면 로컬 데이터 사용
    people_file = os.path.join(os.path.dirname(__file__), "people.json")
    if os.path.exists(people_file):
        try:
            with open(people_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                users = data
            print("✅ 로컬 people.json 데이터 사용")
        except Exception as e:
            print(f"❌ people.json 읽기 실패: {e}")
            return
    else:
        # API 연결 테스트
        try:
            response = client.auth_test()
            print(f"✅ Slack 연결 성공! Bot: {response['user']}")
            users = client.users_list()
        except Exception as e:
            print(f"❌ 오류: {e}")
            return

    print("\n현재 워크스페이스 멤버들:")

    for user in users["members"]:
        if not user.get("deleted", False) and not user.get("is_bot", False):
            real_name = user["real_name"]
            team_name, name = "\t", ""
            if len(real_name.split("_")) < 2:
                name = real_name
            else:
                team_name = real_name.split("_")[1]
                name = real_name.split("_")[0]
            print(f"{team_name} (@{name}) - ID: {user['id']}")

    target = "U09DCP3CU92"
    for user in users["members"]:
        if user["id"] == target:
            print(user["real_name"])


def send_dm(user_id, content):
    """특정 사용자에게 DM 전송 테스트"""
    try:
        response = client.chat_postMessage(channel=user_id, text=content)
        print(f"✅ DM 전송 성공! 메시지 ID: {response['ts']}")
    except Exception as e:
        print(f"❌ DM 전송 실패: {e}")


if __name__ == "__main__":
    send_dm("U09DCP3CU92", "hello ${i}")
