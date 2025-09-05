import sqlite3
from is_same_team import is_same_team

def get_members_without_meeting():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, data FROM member WHERE has_meeting = false")
    members = cursor.fetchall()
    
    conn.close()
    return members

def generate_meeting_pairs():
    members = get_members_without_meeting()
    pairs = []
    used = set()
    
    for i in range(len(members)):
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
    
    # 홀수면 마지막 남은 한 사람 출력
    remaining = [member for member in members if member[0] not in used]
    if remaining:
        print(f"남은 멤버: {remaining[0]}")
    
    return pairs

def create_meetings(pairs):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    for pair in pairs:
        # member_meeting 생성
        cursor.execute("INSERT INTO member_meeting (member_id, accept) VALUES (?, ?)", (pair[0][0], False))
        member_meeting_id1 = cursor.lastrowid
        
        cursor.execute("INSERT INTO member_meeting (member_id, accept) VALUES (?, ?)", (pair[1][0], False))
        member_meeting_id2 = cursor.lastrowid
        
        # meeting 생성
        cursor.execute("INSERT INTO meeting (member_meeting_id1, member_meeting_id2, accept) VALUES (?, ?, ?)", 
                      (member_meeting_id1, member_meeting_id2, False))
    
    conn.commit()
    conn.close()