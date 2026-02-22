/**
 * MetaboSim — Simulation Report Generator
 * Generates a self-contained HTML report and triggers a browser download.
 */

const STATUS_LABELS = {
  active: '✅ Active',
  inhibited: '🔴 Inhibited',
  allosteric: '🟡 Allosteric',
  bypass: '🟣 Bypass',
};

// Per-pathway biochemistry context for the report
const PATHWAY_CONTEXT = {
  glycolysis: {
    overview: 'Glycolysis converts one molecule of glucose into 2 pyruvate, generating a net 2 ATP via substrate-level phosphorylation and 2 NADH reducing equivalents.',
    atpInvestment: [
      { step: 'Hexokinase (HK)', amount: '−1 ATP', reason: 'Phosphorylates glucose → Glucose-6-Phosphate to trap it inside the cell.' },
      { step: 'Phosphofructokinase-1 (PFK-1)', amount: '−1 ATP', reason: 'Commits F6P → F1,6BP; the major regulatory step of glycolysis.' },
    ],
    atpGain: [
      { step: 'Phosphoglycerate Kinase (PGK)', amount: '+2 ATP', reason: 'Substrate-level phosphorylation: 1,3-BPG → 3-PG for each triose (×2).' },
      { step: 'Pyruvate Kinase (PK)', amount: '+2 ATP', reason: 'Substrate-level phosphorylation: PEP → Pyruvate for each triose (×2).' },
    ],
    reducingEquivalents: [
      { name: 'NADH ×2', source: 'GAPDH (step 6)', fate: 'Transferred to mitochondria for OxPhos. Yields ~2.5 ATP each in the ETC (malate-aspartate shuttle).' },
    ],
    inhibitors: [
      { name: 'ATP', target: 'PFK-1', mechanism: 'Allosteric inhibition — high ATP signals energy surplus, slowing glycolysis.' },
      { name: 'Citrate', target: 'PFK-1', mechanism: 'Signals active TCA cycle; reduces glycolytic flux to prevent substrate overflow.' },
      { name: 'G6P', target: 'Hexokinase', mechanism: 'Product inhibition — prevents futile phosphorylation when glucose-6-P is abundant.' },
      { name: 'Glucagon/Alanine', target: 'Pyruvate Kinase', mechanism: 'Phosphorylates PK → inactive; diverts PEP toward gluconeogenesis instead.' },
    ],
    activators: [
      { name: 'AMP/ADP', target: 'PFK-1', mechanism: 'Signals low energy charge; strongly activates glycolysis.' },
      { name: 'Fructose-2,6-BP', target: 'PFK-1', mechanism: 'Produced by PFK-2 (activated by insulin); most potent allosteric activator of PFK-1.' },
      { name: 'F1,6BP', target: 'Pyruvate Kinase', mechanism: 'Feed-forward activation — ensures PK accelerates when upstream flux is high.' },
    ],
  },
  gluconeogenesis: {
    overview: 'Gluconeogenesis synthesises glucose from non-carbohydrate precursors (lactate, alanine, glycerol, OAA). It consumes 6 ATP + 2 GTP equivalents per glucose made.',
    atpInvestment: [
      { step: 'Pyruvate Carboxylase (PC)', amount: '−1 ATP ×2', reason: 'Pyruvate + CO₂ → OAA; requires biotin. Bypasses Pyruvate Kinase.' },
      { step: 'PEPCK', amount: '−1 GTP ×2', reason: 'OAA → PEP + CO₂.' },
      { step: 'Phosphoglycerate Kinase (PGK, reverse)', amount: '−1 ATP ×2', reason: '3-PG → 1,3-BPG requires ATP investment.' },
    ],
    atpGain: [],
    reducingEquivalents: [
      { name: 'NADH ×2', source: 'Lactate dehydrogenase / malate shuttle', fate: 'Used to reduce 1,3-BPG → G3P in the cytoplasm.' },
    ],
    inhibitors: [
      { name: 'Insulin', target: 'PEPCK / PC', mechanism: 'Suppresses transcription of GNG enzymes; promotes glycolysis instead.' },
      { name: 'ADP / AMP', target: 'Pyruvate Carboxylase', mechanism: 'Low energy state inhibits GNG — cell needs to make ATP, not glucose.' },
    ],
    activators: [
      { name: 'Glucagon / cAMP', target: 'PEPCK transcription', mechanism: 'Fasting state: glucagon induces PEPCK, PC expression via CREB.' },
      { name: 'Acetyl-CoA', target: 'Pyruvate Carboxylase', mechanism: 'High fat oxidation → high Acetyl-CoA → activates PC to make OAA.' },
    ],
  },
  tca_cycle: {
    overview: 'The TCA (Krebs) cycle oxidises one acetyl-CoA turn to produce 3 NADH, 1 FADH₂, 1 GTP, and 2 CO₂. NADH and FADH₂ are the primary products — they deliver electrons to the ETC in OxPhos.',
    atpInvestment: [],
    atpGain: [
      { step: 'Succinyl-CoA Synthetase (SCS)', amount: '+1 GTP', reason: 'The only direct energy capture step; GTP ≡ ATP.' },
    ],
    reducingEquivalents: [
      { name: 'NADH ×3/turn', source: 'IDH, α-KGDH, MDH', fate: 'Each NADH → ~2.5 ATP in OxPhos (Complex I → ATP Synthase).' },
      { name: 'FADH₂ ×1/turn', source: 'Succinate Dehydrogenase (Complex II)', fate: 'FADH₂ → ~1.5 ATP (bypasses Complex I; fewer protons pumped).' },
    ],
    inhibitors: [
      { name: 'NADH', target: 'IDH, AKGDH, CS, MDH', mechanism: 'Product inhibition — high NADH (ETC blocked in hypoxia) arrests the cycle.' },
      { name: 'ATP / NADH', target: 'Isocitrate Dehydrogenase (IDH)', mechanism: 'High energy charge slows TCA; allosteric.' },
      { name: 'Succinyl-CoA', target: 'CS, α-KGDH', mechanism: 'Product inhibition on upstream enzymes.' },
    ],
    activators: [
      { name: 'ADP / Ca²⁺', target: 'IDH, α-KGDH', mechanism: 'Exercise and low energy charge accelerate TCA to match demand.' },
      { name: 'Acetyl-CoA (substrate)', target: 'Citrate Synthase', mechanism: 'High acetyl-CoA availability drives CS forward.' },
    ],
  },
  oxphos: {
    overview: 'Oxidative phosphorylation converts the reducing power of NADH and FADH₂ into ATP via the electron transport chain (Complexes I–IV) and ATP Synthase (Complex V). Requires O₂ as the terminal electron acceptor.',
    atpInvestment: [],
    atpGain: [
      { step: 'Complex I → ATP Synthase (NADH)', amount: '~2.5 ATP per NADH', reason: 'Complex I pumps 4H⁺; NADH electrons pass through I→III→IV.' },
      { step: 'Complex II → ATP Synthase (FADH₂)', amount: '~1.5 ATP per FADH₂', reason: 'Complex II does NOT pump H⁺; FADH₂ electrons enter at CoQ, bypassing Complex I.' },
    ],
    reducingEquivalents: [
      { name: 'NADH (mito)', source: 'TCA cycle (3/turn)', fate: 'Oxidised by Complex I → NAD⁺ regenerated for TCA.' },
      { name: 'FADH₂ (mito)', source: 'Succinate dehydrogenase (1/turn)', fate: 'Oxidised by Complex II → FAD⁺ regenerated.' },
      { name: 'NADH (cytoplasmic)', source: 'GAPDH in glycolysis', fate: 'Shuttled into mito via malate-aspartate (2.5 ATP) or glycerol-3-P shuttle (1.5 ATP).' },
    ],
    inhibitors: [
      { name: 'CN⁻ / CO', target: 'Complex IV', mechanism: 'Irreversible block of cytochrome c oxidase → PMF collapses → ATP synthase stops.' },
      { name: 'Rotenone', target: 'Complex I', mechanism: 'Classic Complex I inhibitor; used in research & insecticides.' },
      { name: 'Antimycin A', target: 'Complex III', mechanism: 'Blocks ubiquinol oxidation; used in research.' },
      { name: 'Oligomycin', target: 'Complex V (ATP Synthase)', mechanism: 'Blocks F₀ proton channel → increases PMF but stops ATP synthesis (uncoupler test).' },
    ],
    activators: [
      { name: 'ADP + Pi', target: 'ATP Synthase', mechanism: 'ADP availability is the primary substrate that drives ATP synthesis.' },
    ],
  },
  hmp_shunt: {
    overview: 'The HMP Shunt (Pentose Phosphate Pathway) does NOT produce ATP. Its primary outputs are NADPH (antioxidant/reductive biosynthesis) and Ribose-5-Phosphate (nucleotide precursor). G6P is oxidised, not phosphorylated for ATP gain.',
    atpInvestment: [],
    atpGain: [],
    reducingEquivalents: [
      { name: 'NADPH ×2 per G6P', source: 'G6PD + 6PGD (oxidative phase)', fate: 'Regenerates glutathione (GSH) via GR → protects RBCs from oxidative haemolysis. Drives fatty acid, cholesterol, steroid synthesis.' },
    ],
    inhibitors: [
      { name: 'NADPH', target: 'G6PD', mechanism: 'Product inhibition — high NADPH signals sufficient reducing power, slowing the pathway.' },
    ],
    activators: [
      { name: 'NADP⁺', target: 'G6PD', mechanism: 'Oxidised NADP⁺ (from oxidative stress) activates G6PD to regenerate NADPH.' },
    ],
  },
  glycogenesis: {
    overview: 'Glycogenesis stores excess glucose as glycogen. It consumes 2 high-energy phosphate bonds per glucose monomer incorporated (1 ATP for HK + 1 UTP for UDP-glucose formation), making it energetically costly.',
    atpInvestment: [
      { step: 'Hexokinase / Glucokinase (HK/GK)', amount: '−1 ATP', reason: 'Glucose → G6P; traps glucose intracellularly.' },
      { step: 'UTP (via UDP-Glucose Pyrophosphorylase)', amount: '−1 UTP (≡ ATP)', reason: 'G1P + UTP → UDP-Glucose + PPi; PPi hydrolysis makes it irreversible.' },
    ],
    atpGain: [],
    reducingEquivalents: [],
    inhibitors: [
      { name: 'Glucagon (via PKA)', target: 'Glycogen Synthase (GS)', mechanism: 'PKA phosphorylates GS → inactive a-form. Fasting/stress suppress glycogen storage.' },
      { name: 'G6P depletion', target: 'GS (indirect)', mechanism: 'Low G6P promotes allosteric inactivation of GS.' },
    ],
    activators: [
      { name: 'Insulin', target: 'Glycogen Synthase', mechanism: 'Activates PP1 → dephosphorylates GS → active b-form. Fed state promotes glycogen storage.' },
      { name: 'Glucose-6-Phosphate', target: 'GS (allosteric)', mechanism: 'G6P allosterically activates GS even in the absence of insulin (muscle).' },
    ],
  },
  glycogenolysis: {
    overview: 'Glycogenolysis mobilises stored glycogen using inorganic phosphate (Pi), NOT ATP. The G1P product is "pre-phosphorylated" — it enters glycolysis without consuming the hexokinase ATP. This gives a net 1 ATP advantage per glycosyl unit over free glucose.',
    atpInvestment: [],
    atpGain: [
      { step: 'Phosphorolysis advantage (no HK step)', amount: '+1 ATP saved', reason: 'G1P → G6P via PGM, bypassing hexokinase. Saves 1 ATP that free glucose would require.' },
    ],
    reducingEquivalents: [],
    inhibitors: [
      { name: 'Insulin (via PP1)', target: 'Glycogen Phosphorylase (GP-a)', mechanism: 'PP1 dephosphorylates GP-a → inactive GP-b. Insulin strongly suppresses glycogenolysis.' },
      { name: 'Glucose (liver)', target: 'GP-a', mechanism: 'Free glucose allosterically inhibits hepatic Glycogen Phosphorylase (allosteric site).' },
      { name: 'G6P (muscle)', target: 'GP-b', mechanism: 'Accumulated G6P inhibits GP-b allosterically.' },
    ],
    activators: [
      { name: 'Glucagon / Epinephrine (via PKA)', target: 'Phosphorylase Kinase → GP-b → GP-a', mechanism: 'cAMP cascade: adenylate cyclase → PKA → phosphorylase kinase → GP-b phosphorylated → active GP-a.' },
      { name: 'AMP (muscle)', target: 'GP-b (allosteric)', mechanism: 'Low energy charge AMP directly activates GP-b independently of hormones — critical in exercise.' },
      { name: 'Ca²⁺ (muscle)', target: 'Phosphorylase Kinase', mechanism: 'Muscle contraction triggers Ca²⁺ release → activates phosphorylase kinase without PKA.' },
    ],
  },
  fructose_metabolism: {
    overview: 'Hepatic fructose metabolism bypasses PFK-1 regulation. After fructokinase (KHK) and Aldolase B cleavage, DHAP and G3P enter glycolysis below PFK-1. Yields ~0 net substrate-level ATP vs 2 ATP for glucose — the ATP "profit" is realised downstream in OxPhos (via NADH). The unregulated nature drives de novo lipogenesis and uric acid production.',
    atpInvestment: [
      { step: 'Fructokinase (KHK-C)', amount: '−1 ATP', reason: 'Fructose → Fructose-1-Phosphate. Unregulated by insulin/glucagon.' },
      { step: 'Triokinase', amount: '−1 ATP', reason: 'Glyceraldehyde → G3P. Enables entry into glycolysis.' },
    ],
    atpGain: [
      { step: 'PGK + PK (via DHAP and G3P)', amount: '+2 ATP', reason: 'Each fructose yields 2 triose phosphates → same substrate-level return as glucose but missing PFK-1 regulation.' },
    ],
    reducingEquivalents: [
      { name: 'NADH ×2', source: 'GAPDH (for each triose)', fate: 'Goes to OxPhos. Same as glycolysis.' },
    ],
    inhibitors: [
      { name: 'None (KHK)', target: 'Fructokinase', mechanism: 'KHK has NO feedback inhibition — fructose is phosphorylated regardless of energy state, causing Pi depletion.' },
    ],
    activators: [],
  },
  galactose_metabolism: {
    overview: 'Galactose is metabolised via the Leloir pathway in the liver. GALK converts galactose → Gal-1-P (−1 ATP), which then enters the Leloir cycle to eventually yield G6P for glycolysis or glycogenesis. Net substrate-level ATP: ~1 (2 produced − 1 invested by GALK).',
    atpInvestment: [
      { step: 'Galactokinase (GALK)', amount: '−1 ATP', reason: 'Galactose → Galactose-1-Phosphate. Commits galactose to the Leloir pathway.' },
    ],
    atpGain: [
      { step: 'PGK + PK (downstream via G6P → glycolysis)', amount: '+2 ATP', reason: 'G6P enters glycolysis at the payoff phase — same substrate-level return as glucose from G6P.' },
    ],
    reducingEquivalents: [
      { name: 'NADH ×2', source: 'GAPDH (downstream)', fate: 'Transferred to ETC/OxPhos.' },
    ],
    inhibitors: [
      { name: 'Gal-1-P accumulation (GALT deficiency)', target: 'GALT / downstream', mechanism: 'In Classic Galactosaemia, Gal-1-P builds up → inhibits PGM and UDP-glucose recycling → hepatic toxicity.' },
    ],
    activators: [
      { name: 'Substrate availability (Galactose)', target: 'GALK', mechanism: 'GALK is constitutively active; flux is driven by dietary galactose supply.' },
    ],
  },

  // ── Amino Acid Metabolism ──────────────────────────────────────────
  amino_acid_catabolism: {
    overview: 'Amino acid catabolism removes nitrogen via transamination (ALT, AST) and oxidative deamination (GDH). Carbon skeletons enter the TCA cycle as acetyl-CoA, pyruvate, α-KG, succinyl-CoA, fumarate, or OAA. Glucogenic AAs support gluconeogenesis; ketogenic AAs produce ketone bodies.',
    atpInvestment: [],
    atpGain: [
      { step: 'Glucogenic AA → TCA via pyruvate/OAA/α-KG', amount: 'Up to ~17 ATP', reason: 'Carbon enters TCA generating NADH/FADH₂ for OxPhos.' },
      { step: 'Ketogenic AA → Acetyl-CoA → TCA', amount: '~10 ATP per Acetyl-CoA', reason: 'Each TCA turn: 3 NADH + 1 FADH₂ + 1 GTP = ~10 ATP.' },
    ],
    reducingEquivalents: [
      { name: 'NADH (GDH: Glu → α-KG)', source: 'Glutamate oxidative deamination', fate: 'Mitochondrial NADH → Complex I → ~2.5 ATP.' },
    ],
    inhibitors: [
      { name: 'GTP, NADH, ATP', target: 'GDH', mechanism: 'Allosteric inhibition signals energy sufficiency — slows amino acid catabolism in fed state.' },
    ],
    activators: [
      { name: 'ADP + Leucine', target: 'GDH', mechanism: 'Low energy charge and leucine allosterically activate GDH to increase amino acid catabolism.' },
    ],
  },
  urea_cycle: {
    overview: 'The urea cycle detoxifies ammonia → urea for renal excretion. Costs 3 ATP equivalents per urea (2 ATP at CPS1; 1 AMP≡2P at ASS). Occurs across mitochondria (CPS1, OTC) and cytoplasm (ASS, ASL, ARG1). Fumarate released by ASL re-enters TCA, partially recovering the energy investment.',
    atpInvestment: [
      { step: 'CPS-I', amount: '−2 ATP', reason: 'NH₃ + CO₂ → Carbamoyl-Phosphate; 2 ATP consumed.' },
      { step: 'ASS (Argininosuccinate Synthetase)', amount: '−1 ATP (→ AMP + PPi)', reason: 'Citrulline + Aspartate → Argininosuccinic acid; equivalent to 2 phosphate bonds.' },
    ],
    atpGain: [
      { step: 'Fumarate → TCA re-entry', amount: '~+13 ATP (indirect)', reason: 'Fumarate from ASL enters TCA generating NADH/FADH₂.' },
    ],
    reducingEquivalents: [],
    inhibitors: [
      { name: 'NAG depletion', target: 'CPS-I', mechanism: 'N-Acetylglutamate is obligate allosteric activator; its absence blocks the entire urea cycle.' },
    ],
    activators: [
      { name: 'N-Acetylglutamate (NAG)', target: 'CPS-I', mechanism: 'High dietary protein → high glutamate → NAGS makes NAG → CPS-I activated.' },
    ],
  },
  phenylalanine_tyrosine: {
    overview: 'PAH converts Phe → Tyr (requires BH4 cofactor). Tyr branches into catecholamines (TH → DOPA → dopamine → noradrenaline → adrenaline), thyroid hormones, melanin, and catabolism (→ fumarate + acetoacetate). PKU (PAH deficiency) causes Phe accumulation and intellectual disability if untreated.',
    atpInvestment: [
      { step: 'BH4 regeneration (DHPR)', amount: '−1 NADH', reason: 'BH4 consumed stoichiometrically; DHPR regenerates it using NADH.' },
    ],
    atpGain: [
      { step: 'Fumarate (catabolism) → TCA', amount: '~+13 ATP', reason: 'Fumarate from Tyr catabolism enters TCA cycle.' },
    ],
    reducingEquivalents: [],
    inhibitors: [
      { name: 'Elevated Phe', target: 'TH (catecholamine synthesis)', mechanism: 'Phe competitively inhibits TH → reduced dopamine/noradrenaline. Explains neurological effects in PKU.' },
    ],
    activators: [
      { name: 'Phenylalanine (substrate)', target: 'PAH (allosteric)', mechanism: 'Phe activates PAH homotropically — increases flux when dietary Phe is high.' },
    ],
  },
  branched_chain_aa: {
    overview: 'BCAAs (Leu, Ile, Val) catabolised primarily in muscle (BCAT2). BCKDH is the irreversible rate-limiting step; its deficiency = MSUD. Leu is purely ketogenic (~41 ATP); Val is purely glucogenic via succinyl-CoA (~18 ATP); Ile is both (~42 ATP).',
    atpInvestment: [],
    atpGain: [
      { step: 'Leucine → Acetyl-CoA ×2 → TCA', amount: '~41 ATP', reason: 'Purely ketogenic; acetyl-CoA enters TCA for 10 ATP per turn.' },
      { step: 'Valine → Succinyl-CoA → TCA', amount: '~18 ATP', reason: 'Glucogenic; midway TCA entry = lower ATP yield.' },
    ],
    reducingEquivalents: [
      { name: 'NADH (BCKDH)', source: 'Oxidative decarboxylation of BCKAs', fate: 'Mitochondrial NADH → Complex I → 2.5 ATP.' },
    ],
    inhibitors: [
      { name: 'BCKDK phosphorylation', target: 'BCKDH (E1α)', mechanism: 'BCKDK inactivates BCKDH; limits BCAA catabolism in protein-sufficient states.' },
    ],
    activators: [
      { name: 'High BCAA substrate', target: 'BCKDH (via PP2Cm)', mechanism: 'Substrate inactivates BCKDK and activates PP2Cm phosphatase → dephosphorylates BCKDH → active.' },
    ],
  },
  amino_acid_synthesis: {
    overview: 'Non-essential AAs synthesised from TCA intermediates. Glutamate (GDH: α-KG + NH₃) is the central nitrogen donor. GS fixes additional NH₃ into glutamine (−1 ATP). Essential for protein synthesis, nucleotide biosynthesis, and one-carbon metabolism.',
    atpInvestment: [
      { step: 'GDH (reductive amination)', amount: '−1 NADPH', reason: 'α-KG + NH₃ + NADPH → Glutamate; NADPH consumed for nitrogen fixation.' },
      { step: 'Glutamine Synthetase (GS)', amount: '−1 ATP', reason: 'Glu + NH₃ + ATP → Gln + ADP + Pi; high-energy phosphoryl intermediate.' },
    ],
    atpGain: [],
    reducingEquivalents: [
      { name: 'NADPH consumed (GDH biosynthetic direction)', source: 'PPP (G6PD) or malic enzyme', fate: 'NADPH oxidised to NADP⁺ during reductive amination.' },
    ],
    inhibitors: [
      { name: 'GTP, NADH, ATP', target: 'GDH (biosynthetic direction)', mechanism: 'Energy sufficiency suppresses GDH-mediated AA biosynthesis.' },
    ],
    activators: [
      { name: 'NH₃ availability', target: 'GDH', mechanism: 'NH₃ from glutaminase or AA catabolism drives GDH toward reductive amination.' },
    ],
  },

  // ── Lipid Metabolism ───────────────────────────────────────────────
  fatty_acid_oxidation: {
    overview: 'β-Oxidation catabolises palmitoyl-CoA (C16) through 7 cycles: 8 Acetyl-CoA, 7 FADH₂, 7 NADH. Total ATP from palmitate: ~106 ATP (minus 2 for activation). CPT1 is the rate-limiting gatekeeper, potently inhibited by malonyl-CoA — preventing simultaneous FA synthesis and oxidation.',
    atpInvestment: [
      { step: 'Fatty acyl-CoA synthetase (activation)', amount: '−2 ATP (as AMP + PPi)', reason: 'Palmitate → Palmitoyl-CoA; ATP → AMP + PPi, equivalent to 2 ATP consumed.' },
    ],
    atpGain: [
      { step: '7 × FADH₂ → ETC (via ETF-QO)', amount: '+10.5 ATP', reason: 'Each FADH₂ → 1.5 ATP (bypasses Complex I).' },
      { step: '7 × NADH → ETC (Complex I)', amount: '+17.5 ATP', reason: 'Each NADH → 2.5 ATP.' },
      { step: '8 × Acetyl-CoA → TCA cycle', amount: '+80 ATP', reason: 'Each acetyl-CoA turn: 3 NADH + 1 FADH₂ + 1 GTP = ~10 ATP.' },
    ],
    reducingEquivalents: [
      { name: 'FADH₂ ×7', source: 'VLCAD/MCAD/SCAD', fate: 'Via ETF-QO → CoQ → Complex III/IV → ATP Synthase.' },
      { name: 'NADH ×7', source: 'L-3-Hydroxyacyl-CoA dehydrogenase (LHAD)', fate: 'Mitochondrial matrix NADH → Complex I → 2.5 ATP each.' },
    ],
    inhibitors: [
      { name: 'Malonyl-CoA', target: 'CPT-I', mechanism: 'De novo FAS product blocks CPT-I → prevents mitochondrial acyl-CoA import. Mutual exclusion of FAO and FAS.' },
    ],
    activators: [
      { name: 'Glucagon / AMPK (fasting)', target: 'CPT1 (via ACC phosphorylation → ↓ malonyl-CoA)', mechanism: 'Low glucose → AMPK → phosphorylates ACC → ↓ malonyl-CoA → CPT1 disinhibited → FAO activated.' },
      { name: 'PPARα', target: 'CPT1, MCAD, VLCAD (gene expression)', mechanism: 'Fasting-induced PPARα upregulates all major FAO enzymes in liver and heart.' },
    ],
  },
  ketogenesis: {
    overview: 'Ketogenesis converts excess acetyl-CoA (FAO overflow) → ketone bodies (AcAc, β-OHB, acetone) in liver mitochondria — occurs during fasting, DKA, prolonged exercise. HMGCS2 is rate-limiting. Liver cannot oxidise its own ketones (lacks SCOT). Peripheral tissues oxidise β-OHB → acetyl-CoA → TCA.',
    atpInvestment: [],
    atpGain: [
      { step: 'Peripheral β-OHB → 2 Acetyl-CoA → TCA', amount: '~22 ATP per β-OHB', reason: '2 × TCA turns (10 ATP each) + BDH1 NADH (~2 ATP) = ~22 ATP.' },
    ],
    reducingEquivalents: [
      { name: 'NADH → β-OHB (BDH1, liver)', source: 'High NADH:NAD⁺ ratio in fasting drives BDH1 forward in liver', fate: 'β-OHB exported; peripheral BDH1 reversal regenerates AcAc + NADH for oxidation.' },
    ],
    inhibitors: [
      { name: 'Insulin / high carbohydrate', target: 'HMGCS2 (transcriptional suppression)', mechanism: 'Insulin suppresses PPARα and HMGCS2 expression → reduces ketogenesis in fed state.' },
    ],
    activators: [
      { name: 'SIRT5 (fasting-induced)', target: 'HMGCS2 (desuccinylation → activation)', mechanism: 'SIRT5 removes inhibitory succinylation from HMGCS2 → enzyme becomes active during fasting.' },
    ],
  },
  fatty_acid_synthesis: {
    overview: 'De novo lipogenesis: citrate → acetyl-CoA (ACLY) → malonyl-CoA (ACC1, rate-limiting) → palmitate (FASN, 7 malonyl-CoA + 14 NADPH). Net cost: ~8 ATP + 14 NADPH per C16. Induced by insulin/carbohydrate; suppressed by fasting/AMPK. Malonyl-CoA product simultaneously blocks CPT1 (mutual exclusion with FAO).',
    atpInvestment: [
      { step: 'ATP-Citrate Lyase (ACLY)', amount: '−1 ATP', reason: 'Citrate → Acetyl-CoA + OAA; requires ATP hydrolysis.' },
      { step: 'ACC1 (×7)', amount: '−7 ATP', reason: 'Rate-limiting: 7 × (Acetyl-CoA + CO₂ + ATP → Malonyl-CoA).' },
    ],
    atpGain: [],
    reducingEquivalents: [
      { name: 'NADPH ×14 consumed per palmitate', source: 'PPP (G6PD) + Malic Enzyme (ME1)', fate: 'NADPH oxidised at ketoacyl-ACP reductase and enoyl-ACP reductase steps of FASN.' },
    ],
    inhibitors: [
      { name: 'AMPK', target: 'ACC1 (Ser79 phospho-inactivation)', mechanism: 'Low energy → AMPK → ACC1 inactive → ↓ malonyl-CoA → ↑ FAO. Metformin mechanism.' },
      { name: 'PUFAs (dietary)', target: 'SREBP-1c → ACC1 + FASN', mechanism: 'PUFAs suppress SREBP-1c maturation → ↓ lipogenic gene expression.' },
    ],
    activators: [
      { name: 'Insulin → SREBP-1c + ChREBP', target: 'ACC1 + FASN (gene expression)', mechanism: 'Fed-state hormonal induction of lipogenic genes; ACC1 also dephosphorylated (activated).' },
      { name: 'Citrate (allosteric)', target: 'ACC1 (polymerisation)', mechanism: 'Cytoplasmic citrate promotes ACC1 filament formation → fully active enzyme.' },
    ],
  },
  cholesterol_synthesis: {
    overview: 'Mevalonate pathway: 18 acetyl-CoA → cholesterol in 30+ steps. HMG-CoA Reductase (HMGCR) is the irreversible rate-limiting step and statin target. Intermediates include CoQ10 (ETC), dolichol (glycoprotein synthesis), and prenyl groups (protein prenylation). SREBP-2 controls HMGCR and LDLR transcription co-ordinately.',
    atpInvestment: [
      { step: 'HMGCR (HMG-CoA → Mevalonate)', amount: '−2 NADPH', reason: 'Irreversible reduction; statin target.' },
      { step: 'Mevalonate kinase → phosphomevalonate kinase', amount: '−2 ATP', reason: 'Sequential phosphorylation of mevalonate to mevalonate-5-PP.' },
    ],
    atpGain: [],
    reducingEquivalents: [
      { name: 'NADPH ×38 total consumed', source: 'PPP (main source)', fate: 'Required for multiple sterol ring reduction steps throughout cholesterol synthesis.' },
    ],
    inhibitors: [
      { name: 'Statins', target: 'HMGCR (competitive)', mechanism: 'Mimic HMG-CoA transition state → competitive inhibition → ↓ mevalonate → ↓ cholesterol + ↑ LDLR.' },
      { name: 'AMPK', target: 'HMGCR (phospho-inactivation)', mechanism: 'Low energy → AMPK phosphorylates HMGCR → inactive. Co-ordinates with FA synthesis suppression.' },
    ],
    activators: [
      { name: 'SREBP-2 (low cholesterol sensor)', target: 'HMGCR + LDLR (gene expression)', mechanism: 'Low intracellular cholesterol → SCAP escorts SREBP-2 to Golgi → S1P/S2P cleavage → nuclear SREBP-2 → HMGCR + LDLR induction.' },
    ],
  },
  lipoprotein_metabolism: {
    overview: 'Lipoproteins transport hydrophobic lipids in blood: chylomicrons (dietary fat via LPL) → VLDL → IDL → LDL (delivers cholesterol via LDLR). HDL performs reverse cholesterol transport (RCT: ABCA1 → ApoA-I → LCAT → SR-BI). PCSK9 degrades LDLR — inhibition by evolocumab/inclisiran lowers LDL 50–70%.',
    atpInvestment: [],
    atpGain: [],
    reducingEquivalents: [],
    inhibitors: [
      { name: 'PCSK9', target: 'LDLR recycling', mechanism: 'PCSK9 directs LDLR to lysosomal degradation → reduces LDL clearance. Anti-PCSK9 mAbs prevent this → ↓ LDL 50–70%.' },
      { name: 'ApoC-III', target: 'LPL inhibition', mechanism: 'ApoC-III on VLDL/IDL inhibits LPL activity → raises triglycerides.' },
    ],
    activators: [
      { name: 'ApoC-II', target: 'LPL (obligate activator)', mechanism: 'ApoC-II on CM/VLDL is required for LPL catalytic activity; deficiency → chylomicronaemia.' },
      { name: 'ApoA-I', target: 'LCAT', mechanism: 'ApoA-I activates LCAT to esterify cholesterol on HDL — drives HDL maturation and RCT.' },
    ],
  },

  // ── Nucleotide Metabolism ──────────────────────────────────────────
  purine_synthesis: {
    overview: 'De novo purine synthesis builds the bicyclic ring in 10 steps on ribose-5-phosphate (from PRPP). Costs ~9 ATP per AMP/GMP. IMP is the branch-point → AMP or GMP. PPAT is rate-limiting (AMP/GMP-inhibited). Salvage (HGPRT) is far more efficient — uses just 1 PRPP.',
    atpInvestment: [
      { step: 'PRPP synthesis (PRPS)', amount: '−1 ATP', reason: 'R5P + ATP → PRPP + AMP; activated ribose scaffold for ring construction.' },
      { step: 'Multiple ring-closure steps (GART, PFAS, ADSS)', amount: '−5 ATP + 1 GTP', reason: 'Steps 3, 5, 7, 9, 10 each consume ATP/GTP for amination, ring closure, and carbon transfer.' },
    ],
    atpGain: [],
    reducingEquivalents: [
      { name: 'NADH (IMPDH: IMP → XMP)', source: 'IMP oxidation to xanthylate', fate: 'NAD⁺ → NADH; goes to ETC.' },
    ],
    inhibitors: [
      { name: 'AMP + GMP (synergistic)', target: 'PPAT (rate-limiting)', mechanism: 'End-product feedback — purines inhibit their own synthesis to balance the purine pool.' },
      { name: 'Azathioprine / 6-MP', target: 'PPAT + multiple steps', mechanism: '6-thio-IMP competes with IMP → blocks purine synthesis. Used in IBD, transplant rejection.' },
    ],
    activators: [
      { name: 'High PRPP (e.g. HGPRT deficiency)', target: 'PPAT (substrate-driven)', mechanism: 'PRPP accumulation drives PPAT forward → excess purine synthesis → uric acid overproduction → gout.' },
    ],
  },
  pyrimidine_synthesis: {
    overview: 'De novo pyrimidine synthesis builds the ring first, then attaches to PRPP. CAD (trifunctional: CPS-II, ATCase, DHOase) is rate-limiting. DHODH (mitochondrial, links to ETC) oxidises DHO → orotate. UMP → UTP/CTP (RNA); dUMP → dTMP via TYMS + DHFR — the 5-FU and methotrexate targets in cancer therapy.',
    atpInvestment: [
      { step: 'CAD: CPS-II domain', amount: '−2 ATP', reason: 'Carbamoyl-phosphate from Gln + CO₂ (cytoplasmic CPS-II, not mitochondrial CPS-I).' },
    ],
    atpGain: [],
    reducingEquivalents: [
      { name: 'Ubiquinol (CoQH₂) at DHODH', source: 'DHO → Orotate electrons → CoQ → Complex III', fate: 'DHODH links pyrimidine synthesis to ETC; inhibited by leflunomide (RA/MS treatment).' },
      { name: 'NADPH (DHFR step)', source: 'Regenerates THF from DHF after TYMS', fate: 'THF recycled for each new dTMP synthesis; MTX/trimethoprim target DHFR here.' },
    ],
    inhibitors: [
      { name: '5-FU (→ FdUMP)', target: 'TYMS (covalent)', mechanism: 'FdUMP + CH₂-THF → irreversible ternary complex → no dTMP → DNA strand breaks.' },
      { name: 'Methotrexate', target: 'DHFR', mechanism: 'MTX depletes THF → blocks TYMS + purine synthesis → DNA/RNA synthesis arrest.' },
      { name: 'Leflunomide (teriflunomide)', target: 'DHODH', mechanism: 'Inhibits DHODH → depletes pyrimidines → suppresses lymphocyte proliferation (RA/MS).' },
    ],
    activators: [
      { name: 'E2F transcription factors (S-phase)', target: 'CAD + TYMS', mechanism: 'G1→S cell cycle progression upregulates CAD and TYMS to meet pyrimidine demand for DNA replication.' },
    ],
  },
  purine_salvage: {
    overview: 'Purine salvage recycles hypoxanthine (→ IMP), guanine (→ GMP), adenine (→ AMP) using PRPP — far cheaper than de novo (~1 PRPP vs ~9 ATP). HGPRT deficiency: partial → gout; complete → Lesch-Nyhan syndrome. ADA deficiency → dATP accumulation → lymphocyte apoptosis → ADA-SCID (first gene therapy disease).',
    atpInvestment: [
      { step: 'HGPRT / APRT', amount: '−1 PRPP (≡ 1 ATP)', reason: 'Base + PRPP → NMP + PPi; highly efficient vs de novo synthesis.' },
    ],
    atpGain: [
      { step: 'AMP → ATP (adenylate kinase + NDPK)', amount: '+2 ATP', reason: 'Salvaged AMP phosphorylated to ADP then ATP — full recovery of adenine energy.' },
    ],
    reducingEquivalents: [],
    inhibitors: [
      { name: 'IMP and GMP (product inhibition)', target: 'HGPRT', mechanism: 'End-product inhibition prevents excessive purine salvage and accumulation.' },
    ],
    activators: [
      { name: 'Purine base availability (nucleotide turnover)', target: 'HGPRT / APRT', mechanism: 'Released bases from RNA/DNA turnover are immediately salvaged when HGPRT is functional.' },
    ],
  },
  nucleotide_degradation: {
    overview: 'Purines degraded to uric acid (poorly soluble in humans — no uricase): AMP/GMP → nucleoside → (PNP) free base → (XO) xanthine → uric acid. XO generates H₂O₂/O₂·⁻ — major ROS source in ischaemia-reperfusion. Allopurinol (→ alloxanthine) and febuxostat inhibit XO. Pyrimidines degraded to β-alanine/β-aminoisobutyrate and recycled.',
    atpInvestment: [],
    atpGain: [],
    reducingEquivalents: [
      { name: 'H₂O₂ + O₂·⁻ (ROS, at XO)', source: 'Xanthine oxidase using O₂ as electron acceptor', fate: 'Detoxified by SOD + catalase; pathological in ischaemia-reperfusion (allopurinol protective).' },
    ],
    inhibitors: [
      { name: 'Allopurinol → Alloxanthine', target: 'XO (mechanism-based)', mechanism: 'XO oxidises allopurinol → alloxanthine irreversibly inhibits Mo-cofactor → ↓ uric acid.' },
      { name: 'Febuxostat', target: 'XO (non-purine, non-competitive)', mechanism: 'Inhibits both oxidised and reduced XO forms; used in allopurinol-hypersensitive patients.' },
    ],
    activators: [
      { name: 'Ischaemia → XDH→XO conversion', target: 'XO flux', mechanism: 'Ischaemia converts XDH (NAD⁺-dependent) → XO (O₂-dependent) via proteolysis → reperfusion → ROS burst → reperfusion injury.' },
    ],
  },
};

