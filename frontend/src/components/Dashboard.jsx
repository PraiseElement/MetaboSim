const PATHWAY_GROUPS = [
  {
    domain: 'Carbohydrate Metabolism',
    emoji: '🍬',
    accentColor: '#00ff88',
    pathways: [
      { id: 'glycolysis',          name: 'Glycolysis',                color: '#00ff88', glow: 'rgba(0,255,136,0.2)',   desc: '10-step glucose breakdown → 2 pyruvate. Foundation of cellular energy.', location: 'Cytoplasm', atp: 'Net +2 ATP, 2 NADH', steps: 10 },
      { id: 'gluconeogenesis',     name: 'Gluconeogenesis',           color: '#ffaa00', glow: 'rgba(255,170,0,0.2)',   desc: 'Synthesis of glucose from lactate, amino acids, glycerol. Active in fasting.', location: 'Liver / Kidney', atp: '−6 ATP net cost', steps: 11 },
      { id: 'tca_cycle',           name: 'TCA Cycle',                 color: '#00d4ff', glow: 'rgba(0,212,255,0.2)',   desc: '8-step cycle oxidising acetyl-CoA to CO₂; produces NADH, FADH₂ and GTP.', location: 'Mitochondrial matrix', atp: '1 GTP + 3 NADH + 1 FADH₂/turn', steps: 8 },
      { id: 'oxphos',              name: 'Oxidative Phosphorylation', color: '#b388ff', glow: 'rgba(179,136,255,0.2)', desc: 'ETC (I–IV) builds proton gradient; Complex V captures ~28 ATP per glucose.', location: 'Inner mito membrane', atp: '~28 ATP per glucose', steps: 5 },
      { id: 'hmp_shunt',           name: 'HMP Shunt (PPP)',           color: '#c084fc', glow: 'rgba(192,132,252,0.2)', desc: 'Generates 2 NADPH + R5P for nucleotide synthesis. G6PD deficiency.', location: 'Cytoplasm', atp: '0 ATP; +2 NADPH', steps: 8 },
      { id: 'glycogenesis',        name: 'Glycogenesis',              color: '#34d399', glow: 'rgba(52,211,153,0.2)',  desc: 'Stores glucose as glycogen chains. Glycogen synthase + branching enzyme.', location: 'Cytoplasm', atp: '−2 ATP per glucose', steps: 5 },
      { id: 'glycogenolysis',      name: 'Glycogenolysis',            color: '#f87171', glow: 'rgba(248,113,113,0.2)', desc: 'Phosphorolysis of glycogen → G1P → free glucose (liver G6Pase).', location: 'Cytoplasm', atp: '+1 ATP advantage', steps: 5 },
      { id: 'fructose_metabolism', name: 'Fructose Metabolism',       color: '#fbbf24', glow: 'rgba(251,191,36,0.2)',  desc: 'Hepatic fructolysis via KHK → Aldolase B. Bypasses PFK-1 regulation.', location: 'Liver', atp: 'Net +2 ATP', steps: 5 },
      { id: 'galactose_metabolism',name: 'Galactose Metabolism',      color: '#2dd4bf', glow: 'rgba(45,212,191,0.2)',  desc: 'Leloir pathway: Gal → Gal-1-P → UDP-Gal ⇌ UDP-Glu. Classic galactosaemia.', location: 'Cytoplasm / liver', atp: 'Net ~2.8 ATP', steps: 5 },
      { id: 'integrated',          name: 'Integrated (All)',          color: '#60a5fa', glow: 'rgba(96,165,250,0.2)',  desc: 'Combined glycolysis + TCA + OxPhos — full aerobic glucose oxidation.', location: 'Cytoplasm + Mito', atp: '~30–32 ATP per glucose', steps: 23 },
    ],
  },
  {
    domain: 'Amino Acid Metabolism',
    emoji: '🧬',
    accentColor: '#f472b6',
    pathways: [
      { id: 'amino_acid_catabolism', name: 'Amino Acid Catabolism',    color: '#f472b6', glow: 'rgba(244,114,182,0.2)', desc: 'Transamination (ALT/AST), GDH, TCA entry — glucogenic & ketogenic AAs.', location: 'Cytoplasm + Mito', atp: 'Variable by AA', steps: 5 },
      { id: 'urea_cycle',            name: 'Urea Cycle',               color: '#fb923c', glow: 'rgba(251,146,60,0.2)',  desc: 'NH₃ + CO₂ + Asp → Urea. OTC, CPS-I, ASS, ASL, Arginase-1. UCDs.', location: 'Mito + Cytoplasm', atp: '−3 ATP per urea', steps: 5 },
      { id: 'phenylalanine_tyrosine',name: 'Phenylalanine & Tyrosine', color: '#a78bfa', glow: 'rgba(167,139,250,0.2)', desc: 'PAH (PKU), catecholamines, melanin, and tyrosinaemia — aromatic AA hub.', location: 'Cytoplasm + ER', atp: '0 direct ATP', steps: 8 },
      { id: 'branched_chain_aa',     name: 'BCAA Catabolism',          color: '#4ade80', glow: 'rgba(74,222,128,0.2)', desc: 'Val/Leu/Ile catabolism via BCAT + BCKDH. MSUD, isovaleric acidaemia, MMA.', location: 'Mitochondria', atp: '0 direct ATP', steps: 6 },
      { id: 'amino_acid_synthesis',  name: 'Amino Acid Synthesis',     color: '#38bdf8', glow: 'rgba(56,189,248,0.2)', desc: 'Non-essential AA from TCA intermediates (GS, PHGDH, AS, ALT). Conditionally essential.', location: 'Cytoplasm + Mito', atp: '−1 to −2 per AA', steps: 6 },
    ],
  },
  {
    domain: 'Lipid Metabolism',
    emoji: '💧',
    accentColor: '#facc15',
    pathways: [
      { id: 'fatty_acid_oxidation',  name: 'β-Oxidation',             color: '#facc15', glow: 'rgba(250,204,21,0.2)',  desc: 'Palmitate → 8 Acetyl-CoA via CPT-I + MCAD. MCAD deficiency — commonest FAO disorder.', location: 'Mito matrix', atp: '−2 invest; 7 FADH₂ + 7 NADH', steps: 5 },
      { id: 'fatty_acid_synthesis',  name: 'FA Synthesis (DNL)',       color: '#e879f9', glow: 'rgba(232,121,249,0.2)', desc: 'ACC + FAS complex: Acetyl-CoA + 7 malonyl-CoA → palmitate. NAFLD, obesity.', location: 'Cytoplasm', atp: '−7 ATP, −14 NADPH', steps: 4 },
      { id: 'ketogenesis',           name: 'Ketogenesis & Ketolysis',  color: '#f97316', glow: 'rgba(249,115,22,0.2)',  desc: 'HMGS2 → AcAc/β-OHB in hepatocytes; SCOT → ketolysis extrahepatic. DKA.', location: 'Mito (liver)', atp: '0 direct; ~22 in ketolysis', steps: 5 },
      { id: 'cholesterol_synthesis', name: 'Cholesterol Synthesis',    color: '#84cc16', glow: 'rgba(132,204,22,0.2)', desc: 'Mevalonate pathway: HMGCR (statins), MVK, DHCR7 (SLO). CoQ / dolichol branches.', location: 'ER + Cytoplasm', atp: '−18 ATP, −16 NADPH', steps: 5 },
      { id: 'lipoprotein_metabolism',name: 'Lipoprotein Metabolism',   color: '#22d3ee', glow: 'rgba(34,211,238,0.2)', desc: 'Chylomicron → LDL/HDL cascade: LPL, LDLR, PCSK9, LCAT, ABCA1. FH.', location: 'Plasma + Liver', atp: '0 direct', steps: 6 },
    ],
  },
  {
    domain: 'Nucleotide Metabolism',
    emoji: '🧪',
    accentColor: '#67e8f9',
    pathways: [
      { id: 'purine_synthesis',       name: 'Purine De Novo Synthesis', color: '#67e8f9', glow: 'rgba(103,232,249,0.2)', desc: 'PRPP → IMP → AMP/GMP. IMPDH (mycophenolate), ADSS/ADSL, MTX mechanism.', location: 'Cytoplasm', atp: '−5 to −7 ATP per purine', steps: 5 },
      { id: 'pyrimidine_synthesis',   name: 'Pyrimidine Synthesis',    color: '#818cf8', glow: 'rgba(129,140,248,0.2)', desc: 'CAD → DHODH (leflunomide) → UMPS → UMP/CTP. TYMS (5-FU), DHFR (MTX).', location: 'Cytoplasm + Mito', atp: '~−5 ATP per CTP', steps: 6 },
      { id: 'purine_salvage',         name: 'Purine Salvage',          color: '#34d399', glow: 'rgba(52,211,153,0.2)',  desc: 'HGPRT (Lesch-Nyhan), APRT (2,8-DHA stones), ADA (SCID), CD73 (tumour immunity).', location: 'Cytoplasm', atp: '~0 net (saves 4 vs de novo)', steps: 5 },
      { id: 'nucleotide_degradation', name: 'Nucleotide Degradation',  color: '#f43f5e', glow: 'rgba(244,63,94,0.2)',  desc: 'XO (allopurinol/febuxostat/gout/TLS), PNP (T-cell SCID), DPYD (5-FU toxicity).', location: 'Cytoplasm + Liver', atp: '0 direct', steps: 5 },
    ],
  },
];

