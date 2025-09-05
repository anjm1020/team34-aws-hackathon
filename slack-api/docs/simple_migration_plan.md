# 간단한 Lambda 마이그레이션 플랜

## 목표
로컬 Slack Bot을 AWS Lambda로 옮겨서 외부에서 API 호출로 메시지 전송 가능하게 만들기

## 아키텍처
```
외부 호출 → API Gateway → Lambda → Slack API
```

## 작업 순서 (총 1시간)

### 1. 환경변수 AWS로 이동 (10분)
- [ ] AWS Parameter Store에 토큰 저장
  ```bash
  aws ssm put-parameter --name "/slack/bot-token" --value "xoxb-your-token" --type "SecureString"
  aws ssm put-parameter --name "/slack/signing-secret" --value "your-secret" --type "SecureString"
  ```

### 2. Lambda 코드 작성 (15분)
- [ ] `lambda_function.py` 생성
- [ ] 기존 `bot.py`에서 DM 전송 로직만 추출
- [ ] Parameter Store에서 토큰 읽기 추가
- [ ] API Gateway 요청 처리 추가

### 3. SAM 템플릿 작성 (10분)
- [ ] `template.yaml` 생성
- [ ] Lambda 함수 정의
- [ ] API Gateway 연결
- [ ] 필요한 권한 설정

### 4. 배포 (15분)
- [ ] `sam build` 실행
- [ ] `sam deploy --guided` 실행
- [ ] API 엔드포인트 URL 확인

### 5. 테스트 (10분)
- [ ] curl로 API 호출 테스트
- [ ] Slack DM 전송 확인

## 필요한 파일들

### 1. lambda_function.py
```python
import json
import boto3
from slack_sdk import WebClient

def get_parameter(name):
    ssm = boto3.client('ssm')
    return ssm.get_parameter(Name=name, WithDecryption=True)['Parameter']['Value']

def lambda_handler(event, context):
    # Parameter Store에서 토큰 가져오기
    token = get_parameter('/slack/bot-token')
    client = WebClient(token=token)
    
    # 요청 본문 파싱
    body = json.loads(event['body'])
    user_id = body['user_id']
    message = body['message']
    
    # Slack DM 전송
    try:
        response = client.chat_postMessage(
            channel=user_id,
            text=message
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'success': True, 'message_id': response['ts']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'success': False, 'error': str(e)})
        }
```

### 2. template.yaml
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  SlackBotFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: ./
      Handler: lambda_function.lambda_handler
      Runtime: python3.9
      Timeout: 30
      Events:
        Api:
          Type: Api
          Properties:
            Path: /send
            Method: post
      Policies:
        - SSMParameterReadPolicy:
            ParameterName: /slack/*

Outputs:
  ApiUrl:
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/send"
```

### 3. requirements.txt
```
slack-sdk==3.26.2
boto3
```

## 사용법
배포 완료 후:
```bash
curl -X POST https://your-api-url/send \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U09CU4ZJ9NH", "message": "테스트 메시지"}'
```

## 성공 기준
- [ ] API 호출 시 200 응답
- [ ] Slack DM 정상 전송
- [ ] CloudWatch 로그 확인 가능

## 확장 계획
나중에 추가할 시스템들:
- Bedrock AI 서비스
- 다른 Lambda 함수들
- 공통 Parameter Store 사용
- 같은 API Gateway에 경로 추가