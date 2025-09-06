import json
import requests
import os
from pathlib import Path

def call_icebreaking_api(survey_data, linkedin_data):
    """아이스브레이킹 API 호출"""
    url = "https://i4sauf4dfs3d57hqjbbxmqp2iq0soahi.lambda-url.us-east-1.on.aws/"
    
    payload = {
        "survey": {
            "hobbies": survey_data.get("hobbies", ""),
            "interests": survey_data.get("interests", ""),
            "job_field": survey_data.get("job_field", ""),
            "timestamp": survey_data.get("timestamp", ""),
            "linkedin_url": survey_data.get("linkedin_url", "")
        },
        "sns": {
            "url": linkedin_data.get("url", ""),
            "name": linkedin_data.get("name", ""),
            "about": linkedin_data.get("about", ""),
            "email": linkedin_data.get("email"),
            "skills": linkedin_data.get("skills", []),
            "headline": linkedin_data.get("headline", ""),
            "location": linkedin_data.get("location", ""),
            "websites": linkedin_data.get("websites", []),
            "education": linkedin_data.get("education", []),
            "experiences": linkedin_data.get("experiences", [])
        }
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API 호출 실패: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ API 호출 오류: {e}")
        return None

def upload_to_db(json_file_path):
    """데이터를 member2 테이블에 업로드 (ice_breaking 분리)"""
    import sys
    from dotenv import load_dotenv
    
    load_dotenv()
    sys.path.append('linkedin-scraper-mcp')
    from postgres_config import PostgreSQLClient
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        member_data = json.load(f)
    
    db_client = PostgreSQLClient()
    if not db_client.connect():
        return False
    
    try:
        cursor = db_client.connection.cursor()
        slack_id = member_data.get("original_slack_id", "")
        
        # ice_breaking 제외한 데이터
        data_without_ice = {k: v for k, v in member_data.items() if k != "ice_breaking"}
        
        # 기본 데이터 UPSERT
        upsert_query = """
        INSERT INTO member2 (id, data, has_meeting, ice_break)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) 
        DO UPDATE SET
            data = EXCLUDED.data,
            has_meeting = EXCLUDED.has_meeting,
            ice_break = EXCLUDED.ice_break
        RETURNING id;
        """
        
        ice_breaking = member_data.get("ice_breaking")
        
        cursor.execute(upsert_query, (
            slack_id,
            json.dumps(data_without_ice, ensure_ascii=False),
            False,
            json.dumps(ice_breaking, ensure_ascii=False) if ice_breaking else None
        ))
        
        db_client.connection.commit()
        return True
        
    except Exception as e:
        print(f"❌ DB 업로드 실패: {e}")
        if db_client.connection:
            db_client.connection.rollback()
        return False
    finally:
        db_client.close()

def add_icebreaking_to_all():
    """모든 result 파일에 아이스브레이킹 데이터 추가 및 DB 업로드"""
    result_dir = Path("result")
    
    for json_file in result_dir.glob("*.json"):
        print(f"\n🔄 처리 중: {json_file.name}")
        
        # 기존 데이터 로드
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # API 호출 (아이스브레이킹이 없는 경우만)
        if "ice_breaking" not in data:
            survey_data = data.get("survey_data", {})
            linkedin_data = data.get("linkedin_data", {})
            
            ice_breaking_response = call_icebreaking_api(survey_data, linkedin_data)
            
            if ice_breaking_response:
                data["ice_breaking"] = ice_breaking_response
                
                # 파일 저장
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 아이스브레이킹 데이터 추가 완료: {json_file.name}")
            else:
                print(f"❌ 아이스브레이킹 데이터 추가 실패: {json_file.name}")
        
        # DB 업로드
        if upload_to_db(json_file):
            print(f"✅ DB 업로드 성공: {json_file.name}")
        else:
            print(f"❌ DB 업로드 실패: {json_file.name}")

if __name__ == "__main__":
    add_icebreaking_to_all()