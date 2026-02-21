/**
 * 메모리 그래프 시각화 컴포넌트
 * D3를 사용한 관찰 전용 그래프
 */
import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { graphAPI, type GraphData, type GraphNode } from '../services/api';

// D3 시뮬레이션용 노드 타입 정의 (d3.SimulationNodeDatum 상속)
interface SimulationNode extends GraphNode, d3.SimulationNodeDatum { }

// D3 시뮬레이션용 링크 타입 정의 (d3.SimulationLinkDatum 상속)
interface SimulationLink extends d3.SimulationLinkDatum<SimulationNode> {
    strength: number;
}

const MemoryGraph: React.FC = () => {
    const svgRef = useRef<SVGSVGElement>(null);
    const [graphData, setGraphData] = useState<GraphData | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadGraph();
    }, []);

    const loadGraph = async () => {
        try {
            setLoading(true);
            const data = await graphAPI.get();
            setGraphData(data);
        } catch (error) {
            console.error('Failed to load graph:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (!graphData || !svgRef.current) return;

        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove(); // 기존 내용 제거

        const width = 800;
        const height = 600;

        svg.attr('width', width).attr('height', height);

        // 줌 기능 추가
        const g = svg.append('g');

        const zoom = d3.zoom<SVGSVGElement, unknown>()
            .scaleExtent([0.1, 4])
            .on('zoom', (event) => {
                g.attr('transform', event.transform);
            });

        svg.call(zoom);

        // D3 Simulation setup
        // 노드와 링크의 깊은 복사본을 생성하여 시뮬레이션에 사용 (D3가 객체를 직접 수정하므로)
        const nodes: SimulationNode[] = graphData.nodes.map(d => ({ ...d }));
        // 링크 초기화 시 source/target은 id(number) 상태이지만, forceLink가 이를 객체 참조로 변환함
        // 타입 호환성을 위해 unknown을 거쳐서 캐스팅
        const links: SimulationLink[] = graphData.edges.map(d => ({ ...d })) as unknown as SimulationLink[];

        const simulation = d3.forceSimulation<SimulationNode>(nodes)
            .force('link', d3.forceLink<SimulationNode, SimulationLink>(links)
                .id((d) => d.id) // 노드의 id 접근자
                .distance((d) => 100 / (d.strength || 1)) // 강한 연결일수록 가까이
            )
            .force('charge', d3.forceManyBody().strength(-200))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(30));

        // 엣지 (연결선) 그리기
        const link = g.append('g')
            .selectAll('line')
            .data(links)
            .join('line')
            .attr('stroke', 'rgba(255, 255, 255, 0.3)')
            .attr('stroke-opacity', 0.6)
            .attr('stroke-width', (d) => d.strength * 3);

        // 노드 (메모) 그리기
        const node = g.append('g')
            .selectAll<SVGCircleElement, SimulationNode>('circle')
            .data(nodes)
            .join('circle')
            .attr('r', 8)
            .attr('fill', '#34d399') // Emerald-400 (Mint Green)
            .attr('stroke', '#fff')
            .attr('stroke-width', 2)
            .style('cursor', 'pointer');

        // 노드 레이블 그리기
        const labels = g.append('g')
            .selectAll('text')
            .data(nodes)
            .join('text')
            .text((d) => {
                const preview = d.content.substring(0, 20);
                return preview.length < d.content.length ? preview + '...' : preview;
            })
            .attr('font-size', 10)
            .attr('fill', '#e2e8f0') // Light text for dark mode
            .attr('dx', 12)
            .attr('dy', 4)
            .style('pointer-events', 'none');

        // 툴팁 설정
        const tooltip = d3.select('body').append('div')
            .attr('class', 'graph-tooltip')
            .style('position', 'absolute')
            .style('visibility', 'hidden')
            .style('background', 'rgba(0, 0, 0, 0.8)')
            .style('color', 'white')
            .style('padding', '8px')
            .style('border-radius', '4px')
            .style('font-size', '12px')
            .style('max-width', '300px')
            .style('z-index', '1000');

        // 노드 이벤트 핸들링
        node
            .on('mouseover', function (d) {
                d3.select(this).attr('r', 12);
                tooltip
                    .style('visibility', 'visible')
                    .html(`
            <strong>ID: ${d.id}</strong><br/>
            ${d.content}<br/>
            <em>${new Date(d.created_at).toLocaleDateString('ko-KR')}</em>
          `);
            })
            .on('mousemove', function (event) {
                tooltip
                    .style('top', (event.pageY - 10) + 'px')
                    .style('left', (event.pageX + 10) + 'px');
            })
            .on('mouseout', function () {
                d3.select(this).attr('r', 8);
                tooltip.style('visibility', 'hidden');
            });

        // 시뮬레이션 틱마다 위치 업데이트
        simulation.on('tick', () => {
            link
                .attr('x1', (d) => (d.source as SimulationNode).x || 0)
                .attr('y1', (d) => (d.source as SimulationNode).y || 0)
                .attr('x2', (d) => (d.target as SimulationNode).x || 0)
                .attr('y2', (d) => (d.target as SimulationNode).y || 0);

            node
                .attr('cx', (d) => d.x || 0)
                .attr('cy', (d) => d.y || 0);

            labels
                .attr('x', (d) => d.x || 0)
                .attr('y', (d) => d.y || 0);
        });

        // 드래그 동작 정의
        const drag = d3.drag<SVGCircleElement, SimulationNode>()
            .on('start', (event, d) => {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            })
            .on('drag', (event, d) => {
                d.fx = event.x;
                d.fy = event.y;
            })
            .on('end', (event, d) => {
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            });

        node.call(drag);

        // 컴포넌트 언마운트 시 정리
        return () => {
            simulation.stop();
            tooltip.remove();
        };
    }, [graphData]);

    if (loading) {
        return <div className="graph-loading">Loading graph...</div>;
    }

    if (!graphData || graphData.nodes.length === 0) {
        return <div className="graph-empty">No memories yet.</div>;
    }

    return (
        <div className="memory-graph-container">
            <div className="graph-header">
                <h3>Memory Connection Graph</h3>
                <button onClick={loadGraph}>Refresh</button>
            </div>
            <svg ref={svgRef}></svg>
            <div className="graph-legend">
                <p>💡 Drag nodes to adjust positions (Observation only). Line thickness indicates connection strength</p>
            </div>
        </div>
    );
};

export default MemoryGraph;
