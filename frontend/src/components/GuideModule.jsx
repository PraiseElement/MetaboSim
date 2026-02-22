import { useState } from 'react';

const SECTIONS = [
  { id: 'overview',    icon: '◈', label: 'Overview' },
  { id: 'dashboard',  icon: '▦', label: 'Dashboard' },
  { id: 'simulate',   icon: '⬡', label: 'Simulation' },
  { id: 'pathwaymap', icon: '⬡', label: 'Pathway Map' },
  { id: 'clinical',   icon: '✚', label: 'Clinical Cases' },
  { id: 'quiz',       icon: '◆', label: 'Quiz Mode' },
  { id: 'shortcuts',  icon: '⌨', label: 'Shortcuts' },
  { id: 'faq',        icon: '?', label: 'FAQ' },
];

function SectionCard({ title, children }) {
  return (
    <div style={{
      background: 'var(--bg-card)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-lg)',
      padding: '1.75rem 2rem',
      marginBottom: '1.5rem',
    }}>
      <h2 style={{
        fontSize: '1.15rem', fontWeight: 700,
        color: 'var(--text-primary)', marginBottom: '1.25rem',
        display: 'flex', alignItems: 'center', gap: '0.6rem',
        borderBottom: '1px solid var(--border)', paddingBottom: '0.75rem',
      }}>{title}</h2>
      {children}
    </div>
  );
}

function Step({ num, title, children }) {
  return (
    <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.25rem' }}>
      <div style={{
        width: 32, height: 32, borderRadius: '50%', flexShrink: 0,
        background: 'var(--cyan-dim)', border: '1px solid var(--cyan)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: '0.8rem', fontWeight: 800, color: 'var(--cyan)',
        fontFamily: 'var(--font-mono)',
      }}>{num}</div>
      <div>
        <div style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.3rem', fontSize: '0.95rem' }}>
          {title}
        </div>
        <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.7 }}>
          {children}
        </div>
      </div>
    </div>
  );
}

function Callout({ type = 'info', children }) {
  const colors = {
    info:    { bg: 'rgba(0,229,255,0.06)',  border: 'var(--cyan)',   icon: 'ℹ' },
    tip:     { bg: 'rgba(0,255,157,0.06)',  border: 'var(--green)',  icon: '★' },
    warning: { bg: 'rgba(255,165,0,0.06)',  border: '#f59e0b',       icon: '⚠' },
  };
  const c = colors[type];
  return (
    <div style={{
      background: c.bg, border: `1px solid ${c.border}33`,
      borderLeft: `3px solid ${c.border}`,
      borderRadius: 8, padding: '0.85rem 1rem',
      marginBottom: '1rem', display: 'flex', gap: '0.65rem',
      fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.65,
    }}>
      <span style={{ color: c.border, flexShrink: 0, fontSize: '0.9rem' }}>{c.icon}</span>
      <div>{children}</div>
    </div>
  );
}

function KbdShortcut({ keys, description }) {
  return (
    <div style={{
      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      padding: '0.65rem 0', borderBottom: '1px solid var(--border)',
    }}>
      <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>{description}</span>
      <div style={{ display: 'flex', gap: '0.3rem' }}>
        {keys.map(k => (
          <kbd key={k} style={{
            padding: '2px 8px', borderRadius: 5,
            border: '1px solid var(--border-hover)',
            background: 'var(--bg-surface)',
            fontFamily: 'var(--font-mono)', fontSize: '0.78rem',
            color: 'var(--text-primary)',
            boxShadow: '0 1px 0 var(--border)',
          }}>{k}</kbd>
        ))}
      </div>
    </div>
  );
}

