import os
import json
import psycopg2
from dotenv import load_dotenv
from slack_sdk import WebClient

# 환경변수 로드
load_dotenv()

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

def get_peoples():
    """Slack 워크스페이스 멤버 정보를 가져와 people.json에 저장"""
    try:
        response = client.auth_test()
        print(f"✅ Slack 연결 성공! Bot: {response['user']}")

        users = client.users_list()
        
        with open('people.json', 'w', encoding='utf-8') as f:
            json.dump(users.data, f, ensure_ascii=False, indent=2)
        print("✅ people.json 파일로 저장 완료!")
        return True
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def is_same_team(user_1, user_2):
    """두 사용자가 같은 팀인지 확인"""
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
        try:
            users = client.users_list()
        except Exception as e:
            print(f"❌ Slack API 오류: {e}")
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
                user_1_team = team_name
            if user["id"] == user_2:
                user_2_team = team_name
    
    return user_1_team == user_2_team

def get_members_without_meeting():
    """PostgreSQL에서 미팅이 배정되지 않은 멤버들 조회"""
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT", 5432)
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, data FROM member WHERE has_meeting = false")
        members = cursor.fetchall()
        
        conn.close()
        return members
    except Exception as e:
        print(f"❌ DB 연결 실패: {e}")
        # 테스트용 가상 데이터 반환
        return [
            ('U09E8FX7GAC', '김민석'),
            ('U09CU4ZJ9NH', '정재민_AWS_SA'),
            ('U09CUB0BU95', '곽혜정_QQQ'),
            ('U09CUBD6VPZ', '최정은_QQQ')
        ]

def generate_meeting_pairs(max_pairs):
    """다른 팀 멤버끼리 미팅 페어 생성 (최대 5개 페어)"""
    members = get_members_without_meeting()
    pairs = []
    used = set()
    
    for i in range(len(members)):
        if len(pairs) >= max_pairs:  # 5개 페어 제한
            break
        if members[i][0] in used:
            continue
        for j in range(i + 1, len(members)):
            if members[j][0] in used:
                continue
            if not is_same_team(members[i][0], members[j][0]):
                pairs.append((members[i], members[j]))
                used.add(members[i][0])
                used.add(members[j][0])
                break
    
    remaining = [member for member in members if member[0] not in used]
    if remaining:
        print(f"남은 멤버: {len(remaining)}명")
    
    return pairs

def create_meetings(pairs):
    """미팅 페어를 meeting 테이블에 저장 (장소 겹치지 않게)"""
    import random
    
    # 1~5 장소를 섞어서 순차 배정
    places = list(range(1, 6))  # [1, 2, 3, 4, 5]
    random.shuffle(places)
    
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT", 5432)
        )
        cursor = conn.cursor()
        
        for i, pair in enumerate(pairs):
            place = places[i]  # 겹치지 않는 장소 배정
            cursor.execute(
                "INSERT INTO meeting (member_meeting_id1, member_meeting_id2, accept, time, place) VALUES (%s, %s, %s, %s, %s)",
                (pair[0][0], pair[1][0], False, None, place)
            )
            
            # member_meeting 테이블에 각 멤버 삽입 (수락 시 True)
            cursor.execute(
                "INSERT INTO member_meeting (member_id, accept) VALUES (%s, %s)",
                (pair[0][0], True)
            )
            cursor.execute(
                "INSERT INTO member_meeting (member_id, accept) VALUES (%s, %s)",
                (pair[1][0], True)
            )
            
            print(f"   페어 {i+1}: {pair[0][1]} ↔ {pair[1][1]} (장소: {place})")
        
        conn.commit()
        conn.close()
        print("✅ DB에 미팅 정보 저장 완료")
        
    except Exception as e:
        print(f"❌ DB 저장 실패: {e}")
        # 테스트용 콘솔 출력
        for i, pair in enumerate(pairs):
            place = places[i]
            print(f"   페어 {i+1}: {pair[0][1]} ↔ {pair[1][1]} (장소: {place})")
            print(f"   member_meeting 테이블에 {pair[0][1]}, {pair[1][1]} 삽입 (accept: True)")

def send_dm(user_id, content):
    """특정 사용자에게 DM 전송"""
    try:
        response = client.chat_postMessage(channel=user_id, text=content)
        print(f"✅ DM 전송 성공! 메시지 ID: {response['ts']}")
        return True
    except Exception as e:
        print(f"❌ DM 전송 실패: {e}")
        return False

def main():
    """전체 프로세스 실행"""
    print("🚀 팀 미팅 매칭 시스템 테스트 시작")
    
    # 1. Slack 사용자 정보 수집
    print("\n1️⃣ Slack 사용자 정보 수집 중...")
    if not get_peoples():
        print("❌ 사용자 정보 수집 실패")
        return
    
    # 2. 미팅 페어 생성
    print("\n2️⃣ 미팅 페어 생성 중...")
    pairs = generate_meeting_pairs(5)
    print(f"✅ {len(pairs)}개의 미팅 페어 생성 완료 (최대 5개 제한)")
    
    # 3. 데이터베이스에 저장
    print("\n3️⃣ 데이터베이스에 저장 중...")
    create_meetings(pairs)
    print("✅ 미팅 정보 저장 완료")
    
    # 4. 테스트 DM 전송 (나에게만)
    print("\n4️⃣ 테스트 DM 전송 중...")
    test_message = f"🤖 팀 미팅 매칭 테스트 완료!\n\n📋 생성된 페어 수: {len(pairs)}개\n\n생성된 페어:\n"
    for i, pair in enumerate(pairs, 1):
        test_message += f"{i}. {pair[0][1]} ↔ {pair[1][1]}\n"
    
    if send_dm("U09E8FX7GAC", test_message):
        print("✅ 테스트 DM 전송 완료")
    
    print("\n🎉 팀 미팅 매칭 테스트 완료!")

if __name__ == "__main__":
    main()