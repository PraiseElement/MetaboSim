import { useState, useEffect } from 'react';
import { runSimulation, fetchScenarios } from '../utils/api';

const PATHWAY_GROUPS = [
  {
    label: '🍬 Carbohydrate Metabolism',
    pathways: [
      { id: 'glycolysis',          name: 'Glycolysis' },
      { id: 'gluconeogenesis',     name: 'Gluconeogenesis' },
      { id: 'tca_cycle',           name: 'TCA Cycle' },
      { id: 'oxphos',              name: 'Oxidative Phosphorylation' },
      { id: 'hmp_shunt',           name: 'HMP Shunt (Pentose Phosphate)' },
      { id: 'glycogenesis',        name: 'Glycogenesis' },
      { id: 'glycogenolysis',      name: 'Glycogenolysis' },
      { id: 'fructose_metabolism', name: 'Fructose Metabolism' },
      { id: 'galactose_metabolism',name: 'Galactose Metabolism' },
      { id: 'integrated',          name: 'Integrated (All Carbohydrate)' },
    ],
  },
  {
    label: '🧬 Amino Acid Metabolism',
    pathways: [
      { id: 'amino_acid_catabolism', name: 'Amino Acid Catabolism' },
      { id: 'urea_cycle',            name: 'Urea Cycle' },
      { id: 'phenylalanine_tyrosine',name: 'Phenylalanine & Tyrosine' },
      { id: 'branched_chain_aa',     name: 'BCAA Catabolism' },
      { id: 'amino_acid_synthesis',  name: 'Amino Acid Synthesis' },
    ],
  },
  {
    label: '💧 Lipid Metabolism',
    pathways: [
      { id: 'fatty_acid_oxidation',  name: 'β-Oxidation (FA Oxidation)' },
      { id: 'fatty_acid_synthesis',  name: 'Fatty Acid Synthesis (DNL)' },
      { id: 'ketogenesis',           name: 'Ketogenesis & Ketolysis' },
      { id: 'cholesterol_synthesis', name: 'Cholesterol Synthesis' },
      { id: 'lipoprotein_metabolism',name: 'Lipoprotein Metabolism' },
    ],
  },
  {
    label: '🧪 Nucleotide Metabolism',
    pathways: [
      { id: 'purine_synthesis',       name: 'Purine De Novo Synthesis' },
      { id: 'pyrimidine_synthesis',   name: 'Pyrimidine De Novo Synthesis' },
      { id: 'purine_salvage',         name: 'Purine Salvage' },
      { id: 'nucleotide_degradation', name: 'Nucleotide Degradation' },
    ],
  },
];

// Flat list for compatibility
const PATHWAYS = PATHWAY_GROUPS.flatMap(g => g.pathways);


const DEFAULT_PARAMS = {
  glucose_mM: 5.0,
  oxygen_pct: 100,
  insulin_fold: 1.0,
  glucagon_fold: 1.0,
  energy_demand: 1.0,
  nutritional_state: 'fed',
};

