import { useEffect, useRef, useMemo } from 'react';
import * as d3 from 'd3';
import { PATHWAYS_DATA } from '../utils/pathwayData';

const STATUS_COLORS = {
  active:     '#00ff88',
  allosteric: '#ffaa00',
  inhibited:  '#ff4d6d',
  bypass:     '#b388ff',
};

export default function PathwayMap({ pathway, simulationResult, isLoading, onEnzymeClick }) {
  const svgRef = useRef(null);

  const pathwayDef = PATHWAYS_DATA[pathway] || PATHWAYS_DATA.glycolysis;

  // Build enzyme status lookup from simulation result
  const enzymeStatus = useMemo(() => {
    const map = {};
    if (simulationResult?.enzymes) {
      for (const e of simulationResult.enzymes) {
        map[e.enzyme_id] = e;
      }
    }
    return map;
  }, [simulationResult]);

  useEffect(() => {
    if (!svgRef.current) return;
    const nodes = pathwayDef.nodes;
    const edges = pathwayDef.edges;

    const svgEl = svgRef.current;
    const W = svgEl.clientWidth || 680;
    const H = svgEl.clientHeight || 760;

    // Clear previous
    d3.select(svgEl).selectAll('*').remove();

    const svg = d3.select(svgEl)
      .attr('viewBox', `0 0 760 780`)
      .attr('preserveAspectRatio', 'xMidYMid meet');

    // Arrow marker definition
    svg.append('defs').selectAll('marker')
      .data(['arrow-active', 'arrow-dim'])
      .join('marker')
      .attr('id', d => d)
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 16)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', (d) => d === 'arrow-active' ? '#00d4ff' : 'rgba(255,255,255,0.15)');

    // Node lookup
    const nodeById = {};
    for (const n of nodes) nodeById[n.id] = n;

    // Draw edges
    const edgeGroup = svg.append('g').attr('class', 'edges');
    for (const edge of edges) {
      const s = nodeById[edge.source];
      const t = nodeById[edge.target];
      if (!s || !t) continue;

      const eState = enzymeStatus[edge.enzyme];
      const flux = eState?.flux ?? 0;
      const hasResult = !!simulationResult;
      const color = hasResult
        ? (flux > 0.65 ? '#00ff88' : flux > 0.35 ? '#ffaa00' : '#ff4d6d')
        : 'rgba(255,255,255,0.15)';
      const strokeW = hasResult ? 1.5 + flux * 3 : 1.5;

      edgeGroup.append('line')
        .attr('x1', s.x).attr('y1', s.y)
        .attr('x2', t.x).attr('y2', t.y)
        .attr('stroke', color)
        .attr('stroke-width', strokeW)
        .attr('marker-end', `url(#${hasResult ? 'arrow-active' : 'arrow-dim'})`)
        .attr('opacity', hasResult ? 0.85 : 0.25)
        .style('filter', hasResult && flux > 0.6 ? `drop-shadow(0 0 4px ${color})` : 'none')
        .style('transition', 'all 0.5s ease');
    }

    // Draw nodes
    const nodeGroup = svg.append('g').attr('class', 'nodes');

    for (const node of nodes) {
      const isEnzyme = node.type === 'enzyme';
      const eState = isEnzyme ? enzymeStatus[node.enzymeid] : null;
      const status = eState?.status ?? 'active';
      const flux = eState?.flux ?? 0;
      const hasResult = !!simulationResult;
      const r = 22; // metabolite circle radius — declared here so label code can access it

      const color = isEnzyme && hasResult
        ? (STATUS_COLORS[status] || '#8b9ab8')
        : isEnzyme ? '#0080ff' : '#4a6080';

      const g = nodeGroup.append('g')
        .attr('transform', `translate(${node.x},${node.y})`)
        .style('cursor', isEnzyme ? 'pointer' : 'default');

      if (isEnzyme) {
        // Rectangle for enzyme
        const w = 108, h = 30;
        g.append('rect')
          .attr('x', -w / 2).attr('y', -h / 2)
          .attr('width', w).attr('height', h)
          .attr('rx', 6)
          .attr('fill', hasResult ? `${color}1a` : 'rgba(10,20,40,0.8)')
          .attr('stroke', color)
          .attr('stroke-width', hasResult ? 1.5 : 0.7)
          .style('filter', hasResult && flux > 0.6 ? `drop-shadow(0 0 8px ${color})` : 'none')
          .style('transition', 'all 0.5s ease');

        // Flux bar beneath enzyme
        if (hasResult) {
          g.append('rect')
            .attr('x', -w / 2 + 2).attr('y', h / 2 + 3)
            .attr('width', (w - 4) * flux).attr('height', 3)
            .attr('rx', 2)
            .attr('fill', color)
            .attr('opacity', 0.7)
            .style('transition', 'width 0.6s ease');
        }

        g.on('click', () => eState && onEnzymeClick(eState));
        g.on('mouseenter', function () {
          d3.select(this).select('rect').attr('fill', `${color}30`);
        });
        g.on('mouseleave', function () {
          d3.select(this).select('rect').attr('fill', hasResult ? `${color}1a` : 'rgba(10,20,40,0.8)');
        });
      } else {
        // Circle for metabolite
        const mState = simulationResult?.metabolites?.find(m => m.metabolite_id === node.id);
        const conc = mState?.concentration ?? 0;
        const mColor = hasResult
          ? (conc > 0.6 ? '#00ff88' : conc > 0.3 ? '#00d4ff' : '#607090')
          : 'rgba(30,50,80,0.9)';
        const mStroke = hasResult
          ? (conc > 0.6 ? '#00ff88' : conc > 0.3 ? '#00d4ff' : '#4a6080')
          : '#2a3a55';

        g.append('circle')
          .attr('r', r)
          .attr('fill', mColor + (hasResult ? '28' : ''))
          .attr('stroke', mStroke)
          .attr('stroke-width', hasResult ? 1.8 : 1)
          .style('transition', 'all 0.5s ease');

        if (hasResult && conc > 0.5) {
          g.append('circle')
            .attr('r', r + 6)
            .attr('fill', 'none')
            .attr('stroke', mStroke)
            .attr('stroke-width', 0.5)
            .attr('opacity', 0.35)
            .attr('class', 'pulse');
        }
      }

      // Label
      const labelLines = node.label.split('\n');
      labelLines.forEach((line, i) => {
        g.append('text')
          .attr('text-anchor', 'middle')
          .attr('y', isEnzyme ? (labelLines.length > 1 ? (i - 0.3) * 11 : 4) : (r + 14 + i * 11))
          .attr('fill', isEnzyme ? color : 'var(--text-secondary)')
          .attr('font-size', isEnzyme ? '9.5px' : '10px')
          .attr('font-family', 'Inter, sans-serif')
          .attr('font-weight', isEnzyme ? '600' : '500')
          .text(line);
      });

      // ATP / NADH / FADH2 badges — small pills below enzyme rect
      if (isEnzyme) {
        const badges = [];
        if (node.atp === 'consumed')  badges.push({ text: 'ATP↓', fill: '#ff4d6d33', stroke: '#ff4d6d', textColor: '#ff6b82' });
        if (node.atp === 'produced')  badges.push({ text: 'ATP↑', fill: '#00d4ff22', stroke: '#00d4ff', textColor: '#00d4ff' });
        if (node.nadh === 'produced') badges.push({ text: 'NADH↑', fill: '#ffcc0022', stroke: '#ffcc00', textColor: '#ffcc00' });
        if (node.nadh === 'consumed') badges.push({ text: 'NADH↓', fill: '#ffffff11', stroke: '#607090', textColor: '#8090a8' });
        if (node.fadh2 === 'produced')badges.push({ text: 'FADH₂↑', fill: '#fb923c22', stroke: '#fb923c', textColor: '#fb923c' });

        const bw = 36, bh = 11, gap = 3;
        const totalW = badges.length * bw + (badges.length - 1) * gap;
        const startX = -totalW / 2;
        const baseY = 22; // below the rect (rect h=30, half=15, +7 pad)

        badges.forEach((b, bi) => {
          const bx = startX + bi * (bw + gap);
          const bg = g.append('g').attr('transform', `translate(${bx + bw/2}, ${baseY})`);
          bg.append('rect')
            .attr('x', -bw/2).attr('y', -bh/2)
            .attr('width', bw).attr('height', bh)
            .attr('rx', 3)
            .attr('fill', b.fill)
            .attr('stroke', b.stroke)
            .attr('stroke-width', 0.6);
          bg.append('text')
            .attr('text-anchor', 'middle')
            .attr('y', 4)
            .attr('font-size', '7px')
            .attr('font-family', 'Inter, sans-serif')
            .attr('font-weight', '700')
            .attr('fill', b.textColor)
            .text(b.text);
        });
      }
    }
  }, [pathwayDef, enzymeStatus, simulationResult]);

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      {/* Header */}
      <div style={{
        padding: '0.85rem 1.25rem',
        borderBottom: '1px solid var(--border)',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <span style={{ color: pathwayDef.color, fontSize: '1.2rem' }}>
            {{ glycolysis: '🍬', tca_cycle: '🔃', oxphos: '⚡', gluconeogenesis: '🔄', integrated: '🌐' }[pathway] || '🧬'}
          </span>
          <span style={{ fontWeight: 700, fontSize: '1rem' }}>{pathwayDef.name}</span>
        </div>
        {simulationResult && (
          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            <span style={{ color: 'var(--green)', fontWeight: 700 }}>●</span> Simulation active
            <span style={{ marginLeft: '0.5rem' }}>Click enzymes for info</span>
          </div>
        )}
        {!simulationResult && !isLoading && (
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Run simulation to activate</span>
        )}
        {isLoading && (
          <span style={{ fontSize: '0.78rem', color: 'var(--cyan)' }} className="pulse">Simulating…</span>
        )}
      </div>

      {/* Legend */}
      {simulationResult && (
        <div style={{
          position: 'absolute', bottom: 12, left: 12,
          display: 'flex', gap: '12px', fontSize: '0.72rem',
          background: 'rgba(6,8,15,0.85)', padding: '6px 12px', borderRadius: 8,
          backdropFilter: 'blur(8px)',
        }}>
          {Object.entries(STATUS_COLORS).map(([s, c]) => (
            <span key={s} style={{ display: 'flex', alignItems: 'center', gap: 4, color: c }}>
              <span style={{ width: 8, height: 8, background: c, borderRadius: 2, display: 'inline-block' }} />
              {s}
            </span>
          ))}
        </div>
      )}

      <svg
        ref={svgRef}
        style={{ width: '100%', height: 'calc(100% - 52px)', display: 'block' }}
      />
    </div>
  );
}
