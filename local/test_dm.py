import os
from dotenv import load_dotenv
from slack_sdk import WebClient

# 환경변수 로드
load_dotenv()

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

def test_send_dm():
    """테스트용 DM 전송 - U09E8FX7GAC (김민석)에게만"""
    test_user_id = "U09E8FX7GAC"
    test_message = "🤖 테스트 메시지입니다! 팀 미팅 매칭 시스템이 정상 작동 중입니다."
    
    try:
        response = client.chat_postMessage(
            channel=test_user_id, 
            text=test_message
        )
        print(f"✅ 테스트 DM 전송 성공!")
        print(f"📧 수신자: 김민석 (U09E8FX7GAC)")
        print(f"📨 메시지 ID: {response['ts']}")
        return True
    except Exception as e:
        print(f"❌ 테스트 DM 전송 실패: {e}")
        return False

if __name__ == "__main__":
    print("🧪 DM 전송 테스트 시작")
    test_send_dm()