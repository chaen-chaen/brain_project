"""
그래프 시각화 API 엔드포인트
메모 간 연결 그래프 데이터 제공
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from app.database import get_db
from app.schemas.graph import GraphResponse, GraphNode, GraphEdge
from app.config import settings

router = APIRouter(prefix="/api/graph", tags=["graph"])


@router.get("", response_model=GraphResponse)
async def get_graph(
    query: Optional[str] = Query(None, description="필터링할 쿼리 (없으면 전체 그래프)"),
    min_strength: float = Query(0.75, ge=0.0, le=1.0, description="최소 연결 강도"),
    db: Session = Depends(get_db)
):
    """
    연결 그래프 데이터 반환
    
    특징:
    - 전체 연결이 아닌 신뢰도 높은 연결만 (기본 0.75 이상)
    - query가 있으면 관련 메모 중심으로 서브그래프 반환
    - 사용자는 편집 불가, 관찰만 가능
    """
    
    if query:
        # 쿼리 관련 서브그래프
        # 1. 쿼리와 유사한 메모 찾기
        from app.services.embedding import embedding_service
        query_embedding = await embedding_service.get_embedding(query)
        
        # 2. 상위 20개 유사 메모
        similar_query = text("""
            SELECT id, content, created_at
            FROM notes
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> :embedding
            LIMIT 20
        """)
        
        result = db.execute(similar_query, {"embedding": str(query_embedding)})
        note_ids = [row.id for row in result.fetchall()]
        
        if not note_ids:
            return GraphResponse(nodes=[], edges=[])
        
        # 3. 해당 메모들과 연결된 메모 포함
        nodes_query = text("""
            SELECT DISTINCT n.id, n.content, n.created_at
            FROM notes n
            WHERE n.id = ANY(:note_ids)
                OR n.id IN (
                    SELECT target_note_id FROM memory_links 
                    WHERE source_note_id = ANY(:note_ids) AND strength >= :min_strength
                )
            ORDER BY n.created_at DESC
            LIMIT 50
        """)
        
        result = db.execute(
            nodes_query, 
            {"note_ids": note_ids, "min_strength": min_strength}
        )
        nodes_data = result.fetchall()
        
    else:
        # 전체 그래프 (최근 50개 메모)
        nodes_query = text("""
            SELECT id, content, created_at
            FROM notes
            ORDER BY created_at DESC
            LIMIT 50
        """)
        
        result = db.execute(nodes_query)
        nodes_data = result.fetchall()
    
    # 노드 구성
    nodes = [
        GraphNode(
            id=row.id,
            content=row.content,
            created_at=row.created_at
        )
        for row in nodes_data
    ]
    
    node_ids = [node.id for node in nodes]
    
    if not node_ids:
        return GraphResponse(nodes=[], edges=[])
    
    # 엣지 조회 (해당 노드들 간의 연결만)
    edges_query = text("""
        SELECT source_note_id, target_note_id, strength, reason
        FROM memory_links
        WHERE source_note_id = ANY(:node_ids)
            AND target_note_id = ANY(:node_ids)
            AND strength >= :min_strength
        ORDER BY strength DESC
    """)
    
    result = db.execute(
        edges_query,
        {"node_ids": node_ids, "min_strength": min_strength}
    )
    
    edges = [
        GraphEdge(
            source=row.source_note_id,
            target=row.target_note_id,
            strength=float(row.strength),
            reason=row.reason
        )
        for row in result.fetchall()
    ]
    
    return GraphResponse(nodes=nodes, edges=edges)