function PathwayTable() {
  const pathways = [
    { cat: 'Carbohydrate', name: 'Glycolysis',            loc: 'Cytoplasm',              atp: '+2 net' },
    { cat: 'Carbohydrate', name: 'TCA Cycle',              loc: 'Mitochondria',            atp: '+10 (NADH × 3, FADH₂ × 1, GTP × 1)' },
    { cat: 'Carbohydrate', name: 'Oxidative Phosphorylation', loc: 'Inner mito. membrane', atp: '+~28' },
    { cat: 'Carbohydrate', name: 'Gluconeogenesis',        loc: 'Cyto + Mito',            atp: '−6' },
    { cat: 'Carbohydrate', name: 'HMP Shunt',              loc: 'Cytoplasm',              atp: 'NADPH + ribose-5P' },
    { cat: 'Carbohydrate', name: 'Glycogenesis',           loc: 'Cytoplasm',              atp: '−2 (UDP-glucose)' },
    { cat: 'Carbohydrate', name: 'Glycogenolysis',         loc: 'Cytoplasm',              atp: '+1 (G-1-P entry)' },
    { cat: 'Carbohydrate', name: 'Fructose Metabolism',    loc: 'Liver cytoplasm',        atp: '−1' },
    { cat: 'Carbohydrate', name: 'Galactose Metabolism',   loc: 'Liver cytoplasm',        atp: '−1 (UTP)' },
    { cat: 'Amino Acid',   name: 'AA Catabolism',          loc: 'Liver (mito + cyto)',    atp: '+variable' },
    { cat: 'Amino Acid',   name: 'Urea Cycle',             loc: 'Liver (mito + cyto)',    atp: '−4' },
    { cat: 'Amino Acid',   name: 'Phe / Tyr Metabolism',   loc: 'Liver (mito + cyto)',    atp: 'cofactor-driven' },
    { cat: 'Amino Acid',   name: 'Branched-Chain AAs',     loc: 'Muscle/Liver mito',      atp: '+variable' },
    { cat: 'Amino Acid',   name: 'AA Synthesis',           loc: 'Cytoplasm / Mito',       atp: '−1 to −2' },
    { cat: 'Lipid',        name: 'β-Oxidation (FAO)',       loc: 'Mitochondria',            atp: '+106 (palmitoyl-CoA)' },
    { cat: 'Lipid',        name: 'Fatty Acid Synthesis',   loc: 'Cytoplasm',              atp: '−7 ATP, −14 NADPH' },
    { cat: 'Lipid',        name: 'Ketogenesis',            loc: 'Liver mitochondria',      atp: 'produces AcAc' },
    { cat: 'Lipid',        name: 'Cholesterol Synthesis',  loc: 'ER + Cytoplasm',         atp: '−18 ATP, −16 NADPH' },
    { cat: 'Lipid',        name: 'Lipoprotein Metabolism', loc: 'Plasma / Liver',         atp: 'LPL, LCAT driven' },
    { cat: 'Nucleotide',   name: 'Purine Synthesis',       loc: 'Cytoplasm',              atp: '−5 per IMP' },
    { cat: 'Nucleotide',   name: 'Pyrimidine Synthesis',   loc: 'Cyto + Mito (DHODH)',    atp: '−5 per UMP' },
    { cat: 'Nucleotide',   name: 'Purine Salvage',         loc: 'Cytoplasm',              atp: '−1 (PRPP)' },
    { cat: 'Nucleotide',   name: 'Nucleotide Degradation', loc: 'Cytoplasm / Blood',      atp: 'releases uric acid' },
  ];

  const categories = ['Carbohydrate', 'Amino Acid', 'Lipid', 'Nucleotide'];
  const catColors = {
    'Carbohydrate': '#00e5ff',
    'Amino Acid':   '#c084fc',
    'Lipid':        '#facc15',
    'Nucleotide':   '#34d399',
  };

  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.83rem' }}>
        <thead>
          <tr style={{ background: 'var(--bg-surface)' }}>
            {['Domain', 'Pathway', 'Subcellular Location', 'Net ATP / Product'].map(h => (
              <th key={h} style={{
                padding: '0.6rem 0.85rem', textAlign: 'left',
                borderBottom: '2px solid var(--border)',
                color: 'var(--text-muted)', fontWeight: 600, fontSize: '0.78rem',
                letterSpacing: '0.05em', textTransform: 'uppercase',
              }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {categories.map(cat => {
            const rows = pathways.filter(p => p.cat === cat);
            return rows.map((p, i) => (
              <tr key={p.name} style={{
                borderBottom: '1px solid var(--border)',
                background: i % 2 === 0 ? 'transparent' : 'var(--bg-surface)',
              }}>
                {i === 0 && (
                  <td rowSpan={rows.length} style={{
                    padding: '0.6rem 0.85rem', verticalAlign: 'middle',
                    fontWeight: 700, fontSize: '0.78rem', letterSpacing: '0.04em',
                    color: catColors[cat], textTransform: 'uppercase',
                  }}>{cat}</td>
                )}
                <td style={{ padding: '0.6rem 0.85rem', color: 'var(--text-primary)', fontWeight: 600 }}>{p.name}</td>
                <td style={{ padding: '0.6rem 0.85rem', color: 'var(--text-muted)' }}>{p.loc}</td>
                <td style={{ padding: '0.6rem 0.85rem', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)', fontSize: '0.78rem' }}>{p.atp}</td>
              </tr>
            ));
          })}
        </tbody>
      </table>
    </div>
  );
}

// ─── Section Content ──────────────────────────────────────────────────────────

function OverviewContent() {
  return (
    <>
      <Callout type="tip">
        <strong>MetaboSim v1.0</strong> — An interactive biochemistry education platform covering 23 metabolic
        pathways across carbohydrate, amino acid, lipid, and nucleotide metabolism.
      </Callout>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.8, marginBottom: '1.25rem' }}>
        MetaboSim lets you simulate real metabolic pathways with adjustable parameters — glucose concentration,
        insulin/glucagon levels, nutritional state, energy demand — and instantly see how enzyme activity, metabolite
        concentrations, and ATP yield respond. Every enzyme node is clickable, revealing clinical relevance, EC
        numbers, cofactors, and disease associations.
      </p>
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
        gap: '1rem', marginBottom: '1.25rem',
      }}>
        {[
          { n: '23', label: 'Metabolic Pathways' },
          { n: '134+', label: 'Enzyme Entries' },
          { n: '24', label: 'Quiz Categories' },
          { n: '50+', label: 'Clinical Cases' },
        ].map(s => (
          <div key={s.label} style={{
            background: 'var(--bg-surface)',
            border: '1px solid var(--border)',
            borderRadius: 10, padding: '1rem',
            textAlign: 'center',
          }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 900, color: 'var(--cyan)', fontFamily: 'var(--font-mono)' }}>{s.n}</div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>{s.label}</div>
          </div>
        ))}
      </div>
      <h3 style={{ color: 'var(--text-primary)', fontSize: '0.95rem', fontWeight: 700, marginBottom: '0.75rem' }}>All Simulated Pathways</h3>
      <PathwayTable />
    </>
  );
}

