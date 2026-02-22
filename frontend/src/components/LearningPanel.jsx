const ENZYME_INFO = {
  HK: {
    full: "Hexokinase",
    ec: "EC 2.7.1.1",
    reaction: "Glucose + ATP → Glucose-6-Phosphate + ADP",
    clinical: "Hexokinase deficiency causes non-spherocytic haemolytic anaemia. Red cells depend entirely on glycolysis for ATP.",
    mnemonic: "HK is inhibited by its own product (G6P) — product inhibition prevents wasting ATP.",
  },
  PFK1: {
    full: "Phosphofructokinase-1",
    ec: "EC 2.7.1.11",
    reaction: "Fructose-6-P + ATP → Fructose-1,6-BP + ADP",
    clinical: "PFK deficiency (Tarui disease) causes exercise intolerance and haemolytic anaemia. Muscle cannot perform glycolysis.",
    mnemonic: "PFK-1 is THE master switch of glycolysis. Think: PFK = 'Please Fast, Keep' energy balance checked.",
  },
  PK: {
    full: "Pyruvate Kinase",
    ec: "EC 2.7.1.40",
    reaction: "PEP + ADP → Pyruvate + ATP",
    clinical: "PK deficiency is the most common RBC enzyme defect after G6PD deficiency. Causes chronic haemolysis.",
    mnemonic: "PK produces the second ATP molecule in glycolysis. It is activated by F1,6BP — the feedforward signal from PFK-1.",
  },
  GAPDH: {
    full: "Glyceraldehyde-3-Phosphate Dehydrogenase",
    ec: "EC 1.2.1.12",
    reaction: "G3P + NAD⁺ + Pi → 1,3-BPG + NADH",
    clinical: "GAPDH inhibition by hypoxia (NADH accumulation) forces cells into lactate production to regenerate NAD⁺.",
    mnemonic: "GAPDH couples oxidation to phosphorylation — it is the site of redox-energy capture in glycolysis.",
  },
  IDH: {
    full: "Isocitrate Dehydrogenase",
    ec: "EC 1.1.1.41",
    reaction: "Isocitrate + NAD⁺ → α-KG + CO₂ + NADH",
    clinical: "IDH1/IDH2 mutations are common in glioma and AML. They produce an oncometabolite (2-HG) that drives cancer epigenetics.",
    mnemonic: "IDH: 'I Divert Here'. First CO₂-releasing step of TCA. Activated by Ca²⁺ during exercise.",
  },
  AKGDH: {
    full: "α-Ketoglutarate Dehydrogenase",
    ec: "EC 1.2.4.2",
    reaction: "α-KG + NAD⁺ + CoA → Succinyl-CoA + CO₂ + NADH",
    clinical: "Requires thiamine (B1) as cofactor (part of complex). Thiamine deficiency disrupts TCA flux → Wernicke's encephalopathy.",
    mnemonic: "Analogous to PDH — multi-enzyme complex, same cofactors. Second CO₂ release in TCA.",
  },
  SDH: {
    full: "Succinate Dehydrogenase / Complex II",
    ec: "EC 1.3.5.1",
    reaction: "Succinate + FAD → Fumarate + FADH₂",
    clinical: "SDH subunit mutations cause hereditary paraganglioma and phaeochromocytoma (rare tumours of chromaffin tissue).",
    mnemonic: "SDH is the only TCA enzyme that is also an ETC complex. It does NOT pump protons — FADH₂ has lower P/O ratio.",
  },
  CI: {
    full: "NADH:Ubiquinone Oxidoreductase",
    ec: "EC 1.6.5.3",
    reaction: "NADH + Q → NAD⁺ + QH₂ (pumps 4H⁺)",
    clinical: "Complex I deficiency is the most common mitochondrial respiratory chain disease. Presents with MELAS, Leigh syndrome.",
    mnemonic: "Complex I: NADH → ubiquinone. Rotenone inhibits it (in pesticides). The entry point of electrons from NADH.",
  },
  CIV: {
    full: "Cytochrome c Oxidase",
    ec: "EC 1.9.3.1",
    reaction: "4 Cyt c (red) + O₂ + 4H⁺ → 4 Cyt c (ox) + 2H₂O (pumps 2H⁺)",
    clinical: "Inhibited irreversibly by CN⁻ and CO. Both bind the haem iron. Explains the rapid lethality of cyanide and CO poisoning.",
    mnemonic: "Complex IV = the O₂ consumer. No O₂ = ETC stops = PMF collapses = ATP synthase stops = cell death.",
  },
  CV: {
    full: "ATP Synthase (F₀F₁-ATPase)",
    ec: "EC 3.6.3.14",
    reaction: "ADP + Pi + (flow of ~3H⁺ through F₀) → ATP + H₂O",
    clinical: "Oligomycin blocks the F₀ proton channel — used in research. Leigh syndrome mutations in Complex V are also known.",
    mnemonic: "ATP synthase is a molecular motor. 3 protons flow through the F₀ channel per ATP synthesised. ~100 turns per second.",
  },
  PEPCK: {
    full: "Phosphoenolpyruvate Carboxykinase",
    ec: "EC 4.1.1.32",
    reaction: "OAA + GTP → PEP + CO₂ + GDP",
    clinical: "PEPCK deficiency → severe hypoglycaemia and lactic acidosis in infancy. Also a cancer metabolism target.",
    mnemonic: "PEPCK is the main transcriptional control point of gluconeogenesis. Glucagon on, insulin off.",
  },
  PC: {
    full: "Pyruvate Carboxylase",
    ec: "EC 6.4.1.1",
    reaction: "Pyruvate + CO₂ + ATP → OAA + ADP + Pi (requires biotin)",
    clinical: "PC deficiency causes severe hypoglycaemia, lactic acidosis, and encephalopathy. OAA supply for TCA is also impaired.",
    mnemonic: "Activated by acetyl-CoA — signals that fat is being oxidised and glucose synthesis is needed.",
  },
};

