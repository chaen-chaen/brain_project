"""
재등장(Recall) API 엔드포인트
질문/사고에 대한 메모 재등장 처리
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.recall import RecallRequest, RecallResponse, MemoryCluster, RecalledNote
from app.services.recall import recall_service

router = APIRouter(prefix="/api/recall", tags=["recall"])


@router.post("", response_model=RecallResponse)
async def recall_memories(
    request: RecallRequest,
    db: Session = Depends(get_db)
):
    """
    재등장 API
    
    단순 검색이 아닌 "재등장" 개념:
    - 의미 유사도 + 시간 가중치 적용
    - 연결된 메모를 맥락 묶음으로 반환
    - 오래된 메모라도 의미가 강하면 노출
    """
    # 재등장 실행
    clusters = await recall_service.recall(
        db=db,
        query=request.query,
        limit=request.limit
    )
    
    # 응답 구성
    recalled_memories = []
    for cluster in clusters:
        memory_cluster = MemoryCluster(
            cluster_reason=cluster["cluster_reason"],
            notes=[
                RecalledNote(
                    id=note["id"],
                    content=note["content"],
                    relevance_score=note["relevance_score"],
                    created_at=note["created_at"]
                )
                for note in cluster["notes"]
            ]
        )
        recalled_memories.append(memory_cluster)
    
    return RecallResponse(recalled_memories=recalled_memories)
