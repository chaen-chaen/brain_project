"""
Recall (재등장) 관련 Pydantic 스키마
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class RecallRequest(BaseModel):
    """재등장 요청"""
    query: str = Field(..., min_length=1, description="질문 또는 사고 내용")
    limit: int = Field(10, ge=1, le=50, description="최대 반환 개수")


class RecalledNote(BaseModel):
    """재등장한 메모"""
    id: int
    content: str
    relevance_score: float = Field(..., description="관련성 점수 (유사도 + 시간 가중치)")
    created_at: datetime
    
    class Config:
        from_attributes = True


class MemoryCluster(BaseModel):
    """맥락 묶음 (연결된 메모들의 클러스터)"""
    cluster_reason: str = Field(..., description="묶음 이유")
    notes: List[RecalledNote]


class RecallResponse(BaseModel):
    """재등장 응답"""
    recalled_memories: List[MemoryCluster]
