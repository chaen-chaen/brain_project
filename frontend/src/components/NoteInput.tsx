/**
 * 메모 입력 컴포넌트
 * 자유롭게 메모를 "던지듯" 저장
 */
import React, { useState } from 'react';
import { noteAPI, type Note } from '../services/api';

interface NoteInputProps {
    onNoteCreated?: (note: Note) => void;
}

const NoteInput: React.FC<NoteInputProps> = ({ onNoteCreated }) => {
    const [content, setContent] = useState('');
    const [loading, setLoading] = useState(false);
    const [lastNote, setLastNote] = useState<Note | null>(null);

    const submitNote = async () => {
        if (!content.trim()) return;

        try {
            setLoading(true);
            const note = await noteAPI.create(content);
            setLastNote(note);
            setContent(''); // 저장 후 즉시 클리어

            if (onNoteCreated) {
                onNoteCreated(note);
            }
        } catch (error) {
            console.error('Failed to save note:', error);
            alert('Failed to save note.');
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        await submitNote();
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        // Ctrl/Cmd + Enter로 저장
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            submitNote();
        }
    };

    return (
        <div className="note-input-container">
            <form onSubmit={handleSubmit}>
                <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Just cast your thought... (Ctrl+Enter to save)"
                    disabled={loading}
                    rows={4}
                />
                <button type="submit" disabled={loading || !content.trim()}>
                    {loading ? 'Saving...' : 'Save'}
                </button>
            </form>

            {lastNote && lastNote.related_notes && lastNote.related_notes.length > 0 && (
                <div className="related-notes">
                    <h4>Automatically Connected:</h4>
                    <ul>
                        {lastNote.related_notes.slice(0, 3).map((related) => (
                            <li key={related.id}>
                                <span className="strength">{(related.strength * 100).toFixed(0)}%</span>
                                <span className="content">
                                    {related.content.length > 50
                                        ? related.content.substring(0, 50) + '...'
                                        : related.content}
                                </span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default NoteInput;
