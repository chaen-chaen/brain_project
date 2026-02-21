/**
 * 재등장(Recall) 입력 컴포넌트
 * 질문/사고 입력 시 관련 메모가 재등장
 */
import React, { useState } from 'react';
import { recallAPI, type RecallResponse } from '../services/api';

const RecallInput: React.FC = () => {
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<RecallResponse | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!query.trim()) return;

        try {
            setLoading(true);
            const recallResult = await recallAPI.recall(query);
            setResult(recallResult);
        } catch (error) {
            console.error('Recall failed:', error);
            alert('Recall failed.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="recall-input-container">
            <form onSubmit={handleSubmit}>
                <textarea
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask a question or enter a thought..."
                    disabled={loading}
                    rows={4}
                />
                <button type="submit" disabled={loading || !query.trim()}>
                    {loading ? 'Recalling...' : 'Recall'}
                </button>
            </form>

            {result && result.recalled_memories && result.recalled_memories.length > 0 && (
                <div className="recall-results">
                    {result.recalled_memories.map((cluster, clusterIdx) => (
                        <div key={clusterIdx} className="memory-cluster">
                            <h3>{cluster.cluster_reason}</h3>
                            <div className="cluster-notes">
                                {cluster.notes.map((note) => (
                                    <div key={note.id} className="recalled-note">
                                        <div className="note-header">
                                            <span className="relevance">
                                                Relevance: {(note.relevance_score * 100).toFixed(0)}%
                                            </span>
                                            <span className="date">
                                                {new Date(note.created_at).toLocaleDateString('ko-KR')}
                                            </span>
                                        </div>
                                        <p className="note-content">{note.content}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {result && result.recalled_memories && result.recalled_memories.length === 0 && (
                <div className="no-results">
                    <p>No related memories found.</p>
                </div>
            )}
        </div>
    );
};

export default RecallInput;
