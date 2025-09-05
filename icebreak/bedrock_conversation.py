import boto3
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

def get_conversation_recommendations(prompt):
    """AWS Bedrock을 사용해 대화 추천 목록을 받아오는 함수"""
    
    # AWS 자격 증명 설정 (테스트용)
    bedrock_runtime = boto3.client(
        'bedrock-runtime',
        region_name='us-east-1'
    )
    
    try:
        # Bedrock API 호출
        response = bedrock_runtime.converse(
            modelId="arn:aws:bedrock:us-east-1:637423276945:prompt/XWDHEIPEV7",
            promptVariables={
                "survey": {
                    "text": prompt
                }
                "sns": {
                    
                }
            }
        )
        
        # 응답 파싱
        conversation_list = response['output']['message']['content'][0]['text']
        
        return conversation_list
        
    except Exception as e:
        if "ThrottlingException" in str(e) or "Too many requests" in str(e):
            print(f"요청 제한 발생. 5초 대기 후 재시도...")
            time.sleep(5)
            try:
                response = bedrock_runtime.converse(
                    modelId="arn:aws:bedrock:us-east-1:637423276945:prompt/XWDHEIPEV7",
                    promptVariables={
                        "survey": {
                            "text": prompt
                        }
                    }
                )
                return response['output']['message']['content'][0]['text']
            except Exception as retry_e:
                print(f"재시도 실패: {retry_e}")
                return "[시뮬레이션] 대화 주제 생성 실패"
        else:
            print(f"오류 발생: {e}")
            return "[시뮬레이션] 대화 주제 생성 실패"
            
# 사용 예시
if __name__ == "__main__":
    # prompt.json에서 예시 프롬프트들 읽기
    with open('prompt.json', 'r', encoding='utf-8') as f:
        prompts = json.load(f)
    
    # 각 프롬프트에 대해 요청 보내기
    for i, prompt in enumerate(prompts, 1):
        print(f"\n=== 예시 {i} ===")
        print(f"입력: {json.dumps(prompt, ensure_ascii=False)}")
        
        recommendations = get_conversation_recommendations(json.dumps(prompt, ensure_ascii=False))
        
        if recommendations:
            print("추천 대화 목록:")
            print(recommendations)
        print("-" * 50)
        
        # 요청 간 대기 시간
        if i < len(prompts):
            time.sleep(2)