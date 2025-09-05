import boto3
import json
import os
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
            }
        )
        
        # 응답 파싱
        conversation_list = response['output']['message']['content'][0]['text']
        
        return conversation_list
        
    except Exception as e:
        print(f"오류 발생: {e}")
        return "[시뮬레이션] 보안 컨설턴트를 위한 대화 주제:\n1. 최근 공급망 공격 사례에 대한 의견\n2. 네트워크 보안 동향과 전망\n3. 취약점 분석 방법론\n4. 크로스핏 운동의 장점\n5. 캠핑 장비와 추천 장소"
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