function DashboardContent() {
  return (
    <>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.75, marginBottom: '1.25rem' }}>
        The Dashboard is your homepage. It gives you an instant overview of the application's capabilities
        and quick-launch tiles for every metabolic domain.
      </p>
      <Step num="1" title="Read the Stat Cards">
        The top row shows: total pathways, enzyme entries, quiz questions, and clinical cases. These update
        automatically as the platform is expanded.
      </Step>
      <Step num="2" title="Choose a Domain">
        Four colour-coded domain cards (Carbohydrate, Amino Acid, Lipid, Nucleotide) give you a summary
        and pathway count. Click one to navigate directly to the Simulation page with that domain pre-selected.
      </Step>
      <Step num="3" title="Recent Activity">
        The dashboard also surfaces recent simulation results and highlights new quiz categories as they are added.
      </Step>
      <Callout type="info">
        The dashboard adapts to light and dark mode. Use the <strong>☀ / ☾</strong> toggle in the header
        to switch themes — your preference is saved in the browser.
      </Callout>
    </>
  );
}

function SimulateContent() {
  return (
    <>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.75, marginBottom: '1.25rem' }}>
        The <strong>Simulate</strong> page is the core of MetaboSim. The three-panel layout gives you
        precise control over physiological parameters while immediately surfacing pathway-level insights.
      </p>
      <Step num="1" title="Select a Pathway">
        Use the <strong>Pathway dropdown</strong> in the left panel to choose any of the 23 available pathways.
        They are grouped by metabolic domain (Carbohydrate, Amino Acid, Lipid, Nucleotide).
      </Step>
      <Step num="2" title="Apply a Scenario Preset (optional)">
        Under the pathway selector, the <strong>Scenario</strong> dropdown offers physiological presets:
        <em> Fed State, Fasted, Diabetic, Intense Exercise, Liver Failure</em> and more. Selecting a preset
        populates all parameters automatically. Great for quick comparisons.
      </Step>
      <Step num="3" title="Fine-tune Parameters">
        Use the sliders and number inputs to set:
        <ul style={{ marginTop: '0.5rem', paddingLeft: '1.2rem', lineHeight: 2 }}>
          <li><strong>Glucose (mM)</strong> — blood glucose concentration (normal fasting: 4–5 mM)</li>
          <li><strong>Insulin Fold</strong> — insulin level relative to basal (1× = fasting, 4× = postprandial)</li>
          <li><strong>Glucagon Fold</strong> — glucagon level (rises in fasting/hypoglycaemia)</li>
          <li><strong>Energy Demand</strong> — workload multiplier (1 = rest, 5 = maximal exercise)</li>
          <li><strong>Nutritional State</strong> — Fed, Fasted, or Starved</li>
        </ul>
      </Step>
      <Step num="4" title="Run Simulation">
        Click <strong>Run Simulation</strong> (or press <kbd style={{ fontFamily: 'var(--font-mono)', padding: '1px 5px', borderRadius: 4, border: '1px solid var(--border)', background: 'var(--bg-surface)' }}>Ctrl+↵</kbd>).
        Results appear in the Pathway Map (centre) and Metrics + Learning panels (right) within ~200 ms.
      </Step>
      <Step num="5" title="Interpret Results">
        <ul style={{ paddingLeft: '1.2rem', lineHeight: 2 }}>
          <li>Enzyme nodes turn <span style={{ color: '#00e5ff' }}>cyan</span> (active), <span style={{ color: '#f59e0b' }}>amber</span> (allosteric), or <span style={{ color: '#ef4444' }}>red</span> (inhibited) based on flux.</li>
          <li>The <strong>Metrics Panel</strong> shows ATP yield, NADH, FADH₂, CO₂, and net fluxes.</li>
          <li>The <strong>Learning Panel</strong> shows enzyme-specific educational notes when you click a node.</li>
        </ul>
      </Step>
      <Callout type="warning">
        All simulated values are <strong>relative flux units</strong>, not absolute concentrations. They are
        designed to illustrate directional changes and physiological relationships, not replace quantitative models.
      </Callout>
    </>
  );
}