// Flat list for pathway card rendering
const ALL_PATHWAY_CARDS = PATHWAY_GROUPS.flatMap(g =>
  g.pathways.map(p => ({ ...p, domain: g.domain, domainEmoji: g.emoji }))
);


export default function Dashboard({ onNavigate, onSelectPathway }) {
  return (
    <div style={{ padding: '2.5rem 2rem', maxWidth: 1300, margin: '0 auto' }}>
      {/* Hero */}
      <div className="animate-in" style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
        <div style={{ fontSize: '3.5rem', marginBottom: '0.75rem' }}>🧬</div>
        <h1 style={{ fontSize: '2.8rem', marginBottom: '0.75rem' }}>
          Metabolic Pathway <span style={{ color: 'var(--cyan)' }}>Simulator</span>
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', maxWidth: 680, margin: '0 auto 2rem' }}>
        interactively simulate and visualise <strong>23 metabolic pathways</strong> across
          carbohydrate, amino acid, lipid, and nucleotide metabolism.
          Built for clinical biochemistry education.
        </p>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button
            id="btn-start-simulation"
            className="btn btn-primary btn-lg"
            onClick={() => onNavigate('simulate')}
          >
            ⚗️ Start Simulation
          </button>
          <button
            id="btn-take-quiz"
            className="btn btn-secondary btn-lg"
            onClick={() => onNavigate('quiz')}
          >
            📝 Take a Quiz
          </button>
          <button
            id="btn-clinical-cases"
            className="btn btn-secondary btn-lg"
            onClick={() => onNavigate('clinical')}
          >
            🏥 Clinical Cases
          </button>
        </div>
      </div>

      {/* Pathway cards — grouped by domain */}
      {PATHWAY_GROUPS.map(group => (
        <div key={group.domain} style={{ marginBottom: '2.5rem' }}>
          {/* Domain header */}
          <h2 style={{
            marginBottom: '1rem', fontSize: '0.8rem', textTransform: 'uppercase',
            letterSpacing: '0.1em', fontWeight: 700, color: 'var(--text-muted)',
            display: 'flex', alignItems: 'center', gap: '0.5rem',
            borderBottom: `1px solid ${group.accentColor}33`, paddingBottom: '0.5rem',
          }}>
            <span>{group.emoji}</span> {group.domain}
          </h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))',
            gap: '0.85rem',
          }}>
            {group.pathways.map((p, i) => (
              <div
                key={p.id}
                id={`pathway-card-${p.id}`}
                className="card animate-in"
                style={{
                  animationDelay: `${i * 0.05}s`,
                  cursor: 'pointer',
                  borderColor: 'var(--border)',
                  transition: 'all 0.22s ease',
                }}
                onClick={() => { onSelectPathway(p.id); onNavigate('simulate'); }}
                onMouseEnter={e => {
                  e.currentTarget.style.borderColor = p.color;
                  e.currentTarget.style.boxShadow = `0 0 20px ${p.glow}`;
                  e.currentTarget.style.transform = 'translateY(-3px)';
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.borderColor = 'var(--border)';
                  e.currentTarget.style.boxShadow = 'none';
                  e.currentTarget.style.transform = 'translateY(0)';
                }}
              >
                <h3 style={{ color: p.color, marginBottom: '0.25rem', fontSize: '0.9rem' }}>{p.name}</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.73rem', marginBottom: '0.4rem' }}>📍 {p.location}</p>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', lineHeight: 1.5, marginBottom: '0.6rem' }}>
                  {p.desc}
                </p>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.73rem', color: 'var(--text-muted)' }}>
                  <span>⚡ {p.atp}</span>
                  <span>{p.steps} steps</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* Quick stats */}
      <h2 style={{ marginBottom: '1.25rem', color: 'var(--text-secondary)', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 600 }}>
        At a Glance
      </h2>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
        gap: '1rem',
      }}>
        {[
          { label: 'Pathways',         value: '23',   color: 'var(--cyan)',   icon: '🧭' },
          { label: 'Enzymes modelled', value: '100+', color: 'var(--green)', icon: '⚙️' },
          { label: 'Clinical Cases',   value: '50+',  color: 'var(--amber)', icon: '🏥' },
          { label: 'Quiz Questions',   value: '260+', color: 'var(--purple)', icon: '📝' },
        ].map(s => (
          <div key={s.label} className="card" style={{ textAlign: 'center', padding: '1.25rem' }}>
            <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>{s.icon}</div>
            <div className="metric-value" style={{ color: s.color, fontSize: '1.8rem' }}>{s.value}</div>
            <div className="metric-label" style={{ marginTop: '0.2rem' }}>{s.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
