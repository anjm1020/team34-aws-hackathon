import boto3
import json
import os

os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "bedrock-api-key-YmVkcm9jay5hbWF6b25hd3MuY29tLz9BY3Rpb249Q2FsbFdpdGhCZWFyZXJUb2tlbiZYLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFTSUFaSTJMREtPSTNRQzc3SVE2JTJGMjAyNTA5MDUlMkZ1cy1lYXN0LTElMkZiZWRyb2NrJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTA5MDVUMTMxMDUwWiZYLUFtei1FeHBpcmVzPTQzMjAwJlgtQW16LVNlY3VyaXR5LVRva2VuPUlRb0piM0pwWjJsdVgyVmpFQTRhQ1hWekxXVmhjM1F0TVNKR01FUUNJRUFvbklLU0l1SSUyRmRKMlduRDRDUjJTSWxzVmN0WlNSRTVOZ3VWd2UwS0lmQWlBR3BSS2NodnBJSDYzMm1OV0YxckdoR2NVb0tpOWdQN1pFYWNBJTJCUjhOeW1pckdBd2gyRUFBYUREWXpOelF5TXpJM05qazBOU0lNczNTdGs2Uk5SWmkzZTVrMktxTURaaGNkUzJ6NndPR0hDZktiUXV3bCUyQmhtRzZGWGhwejNxT25mV2tlVSUyRiUyRmpKWWtoNGY3a1ZSeVRNR1pTWHlHZktHcVFOblFKd0RYc0lobUxtcjhoODd5bXQlMkZEWjBYUW5qNmEyTEVzOWJZS1gzSlRsR0hBR0pWTXBDT1hqRjdXTjlGb3A0U2YlMkJSRUI2c3A4RTVVcU9zVSUyQlpFWXI2bnJVbGxCcEZwckZVdGQlMkZzYUZpWW80cTZpTUhreWZIUm0xeWltektuYTI4V0NEOHVPQk1oZG5oU25OWERBc0IlMkZHS3RCUzBVQkxXZ3Jnb2tzWmJaS3pRczlNNEU1VjFnUFNsWTJpWXdaMUxCY0dGT0pmUnNSVVhObm9mSU92MyUyRllTWXJXNG1BbjVNN2loc3dFakN0cXNMNGxxSk5WWjh4ZSUyQnJiOGZoU0hMNnV0eVd1WFZheWlUQ3JldTNOb0JsakJwOGlDMFBkTEVBekVZUXlINEJFU1RTVFAyZUxvRmJ3OGYzSGpRcEp3bHdSTjI5NVpzaEttZmlPd3pSU3lQNnhXalp5Z0NoVnpLYVM1VXpyY0V2MzJWa093RVNDUkdla3h2SGx0Z08yajVoJTJGJTJGb1dHdlJZRXhpZ1FmcnlGejQlMkZWQjkwSk5XRUJOViUyRkpJU3JKRE03UDUyYXFGUyUyRjdlNVQlMkJKaWFZT1ZyQ1lzMEg1NHFvREI3cTdRQWlxVTRJS2huWDBCeVV6ZVprTFdKVU5wd2dranNyanN3bHZEcXhRWTYzd0p5ZUxZR21DYSUyRjhTcFphT25JTlJkUXY1VHIzWEZxdFBOcWdMeTM5OFBWM0VtWm5pWkJkWVNiVGlJdUd3WFhrTjJLUlpFaW1sSFliblglMkI3cVVnZldSNmkwSlNoWkhyWnZtN3EyeXZsVGF0WFBnVFYlMkZMd2ZJUG1RZlNzSlFMTm81NSUyQlFWd1VkRVJvcyUyQll1MHBDQUhzYW1heTYzUjZuU2l6emVWTnpqOVElMkZGdHZZV2xSWld0RzBGTUZ1VUprMWp6bkklMkZIZzBoYnZJZ2JOaXV5WDU4ZkFsNXA3QzVIR05CVkN1aTNsQ2lQZlp1NVBrSThacWhxdXRsdUVXZkY5JTJCdXM3MERaSDJLJTJCNTlSJTJGdmZKTnFmJTJGSVN1QUVJazd1eWM4T2Rxb2dqV3BGdk9JUXRjS0VIWWI4bEVqQSUyRjNSU3klMkZ6Tktia3F4QmFvNXIlMkIxWU5VNkZ3ejZQS3o0dGV5NVBtc0V5VURBbXB5dkt2eGZIRE90bTRHaDZuJTJGcmdZd211UFk0RGUwVVl0RWRETE9EdXIzWHRBQ1Ribml4czFkRkxnSWdhOTVVVUFQbEJEZlBkQkFEZ1BRdm1SNnAydVUxNWU5JTJGNlM4SzVuQmZaNVQ4RzJjQkFWZFYyQSUzRCZYLUFtei1TaWduYXR1cmU9NTBmYmQ1ZDk5Zjk3ZTUwMWMyNzljMGM5OWMxMjZmNWJkNjdjOWY0OTNjMjI1ODllZGYwNTMwNTU2YTBiODRlYiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmVmVyc2lvbj0x"
base_prompt= "다음 입력은 네트워킹의 첫만남을 가질 상대방이 사전에 설문에 답한 내용이야. 각 질문은 아래와 같아. - 현재 종사하는 직군 혹은 전공이 무엇인가요? (예: IT 기업, 컴퓨터공학과) - IT관련 관심 분야가 무엇인가요? (예: AI, Cloud, DevOps) - 최근 가장 흥미롭게 본 기술이나 트렌드는 무엇인가요? - 휴식 시간에 진행하는 취미 활동은 무엇인가요? 입력된 답변을 봤을때 해당 상대방과 처음 아이스브레이킹을 위해 꺼낼만한 질문을 각 큰 주제별로 3개씩 추천해줘. 답변은 아래와 같은 JSON형식으로 해줘."

def get_conversation_recommendations(prompt):
    """AWS Bedrock을 사용해 대화 추천 목록을 받아오는 함수"""
    
    # AWS 자격 증명 설정 (테스트용)
    bedrock_runtime = boto3.client(
        'bedrock-runtime',
        region_name='us-east-1'
    )
    
    kwargs ={
        "modelId": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        "contentType": "application/json",
        "body": json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "system": base_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        })
    }
    
    try:
        # Bedrock API 호출
        response = bedrock_runtime.invoke_model(**kwargs)
        
        # 응답 파싱
        response_body = json.loads(response['body'].read())
        conversation_list = response_body['content'][0]['text']
        
        return conversation_list
        
    except Exception as e:
        print(f"오류 발생: {e}")
        return "[시뮬레이션] 보안 컨설턴트를 위한 대화 주제:\n1. 최근 공급망 공격 사례에 대한 의견\n2. 네트워크 보안 동향과 전망\n3. 취약점 분석 방법론\n4. 크로스핏 운동의 장점\n5. 캠핑 장비와 추천 장소"
# 사용 예시
if __name__ == "__main__":
    prompt = {
        "직군/전공": "보안 컨설턴트",
        "관심 분야": "네트워크 보안과 취약점 분석",
        "최근 흥미로운 트렌드": "공급망 공격 사례 증가",
        "취미 활동": "크로스핏과 캠핑"
    }
    
    recommendations = get_conversation_recommendations(json.dumps(prompt, ensure_ascii=False))
    
    if recommendations:
        print("추천 대화 목록:")
        print(recommendations)