function PathwayMapContent() {
  return (
    <>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.75, marginBottom: '1.25rem' }}>
        The <strong>Pathway Map</strong> is an interactive SVG diagram that colour-codes every enzyme node
        in real time based on the current simulation result.
      </p>
      <Step num="1" title="Read Enzyme Colours">
        After running a simulation, every enzyme box is coloured by its computed activity:
        <ul style={{ marginTop: '0.5rem', paddingLeft: '1.2rem', lineHeight: 2 }}>
          <li><span style={{ color: '#00e5ff', fontWeight: 700 }}>■ Cyan / Green border</span> — enzyme is <strong>active</strong> (flux ≥ 0.65)</li>
          <li><span style={{ color: '#f59e0b', fontWeight: 700 }}>■ Amber border</span> — enzyme is <strong>allosterically regulated</strong> (flux 0.30–0.64)</li>
          <li><span style={{ color: '#ef4444', fontWeight: 700 }}>■ Red border</span> — enzyme is <strong>inhibited</strong> (flux &lt; 0.30)</li>
          <li><span style={{ color: '#6b7280', fontWeight: 700 }}>■ Grey / dim</span> — no simulation data for this node yet</li>
        </ul>
      </Step>
      <Step num="2" title="Click an Enzyme Node">
        Clicking any <strong>enzyme box</strong> (rectangular nodes) opens the <em>Enzyme Detail Modal</em>.
        This shows: formal name, EC number, enzymatic class, cofactors, reaction formula, subcellular location,
        allosteric regulators, and a detailed clinical note.
      </Step>
      <Step num="3" title="Enzyme Detail Modal">
        The modal also shows:
        <ul style={{ marginTop: '0.5rem', paddingLeft: '1.2rem', lineHeight: 2 }}>
          <li>The enzyme's PDB structure ID (links to structural context)</li>
          <li>Key diseases caused by deficiency or overactivity</li>
          <li>Drug targets: which drugs inhibit or activate this enzyme</li>
        </ul>
        Press <kbd style={{ fontFamily: 'var(--font-mono)', padding: '1px 5px', borderRadius: 4, border: '1px solid var(--border)', background: 'var(--bg-surface)' }}>Esc</kbd> or click outside to close.
      </Step>
      <Step num="4" title="Pathway Navigation">
        Use the <strong>ATP Report</strong> button (📄 icon in the panel header) to download a printable
        PDF-ready summary of the current simulation, including metrics, enzyme notes, and metabolite table.
      </Step>
      <Callout type="tip">
        The star (★) beside an enzyme name means it is a <strong>key regulatory enzyme</strong> —
        typically allosteric, rate-limiting, and clinically important.
      </Callout>
    </>
  );
}

