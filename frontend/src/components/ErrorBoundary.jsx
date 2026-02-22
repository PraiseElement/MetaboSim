import React from 'react';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    console.error('[MetaboSim ErrorBoundary]', error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          padding: '2rem',
          background: 'rgba(255,77,109,0.08)',
          border: '1px solid rgba(255,77,109,0.3)',
          borderRadius: 12,
          color: '#ffa0b0',
          margin: '1rem',
        }}>
          <div style={{ fontWeight: 700, marginBottom: '0.5rem' }}>⚠️ Render Error</div>
          <pre style={{ fontSize: '0.78rem', whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
            {this.state.error?.message}
          </pre>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            style={{
              marginTop: '1rem',
              padding: '0.5rem 1rem',
              background: 'rgba(255,77,109,0.2)',
              border: '1px solid rgba(255,77,109,0.4)',
              borderRadius: 8,
              color: '#ffa0b0',
              cursor: 'pointer',
              fontFamily: 'inherit',
            }}
          >
            ↺ Try Again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
