import { getEnzymeData } from '../utils/enzymeDatabase';

export default function EnzymeModal({ enzymeState, onClose }) {
  if (!enzymeState) return null;

  const db = getEnzymeData(enzymeState.enzyme_id);
  const status = enzymeState.status || 'active';
  const flux = enzymeState.flux ?? 0;
  const pct = Math.round(flux * 100);

  const statusColors = {
    active: 'var(--green)',
    inhibited: 'var(--red)',
    allosteric: 'var(--amber)',
    bypass: 'var(--purple)',
  };
  const statusColor = statusColors[status] || 'var(--text-secondary)';

  const ecClassColors = {
    Oxidoreductase: '#ef4444',
    Transferase: '#3b82f6',
    Hydrolase: '#10b981',
    Lyase: '#f59e0b',
    Isomerase: '#8b5cf6',
    Ligase: '#06b6d4',
  };
  const ecColor = db ? (ecClassColors[db.class] || '#6b7280') : '#6b7280';

  return (
    <div
      style={{
        position: 'fixed', inset: 0, zIndex: 1000,
        background: 'rgba(0,0,0,0.72)',
        backdropFilter: 'blur(6px)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        padding: '1rem',
        animation: 'fadeIn 0.18s ease',
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: 'var(--bg-card)',
          border: '1px solid var(--border-hover)',
          borderRadius: 'var(--radius-xl)',
          padding: '1.75rem',
          maxWidth: 560,
          width: '100%',
          maxHeight: '88vh',
          overflowY: 'auto',
          boxShadow: 'var(--shadow-lg)',
          animation: 'fadeInUp 0.22s cubic-bezier(0.4,0,0.2,1)',
          position: 'relative',
        }}
        onClick={e => e.stopPropagation()}
      >
        {/* Close button */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute', top: 14, right: 14,
            background: 'var(--bg-surface)', border: '1px solid var(--border)',
            borderRadius: 8, width: 30, height: 30,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            cursor: 'pointer', color: 'var(--text-muted)', fontSize: '1rem',
            transition: 'all var(--transition)',
          }}
          onMouseEnter={e => { e.target.style.color = 'var(--text-primary)'; e.target.style.borderColor = 'var(--border-active)'; }}
          onMouseLeave={e => { e.target.style.color = 'var(--text-muted)'; e.target.style.borderColor = 'var(--border)'; }}
        >✕</button>

        {/* Header */}
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start', marginBottom: '1.25rem', paddingRight: '2rem' }}>
          {/* Enzyme class colour dot */}
          <div style={{
            width: 52, height: 52, borderRadius: 12, flexShrink: 0,
            background: `${ecColor}18`, border: `2px solid ${ecColor}44`,
            display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
            gap: 2,
          }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: ecColor, fontWeight: 700, letterSpacing: '0.06em' }}>EC</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: ecColor, fontWeight: 700, lineHeight: 1 }}>
              {db?.ec?.split('.')[0] || '?'}
            </div>
          </div>
          <div>
            <h3 style={{ margin: 0, fontFamily: 'var(--font-sans)', letterSpacing: '-0.02em' }}>
              {db?.fullName || enzymeState.enzyme_name || enzymeState.enzyme_id}
            </h3>
            {db?.ec && (
              <div style={{
                display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.4rem', flexWrap: 'wrap',
              }}>
                <span style={{
                  fontFamily: 'var(--font-mono)', fontSize: '0.72rem',
                  padding: '2px 8px', borderRadius: 99,
                  background: `${ecColor}15`, color: ecColor, border: `1px solid ${ecColor}30`,
                }}>EC {db.ec}</span>
                <span style={{
                  fontFamily: 'var(--font-mono)', fontSize: '0.72rem',
                  padding: '2px 8px', borderRadius: 99,
                  background: 'var(--bg-surface)', border: '1px solid var(--border)', color: 'var(--text-secondary)',
                }}>{db.class}</span>
                <span style={{
                  padding: '2px 8px', borderRadius: 99, fontSize: '0.72rem', fontWeight: 700,
                  background: `${statusColor}15`, color: statusColor, border: `1px solid ${statusColor}30`,
                }}>{status}</span>
              </div>
            )}
          </div>
        </div>

        {/* Current flux state */}
        <div style={{ marginBottom: '1.25rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)', padding: '0.9rem', border: '1px solid var(--border)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
              Current Simulation State
            </span>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', fontWeight: 700, color: statusColor }}>
              {pct}% flux
            </span>
          </div>
          <div style={{ height: 6, background: 'rgba(255,255,255,0.06)', borderRadius: 99, overflow: 'hidden' }}>
            <div style={{
              height: '100%', borderRadius: 99,
              width: `${pct}%`,
              background: pct >= 65 ? 'var(--green)' : pct >= 35 ? 'var(--amber)' : 'var(--red)',
              transition: 'width 0.6s ease',
            }} />
          </div>
          {enzymeState.regulators?.length > 0 && (
            <div style={{ marginTop: '0.6rem', display: 'flex', gap: '5px', flexWrap: 'wrap' }}>
              {enzymeState.regulators.map((r, i) => (
                <span key={i} style={{
                  fontSize: '0.7rem', padding: '1px 7px', borderRadius: 99,
                  background: 'var(--bg-card)', border: '1px solid var(--border)', color: 'var(--text-secondary)',
                  fontFamily: 'var(--font-mono)',
                }}>{r}</span>
              ))}
            </div>
          )}
        </div>

        {db && (
          <>
            {/* Reaction */}
            <div style={{ marginBottom: '1rem' }}>
              <div className="section-title">⚗️ Catalysed Reaction</div>
              <div style={{
                fontFamily: 'var(--font-mono)', fontSize: '0.82rem',
                background: 'var(--bg-surface)', border: '1px solid var(--border)',
                borderLeft: `3px solid ${ecColor}`,
                borderRadius: '0 8px 8px 0', padding: '0.75rem 1rem',
                color: 'var(--text-primary)', lineHeight: 1.6,
              }}>{db.reaction}</div>
            </div>

            {/* Details grid */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', marginBottom: '1rem' }}>
              {[
                ['Enzyme Class', db.class],
                ['Subclass', db.subclass],
                ['Location', db.location],
                ['EC Number', db.ec],
              ].map(([label, val]) => (
                <div key={label} style={{ background: 'var(--bg-surface)', border: '1px solid var(--border)', borderRadius: 8, padding: '0.65rem 0.8rem' }}>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', fontFamily: 'var(--font-mono)', marginBottom: '0.25rem', fontWeight: 600 }}>{label}</div>
                  <div style={{ fontSize: '0.82rem', color: 'var(--text-primary)', fontWeight: 500 }}>{val}</div>
                </div>
              ))}
            </div>

            {/* Regulation */}
            {db.regulation && (
              <div style={{ marginBottom: '1rem' }}>
                <div className="section-title">🔬 Regulation</div>
                <div style={{ background: 'rgba(255,183,0,0.07)', border: '1px solid rgba(255,183,0,0.2)', borderRadius: 8, padding: '0.75rem', fontSize: '0.83rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  {db.regulation}
                </div>
              </div>
            )}

            {/* Clinical note */}
            {db.clinicalNote && (
              <div style={{ marginBottom: '1rem' }}>
                <div className="section-title">🏥 Clinical Relevance</div>
                <div style={{ background: 'rgba(0,229,255,0.05)', border: '1px solid rgba(0,229,255,0.15)', borderRadius: 8, padding: '0.75rem', fontSize: '0.83rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  {db.clinicalNote}
                </div>
              </div>
            )}

            {/* PDB structure link */}
            {db.pdbId && (
              <div>
                <div className="section-title">🧬 3D Structure</div>
                <a
                  href={`https://www.rcsb.org/structure/${db.pdbId}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    display: 'inline-flex', alignItems: 'center', gap: '0.4rem',
                    padding: '0.5rem 1rem',
                    background: 'var(--blue-dim)', border: '1px solid rgba(68,136,255,0.3)',
                    borderRadius: 8, color: 'var(--blue)',
                    textDecoration: 'none', fontSize: '0.82rem', fontWeight: 600,
                    fontFamily: 'var(--font-mono)', transition: 'all var(--transition)',
                  }}
                  onMouseEnter={e => { e.target.style.background = 'rgba(68,136,255,0.12)'; }}
                  onMouseLeave={e => { e.target.style.background = 'var(--blue-dim)'; }}
                >
                  🔗 PDB:{db.pdbId} — View 3D Structure on RCSB
                </a>
              </div>
            )}
          </>
        )}

        {!db && (
          <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center', padding: '1rem' }}>
            Detailed data not yet available for this enzyme.
          </div>
        )}
      </div>
    </div>
  );
}