function ClinicalContent() {
  return (
    <>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.75, marginBottom: '1.25rem' }}>
        The <strong>Clinical Cases</strong> module presents patient vignettes that cross-reference metabolic
        pathway dysfunction with clinical findings. Ideal for medical exam preparation and integration of
        biochemistry with pathophysiology.
      </p>
      <Step num="1" title="Browse Case Categories">
        Cases are grouped by metabolic domain. Use the left sidebar to filter by:
        Carbohydrate disorders, Amino acid disorders, Lipid disorders, Nucleotide disorders,
        Mitochondrial diseases, and Integration cases.
      </Step>
      <Step num="2" title="Open a Case">
        Click any case card to reveal the full patient history, lab results, and diagnostic pathway.
        Work through the questions before revealing the answer.
      </Step>
      <Step num="3" title="Analyse the Enzyme Link">
        Each case links the pathophysiology to a specific enzyme defect. The highlighted enzyme name
        is clickable — it opens the same Enzyme Detail Modal as in the Simulation view.
      </Step>
      <Step num="4" title="Download Case Report">
        Use the <strong>Download</strong> button on any case to export a formatted PDF case summary,
        suitable for revision notes.
      </Step>
      <Callout type="info">
        Clinical cases follow the same metabolic logic as the simulation engine. Running the Simulation
        with "Enzyme Deficiency" scenario parameters mirrors the biochemistry behind each case.
      </Callout>
    </>
  );
}

function QuizContent() {
  return (
    <>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.75, marginBottom: '1.25rem' }}>
        The <strong>Quiz Module</strong> tests your understanding of all 24 metabolic pathway categories
        with exam-style multiple-choice questions.
      </p>
      <Step num="1" title="Select a Pathway Category">
        Choose from 24 categories grouped into 5 domains: Carbohydrate, Amino Acid, Lipid,
        Nucleotide, and Clinical & Integration. Each category badge shows the available question count.
      </Step>
      <Step num="2" title="Answer Questions">
        Each question shows 4 options (A–D). Click your answer. Immediate feedback shows:
        <ul style={{ marginTop: '0.5rem', paddingLeft: '1.2rem', lineHeight: 2 }}>
          <li>✅ Correct: the answer highlights green with a brief explanation.</li>
          <li>❌ Wrong: the correct answer is revealed in green; yours turns red.</li>
        </ul>
      </Step>
      <Step num="3" title="Explanation Panel">
        After each answer, an <strong>Explanation</strong> block appears with the biochemical rationale.
        These explanations reference the same simulation engine logic used elsewhere in the app.
      </Step>
      <Step num="4" title="Progress Tracking">
        Your score is tracked within the session. At the end of a pathway, your result is shown with
        a performance rating. Restart any time to reshuffle the question order.
      </Step>
      <Callout type="tip">
        The quiz is designed to mirror the style of USMLE Step 1, PLAB, and graduate biochemistry
        examinations. Focus on <em>why</em> a mechanism occurs, not just memorising the answer.
      </Callout>
    </>
  );
}

function ShortcutsContent() {
  return (
    <>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.75, marginBottom: '1.25rem' }}>
        MetaboSim supports the following keyboard shortcuts for faster navigation.
      </p>
      <KbdShortcut keys={['Alt', '1']} description="Navigate to Dashboard" />
      <KbdShortcut keys={['Alt', '2']} description="Navigate to Simulate" />
      <KbdShortcut keys={['Alt', '3']} description="Navigate to Clinical Cases" />
      <KbdShortcut keys={['Alt', '4']} description="Navigate to Quiz" />
      <KbdShortcut keys={['Alt', '5']} description="Navigate to this Guide" />
      <KbdShortcut keys={['Ctrl', '↵']} description="Run Simulation (when on Simulate page)" />
      <KbdShortcut keys={['Esc']} description="Close Enzyme Modal / dismiss popups" />
      <KbdShortcut keys={['T']} description="Toggle Dark / Light Theme" />
    </>
  );
}

