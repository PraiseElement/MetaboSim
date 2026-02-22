import { useState } from 'react';
import { fetchQuiz, checkAnswer } from '../utils/api';

const PATHWAY_GROUPS = [
  {
    group: '🔵 Carbohydrate Metabolism',
    color: '#00e5ff',
    pathways: [
      { id: 'glycolysis',          name: 'Glycolysis',           icon: '⬡', count: 25 },
      { id: 'tca_cycle',           name: 'TCA Cycle',            icon: '◎', count: 22 },
      { id: 'oxphos',              name: 'Oxidative Phosph.',    icon: '⚡', count: 22 },
      { id: 'gluconeogenesis',     name: 'Gluconeogenesis',      icon: '↺',  count: 18 },
      { id: 'hmp_shunt',           name: 'HMP Shunt',            icon: '⬢', count: 15 },
      { id: 'glycogenesis',        name: 'Glycogenesis',         icon: '📦', count: 12 },
      { id: 'glycogenolysis',      name: 'Glycogenolysis',       icon: '📤', count: 12 },
      { id: 'fructose_metabolism', name: 'Fructose Metabolism',  icon: '🍑', count: 10 },
    ],
  },
  {
    group: '🟣 Amino Acid Metabolism',
    color: '#c084fc',
    pathways: [
      { id: 'amino_acid_catabolism',  name: 'AA Catabolism',      icon: '🔸', count: 12 },
      { id: 'urea_cycle',             name: 'Urea Cycle',         icon: '♻️',  count: 12 },
      { id: 'amino_acid_synthesis',   name: 'AA Synthesis',       icon: '🔷', count: 10 },
      { id: 'phenylalanine_tyrosine', name: 'Phe / Tyr',          icon: '💊', count: 10 },
      { id: 'branched_chain_aa',      name: 'Branched-Chain AAs', icon: '🌿', count: 10 },
    ],
  },
  {
    group: '🟡 Lipid Metabolism',
    color: '#ffb700',
    pathways: [
      { id: 'fatty_acid_oxidation',   name: 'β-Oxidation',          icon: '⚗️', count: 12 },
      { id: 'fatty_acid_synthesis',   name: 'FA Synthesis',          icon: '🧪', count: 10 },
      { id: 'ketogenesis',            name: 'Ketogenesis',           icon: '🔥', count: 10 },
      { id: 'cholesterol_synthesis',  name: 'Cholesterol Synthesis', icon: '🫀', count: 10 },
      { id: 'lipoprotein_metabolism', name: 'Lipoproteins',          icon: '🩸', count: 10 },
    ],
  },
  {
    group: '🟢 Nucleotide Metabolism',
    color: '#00ff9d',
    pathways: [
      { id: 'purine_synthesis',       name: 'Purine Synthesis',      icon: '🔬', count: 10 },
      { id: 'pyrimidine_synthesis',   name: 'Pyrimidine Synthesis',  icon: '🧬', count: 10 },
      { id: 'purine_salvage',         name: 'Purine Salvage',        icon: '♻️',  count: 8  },
      { id: 'nucleotide_degradation', name: 'Nucleotide Degradation',icon: '💥', count: 8  },
    ],
  },
  {
    group: '🔴 Clinical & Integration',
    color: '#ff4d6d',
    pathways: [
      { id: 'clinical',              name: 'Clinical Disorders',    icon: '✚', count: 20 },
      { id: 'integrated_metabolism', name: 'Integrated Metabolism', icon: '🌐', count: 20 },
    ],
  },
];

// Flat list for name lookups
const PATHWAY_OPTIONS = PATHWAY_GROUPS.flatMap(g => g.pathways);

