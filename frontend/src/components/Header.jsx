import { useState, useEffect } from 'react';
import { useTheme } from '../context/ThemeContext';

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: '◈', shortcut: '1' },
  { id: 'simulate',  label: 'Simulate',  icon: '⬡', shortcut: '2' },
  { id: 'clinical',  label: 'Clinical',  icon: '✚', shortcut: '3' },
  { id: 'quiz',      label: 'Quiz',      icon: '◆', shortcut: '4' },
  { id: 'guide',     label: 'Guide',     icon: '?', shortcut: '5' },
];


function Clock() {
  const [t, setT] = useState(new Date());
  useEffect(() => {
    const id = setInterval(() => setT(new Date()), 1000);
    return () => clearInterval(id);
  }, []);
  const hh = String(t.getHours()).padStart(2, '0');
  const mm = String(t.getMinutes()).padStart(2, '0');
  const ss = String(t.getSeconds()).padStart(2, '0');
  return (
    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--text-muted)', letterSpacing: '0.06em' }}>
      {hh}:{mm}:{ss}
    </span>
  );
}

function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === 'dark';
  return (
    <button
      id="btn-theme-toggle"
      onClick={toggleTheme}
      title={isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
      style={{
        width: 34, height: 34,
        borderRadius: 9,
        border: '1px solid var(--border-hover)',
        background: 'var(--bg-card)',
        cursor: 'pointer',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: '1rem',
        color: 'var(--text-secondary)',
        transition: 'all var(--transition)',
        flexShrink: 0,
      }}
      onMouseEnter={e => {
        e.currentTarget.style.borderColor = 'var(--cyan)';
        e.currentTarget.style.color = 'var(--cyan)';
        e.currentTarget.style.boxShadow = 'var(--cyan-glow)';
      }}
      onMouseLeave={e => {
        e.currentTarget.style.borderColor = 'var(--border-hover)';
        e.currentTarget.style.color = 'var(--text-secondary)';
        e.currentTarget.style.boxShadow = 'none';
      }}
    >
      {isDark ? '☀' : '☾'}
    </button>
  );
}

export default function Header({ activePage, onNavigate }) {
  return (
    <header style={{
      height: 'var(--header-h)',
      background: 'var(--bg-glass)',
      backdropFilter: 'blur(24px)',
      WebkitBackdropFilter: 'blur(24px)',
      borderBottom: '1px solid var(--border-hover)',
      display: 'flex',
      alignItems: 'center',
      padding: '0 1.25rem',
      gap: '1.5rem',
      position: 'sticky',
      top: 0,
      zIndex: 100,
    }}>
      {/* Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.7rem', flexShrink: 0 }}>
        <div style={{
          width: 34, height: 34,
          background: 'linear-gradient(135deg, #00e5ff 0%, #00b4d8 50%, #0077b6 100%)',
          borderRadius: 9,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '1.1rem',
          boxShadow: '0 0 18px rgba(0,229,255,0.35), 0 2px 6px rgba(0,0,0,0.3)',
          flexShrink: 0,
        }}>⬡</div>
        <div>
          <div style={{
            fontFamily: 'var(--font-sans)',
            fontWeight: 800, fontSize: '1.05rem', lineHeight: 1.1,
            letterSpacing: '-0.04em',
            color: 'var(--text-primary)',
          }}>
            Metabo<span style={{ color: 'var(--cyan)' }}>Sim</span>
          </div>
          <div style={{
            fontSize: '0.6rem', color: 'var(--text-muted)',
            letterSpacing: '0.14em', textTransform: 'uppercase',
            fontFamily: 'var(--font-mono)',
          }}>
            Metabolic Pathway Simulator
          </div>
        </div>
      </div>

      {/* Separator */}
      <div style={{ width: 1, height: 28, background: 'var(--border)', flexShrink: 0 }} />

      {/* Navigation */}
      <nav style={{ display: 'flex', gap: '3px', flex: 1, justifyContent: 'center' }}>
        {NAV_ITEMS.map(item => {
          const active = activePage === item.id;
          return (
            <button
              key={item.id}
              id={`nav-${item.id}`}
              onClick={() => onNavigate(item.id)}
              style={{
                padding: '0.42rem 1.15rem',
                borderRadius: 8,
                border: active ? '1px solid var(--border-active)' : '1px solid transparent',
                background: active
                  ? 'linear-gradient(135deg, var(--cyan-dim), rgba(0,180,216,0.05))'
                  : 'transparent',
                color: active ? 'var(--cyan)' : 'var(--text-secondary)',
                fontFamily: 'var(--font-sans)',
                fontWeight: 600,
                fontSize: '0.855rem',
                cursor: 'pointer',
                transition: 'all var(--transition)',
                display: 'flex', alignItems: 'center', gap: '0.45rem',
                boxShadow: active ? 'inset 0 1px 0 rgba(0,229,255,0.12)' : 'none',
                letterSpacing: '0.01em',
              }}
              onMouseEnter={e => {
                if (!active) {
                  e.currentTarget.style.color = 'var(--text-primary)';
                  e.currentTarget.style.background = 'var(--bg-card)';
                }
              }}
              onMouseLeave={e => {
                if (!active) {
                  e.currentTarget.style.color = 'var(--text-secondary)';
                  e.currentTarget.style.background = 'transparent';
                }
              }}
            >
              <span style={{
                fontSize: active ? '0.9rem' : '0.8rem',
                opacity: active ? 1 : 0.5,
                transition: 'all var(--transition)',
              }}>{item.icon}</span>
              {item.label}
            </button>
          );
        })}
      </nav>

      {/* Right-side status + theme toggle */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexShrink: 0 }}>
        <Clock />
        <div style={{ width: 1, height: 20, background: 'var(--border)' }} />
        {/* API status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.7rem' }}>
          <span style={{
            width: 7, height: 7, borderRadius: '50%',
            background: 'var(--green)',
            boxShadow: '0 0 8px rgba(0,255,157,0.6)',
            animation: 'pulse 2s ease-in-out infinite',
            display: 'inline-block',
          }} />
          <span style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', letterSpacing: '0.04em' }}>API LIVE</span>
        </div>
        <div style={{ width: 1, height: 20, background: 'var(--border)' }} />
        {/* Theme toggle */}
        <ThemeToggle />
        <div style={{
          padding: '3px 10px', borderRadius: 99,
          background: 'var(--green-dim)', color: 'var(--green)',
          border: '1px solid rgba(0,255,157,0.18)',
          fontSize: '0.68rem', fontWeight: 700,
          letterSpacing: '0.06em', fontFamily: 'var(--font-mono)',
        }}>
          v2.0
        </div>
      </div>
    </header>
  );
}
