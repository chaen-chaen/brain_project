/**
 * API 클라이언트 서비스
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 타입 정의
export interface Note {
    id: number;
    content: string;
    created_at: string;
    related_notes?: RelatedNote[];
}

export interface RelatedNote {
    id: number;
    content: string;
    strength: number;
    created_at: string;
}

export interface RecalledNote {
    id: number;
    content: string;
    relevance_score: number;
    created_at: string;
}

export interface MemoryCluster {
    cluster_reason: string;
    notes: RecalledNote[];
}

export interface RecallResponse {
    recalled_memories: MemoryCluster[];
}

export interface GraphNode {
    id: number;
    content: string;
    created_at: string;
}

export interface GraphEdge {
    source: number;
    target: number;
    strength: number;
    reason?: string;
}

export interface GraphData {
    nodes: GraphNode[];
    edges: GraphEdge[];
}

// API 함수들
export const noteAPI = {
    /**
     * 메모 생성
     */
    create: async (content: string): Promise<Note> => {
        const response = await api.post<Note>('/api/notes', { content });
        return response.data;
    },

    /**
     * 메모 조회
     */
    get: async (id: number): Promise<Note> => {
        const response = await api.get<Note>(`/api/notes/${id}`);
        return response.data;
    },
};

export const recallAPI = {
    /**
     * 재등장 요청
     */
    recall: async (query: string, limit: number = 10): Promise<RecallResponse> => {
        const response = await api.post<RecallResponse>('/api/recall', {
            query,
            limit,
        });
        return response.data;
    },
};

export const graphAPI = {
    /**
     * 그래프 데이터 조회
     */
    get: async (query?: string, minStrength: number = 0.75): Promise<GraphData> => {
        const params: any = { min_strength: minStrength };
        if (query) {
            params.query = query;
        }
        const response = await api.get<GraphData>('/api/graph', { params });
        return response.data;
    },
};

export default api;
