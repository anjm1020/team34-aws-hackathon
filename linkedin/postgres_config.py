import json
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# 상위 디렉토리의 .env 파일도 찾아서 로드
load_dotenv()
load_dotenv('../.env')
class PostgreSQLClient:
    def __init__(self):
        # RDS PostgreSQL 연결 정보
        self.host = os.getenv('POSTGRES_HOST')
        self.port = os.getenv('POSTGRES_PORT', '5432')
        self.database = os.getenv('POSTGRES_DATABASE', 'linkedin_profiles')
        self.username = os.getenv('POSTGRES_USERNAME')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.connection = None
    def connect(self):
        """PostgreSQL에 연결"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password,
                sslmode='require'
            )
            print(":흰색_확인_표시: PostgreSQL 연결 성공")
            return True
        except Exception as e:
            print(f":x: PostgreSQL 연결 실패: {e}")
            return False
    def create_table(self):
        """member 테이블이 이미 존재한다고 가정"""
        print(":흰색_확인_표시: 기존 member 테이블 사용")
        return True
    def insert_profile(self, profile_data):
        """member 테이블에 LinkedIn 데이터 삽입"""
        try:
            cursor = self.connection.cursor()
            # URL을 id로 사용 (중복 방지)
            profile_id = profile_data.get('url', '').replace('https://www.linkedin.com/in/', '').rstrip('/')
            # 전체 데이터를 JSONB로 저장
            profile_data['scraped_at'] = 'CURRENT_TIMESTAMP'
            # UPSERT 쿼리
            upsert_query = """
            INSERT INTO member2 (id, data)
            VALUES (%s, %s)
            ON CONFLICT (id)
            DO UPDATE SET
                data = EXCLUDED.data
            RETURNING id;
            """
            cursor.execute(upsert_query, (
                profile_id,
                json.dumps(profile_data)
            ))
            result = cursor.fetchone()
            self.connection.commit()
            cursor.close()
            print(f":흰색_확인_표시: 프로필 저장 완료: {profile_data.get('name')} (ID: {result[0]})")
            return result[0]
        except Exception as e:
            print(f":x: 프로필 저장 실패: {e}")
            if self.connection:
                self.connection.rollback()
            return None
    def get_profile(self, url):
        """URL로 프로필 조회"""
        try:
            profile_id = url.replace('https://www.linkedin.com/in/', '').rstrip('/')
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM member2 WHERE id = %s", (profile_id,))
            result = cursor.fetchone()
            cursor.close()
            return dict(result) if result else None
        except Exception as e:
            print(f":x: 프로필 조회 실패: {e}")
            return None
    def get_all_profiles(self):
        """모든 프로필 조회"""
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM member2 ORDER BY id")
            results = cursor.fetchall()
            cursor.close()
            return [dict(row) for row in results]
        except Exception as e:
            print(f":x: 프로필 목록 조회 실패: {e}")
            return []
    def insert_profile_with_user_id(self, member_data):
        """user_id를 기본키로 사용하여 멤버 데이터 삽입"""
        try:
            cursor = self.connection.cursor()
            # UPSERT 쿼리 (user_id 기반)
            upsert_query = """
            INSERT INTO member2 (id, data, has_meeting)
            VALUES (%s, %s, %s)
            ON CONFLICT (id)
            DO UPDATE SET
                data = EXCLUDED.data,
                has_meeting = EXCLUDED.has_meeting
            RETURNING id;
            """
            cursor.execute(upsert_query, (
                str(member_data["user_id"]),
                json.dumps(member_data, ensure_ascii=False),
                False  # has_meeting 기본값
            ))
            result = cursor.fetchone()
            self.connection.commit()
            cursor.close()
            print(f":흰색_확인_표시: 멤버 데이터 저장 완료: User ID {member_data['user_id']}")
            return result[0]
        except Exception as e:
            print(f":x: 멤버 데이터 저장 실패: {e}")
            if self.connection:
                self.connection.rollback()
            return None
    def insert_profile_with_slack_id(self, slack_id, member_data):
        """슬랙 ID를 기본키로 사용하여 멤버 데이터 삽입"""
        try:
            cursor = self.connection.cursor()
            # UPSERT 쿼리 (Slack ID 기반)
            upsert_query = """
            INSERT INTO member2 (id, data, has_meeting)
            VALUES (%s, %s, %s)
            ON CONFLICT (id)
            DO UPDATE SET
                data = EXCLUDED.data,
                has_meeting = EXCLUDED.has_meeting
            RETURNING id;
            """
            cursor.execute(upsert_query, (
                slack_id,
                json.dumps(member_data, ensure_ascii=False),
                False  # has_meeting 기본값
            ))
            result = cursor.fetchone()
            self.connection.commit()
            cursor.close()
            print(f":흰색_확인_표시: 멤버 데이터 저장 완료: Slack ID {slack_id}")
            return result[0]
        except Exception as e:
            print(f":x: 멤버 데이터 저장 실패: {e}")
            if self.connection:
                self.connection.rollback()
            return None
    def close(self):
        """연결 종료"""
        if self.connection:
            self.connection.close()
            print(":흰색_확인_표시: PostgreSQL 연결 종료")