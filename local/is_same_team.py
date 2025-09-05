import os
import json

from dotenv import load_dotenv
from slack_sdk import WebClient

# 환경변수 로드
load_dotenv()

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def is_same_team(user_1, user_2):
    # people.json 파일이 존재하면 로컬 데이터 사용
    people_file = os.path.join(os.path.dirname(__file__), 'people.json')
    if os.path.exists(people_file):
        try:
            with open(people_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                users = data
        except Exception as e:
            print(f"❌ people.json 읽기 실패: {e}")
            return False
    else:
        # API 호출
        try:
            response = client.auth_test()
            print(f"✅ Slack 연결 성공! Bot: {response['user']}")
            users = client.users_list()
        except Exception as e:
            print(f"❌ 오류: {e}")
            return False

    user_1_team = ""
    user_2_team = ""

    for user in users["members"]:
        if not user.get("deleted", False) and not user.get("is_bot", False):
            real_name = user["real_name"]
            team_name = ""
            if len(real_name.split("_")) >= 2:
                team_name = real_name.split("_")[1]
            if user["id"] == user_1:
                print("user1: ", real_name)
                user_1_team = team_name
            if user["id"] == user_2:
                print("user2: ", real_name)
                user_2_team = team_name
    return user_1_team == user_2_team


def send_dm(user_id, content):
    """특정 사용자에게 DM 전송 테스트"""
    try:
        response = client.chat_postMessage(channel=user_id, text=content)
        print(f"✅ DM 전송 성공! 메시지 ID: {response['ts']}")
    except Exception as e:
        print(f"❌ DM 전송 실패: {e}")


if __name__ == "__main__":
    print(is_same_team("U09DFKY0GAE", "U09DCP3CU92"))