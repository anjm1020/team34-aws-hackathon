#!/usr/bin/env python3
import pandas as pd
import json
import os
import sys
import subprocess
import argparse
from pathlib import Path

sys.path.append('linkedin-scraper-mcp')
from postgres_config import PostgreSQLClient

def excel_to_json(excel_file_path, output_dir="converted_json"):
    """엑셀 파일을 JSON으로 변환"""
    Path(output_dir).mkdir(exist_ok=True)
    
    df = pd.read_excel(excel_file_path)
    headers = df.iloc[0].tolist()
    data_rows = df.iloc[1:]
    
    json_data = []
    for _, row in data_rows.iterrows():
        record = {
            "linkedin_url": str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else "",
            "job_field": str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "",
            "interests": str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else "",
            "hobbies": str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else "",
            "user_id": str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else "",
            "timestamp": str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else ""
        }
        
        if any(record.values()):
            json_data.append(record)
    
    base_name = Path(excel_file_path).stem
    json_file_path = f"{output_dir}/{base_name}.json"
    
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 엑셀 변환 완료: {json_file_path} ({len(json_data)}개 레코드)")
    return json_file_path

def is_valid_linkedin_url(url):
    """유효한 LinkedIn URL인지 확인"""
    if not url or url.strip() == "":
        return False
    return "linkedin.com/in/" in url and "feed" not in url

def normalize_url(url):
    """URL 정규화"""
    if not url:
        return ""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url.rstrip('/')

def scrape_linkedin(url):
    """LinkedIn 프로필 스크래핑"""
    try:
        normalized_url = normalize_url(url)
        result = subprocess.run(
            ["python", "main.py", normalized_url],
            capture_output=True,
            text=True,
            timeout=120,
            cwd="linkedin-scraper-mcp"
        )
        
        if result.returncode == 0:
            print(f"✅ LinkedIn 스크래핑 성공: {url}")
            return True
        else:
            print(f"❌ LinkedIn 스크래핑 실패: {url}")
            return False
    except Exception as e:
        print(f"❌ 스크래핑 오류: {e}")
        return False

def find_linkedin_data(url, scraped_dir):
    """스크래핑된 LinkedIn 데이터 찾기"""
    for file_path in Path(scraped_dir).glob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'url' in data and normalize_url(data['url']) == normalize_url(url):
                    return data
        except:
            continue
    return None

def create_member_json(member_data, user_id, linkedin_data=None):
    """멤버 JSON 생성"""
    if linkedin_data is None:
        linkedin_data = {
            "url": "",
            "name": "",
            "headline": "",
            "location": "",
            "about": "",
            "experiences": [],
            "education": [],
            "skills": [],
            "websites": [],
            "email": None
        }
    
    return {
        "user_id": user_id,
        "original_slack_id": member_data.get("user_id", ""),
        "survey_data": {
            "linkedin_url": member_data.get("linkedin_url", ""),
            "job_field": member_data.get("job_field", ""),
            "interests": member_data.get("interests", ""),
            "hobbies": member_data.get("hobbies", ""),
            "timestamp": member_data.get("timestamp", "")
        },
        "linkedin_data": linkedin_data
    }

def upload_to_db(json_file_path):
    """DB에 업로드"""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        member_data = json.load(f)
    
    db_client = PostgreSQLClient()
    if not db_client.connect():
        return False
    
    try:
        result = db_client.insert_profile_with_user_id(member_data)
        return result is not None
    except Exception as e:
        print(f"❌ DB 업로드 실패: {e}")
        return False
    finally:
        db_client.close()

def process_all(excel_file, upload_db=False):
    """전체 처리 플로우"""
    
    # 1. 엑셀 → JSON 변환
    survey_json_path = excel_to_json(excel_file)
    
    # 2. 설문 데이터 로드
    with open(survey_json_path, 'r', encoding='utf-8') as f:
        survey_data = json.load(f)
    
    # 3. 폴더 생성
    Path("result").mkdir(exist_ok=True)
    scraped_dir = "linkedin-scraper-mcp/scraped_data"
    
    print(f"\n🚀 총 {len(survey_data)}명의 멤버 처리 시작")
    
    # 4. 각 멤버 처리
    for i, member in enumerate(survey_data, 1):
        user_id = i
        linkedin_url = member.get("linkedin_url", "")
        
        print(f"\n👤 멤버 {user_id} 처리 중...")
        
        linkedin_data = None
        
        # LinkedIn URL 확인 및 처리
        if is_valid_linkedin_url(linkedin_url):
            print(f"🔗 LinkedIn URL 발견: {linkedin_url}")
            
            # 기존 스크래핑 데이터 확인
            linkedin_data = find_linkedin_data(linkedin_url, scraped_dir)
            
            if not linkedin_data:
                print("📥 새로운 스크래핑 시작...")
                if scrape_linkedin(linkedin_url):
                    linkedin_data = find_linkedin_data(linkedin_url, scraped_dir)
        else:
            print("📝 LinkedIn URL 없음 - 설문 데이터만 저장")
        
        # 멤버 JSON 생성
        member_json = create_member_json(member, user_id, linkedin_data)
        
        # result 폴더에 저장
        result_file = f"result/{user_id}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(member_json, f, ensure_ascii=False, indent=2)
        
        print(f"💾 저장 완료: {result_file}")
        
        # DB 업로드 (옵션)
        if upload_db:
            if upload_to_db(result_file):
                print(f"✅ DB 업로드 성공: User {user_id}")
            else:
                print(f"❌ DB 업로드 실패: User {user_id}")
        else:
            print(f"📝 JSON 생성 완료: User {user_id}")
    
    print(f"\n🎉 전체 처리 완료! {len(survey_data)}명")

def main():
    parser = argparse.ArgumentParser(description='LinkedIn 프로필 처리 도구')
    parser.add_argument('excel_file', help='엑셀 파일 경로')
    parser.add_argument('--upload-db', action='store_true', help='DB에 업로드')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.excel_file):
        print(f"❌ 파일을 찾을 수 없습니다: {args.excel_file}")
        sys.exit(1)
    
    process_all(args.excel_file, args.upload_db)

if __name__ == "__main__":
    main()