export default function LearningPanel({ enzyme, result }) {
  const info = enzyme ? (ENZYME_INFO[enzyme.enzyme_id] || null) : null;

  if (!enzyme) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '2rem 1.5rem' }}>
        <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🔬</div>
        <div style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
          Click any enzyme on the pathway map to see detailed regulation info
        </div>
      </div>
    );
  }

  const statusColors = { active: 'var(--green)', allosteric: 'var(--amber)', inhibited: 'var(--red)', bypass: 'var(--purple)' };
  const statusColor = statusColors[enzyme.status] || 'var(--text-secondary)';

  return (
    <div className="card animate-in flex flex-col gap-4">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h3 style={{ color: statusColor, marginBottom: '0.2rem' }}>
            {info?.full || enzyme.enzyme_name}
          </h3>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
            {info?.ec || ''}
          </div>
        </div>
        <span className={`badge badge-${enzyme.status}`}>{enzyme.status}</span>
      </div>

      {/* Reaction */}
      {info?.reaction && (
        <div style={{
          background: 'var(--bg-surface)',
          border: '1px solid var(--border)',
          borderRadius: 8,
          padding: '0.75rem',
          fontSize: '0.8rem',
          fontFamily: 'var(--font-mono)',
          color: 'var(--cyan)',
          lineHeight: 1.6,
        }}>
          {info.reaction}
        </div>
      )}

      {/* Live metrics */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.4rem' }}>
        <div style={{ padding: '0.6rem', background: 'var(--bg-surface)', borderRadius: 8, border: '1px solid var(--border)', textAlign: 'center' }}>
          <div style={{ fontSize: '1.3rem', fontFamily: 'var(--font-mono)', fontWeight: 700, color: statusColor }}>
            {(enzyme.flux * 100).toFixed(0)}%
          </div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Flux rate</div>
        </div>
        <div style={{ padding: '0.6rem', background: 'var(--bg-surface)', borderRadius: 8, border: '1px solid var(--border)', textAlign: 'center' }}>
          <div style={{ fontSize: '1.3rem', fontFamily: 'var(--font-mono)', fontWeight: 700, color: statusColor }}>
            {(enzyme.activity * 100).toFixed(0)}%
          </div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Activity</div>
        </div>
      </div>

      {/* Regulators */}
      {enzyme.regulators?.length > 0 && (
        <div>
          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.4rem', fontWeight: 600 }}>
            Regulators
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {enzyme.regulators.map(r => {
              const isPositive = r.includes('(+)');
              const isNegative = r.includes('(−)') || r.includes('(-)');
              const color = isPositive ? 'var(--green)' : isNegative ? 'var(--red)' : 'var(--text-secondary)';
              return (
                <span key={r} style={{
                  padding: '3px 9px', borderRadius: 99,
                  background: isPositive ? 'var(--green-dim)' : isNegative ? 'var(--red-dim)' : 'var(--bg-surface)',
                  border: `1px solid ${isPositive ? 'rgba(0,255,136,0.2)' : isNegative ? 'rgba(255,77,109,0.2)' : 'var(--border)'}`,
                  fontSize: '0.75rem', color,
                }}>
                  {r}
                </span>
              );
            })}
          </div>
        </div>
      )}

      {/* Clinical relevance */}
      {info?.clinical && (
        <div className="alert alert-warning" style={{ fontSize: '0.8rem' }}>
          🏥 <strong>Clinical:</strong> {info.clinical}
        </div>
      )}

      {/* Mnemonic */}
      {info?.mnemonic && (
        <div className="alert alert-info" style={{ fontSize: '0.8rem' }}>
          💡 {info.mnemonic}
        </div>
      )}
    </div>
  );
}
