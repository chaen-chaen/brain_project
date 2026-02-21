"""
Note (메모) 모델
사용자가 자유롭게 던지는 메모를 저장
"""
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.database import Base
from app.config import settings


class Note(Base):
    """
    메모 모델
    - 제목 없음 (자유로운 입력 장려)
    - 태그/폴더 없음 (의미 기반 연결만 사용)
    """
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)  # 메모 원문
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )  # 생성 시각
    embedding = Column(
        Vector(settings.EMBEDDING_DIMENSION), 
        nullable=True
    )  # 임베딩 벡터 (384차원)
    
    def __repr__(self):
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<Note(id={self.id}, content='{preview}')>"