function Slider({ id, label, unit, min, max, step, value, onChange, color = 'var(--cyan)' }) {
  const pct = ((value - min) / (max - min)) * 100;
  return (
    <div style={{ marginBottom: '1.1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
        <label htmlFor={id} style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', fontWeight: 500 }}>{label}</label>
        <span style={{ fontSize: '0.82rem', fontFamily: 'var(--font-mono)', color, fontWeight: 600 }}>
          {typeof value === 'number' ? value.toFixed(1) : value}{unit}
        </span>
      </div>
      <input
        id={id}
        type="range"
        min={min} max={max} step={step}
        value={value}
        onChange={e => onChange(parseFloat(e.target.value))}
        style={{ '--pct': `${pct}%` }}
      />
    </div>
  );
}

export default function SimulationPanel({ pathway, onPathwayChange, onResult, onLoading }) {
  const [params, setParams] = useState(DEFAULT_PARAMS);
  const [scenarios, setScenarios] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchScenarios().then(setScenarios).catch(() => {});
  }, []);

  const set = (key, val) => setParams(p => ({ ...p, [key]: val }));

  const applyScenario = (key) => {
    const s = scenarios[key];
    if (s) setParams(s.params);
  };

  const handleRun = async () => {
    setLoading(true);
    onLoading(true);
    setError(null);
    console.log('[MetaboSim] Running simulation with params:', { ...params, pathway });
    try {
      const result = await runSimulation({ ...params, pathway });
      console.log('[MetaboSim] Simulation result received:', result);
      console.log('[MetaboSim] Metrics:', result?.metrics);
      console.log('[MetaboSim] Enzyme count:', result?.enzymes?.length);
      onResult(result);
    } catch (e) {
      console.error('[MetaboSim] Simulation error:', e);
      setError('Backend not reachable. Start the Python server first.');
    } finally {
      setLoading(false);
      onLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-4" style={{ padding: '1rem 0' }}>
      {/* Pathway selector — compact dropdown */}
      <div className="card">
        <label
          htmlFor="pathway-select"
          style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.5rem', fontWeight: 600, display: 'block' }}
        >
          Pathway
        </label>
        <select
          id="pathway-select"
          value={pathway}
          onChange={e => onPathwayChange(e.target.value)}
          style={{
            width: '100%',
            padding: '0.6rem 0.85rem',
            borderRadius: 8,
            border: '1px solid var(--border-active)',
            background: 'var(--bg-surface)',
            color: 'var(--cyan)',
            fontFamily: 'var(--font-sans)',
            fontWeight: 600,
            fontSize: '0.88rem',
            cursor: 'pointer',
            outline: 'none',
            appearance: 'none',
            backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2300e5ff' d='M6 8L1 3h10z'/%3E%3C/svg%3E")`,
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'right 0.75rem center',
            paddingRight: '2rem',
          }}
        >
          {PATHWAY_GROUPS.map(group => (
            <optgroup key={group.label} label={group.label}>
              {group.pathways.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </optgroup>
          ))}
        </select>
      </div>


      {/* Scenario presets */}
      <div className="card">
        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.75rem', fontWeight: 600 }}>
          Preset Scenarios
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
          {Object.entries(scenarios).map(([key, s]) => (
            <button
              key={key}
              id={`scenario-${key}`}
              className="btn btn-secondary btn-sm"
              onClick={() => applyScenario(key)}
              title={s.description}
              style={{ borderColor: s.color + '44', color: s.color }}
            >
              {s.icon} {s.label}
            </button>
          ))}
        </div>
      </div>

      {/* Parameter sliders */}
      <div className="card">
        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '1rem', fontWeight: 600 }}>
          Parameters
        </div>

        <Slider id="sl-glucose" label="Blood Glucose" unit=" mM" min={0} max={25} step={0.5}
          value={params.glucose_mM} onChange={v => set('glucose_mM', v)} color="var(--green)" />

        <Slider id="sl-o2" label="O₂ Availability" unit="%" min={0} max={100} step={1}
          value={params.oxygen_pct} onChange={v => set('oxygen_pct', v)} color="var(--cyan)" />

        <Slider id="sl-insulin" label="Insulin Level" unit="× basal" min={0} max={5} step={0.1}
          value={params.insulin_fold} onChange={v => set('insulin_fold', v)} color="var(--green)" />

        <Slider id="sl-glucagon" label="Glucagon Level" unit="× basal" min={0} max={5} step={0.1}
          value={params.glucagon_fold} onChange={v => set('glucagon_fold', v)} color="var(--amber)" />

        <Slider id="sl-demand" label="Energy Demand" unit="×" min={0.1} max={5} step={0.1}
          value={params.energy_demand} onChange={v => set('energy_demand', v)} color="var(--purple)" />

        <div style={{ marginBottom: '0.4rem' }}>
          <label style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', fontWeight: 500, display: 'block', marginBottom: '0.4rem' }}>
            Nutritional State
          </label>
          <select
            id="sel-nutrition"
            value={params.nutritional_state}
            onChange={e => set('nutritional_state', e.target.value)}
            style={{ width: '100%' }}
          >
            <option value="fed">Fed (post-meal)</option>
            <option value="fasted">Fasted (12–24h)</option>
            <option value="starved">Starved (&gt;48h)</option>
          </select>
        </div>
      </div>

      {/* Run button */}
      {error && (
        <div className="alert alert-danger" style={{ fontSize: '0.82rem' }}>
          ⚠️ {error}
        </div>
      )}
      <button
        id="btn-run-simulation"
        className="btn btn-primary"
        onClick={handleRun}
        disabled={loading}
        style={{ width: '100%', justifyContent: 'center', opacity: loading ? 0.7 : 1 }}
      >
        {loading ? <span className="spin" style={{ display: 'inline-block' }}>⟳</span> : '▶'}
        {loading ? 'Simulating...' : 'Run Simulation'}
      </button>

      <button
        id="btn-reset-params"
        className="btn btn-ghost"
        onClick={() => setParams(DEFAULT_PARAMS)}
        style={{ width: '100%', justifyContent: 'center', fontSize: '0.82rem' }}
      >
        ↺ Reset Parameters
      </button>
    </div>
  );
}
