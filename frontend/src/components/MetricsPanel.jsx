import { useState } from 'react';
import { downloadSimulationReport } from '../utils/downloadReport';

function MetricCard({ label, value, unit, color, icon, subtitle }) {
  return (
    <div style={{
      padding: '1rem',
      background: 'var(--bg-surface)',
      borderRadius: 'var(--radius-md)',
      border: '1px solid var(--border)',
      display: 'flex', flexDirection: 'column', gap: '0.25rem',
    }}>
      <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
        {icon} {label}
      </div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.3rem' }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '1.6rem', fontWeight: 700, color, lineHeight: 1 }}>
          {value !== null && value !== undefined ? value : '—'}
        </span>
        {unit && <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{unit}</span>}
      </div>
      {subtitle && <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>{subtitle}</div>}
    </div>
  );
}

function EnzymeRow({ enzyme }) {
  const statusColors = {
    active: 'var(--green)',
    allosteric: 'var(--amber)',
    inhibited: 'var(--red)',
    bypass: 'var(--purple)',
  };
  const color = statusColors[enzyme.status] || 'var(--text-secondary)';
  const pct = Math.round(enzyme.flux * 100);

  return (
    <div style={{
      padding: '0.65rem 0.85rem',
      borderRadius: 8,
      background: 'var(--bg-surface)',
      border: '1px solid var(--border)',
      marginBottom: 6,
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
        <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-primary)' }}>{enzyme.enzyme_name}</span>
        <span className={`badge badge-${enzyme.status}`}>{enzyme.status}</span>
      </div>
      <div className="flux-bar-container">
        <div
          className={`flux-bar ${pct >= 65 ? 'flux-high' : pct >= 35 ? 'flux-medium' : 'flux-low'}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.25rem', textAlign: 'right' }}>
        {pct}% flux
      </div>
    </div>
  );
}

export default function MetricsPanel({ result, isLoading, pathway }) {
  const [downloading, setDownloading] = useState(false);

  const handleDownload = () => {
    setDownloading(true);
    setTimeout(() => {
      downloadSimulationReport(result, pathway);
      setDownloading(false);
    }, 100);
  };

  if (isLoading) {
    return (
      <div className="card">
        <div style={{ marginBottom: '1rem', fontWeight: 700, fontSize: '0.9rem' }}>📊 Metrics</div>
        {[1, 2, 3].map(i => (
          <div key={i} className="skeleton" style={{ height: 70, marginBottom: 8 }} />
        ))}
      </div>
    );
  }

  if (!result) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '2rem 1.5rem' }}>
        <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📊</div>
        <div style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
          Run a simulation to see metrics
        </div>
      </div>
    );
  }

  const m = result.metrics;
  const totalATP = m?.atp_yield ?? 0;
  const atpColor = totalATP > 20 ? 'var(--green)' : totalATP > 5 ? 'var(--cyan)' : 'var(--red)';

  return (
    <div className="flex flex-col gap-3">
      {/* Scenario badge + download button */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
        <div style={{ fontWeight: 700, fontSize: '0.9rem' }}>📊 Simulation Results</div>
        {result.scenario_detected && (
          <span style={{
            padding: '3px 10px', borderRadius: 99,
            background: 'var(--cyan-dim)', color: 'var(--cyan)',
            border: '1px solid var(--border-active)',
            fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em',
          }}>
            {result.scenario_detected?.replace(/_/g, ' ')}
          </span>
        )}
        <button
          id="btn-download-report"
          onClick={handleDownload}
          disabled={downloading}
          style={{
            marginLeft: 'auto',
            padding: '5px 12px',
            borderRadius: 8,
            border: '1px solid var(--border-hover)',
            background: downloading ? 'var(--cyan-dim)' : 'var(--bg-surface)',
            color: downloading ? 'var(--cyan)' : 'var(--text-secondary)',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.72rem', fontWeight: 600,
            cursor: downloading ? 'wait' : 'pointer',
            display: 'flex', alignItems: 'center', gap: '0.35rem',
            transition: 'all var(--transition)',
            letterSpacing: '0.04em',
          }}
          onMouseEnter={e => { if (!downloading) { e.currentTarget.style.borderColor = 'var(--cyan)'; e.currentTarget.style.color = 'var(--cyan)'; } }}
          onMouseLeave={e => { if (!downloading) { e.currentTarget.style.borderColor = 'var(--border-hover)'; e.currentTarget.style.color = 'var(--text-secondary)'; } }}
        >
          {downloading ? '⏳ Downloading…' : '⬇ Download Report'}
        </button>
      </div>

      {/* Key metrics grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
        <MetricCard label="ATP Yield" value={totalATP.toFixed(1)} unit="ATP" color={atpColor} icon="⚡" />
        <MetricCard label="Net Flux" value={(m.net_flux * 100).toFixed(0)} unit="%" color="var(--cyan)" icon="🌊" />
        <MetricCard label="NADH" value={m.nadh_produced?.toFixed(2)} unit="" color="var(--purple)" icon="🔵" />
        <MetricCard label="FADH₂" value={m.fadh2_produced?.toFixed(2)} unit="" color="var(--amber)" icon="🟡" />
        {(m.nadph_produced != null && m.nadph_produced > 0) && (
          <MetricCard label="NADPH" value={m.nadph_produced?.toFixed(2)} unit="" color="#c084fc" icon="🛡️"
            subtitle="Antioxidant / reductive biosynthesis" />
        )}
        <MetricCard label="Lactate" value={(m.lactate_output * 100).toFixed(0)} unit="%" color={m.lactate_output > 0.5 ? 'var(--red)' : 'var(--text-secondary)'} icon="🧪" />
        <MetricCard label="CO₂ Released" value={m.co2_released?.toFixed(2)} unit="" color="var(--text-secondary)" icon="💨" />
      </div>


      {/* Warnings */}
      {result.warnings?.length > 0 && result.warnings.map((w, i) => (
        <div key={i} className="alert alert-danger">⚠️ {w}</div>
      ))}

      {/* Educational notes */}
      {result.educational_notes?.length > 0 && (
        <div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.5rem', fontWeight: 600 }}>
            📚 Key Insights
          </div>
          {result.educational_notes.map((n, i) => (
            <div key={i} className="alert alert-info" style={{ marginBottom: 8, fontSize: '0.82rem' }}>
              💡 {n}
            </div>
          ))}
        </div>
      )}

      {/* Enzyme flux breakdown */}
      {result.enzymes?.length > 0 && (
        <div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.5rem', fontWeight: 600 }}>
            ⚙️ Enzyme Activity
          </div>
          {result.enzymes.map(e => <EnzymeRow key={e.enzyme_id} enzyme={e} />)}
        </div>
      )}
    </div>
  );
}