function FAQContent() {
  const faqs = [
    {
      q: 'Are the simulation values physiologically accurate?',
      a: 'Flux values are dimensionless relative units calibrated to reflect known regulatory relationships (e.g., PFK inhibition by ATP, HMGCR induction by low cholesterol). They are designed for education — not quantitative modelling. For research-grade kinetics, use COPASI or SBtab.'
    },
    {
      q: 'Why does the pathway map show some enzymes in grey (dim)?',
      a: 'The grey state means the simulation has not yet returned data for that enzyme node — either the simulation hasn\'t been run yet, or the pathway was changed without re-running. Click "Run Simulation" to refresh.'
    },
    {
      q: 'How do I get the most out of the Clinical Cases section?',
      a: 'Attempt to diagnose the case before scrolling to the answer. After reading the explanation, go to the Simulate page, set the related pathway, and apply the "Enzyme Deficiency" scenario to see how the metabolic flux changes match the clinical picture.'
    },
    {
      q: 'Can I use this for USMLE / PLAB preparation?',
      a: 'Yes. The quiz questions and clinical cases are written to reflect the style and depth of USMLE Step 1 and PLAB Part 1. The enzyme detail modals include exactly the level of clinical detail tested in those exams.'
    },
    {
      q: 'What do the different enzyme colours mean on the Pathway Map?',
      a: 'Enzyme node colours reflect the computed flux from the current simulation. Cyan/green border = active (flux ≥ 0.65); amber/yellow border = allosterically modulated (flux 0.30–0.64); red border = inhibited or suppressed (flux < 0.30). Grey/dim means no simulation data yet — run the simulation first. The ★ symbol beside an enzyme name marks it as a key regulatory enzyme.'
    },
    {
      q: 'What do insulin and glucagon fold changes actually represent?',
      a: '"Insulin fold" means the insulin level relative to a fasting baseline (1× = fasting, 3–4× = postprandial peak, 0.1× = severe hypoinsulinaemia). Similarly, "Glucagon fold" is relative to basal. High insulin + low glucagon = anabolic fed state (glycogenesis, FA synthesis, protein synthesis up). Low insulin + high glucagon = catabolic state (glycogenolysis, gluconeogenesis, ketogenesis up). These mirror the real hormonal axes governing metabolic flux.'
    },
    {
      q: 'How do I use MetaboSim for studying inherited metabolic disorders?',
      a: 'Each enzyme modal\'s "Clinical Note" describes the disease caused by its deficiency. To simulate the disorder: go to the relevant pathway (e.g., Urea Cycle for OTC deficiency), reduce the energy/insulin to represent fasted state, then click the deficient enzyme (e.g., OTC) to read the biochemical consequences. Cross-reference with the Clinical Cases module for matching patient vignettes and the Quiz for related exam questions.'
    },
    {
      q: 'Why does increasing glucose concentration not always increase ATP yield?',
      a: 'At high glucose (e.g., 15–20 mM), product inhibition and allosteric feedback kick in: accumulated ATP inhibits PFK-1 (the glycolytic pacemaker), NADH buildup slows the TCA cycle, and high citrate inhibits PFK-1 further. This reflects the physiological reality that cells regulate ATP production to match demand, not supply. Increasing "Energy Demand" unlocks higher flux by consuming ATP and relieving these inhibitory signals.'
    },
    {
      q: 'What is the difference between the Learning Panel and the Enzyme Modal?',
      a: 'The Learning Panel (right-side panel on the Simulate page) shows the educational notes returned by the simulation engine — these are context-specific notes about the currently selected pathway and its physiological significance. The Enzyme Modal (opens when you click an enzyme node on the Pathway Map) shows the static enzyme database profile: EC number, cofactors, reaction, subcellular location, and clinical pharmacology. Both are complementary — the panel gives pathway-level context; the modal gives enzyme-level detail.'
    },
    {
      q: 'Do the simulation results change between pathways for the same parameters?',
      a: 'Yes — each of the 23 pathway engines is independently implemented and responds to parameters differently. For example, setting Insulin Fold = 4× activates glycogenesis (glycogen synthesis up), suppresses glycogenolysis and FAO, and increases cholesterol synthesis via SREBP-1c induction. Setting Glucagon Fold = 4× has the opposite effects, plus it activates gluconeogenesis, urea cycle (from AA catabolism), and ketogenesis. Comparing multiple pathways under the same parameters is a powerful way to understand metabolic integration.'
    },

  ];

  return (
    <div>
      {faqs.map((f, i) => (
        <div key={i} style={{
          borderBottom: '1px solid var(--border)',
          padding: '1rem 0',
        }}>
          <div style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.5rem', fontSize: '0.9rem' }}>
            Q: {f.q}
          </div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.7 }}>
            {f.a}
          </div>
        </div>
      ))}
    </div>
  );
}

