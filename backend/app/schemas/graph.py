"""
Graph (그래프 시각화) 관련 Pydantic 스키마
"""
from pydantic import BaseModel
from datetime import datetime
from typing import List


class GraphNode(BaseModel):
    """그래프 노드 (메모)"""
    id: int
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class GraphEdge(BaseModel):
    """그래프 엣지 (연결)"""
    source: int  # source_note_id
    target: int  # target_note_id
    strength: float
    reason: str | None = None
    
    class Config:
        from_attributes = True


class GraphResponse(BaseModel):
    """그래프 데이터 응답"""
    nodes: List[GraphNode]
    edges: List[GraphEdge]