function escHtml(str) {
  return String(str ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function buildATPBreakdownSection(m, pathway) {
  const ctx = PATHWAY_CONTEXT[pathway] || {};
  const invested = m.atp_invested ?? null;
  const produced = m.atp_substrate_produced ?? null;
  const netATP = m.atp_yield ?? 0;
  const nadph = m.nadph_produced ?? 0;
  const nadh = m.nadh_produced ?? 0;
  const fadh2 = m.fadh2_produced ?? 0;
  const gtp = (pathway === 'tca_cycle') ? (m.atp_yield ?? 0) : null;

  const atpColor = netATP > 10 ? '#059669' : netATP > 1 ? '#0077b6' : netATP >= 0 ? '#d97706' : '#dc2626';

  const investmentRows = (ctx.atpInvestment || []).map(r =>
    `<tr>
      <td><strong>${escHtml(r.step)}</strong></td>
      <td style="color:#dc2626;font-family:'JetBrains Mono',monospace;font-weight:700">${escHtml(r.amount)}</td>
      <td style="color:#64748b;font-size:0.8rem">${escHtml(r.reason)}</td>
    </tr>`
  ).join('');

  const gainRows = (ctx.atpGain || []).map(r =>
    `<tr>
      <td><strong>${escHtml(r.step)}</strong></td>
      <td style="color:#059669;font-family:'JetBrains Mono',monospace;font-weight:700">${escHtml(r.amount)}</td>
      <td style="color:#64748b;font-size:0.8rem">${escHtml(r.reason)}</td>
    </tr>`
  ).join('');

  const redoxRows = (ctx.reducingEquivalents || []).map(r =>
    `<tr>
      <td><strong>${escHtml(r.name)}</strong></td>
      <td style="color:#7c3aed;font-family:'JetBrains Mono',monospace">${escHtml(r.source)}</td>
      <td style="color:#64748b;font-size:0.8rem">${escHtml(r.fate)}</td>
    </tr>`
  ).join('');

  const inhibitorRows = (ctx.inhibitors || []).map(r =>
    `<tr>
      <td><strong>${escHtml(r.name)}</strong></td>
      <td style="color:#dc2626;font-size:0.8rem">${escHtml(r.target)}</td>
      <td style="color:#64748b;font-size:0.8rem">${escHtml(r.mechanism)}</td>
    </tr>`
  ).join('');

  const activatorRows = (ctx.activators || []).map(r =>
    `<tr>
      <td><strong>${escHtml(r.name)}</strong></td>
      <td style="color:#059669;font-size:0.8rem">${escHtml(r.target)}</td>
      <td style="color:#64748b;font-size:0.8rem">${escHtml(r.mechanism)}</td>
    </tr>`
  ).join('');

  return `
<h2>🧾 Biochemical Breakdown</h2>

<div style="background:#eff6ff;border-left:4px solid #3b82f6;padding:0.85rem 1.1rem;border-radius:0 8px 8px 0;margin-bottom:1.25rem;font-size:0.85rem;color:#1e3a5f;line-height:1.6">
  <strong>Pathway overview:</strong> ${escHtml(ctx.overview || 'No overview available for this pathway.')}
</div>

<!-- ATP Tally -->
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;margin-bottom:1.25rem">
  <div style="background:#fff;border-radius:10px;padding:0.85rem;border:1px solid #e2e8f0;text-align:center">
    <div style="font-family:'JetBrains Mono',monospace;font-size:1.6rem;font-weight:800;color:#dc2626">${invested !== null ? (-invested).toFixed(1) : '—'}</div>
    <div style="font-size:0.65rem;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-top:3px">ATP Invested</div>
    <div style="font-size:0.72rem;color:#94a3b8;margin-top:2px">consumed in reactions</div>
  </div>
  <div style="background:#fff;border-radius:10px;padding:0.85rem;border:1px solid #e2e8f0;text-align:center">
    <div style="font-family:'JetBrains Mono',monospace;font-size:1.6rem;font-weight:800;color:#059669">${produced !== null ? produced.toFixed(1) : gtp !== null ? gtp.toFixed(1) + ' GTP' : '—'}</div>
    <div style="font-size:0.65rem;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-top:3px">${pathway === 'tca_cycle' ? 'GTP Produced' : 'ATP Produced'}</div>
    <div style="font-size:0.72rem;color:#94a3b8;margin-top:2px">substrate-level</div>
  </div>
  <div style="background:#fff;border-radius:10px;padding:0.85rem;border:1px solid #e2e8f0;text-align:center">
    <div style="font-family:'JetBrains Mono',monospace;font-size:1.6rem;font-weight:800;color:${atpColor}">${netATP.toFixed(1)}</div>
    <div style="font-size:0.65rem;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-top:3px">Net ATP / GTP</div>
    <div style="font-size:0.72rem;color:#94a3b8;margin-top:2px">this pathway only</div>
  </div>
  <div style="background:#fff;border-radius:10px;padding:0.85rem;border:1px solid #e2e8f0;text-align:center">
    ${nadph > 0
      ? `<div style="font-family:'JetBrains Mono',monospace;font-size:1.6rem;font-weight:800;color:#7c3aed">${nadph.toFixed(2)}</div>
         <div style="font-size:0.65rem;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-top:3px">NADPH</div>
         <div style="font-size:0.72rem;color:#94a3b8;margin-top:2px">antioxidant / biosynthesis</div>`
      : `<div style="font-family:'JetBrains Mono',monospace;font-size:1.6rem;font-weight:800;color:#7c3aed">${nadh.toFixed(2)} / ${fadh2.toFixed(2)}</div>
         <div style="font-size:0.65rem;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-top:3px">NADH / FADH₂</div>
         <div style="font-size:0.72rem;color:#94a3b8;margin-top:2px">→ OxPhos (ETC)</div>`}
  </div>
</div>

${investmentRows ? `
<h3 style="font-size:0.92rem;color:#0a1628;margin:1.25rem 0 0.6rem;font-weight:700">⬇ ATP Invested (Consumed)</h3>
<table>
  <thead><tr><th>Enzyme / Step</th><th>ATP Impact</th><th>Why</th></tr></thead>
  <tbody>${investmentRows}</tbody>
</table>` : ''}

${gainRows ? `
<h3 style="font-size:0.92rem;color:#0a1628;margin:1.25rem 0 0.6rem;font-weight:700">⬆ ATP / GTP Gained</h3>
<table>
  <thead><tr><th>Enzyme / Step</th><th>ATP Impact</th><th>Why</th></tr></thead>
  <tbody>${gainRows}</tbody>
</table>` : ''}

${redoxRows ? `
<h3 style="font-size:0.92rem;color:#0a1628;margin:1.25rem 0 0.6rem;font-weight:700">🔋 Reducing Equivalents (Cofactors)</h3>
<p style="font-size:0.8rem;color:#64748b;margin-bottom:0.5rem">These are NOT ATP — they carry electrons to OxPhos where ATP is made.</p>
<table>
  <thead><tr><th>Cofactor</th><th>Source Enzyme</th><th>Downstream Fate</th></tr></thead>
  <tbody>${redoxRows}</tbody>
</table>` : ''}

${inhibitorRows ? `
<h3 style="font-size:0.92rem;color:#0a1628;margin:1.25rem 0 0.6rem;font-weight:700">🔴 Key Inhibitors</h3>
<table>
  <thead><tr><th>Inhibitor</th><th>Target</th><th>Mechanism</th></tr></thead>
  <tbody>${inhibitorRows}</tbody>
</table>` : ''}

${activatorRows ? `
<h3 style="font-size:0.92rem;color:#0a1628;margin:1.25rem 0 0.6rem;font-weight:700">🟢 Key Activators</h3>
<table>
  <thead><tr><th>Activator</th><th>Target</th><th>Mechanism</th></tr></thead>
  <tbody>${activatorRows}</tbody>
</table>` : ''}
`;
}

// ─── Flux Explanation Section ────────────────────────────────────────────────
function buildFluxSection(m, enzymes, pathway) {
  const netFlux = m.net_flux ?? 0;
  const netFluxPct = Math.round(netFlux * 100);
  const atpYield = m.atp_yield ?? 0;

  // Identify bottleneck: enzyme with lowest flux among regulated enzymes
  const regulated = enzymes.filter(e => e.is_regulated);
  const bottleneck = regulated.length > 0
    ? regulated.reduce((a, b) => (a.flux ?? 1) < (b.flux ?? 1) ? a : b)
    : (enzymes.length > 0 ? enzymes.reduce((a, b) => (a.flux ?? 1) < (b.flux ?? 1) ? a : b) : null);

  // Flux interpretation text
  let fluxInterpretation, fluxBgColor, fluxBorderColor;
  if (netFluxPct >= 80) {
    fluxInterpretation = 'High flux — the pathway is running near its maximum capacity. This reflects an active metabolic demand (e.g. high energy demand, abundant substrate, strong hormonal activation). All enzymes are well-saturated. ATP output is near-maximal.';
    fluxBgColor = '#f0fdf4'; fluxBorderColor = '#16a34a';
  } else if (netFluxPct >= 50) {
    fluxInterpretation = 'Moderate flux — the pathway is operating at roughly half its theoretical maximum. One or more regulatory enzymes are under partial allosteric control or substrate limitation. ATP yield is proportionally reduced from the theoretical maximum.';
    fluxBgColor = '#fffbeb'; fluxBorderColor = '#d97706';
  } else if (netFluxPct >= 25) {
    fluxInterpretation = 'Low flux — significant pathway inhibition is occurring. This may reflect a fasted state, hormonal suppression, substrate depletion, product accumulation, or enzymatic disease state. ATP production will be substantially curtailed.';
    fluxBgColor = '#fff7ed'; fluxBorderColor = '#ea580c';
  } else {
    fluxInterpretation = 'Very low / near-zero flux — the pathway is largely arrested. This could indicate severe hypoxia (inability to regenerate NAD⁺), complete hormonal inhibition, enzyme deficiency, or substrate unavailability. Cells must rely on alternative pathways for survival.';
    fluxBgColor = '#fef2f2'; fluxBorderColor = '#dc2626';
  }

  // Enzyme flux table rows
  const enzymeFluxRows = enzymes.map(e => {
    const pct = Math.round((e.flux ?? 0) * 100);
    const barClass = pct >= 65 ? 'bar-high' : pct >= 35 ? 'bar-medium' : 'bar-low';
    const statusExplain = {
      active: 'Operating at or near Vmax; substrate saturated and no significant inhibition.',
      allosteric: 'Partially inhibited or activated by allosteric effectors; flux reduced vs maximum.',
      inhibited: 'Significantly inhibited — either by product accumulation, allosteric inhibitor, or hormonal phosphorylation.',
      bypass: 'Pathway diverted around this step; a bypass reaction is active.',
    }[e.status] || '';
    const atpImpact = e.is_regulated ? `<span style="color:#7c3aed;font-size:0.75rem">Regulated step — flux directly impacts downstream yield</span>` : '<span style="color:#94a3b8;font-size:0.75rem">Near-equilibrium; follows upstream flux</span>';
    return `<tr>
  <td><strong>${escHtml(e.enzyme_name)}</strong></td>
  <td>
    <div style="display:flex;align-items:center;gap:0.5rem">
      <div class="bar-bg" style="width:80px"><div class="bar-fill ${barClass}" style="width:${pct}%"></div></div>
      <span style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;font-weight:700">${pct}%</span>
    </div>
  </td>
  <td><span class="badge badge-${escHtml(e.status)}">${escHtml(STATUS_LABELS[e.status] || e.status)}</span></td>
  <td style="font-size:0.78rem;color:#475569">${escHtml(statusExplain)}</td>
  <td>${atpImpact}</td>
</tr>`;
  }).join('');

  // ATP correlation text
  const theoreticalAtpNote = atpYield !== 0
    ? `At the current flux of <strong>${netFluxPct}%</strong>, this pathway produced <strong>${atpYield.toFixed(2)} ATP</strong> (substrate-level). The theoretical maximum at 100% flux would be proportionally higher — approximately <strong>${(atpYield / Math.max(netFlux, 0.01)).toFixed(1)} ATP at full saturation</strong>.`
    : `This pathway does not produce ATP directly. Its outputs (NADH, FADH₂, NADPH, acetyl-CoA, or reducing equivalents) feed into downstream pathways (OxPhos, TCA) where ATP is generated.`;

  const bottleneckNote = bottleneck
    ? `<p style="margin-top:0.5rem">⚠️ <strong>Rate-limiting enzyme:</strong> <strong>${escHtml(bottleneck.enzyme_name)}</strong> has the lowest flux at <strong>${Math.round((bottleneck.flux ?? 0) * 100)}%</strong>. This is the primary bottleneck constraining overall pathway throughput. Even if all other enzymes were fully active, the pathway cannot exceed this enzyme's current rate.</p>`
    : '';

  return `
<h2>📈 Flux Analysis</h2>

<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:1rem 1.25rem;margin-bottom:1.25rem">
  <p style="font-size:0.83rem;color:#334155;line-height:1.65;margin-bottom:0.6rem">
    <strong>What is "Net Flux"?</strong><br>
    Net flux (expressed as a percentage) represents the fraction of the pathway's theoretical maximum throughput that is currently achieved, given the prevailing metabolic conditions (substrate concentration, hormonal signals, oxygen availability, energy charge, and allosteric effector levels). A flux of 100% means every enzyme is running at maximum rate (Vmax) simultaneously — a theoretical ceiling rarely reached in vivo.
  </p>
  <p style="font-size:0.83rem;color:#334155;line-height:1.65;margin-bottom:0.6rem">
    <strong>Why does flux matter?</strong><br>
    All quantitative outputs of this pathway — ATP yield, NADH/FADH₂ produced, CO₂ released, metabolite concentrations — scale proportionally with flux. Halving the flux halves every output. Flux is set by the most constrained regulatory enzyme (the bottleneck), which propagates its limitation downstream to all subsequent steps.
  </p>
  <p style="font-size:0.83rem;color:#334155;line-height:1.65">${atpCorrelationNote(atpImpact => atpImpact)}</p>
</div>

<!-- Flux state indicator -->
<div style="display:grid;grid-template-columns:1fr 3fr;gap:1rem;margin-bottom:1.25rem;align-items:start">
  <div style="text-align:center;background:#fff;border-radius:12px;padding:1.25rem 1rem;border:2px solid ${fluxBorderColor}">
    <div style="font-family:'JetBrains Mono',monospace;font-size:3rem;font-weight:900;color:${fluxBorderColor};line-height:1">${netFluxPct}%</div>
    <div style="font-size:0.68rem;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-top:6px;font-weight:700">Net Pathway Flux</div>
  </div>
  <div style="background:${fluxBgColor};border-left:4px solid ${fluxBorderColor};padding:0.9rem 1.1rem;border-radius:0 10px 10px 0;font-size:0.83rem;color:#1e3a5f;line-height:1.65">
    <strong>Interpretation:</strong> ${escHtml(fluxInterpretation)}
    ${bottleneck ? `<p style="margin-top:0.4rem">⚠️ <strong>Bottleneck:</strong> <strong>${escHtml(bottleneck.enzyme_name)}</strong> — lowest flux at <strong>${Math.round((bottleneck.flux ?? 0) * 100)}%</strong>. This enzyme limits the entire pathway's throughput.</p>` : ''}
  </div>
</div>

<!-- ATP-flux correlation -->
<div style="background:#f0f9ff;border-left:4px solid #0284c7;border-radius:0 8px 8px 0;padding:0.75rem 1rem;margin-bottom:1.25rem;font-size:0.83rem;color:#0c4a6e;line-height:1.6">
  💡 <strong>Flux → Yield correlation:</strong> ${atpYield !== 0
    ? `At ${netFluxPct}% flux, this pathway produced <strong>${atpYield.toFixed(2)} ATP</strong> (substrate-level). At 100% flux the yield would be approximately <strong>${(atpYield / Math.max(netFlux, 0.01)).toFixed(1)} ATP</strong> — a ${(100 / Math.max(netFluxPct, 1)).toFixed(1)}× increase if all regulatory constraints were removed simultaneously.`
    : `This pathway does not directly produce ATP. Its reducing equivalents (NADH/FADH₂), specialized cofactors (NADPH), and carbon intermediates (acetyl-CoA) feed downstream pathways. Their abundance scales directly with flux — ${netFluxPct}% flux means ${netFluxPct}% of maximum cofactor/intermediate supply to downstream reactions.`}
</div>

${enzymes.length > 0 ? `
<h3 style="font-size:0.92rem;color:#0a1628;margin:1.25rem 0 0.6rem;font-weight:700">Per-Enzyme Flux & Status Interpretation</h3>
<table>
<thead><tr>
  <th>Enzyme</th><th>Flux %</th><th>Status</th><th>What It Means</th><th>Role</th>
</tr></thead>
<tbody>${enzymeFluxRows}</tbody>
</table>` : ''}
`;
}

// Helper called inside template literal — prevents ESLint no-unused issues
function atpCorrelationNote(fn) { return fn(null); }

export function downloadSimulationReport(result, pathway) {
  if (!result) return;

  const m = result.metrics || {};
  const enzymes = result.enzymes || [];
  const metabolites = result.metabolites || [];
  const notes = result.educational_notes || [];
  const warnings = result.warnings || [];
  const ts = new Date().toLocaleString();
  const scenario = result.scenario_detected?.replace(/_/g,' ') || 'Custom';
  const pathwayLabel = pathway?.replace(/_/g,' ').replace(/\b\w/g, c => c.toUpperCase()) || 'Unknown';

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MetaboSim — ${escHtml(pathwayLabel)} Simulation Report</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Inter',sans-serif;background:#f0f4f8;color:#1a2535;padding:0;print-color-adjust:exact}
  
  .cover{background:linear-gradient(135deg,#0a1628 0%,#0c2145 50%,#0a3060 100%);color:#fff;
    padding:3rem 3rem 2rem;min-height:200px;page-break-after:always}
  .cover h1{font-size:2.2rem;font-weight:800;letter-spacing:-0.04em;margin-bottom:0.5rem}
  .cover h1 span{color:#00e5ff}
  .cover .subtitle{font-size:0.9rem;color:rgba(255,255,255,0.55);font-family:'JetBrains Mono',monospace;letter-spacing:0.08em;text-transform:uppercase}
  .cover .meta{margin-top:1.5rem;display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
  .cover .meta-item label{font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.4);font-family:'JetBrains Mono',monospace}
  .cover .meta-item .val{font-size:1rem;font-weight:700;color:#00e5ff;font-family:'JetBrains Mono',monospace}
  
  .content{padding:2rem 3rem}
  
  h2{font-size:1.1rem;font-weight:700;color:#0a1628;margin:2rem 0 1rem;
    display:flex;align-items:center;gap:0.6rem;letter-spacing:-0.02em}
  h2::after{content:'';flex:1;height:1px;background:#e2e8f0}
  h3{color:#1e3a5f;margin-bottom:0.5rem}
  
  .stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:0.75rem;margin-bottom:1.5rem}
  .stat-card{background:#fff;border-radius:12px;padding:1rem;border:1px solid #e2e8f0;
    box-shadow:0 2px 8px rgba(0,0,0,0.06)}
  .stat-card .sv{font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:700;line-height:1}
  .stat-card .sl{font-size:0.68rem;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-top:4px;font-weight:600}
  .cyan{color:#0077b6}.green{color:#059669}.red{color:#dc2626}.amber{color:#d97706}.purple{color:#7c3aed}
  
  table{width:100%;border-collapse:collapse;margin-bottom:1.5rem;font-size:0.82rem}
  thead tr{background:#f8fafc;border-bottom:2px solid #e2e8f0}
  th{text-align:left;padding:0.6rem 0.75rem;font-size:0.68rem;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;font-weight:700}
  td{padding:0.6rem 0.75rem;border-bottom:1px solid #f1f5f9}
  tr:hover td{background:#f8fafc}
  .bar-cell{min-width:120px}
  .bar-bg{background:#f1f5f9;border-radius:99px;height:6px;overflow:hidden}
  .bar-fill{height:100%;border-radius:99px}
  .bar-high{background:linear-gradient(90deg,#10b981,#059669)}
  .bar-medium{background:linear-gradient(90deg,#f59e0b,#d97706)}
  .bar-low{background:linear-gradient(90deg,#ef4444,#dc2626)}
  
  .badge{display:inline-block;padding:2px 8px;border-radius:99px;font-size:0.7rem;font-weight:700;
    font-family:'JetBrains Mono',monospace}
  .badge-active{background:#dcfce7;color:#15803d}
  .badge-inhibited{background:#fee2e2;color:#dc2626}
  .badge-allosteric{background:#fef3c7;color:#b45309}
  .badge-bypass{background:#ede9fe;color:#6d28d9}
  
  .note{background:#eff6ff;border-left:4px solid #3b82f6;padding:0.75rem 1rem;
    border-radius:0 8px 8px 0;margin-bottom:0.5rem;font-size:0.83rem;color:#1e40af;line-height:1.55}
  .warn{background:#fffbeb;border-left:4px solid #f59e0b;padding:0.75rem 1rem;
    border-radius:0 8px 8px 0;margin-bottom:0.5rem;font-size:0.83rem;color:#92400e;line-height:1.55}
  
  .footer{text-align:center;padding:1.5rem;color:#94a3b8;font-size:0.72rem;
    font-family:'JetBrains Mono',monospace;border-top:1px solid #e2e8f0;margin-top:2rem;letter-spacing:0.05em}
  
  @media print{body{background:#fff}@page{margin:1.5cm}}
</style>
</head>
<body>

<div class="cover">
  <div class="subtitle">MetaboSim v2.0 — Simulation Report</div>
  <h1>${escHtml(pathwayLabel)} <span>Pathway Analysis</span></h1>
  <div class="meta">
    <div class="meta-item"><label>Generated</label><div class="val">${escHtml(ts)}</div></div>
    <div class="meta-item"><label>Scenario</label><div class="val">${escHtml(scenario)}</div></div>
    <div class="meta-item"><label>Pathway</label><div class="val">${escHtml(pathwayLabel)}</div></div>
    <div class="meta-item"><label>Author</label><div class="val">Chibuike Praise Okechukwu · praizekene1@gmail.com</div></div>
  </div>
</div>

<div class="content">

<h2>⚡ Energy &amp; Metabolic Metrics</h2>
<div class="stat-grid">
  <div class="stat-card">
    <div class="sv cyan">${(m.atp_yield ?? 0).toFixed(2)}</div>
    <div class="sl">Net ATP Yield</div>
  </div>
  <div class="stat-card">
    <div class="sv ${(m.atp_yield??0) > 10 ? 'green' : 'amber'}">${((m.net_flux ?? 0) * 100).toFixed(1)}%</div>
    <div class="sl">Net Flux</div>
  </div>
  <div class="stat-card">
    <div class="sv purple">${(m.nadh_produced ?? 0).toFixed(2)}</div>
    <div class="sl">NADH Produced</div>
  </div>
  <div class="stat-card">
    <div class="sv amber">${(m.fadh2_produced ?? 0).toFixed(2)}</div>
    <div class="sl">FADH₂ Produced</div>
  </div>
  ${(m.nadph_produced ?? 0) > 0 ? `<div class="stat-card">
    <div class="sv" style="color:#7c3aed">${(m.nadph_produced ?? 0).toFixed(2)}</div>
    <div class="sl">NADPH Produced</div>
  </div>` : ''}
  <div class="stat-card">
    <div class="sv ${(m.lactate_output??0) > 0.5 ? 'red' : 'green'}">${((m.lactate_output ?? 0) * 100).toFixed(1)}%</div>
    <div class="sl">Lactate Output</div>
  </div>
  <div class="stat-card">
    <div class="sv">${(m.co2_released ?? 0).toFixed(2)}</div>
    <div class="sl">CO₂ Released</div>
  </div>
</div>

${buildFluxSection(m, enzymes, pathway)}

${buildATPBreakdownSection(m, pathway)}


${enzymes.length > 0 ? `
<h2>⚙️ Enzyme Activity</h2>
<p style="font-size:0.78rem;color:#64748b;margin-bottom:0.75rem">Flux bars show relative enzyme activity (0–100%). Colour: <span style="color:#059669;font-weight:700">green</span> = active, <span style="color:#d97706;font-weight:700">amber</span> = allosteric, <span style="color:#dc2626;font-weight:700">red</span> = inhibited. Badges like <span style="background:#ff4d6d33;border:1px solid #ff4d6d;color:#ff6b82;font-size:0.65rem;padding:1px 5px;border-radius:3px">ATP↓</span> <span style="background:#ffcc0022;border:1px solid #ffcc00;color:#b8960a;font-size:0.65rem;padding:1px 5px;border-radius:3px">NADH↑</span> <span style="background:#fb923c22;border:1px solid #fb923c;color:#ea7117;font-size:0.65rem;padding:1px 5px;border-radius:3px">FADH₂↑</span> indicate the energy role of each step on the pathway map.</p>
<table>
<thead><tr>
  <th>Enzyme</th><th>ID</th><th>Status</th><th>Flux</th><th style="min-width:140px">Activity</th>
</tr></thead>
<tbody>
${enzymes.map(e => {
  const pct = Math.round((e.flux ?? 0) * 100);
  const barClass = pct >= 65 ? 'bar-high' : pct >= 35 ? 'bar-medium' : 'bar-low';
  return `<tr>
  <td><strong>${escHtml(e.enzyme_name)}</strong></td>
  <td style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#64748b">${escHtml(e.enzyme_id)}</td>
  <td><span class="badge badge-${escHtml(e.status)}">${escHtml(STATUS_LABELS[e.status] || e.status)}</span></td>
  <td style="font-family:'JetBrains Mono',monospace">${(e.flux ?? 0).toFixed(3)}</td>
  <td class="bar-cell">
    <div style="display:flex;align-items:center;gap:0.5rem">
      <div class="bar-bg" style="flex:1"><div class="bar-fill ${barClass}" style="width:${pct}%"></div></div>
      <span style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#64748b">${pct}%</span>
    </div>
  </td>
</tr>`;
}).join('')}
</tbody>
</table>` : ''}

${metabolites.length > 0 ? `
<h2>🧪 Metabolite Concentrations</h2>
<table>
<thead><tr><th>Metabolite</th><th>ID</th><th>Concentration (rel.)</th><th>Trend</th></tr></thead>
<tbody>
${metabolites.map(met => {
  const pct = Math.round((met.concentration ?? 0) * 100);
  return `<tr>
  <td><strong>${escHtml(met.name)}</strong></td>
  <td style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#64748b">${escHtml(met.metabolite_id)}</td>
  <td>
    <div style="display:flex;align-items:center;gap:0.5rem">
      <div class="bar-bg" style="width:100px"><div class="bar-fill bar-high" style="width:${pct}%"></div></div>
      <span style="font-family:'JetBrains Mono',monospace;font-size:0.72rem">${pct}%</span>
    </div>
  </td>
  <td>${escHtml(met.trend || '—')}</td>
</tr>`;
}).join('')}
</tbody>
</table>` : ''}

${warnings.length > 0 ? `<h2>⚠️ Warnings</h2>${warnings.map(w => `<div class="warn">⚠️ ${escHtml(w)}</div>`).join('')}` : ''}

${notes.length > 0 ? `<h2>📚 Educational Notes</h2>${notes.map(n => `<div class="note">💡 ${escHtml(n)}</div>`).join('')}` : ''}

</div>
<div class="footer">METABOSIM v2.0 — GENERATED ${escHtml(ts.toUpperCase())} — AUTHOR: CHIBUIKE PRAISE OKECHUKWU (praizekene1@gmail.com) — FOR EDUCATIONAL PURPOSES ONLY</div>
</body>
</html>`;

  const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `MetaboSim_${pathwayLabel.replace(/\s+/g,'_')}_Report_${Date.now()}.html`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
