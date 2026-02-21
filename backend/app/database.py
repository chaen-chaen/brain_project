"""
데이터베이스 연결 및 세션 관리
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# SQLAlchemy 엔진 생성
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 연결 유효성 확인
    echo=False  # SQL 쿼리 로깅 (개발 시 True로 변경 가능)
)

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 베이스 클래스
Base = declarative_base()


def get_db():
    """
    데이터베이스 세션 의존성
    FastAPI dependency injection에서 사용
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
