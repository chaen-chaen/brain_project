/**
 * 메인 App 컴포넌트
 */
import { useState } from 'react';
import NoteInput from './components/NoteInput';
import RecallInput from './components/RecallInput';
import MemoryGraph from './components/MemoryGraph';
import './App.css';

type TabType = 'note' | 'recall' | 'graph';

function App() {
    const [activeTab, setActiveTab] = useState<TabType>('note');

    return (
        <div className="app">
            <header className="app-header">
                <h1>The Second Brain</h1>
                <p className="subtitle">Offload Your Mind. Delegate to the System.</p>
            </header>

            <nav className="app-nav">
                <button
                    className={activeTab === 'note' ? 'active' : ''}
                    onClick={() => setActiveTab('note')}
                >
                    Input
                </button>
                <button
                    className={activeTab === 'recall' ? 'active' : ''}
                    onClick={() => setActiveTab('recall')}
                >
                    Recall
                </button>
                <button
                    className={activeTab === 'graph' ? 'active' : ''}
                    onClick={() => setActiveTab('graph')}
                >
                    Graph
                </button>
            </nav>

            <main className="app-main">
                {activeTab === 'note' && (
                    <div className="tab-content">
                        <h2>Just Cast Your Thoughts</h2>
                        <p className="tab-description">
                            No titles, no folders, no tags required.
                            The system automatically builds semantic connections for you.
                        </p>
                        <NoteInput />
                    </div>
                )}

                {activeTab === 'recall' && (
                    <div className="tab-content">
                        <h2>Inquire and Ignite</h2>
                        <p className="tab-description">
                            Past memories resurface within the right context.
                            It’s a natural spark of memory during your thought process.
                        </p>
                        <RecallInput />
                    </div>
                )}

                {activeTab === 'graph' && (
                    <div className="tab-content">
                        <h2>Observe the Connections</h2>
                        <p className="tab-description">
                            Visualize the network of thoughts woven by the system.
                            Purely for observation; let the structure reveal itself.
                        </p>
                        <MemoryGraph />
                    </div>
                )}
            </main>
        </div>
    );
}

export default App;
