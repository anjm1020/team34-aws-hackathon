import pandas as pd
import json
import os
from pathlib import Path
from datetime import datetime

def excel_to_json(excel_file_path, output_dir="converted_json"):
    """엑셀 파일을 JSON으로 변환"""
    
    # 출력 디렉토리 생성
    Path(output_dir).mkdir(exist_ok=True)
    
    # 엑셀 파일 읽기 (header=0으로 첫 번째 행을 헤더로 사용)
    df = pd.read_excel(excel_file_path, header=0)
    
    # 파일명에서 확장자 제거
    base_name = Path(excel_file_path).stem
    
    # JSON 파일 경로
    json_file_path = f"{output_dir}/{base_name}.json"
    
    # 데이터 정리 및 구조화
    json_data = []
    for _, row in df.iterrows():
        record = {
            "linkedin_url": str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else "",
            "job_field": str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "",
            "interests": str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else "",
            "hobbies": str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else "",
            "user_id": str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else "",
            "timestamp": str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else ""
        }
        
        # 빈 행 제외
        if any(record.values()):
            json_data.append(record)
    
    # JSON 파일로 저장
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 변환 완료: {json_file_path}")
    print(f"📊 총 {len(json_data)}개 레코드 변환")
    return json_file_path

if __name__ == "__main__":
    # 사용 예시
    excel_file = input("엑셀 파일 경로를 입력하세요: ")
    
    if os.path.exists(excel_file):
        excel_to_json(excel_file)
    else:
        print("❌ 파일을 찾을 수 없습니다.")