export default function QuizModule() {
  const [selectedPathway, setSelectedPathway] = useState(null);
  const [questions, setQuestions]   = useState([]);
  const [current, setCurrent]       = useState(0);
  const [answered, setAnswered]     = useState({});
  const [loading, setLoading]       = useState(false);
  const [error, setError]           = useState(null);

  const startQuiz = async (pathway) => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchQuiz(pathway);
      setQuestions(data.questions);
      setSelectedPathway(pathway);
      setCurrent(0);
      setAnswered({});
    } catch {
      setError('Could not load quiz. Make sure the backend is running.');
    }
    setLoading(false);
  };

  const submit = async (qid, idx) => {
    if (answered[qid]) return;
    try {
      const result = await checkAnswer(selectedPathway, qid, idx);
      setAnswered(a => ({ ...a, [qid]: { submitted: idx, result } }));
    } catch {
      setError('Failed to check answer.');
    }
  };

  const score      = Object.values(answered).filter(a => a.result?.correct).length;
  const total      = questions.length;
  const isFinished = Object.keys(answered).length === total && total > 0;

  // ── Category selection screen ──────────────────────────────────────
  if (!selectedPathway) {
    return (
      <div style={{ padding: '2rem 1.25rem', maxWidth: 860, margin: '0 auto' }}>
        <h2 style={{ marginBottom: '0.4rem' }}>📝 Quiz Mode</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
          Test your understanding of metabolic pathways with scenario-based questions.
        </p>
        {error && <div className="alert alert-danger mb-4">{error}</div>}

        {PATHWAY_GROUPS.map(group => (
          <div key={group.group} style={{ marginBottom: '2rem' }}>
            {/* Group label */}
            <div style={{
              fontSize: '0.72rem',
              fontWeight: 700,
              color: group.color,
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              marginBottom: '0.75rem',
              fontFamily: 'var(--font-mono)',
              borderBottom: `1px solid ${group.color}22`,
              paddingBottom: '0.4rem',
            }}>
              {group.group}
            </div>

            {/* Pathway cards */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))',
              gap: '0.75rem',
            }}>
              {group.pathways.map(p => (
                <div
                  key={p.id}
                  id={`quiz-start-${p.id}`}
                  className="card"
                  style={{ cursor: 'pointer', textAlign: 'center', padding: '1.25rem 0.75rem', transition: 'all 0.2s ease' }}
                  onClick={() => startQuiz(p.id)}
                  onMouseEnter={e => { e.currentTarget.style.borderColor = group.color; e.currentTarget.style.transform = 'translateY(-3px)'; }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.transform = 'translateY(0)'; }}
                >
                  <div style={{ fontSize: '1.5rem', marginBottom: '0.4rem', color: group.color }}>{p.icon}</div>
                  <div style={{ fontWeight: 700, fontSize: '0.82rem', marginBottom: '0.2rem', fontFamily: 'var(--font-sans)', lineHeight: 1.3 }}>{p.name}</div>
                  <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>{p.count} questions</div>
                </div>
              ))}
            </div>
          </div>
        ))}

        {loading && <div style={{ textAlign: 'center', marginTop: '1rem', color: 'var(--cyan)' }} className="pulse">Loading quiz…</div>}
      </div>
    );
  }

  const q = questions[current];

  return (
    <div style={{ padding: '2rem 1.25rem', maxWidth: 680, margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '0.5rem' }}>
        <div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600 }}>
            {PATHWAY_OPTIONS.find(p => p.id === selectedPathway)?.name} Quiz
          </span>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            Question {current + 1} of {total}
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--green)', fontWeight: 700 }}>
            {score} / {Object.keys(answered).length} correct
          </span>
          <button id="btn-quit-quiz" className="btn btn-ghost btn-sm" onClick={() => setSelectedPathway(null)}>
            ✕ Quit
          </button>
        </div>
      </div>

      {/* Progress */}
      <div className="flux-bar-container" style={{ marginBottom: '1.5rem' }}>
        <div className="flux-bar flux-high" style={{ width: `${(Object.keys(answered).length / total) * 100}%` }} />
      </div>

      {/* Finished state */}
      {isFinished && (
        <div className="card animate-in" style={{ textAlign: 'center', padding: '2.5rem', marginBottom: '1.5rem' }}>
          <div style={{ fontSize: '3rem', marginBottom: '0.75rem' }}>
            {score === total ? '🏆' : score >= total * 0.7 ? '🎉' : '📚'}
          </div>
          <h2 style={{ marginBottom: '0.5rem' }}>Quiz Complete!</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            You scored <strong style={{ color: 'var(--cyan)' }}>{score}</strong> out of <strong>{total}</strong>
            {score === total ? ' — Perfect! 🌟' : score >= total * 0.7 ? ' — Well done!' : ' — Keep studying!'}
          </p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <button id="btn-retry-quiz" className="btn btn-primary" onClick={() => startQuiz(selectedPathway)}>↺ Retry</button>
            <button id="btn-change-pathway" className="btn btn-secondary" onClick={() => setSelectedPathway(null)}>
              Pick Another Pathway
            </button>
          </div>
        </div>
      )}

      {/* Question card */}
      {q && (
        <div className="card animate-in" key={q.id} style={{ marginBottom: '1rem' }}>
          <p style={{ fontSize: '1.05rem', fontWeight: 600, lineHeight: 1.5, marginBottom: '1.5rem', color: 'var(--text-primary)' }}>
            {q.question}
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
            {q.options.map((opt, idx) => {
              const ans = answered[q.id];
              let bg = 'var(--bg-surface)', border = 'var(--border)', color = 'var(--text-primary)';
              if (ans) {
                if (idx === ans.result.correct_index)  { bg = 'var(--green-dim)'; border = 'rgba(0,255,136,0.35)'; color = 'var(--green)'; }
                else if (idx === ans.submitted && !ans.result.correct) { bg = 'var(--red-dim)'; border = 'rgba(255,77,109,0.35)'; color = 'var(--red)'; }
              }
              return (
                <button
                  key={idx}
                  id={`quiz-option-${q.id}-${idx}`}
                  onClick={() => submit(q.id, idx)}
                  disabled={!!ans}
                  style={{
                    padding: '0.85rem 1rem', borderRadius: 10,
                    border: `1px solid ${border}`, background: bg, color,
                    textAlign: 'left', fontFamily: 'var(--font-sans)', fontSize: '0.9rem',
                    cursor: ans ? 'default' : 'pointer', transition: 'all 0.2s ease',
                    fontWeight: ans && idx === ans.result.correct_index ? 700 : 400,
                  }}
                  onMouseEnter={e => { if (!ans) e.currentTarget.style.borderColor = 'var(--cyan)'; }}
                  onMouseLeave={e => { if (!ans) e.currentTarget.style.borderColor = 'var(--border)'; }}
                >
                  <span style={{ marginRight: '0.6rem', fontWeight: 700 }}>{['A', 'B', 'C', 'D'][idx]}.</span>
                  {opt}
                </button>
              );
            })}
          </div>

          {/* Explanation */}
          {answered[q.id] && (
            <div
              className={`alert animate-in ${answered[q.id].result.correct ? 'alert-success' : 'alert-danger'}`}
              style={{ marginTop: '1rem', fontSize: '0.85rem' }}
            >
              {answered[q.id].result.correct ? '✅ Correct! ' : '❌ Incorrect. '}
              {answered[q.id].result.explanation}
            </div>
          )}
        </div>
      )}

      {/* Navigation */}
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: '0.5rem' }}>
        <button id="btn-prev-q" className="btn btn-secondary" disabled={current === 0} onClick={() => setCurrent(c => c - 1)}>← Previous</button>
        <button id="btn-next-q" className="btn btn-secondary" disabled={current === total - 1} onClick={() => setCurrent(c => c + 1)}>Next →</button>
      </div>
    </div>
  );
}
