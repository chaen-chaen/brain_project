"""
데이터베이스 초기화 스크립트
pgvector 확장 및 테이블 생성
"""
from app.database import engine, Base
from app.models.note import Note
from app.models.memory_link import MemoryLink
from sqlalchemy import text


def init_db():
    """데이터베이스 초기화"""
    print("데이터베이스 초기화 시작...")
    
    # pgvector 확장 활성화
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
        print("✓ pgvector 확장 활성화")
    
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    print("✓ 테이블 생성 완료")
    
    print("데이터베이스 초기화 완료!")


if __name__ == "__main__":
    init_db()
