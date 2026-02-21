"""
MemoryLink (메모 간 연결) 모델
LLM이 자동으로 생성하는 의미 기반 연결
"""
from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class MemoryLink(Base):
    """
    메모 간 자동 연결 모델
    - 사용자가 직접 생성하지 않음
    - 의미 유사도 기반으로 자동 생성
    """
    __tablename__ = "memory_links"
    
    id = Column(Integer, primary_key=True, index=True)
    source_note_id = Column(
        Integer, 
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )  # 출발 메모
    target_note_id = Column(
        Integer, 
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )  # 도착 메모
    strength = Column(Float, nullable=False)  # 연결 강도 (0.0 ~ 1.0)
    reason = Column(Text, nullable=True)  # 연결 이유 (키워드 또는 LLM 요약)
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )  # 연결 생성 시각
    
    def __repr__(self):
        return f"<MemoryLink(source={self.source_note_id}, target={self.target_note_id}, strength={self.strength:.2f})>"