const CONTENT_MAP = {
  overview:    { title: '◈  MetaboSim — Overview', component: OverviewContent },
  dashboard:   { title: '▦  Dashboard',             component: DashboardContent },
  simulate:    { title: '⬡  Simulation Panel',      component: SimulateContent },
  pathwaymap:  { title: '⬡  Pathway Map',            component: PathwayMapContent },
  clinical:    { title: '✚  Clinical Cases',         component: ClinicalContent },
  quiz:        { title: '◆  Quiz Module',            component: QuizContent },
  shortcuts:   { title: '⌨  Keyboard Shortcuts',    component: ShortcutsContent },
  faq:         { title: '?  FAQ',                    component: FAQContent },
};

// ─── Main Component ───────────────────────────────────────────────────────────

export default function GuideModule() {
  const [active, setActive] = useState('overview');
  const content = CONTENT_MAP[active];
  const ContentComponent = content.component;

  return (
    <div style={{ minHeight: 'calc(100vh - var(--header-h))', background: 'var(--bg-base)', display: 'flex' }}>

      {/* Sidebar */}
      <aside style={{
        width: 210, flexShrink: 0,
        borderRight: '1px solid var(--border)',
        padding: '1.5rem 0',
        background: 'var(--bg-surface)',
        position: 'sticky', top: 'var(--header-h)',
        height: 'calc(100vh - var(--header-h))',
        overflowY: 'auto',
      }}>
        <div style={{ padding: '0 1rem 1rem', borderBottom: '1px solid var(--border)', marginBottom: '0.75rem' }}>
          <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)', letterSpacing: '0.12em', textTransform: 'uppercase', fontFamily: 'var(--font-mono)' }}>User Guide</div>
        </div>
        {SECTIONS.map(s => {
          const isActive = active === s.id;
          return (
            <button
              key={s.id}
              onClick={() => setActive(s.id)}
              style={{
                display: 'flex', alignItems: 'center', gap: '0.6rem',
                width: '100%', padding: '0.55rem 1rem',
                background: isActive ? 'var(--cyan-dim)' : 'transparent',
                border: 'none', borderLeft: isActive ? '2px solid var(--cyan)' : '2px solid transparent',
                color: isActive ? 'var(--cyan)' : 'var(--text-secondary)',
                cursor: 'pointer', fontSize: '0.875rem', fontWeight: isActive ? 700 : 400,
                textAlign: 'left', transition: 'all var(--transition)',
                fontFamily: 'var(--font-sans)',
              }}
              onMouseEnter={e => { if (!isActive) e.currentTarget.style.background = 'var(--bg-card)'; }}
              onMouseLeave={e => { if (!isActive) e.currentTarget.style.background = 'transparent'; }}
            >
              <span style={{ opacity: isActive ? 1 : 0.5, fontSize: '0.8rem' }}>{s.icon}</span>
              {s.label}
            </button>
          );
        })}
      </aside>

      {/* Main Content */}
      <main style={{ flex: 1, padding: '2rem 2.5rem', maxWidth: 900, overflowY: 'auto' }}>
        <SectionCard title={content.title}>
          <ContentComponent />
        </SectionCard>

        {/* Footer */}
        <div style={{
          padding: '1.5rem', borderRadius: 'var(--radius-lg)',
          border: '1px solid var(--border)',
          background: 'var(--bg-surface)',
          textAlign: 'center',
          fontSize: '0.8rem', color: 'var(--text-muted)',
        }}>
          <strong style={{ color: 'var(--text-secondary)' }}>MetaboSim v1.0</strong>
          {' '} — Built by{' '}
          <a href="mailto:praizekene1@gmail.com" style={{ color: 'var(--cyan)', textDecoration: 'none' }}>
            Chibuike Praise Okechukwu
          </a>
          <span style={{ margin: '0 0.5rem', opacity: 0.4 }}>·</span>
          <span>FastAPI + React + Vite</span>
          <span style={{ margin: '0 0.5rem', opacity: 0.4 }}>·</span>
          <span>For education only — not for clinical use</span>
        </div>
      </main>
    </div>
  );
}
