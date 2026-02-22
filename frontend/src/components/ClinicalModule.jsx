import { useState } from 'react';
import { runSimulation } from '../utils/api';

const CLINICAL_CASES = [
  // ── Glycogen Storage Diseases ──────────────────────────────────
  {
    id: 'von_gierke',
    name: 'Von Gierke Disease',
    subtitle: 'GSD Type Ia — G6Pase Deficiency',
    icon: '🧬',
    color: '#ffb700',
    category: 'Glycogen Storage',
    icd: 'E74.01',
    scenario: 'A 3-month-old infant presents with profound hypoglycaemia, markedly hepatomegaly, hyperlipidaemia, and hyperuricaemia. Glucose-6-phosphatase (G6Pase) enzyme activity is undetectable on liver biopsy.',
    params: { glucose_mM: 1.5, oxygen_pct: 100, insulin_fold: 0.2, glucagon_fold: 4.0, energy_demand: 1.0, nutritional_state: 'starved', pathway: 'gluconeogenesis' },
    keyPoints: [
      'G6Pase deficiency blocks BOTH glycogenolysis AND gluconeogenesis from releasing free glucose into blood',
      'G6P accumulates → shunted to glycolysis → pyruvate → lactate (Type B lactic acidosis)',
      'G6P → pentose phosphate pathway → purines → uric acid (hyperuricaemia, risk of gout)',
      'Excess G6P → lipogenesis → hypercholesterolaemia and hypertriglyceridaemia',
      'Treatment: frequent cornstarch feeds to prevent hypoglycaemia; no cure but liver transplant is curative',
    ],
    labs: { glucose: '↓↓', lactate: '↑↑', uricAcid: '↑↑', triglycerides: '↑↑', alanine: 'normal' },
  },
  {
    id: 'pompe',
    name: 'Pompe Disease',
    subtitle: 'GSD Type II — Lysosomal α-1,4-glucosidase (GAA) Deficiency',
    icon: '💪',
    color: '#c084fc',
    category: 'Glycogen Storage',
    icd: 'E74.02',
    scenario: 'A 4-month-old presents with hypertrophic cardiomyopathy, severe hypotonia ("floppy baby"), and respiratory distress. CK is 2000 U/L. ECG shows extremely short PR interval and massive QRS. Acid GAA activity absent on dried blood spot (DBS).',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 2.5, nutritional_state: 'fed', pathway: 'glycolysis' },
    keyPoints: [
      'Lysosomal GAA (acid maltase) breaks down glycogen within lysosomes; deficiency causes glycogen accumulation in ALL tissues',
      'Cardiomegaly and myopathy dominate in infantile form; limb-girdle weakness in late-onset form',
      'Only GSD where the defect is lysosomal (not cytoplasmic) — hence systemic organ involvement',
      'Enzyme replacement therapy (alglucosidase alfa) is life-changing; approved 2006',
      'Newborn screening via GAA DBS now standard in many countries',
    ],
    labs: { glucose: 'normal', lactate: 'normal', CK: '↑↑↑', ecg: 'Giant QRS', echo: 'Hypertrophic CM' },
  },
  {
    id: 'cori',
    name: 'Cori Disease',
    subtitle: 'GSD Type III — Debranching Enzyme Deficiency',
    icon: '🔗',
    color: '#2dd4bf',
    category: 'Glycogen Storage',
    icd: 'E74.03',
    scenario: 'A 6-year-old has hepatomegaly, moderate fasting hypoglycaemia, elevated AST/ALT, and elevated CK. Unlike Von Gierke, lactate and uric acid are normal. Liver biopsy shows limit dextrin accumulation.',
    params: { glucose_mM: 2.8, oxygen_pct: 100, insulin_fold: 0.5, glucagon_fold: 3.0, energy_demand: 1.5, nutritional_state: 'fasted', pathway: 'glycolysis' },
    keyPoints: [
      'Debranching enzyme (amylo-1,6-glucosidase) removes branch-point glucose in glycogen; deficiency causes limit dextrin accumulation',
      'Unlike GSD Ia: gluconeogenesis is INTACT, so hypoglycaemia is milder and lactate is normal',
      'Elevated CK suggests muscle as well as liver involvement (GSD IIIa): distinguish from GSD IIIb (liver only)',
      'High-protein diet with frequent meals is effective management strategy',
    ],
    labs: { glucose: '↓', lactate: 'normal', CK: '↑', AST: '↑', lactateAfterGlucagon: 'no rise' },
  },
  {
    id: 'mcardle',
    name: "McArdle Disease",
    subtitle: 'GSD Type V — Muscle Glycogen Phosphorylase Deficiency',
    icon: '🏃',
    color: '#ff7043',
    category: 'Glycogen Storage',
    icd: 'E74.04',
    scenario: 'A 25-year-old marathon runner develops painful cramp, exercise-induced myoglobinuria (dark red urine), and extreme fatigue after bursts of anaerobic exercise. Symptoms improve after a short rest ("second wind" phenomenon). CK is 5,000 U/L post-exercise.',
    params: { glucose_mM: 5.0, oxygen_pct: 30, insulin_fold: 1.0, glucagon_fold: 2.0, energy_demand: 5.0, nutritional_state: 'fed', pathway: 'glycolysis' },
    keyPoints: [
      'Muscle glycogen phosphorylase (myophosphorylase) deficiency → muscle cannot mobilise glycogen during intense exercise',
      '"Second wind": hepatic glycogenolysis provides circulating glucose after initial glycogen-depleted fatigue',
      'Forearm ischaemic exercise test (modified): lactate fails to rise in McArdle (but ammonia rises normally)',
      'Risk of acute kidney injury from myoglobinuria — adequate hydration critical',
      'Treatment: carbohydrate loading before exercise, sucrose ingestion, regular aerobic training',
    ],
    labs: { lactateExercise: '↔ (no rise)', CK: '↑↑ (post-exercise)', myoglobinuria: '+', EMG: 'normal at rest' },
  },
  {
    id: 'hers',
    name: "Hers Disease",
    subtitle: 'GSD Type VI — Hepatic Glycogen Phosphorylase Deficiency',
    icon: '🫀',
    color: '#4488ff',
    category: 'Glycogen Storage',
    icd: 'E74.09',
    scenario: 'A 2-year-old has mild hepatomegaly, mild fasting hypoglycaemia, and growth delay. Unlike Von Gierke, lactate is normal and hypoglycaemia is not severe. Enzyme activity of liver glycogen phosphorylase is markedly reduced.',
    params: { glucose_mM: 3.0, oxygen_pct: 100, insulin_fold: 0.8, glucagon_fold: 2.5, energy_demand: 1.0, nutritional_state: 'fasted', pathway: 'glycolysis' },
    keyPoints: [
      'Hepatic glycogen phosphorylase failure → glycogen accumulates in liver → hepatomegaly',
      'Gluconeogenesis intact → hypoglycaemia mild compared to GSD Ia',
      'Often improves spontaneously at puberty — generally benign prognosis',
      'Differentiated from GSD IX (kinase deficiency) by enzyme assay',
    ],
    labs: { glucose: '↓ mild', lactate: 'normal', triglycerides: 'mild ↑', hepatomegaly: 'moderate' },
  },

  // ── Enzyme Deficiencies in Glycolysis/Gluconeogenesis ──────────
  {
    id: 'pyk_deficiency',
    name: 'Pyruvate Kinase Deficiency',
    subtitle: 'Haemolytic Anaemia — PKLR Gene Mutation',
    icon: '🔴',
    color: '#ff4d6d',
    category: 'Glycolytic Enzyme Defects',
    icd: 'D55.2',
    scenario: 'A newborn presents with severe jaundice requiring exchange transfusion, splenomegaly, and a haemoglobin of 4 g/dL. Blood smear shows echinocytes. Osmotic fragility is normal. PK enzyme activity in erythrocytes is 15% of normal.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 3.0, nutritional_state: 'fed', pathway: 'glycolysis' },
    keyPoints: [
      'Red blood cells are 100% dependent on glycolysis for ATP (no mitochondria, no TCA/OxPhos)',
      'PK deficiency → pyruvate kinase cannot synthesise ATP at step 10 → ATP depletion → RBC membrane pump failure → haemolysis',
      'Metabolites proximal to PK (2,3-BPG, PEP) accumulate → elevated 2,3-BPG shifts O₂ dissociation curve right (helpful)',
      'Most common glycolytic enzyme deficiency causing CNSHA (Chronic Non-Spherocytic Haemolytic Anaemia)',
      'Splenectomy reduces transfusion requirement; mitapivat (allosteric PK activator) is new therapy',
    ],
    labs: { hb: '4–8 g/dL', reticulocytes: '↑↑', bilirubin: '↑↑', PK_activity: '↓↓', osmotic_fragility: 'normal' },
  },
  {
    id: 'g6pd',
    name: 'G6PD Deficiency',
    subtitle: 'Pentose Phosphate Pathway — Most Common Enzyme Deficiency Worldwide',
    icon: '🧫',
    color: '#00e5ff',
    category: 'Glycolytic Enzyme Defects',
    icd: 'D55.0',
    scenario: 'A 20-year-old of Mediterranean origin develops sudden jaundice and haemoglobinuria 48 hours after taking primaquine for malaria prophylaxis. Hb drops from 13 to 7 g/dL. G6PD activity is 8% of normal.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 2.0, nutritional_state: 'fed', pathway: 'glycolysis' },
    keyPoints: [
      'G6PD generates NADPH via HMP shunt → NADPH regenerates glutathione (GSH) → protects RBCs from oxidative stress',
      'Triggers: primaquine, dapsone, fava beans, infection (all increase oxidative stress)',
      'G6PD deficiency → reduced NADPH → oxidised glutathione accumulates → Heinz bodies (denatured Hb) → haemolysis',
      'X-linked: affects males predominantly; 400 million people affected globally',
      'Neonatal jaundice risk: screen all neonates in endemic regions before phototherapy',
    ],
    labs: { g6pd_activity: '↓↓', heinz_bodies: '+', hb: 'acute drop', bilirubin: '↑↑', reticulocytes: '↑' },
  },
  {
    id: 'fructose_intolerance',
    name: 'Hereditary Fructose Intolerance',
    subtitle: 'Aldolase B Deficiency — Severe Post-Prandial Hypoglycaemia',
    icon: '🍎',
    color: '#f97316',
    category: 'Fructose Metabolism',
    icd: 'E74.12',
    scenario: 'A 6-month-old infant develops vomiting, irritability, and hypoglycaemia after introduction of fruit puree. The mother notes the child avidly avoids sweet foods. LFTs show markedly elevated AST/ALT. A "fructose-free" diet resolves all symptoms.',
    params: { glucose_mM: 2.0, oxygen_pct: 100, insulin_fold: 2.0, glucagon_fold: 1.0, energy_demand: 1.5, nutritional_state: 'fed', pathway: 'glycolysis' },
    keyPoints: [
      'Aldolase B cleaves fructose-1-phosphate into DHAP and glyceraldehyde in liver/kidney/intestine',
      'Deficiency → F1P accumulates → sequesters inorganic phosphate → ATP depletion → hepatocyte damage',
      'High F1P also inhibits PGM and phosphorylase → blocks glucose release from glycogen → hypoglycaemia',
      'Unique: untreated children develop instinctive aversion to sweet foods (natural protective behaviour)',
      'Completely reversible with fructose/sorbitol/sucrose exclusion; cirrhosis occurs if diagnosis delayed',
    ],
    labs: { glucose: '↓ post-fructose', AST: '↑↑↑', phosphate: '↓ (acute)', uricAcid: '↑', reducing_substances_urine: '+' },
  },
  {
    id: 'galactosaemia',
    name: 'Classic Galactosaemia',
    subtitle: 'GALT Deficiency — Galactose-1-Phosphate Uridyltransferase',
    icon: '🥛',
    color: '#a78bfa',
    category: 'Galactose Metabolism',
    icd: 'E74.21',
    scenario: 'A 5-day-old neonate presents with jaundice, sepsis (E. coli), poor feeding, and hepatomegaly after breast milk introduction. Urine dipstick shows reducing substances that are NOT glucose. Galactosaemia is confirmed on newborn screen.',
    params: { glucose_mM: 2.5, oxygen_pct: 100, insulin_fold: 1.2, glucagon_fold: 1.0, energy_demand: 1.5, nutritional_state: 'fed', pathway: 'glycolysis' },
    keyPoints: [
      'Galactose-1-phosphate uridyltransferase (GALT) converts Gal-1-P + UDP-Glucose → Glucose-1-P + UDP-Galactose',
      'Deficiency → Gal-1-P accumulates → inhibits phosphoglucomutase and glycogen phosphorylase → hypoglycaemia',
      'Galactose → galactitol (aldose reductase) → cataracts, neuropathy',
      'E. coli sepsis in neonates: classic association — Gal-1-P impairs neutrophil function',
      'Treatment: eliminate galactose (dairy) immediately; outcomes good if caught early on NBS',
    ],
    labs: { galactose_1P: '↑↑↑', GALT_activity: '↓↓↓', reducing_urine: '+', LFTs: '↑↑', cataracts: 'early' },
  },

  // ── Carbohydrate Oxidation Disorders ─────────────────────────
  {
    id: 'lactic_acidosis',
    name: 'Lactic Acidosis',
    subtitle: 'Type A — Tissue Hypoperfusion / Septic Shock',
    icon: '⚠️',
    color: '#ef4444',
    category: 'Organic Acid Disorders',
    icd: 'E87.2',
    scenario: 'A 45-year-old presents to ED with confusion, tachycardia (HR 130), BP 80/50, and laboured breathing. ABG: pH 7.15, lactate 9.8 mmol/L, BE −16. CT chest: bilateral consolidations. Resuscitation initiated for septic shock.',
    params: { glucose_mM: 5.0, oxygen_pct: 8.0, insulin_fold: 1.0, glucagon_fold: 1.5, energy_demand: 4.0, nutritional_state: 'fed', pathway: 'glycolysis' },
    keyPoints: [
      'Type A lactic acidosis: inadequate tissue oxygen delivery → NADH accumulates → LDH reduces pyruvate to lactate to regenerate NAD⁺',
      'Type B: no hypoperfusion — metformin (Complex I inhibition), thiamine deficiency (PDH co-factor), malignancy',
      'Normal lactate < 2 mmol/L; > 4 mmol/L with metabolic acidosis = lactic acidosis',
      'Blood gas interpretation: AG = Na − (Cl + HCO₃); elevated AG acidosis with high lactate = Type A',
      'Treatment is supportive: O₂, fluids, vasopressors, treat source; sodium bicarbonate controversial',
    ],
    labs: { lactate: '↑↑↑', pH: '↓↓', HCO3: '↓', AG: '↑', base_excess: '↓↓' },
  },
  {
    id: 'pdh_deficiency',
    name: 'Pyruvate Dehydrogenase Deficiency',
    subtitle: 'PDH Complex Deficiency — X-linked Intellectual Disability',
    icon: '🔬',
    color: '#34d399',
    category: 'Organic Acid Disorders',
    icd: 'E74.4',
    scenario: 'A male neonate presents with severe neonatal lactic acidosis, hypotonia, seizures, and brain MRI shows basal ganglia lesions resembling Leigh syndrome. PDH E1α subunit activity is 10% of normal. Father is unaffected; mother is a carrier.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 2.0, nutritional_state: 'fed', pathway: 'tca_cycle' },
    keyPoints: [
      'PDH complex converts pyruvate → acetyl-CoA (CO₂ + NADH), linking glycolysis to TCA cycle',
      'Requires 5 cofactors: thiamine (B1), lipoic acid, CoA, FAD, NAD⁺ — cofactor deficiency mimics PDH deficiency',
      'Deficiency → pyruvate accumulates → shunted to lactate (lactic acidosis) and alanine',
      'Brain depends on glucose/acetyl-CoA: PDH deficiency causes severe neurodegeneration (Leigh-like phenotype)',
      'Thiamine supplementation if cofactor deficiency suspected; ketogenic diet bypasses PDH by providing acetyl-CoA from fatty acids',
    ],
    labs: { lactate: '↑↑', pyruvate: '↑↑', lactate_pyruvate_ratio: '< 20 (normal ratio)', alanine: '↑', CSF_lactate: '↑↑' },
  },
  {
    id: 'mitochondrial_myopathy',
    name: 'MELAS Syndrome',
    subtitle: 'Mitochondrial Encephalomyopathy, Lactic Acidosis & Stroke-like Episodes',
    icon: '🧠',
    color: '#818cf8',
    category: 'Mitochondrial Disorders',
    icd: 'G31.82',
    scenario: 'A 22-year-old woman has sudden-onset hemianopia, confusion, and headache mimicking a stroke. MRI shows non-vascular T2 lesions crossing territories. Lactate is elevated at rest and spikes markedly after exercise. Muscle biopsy shows ragged-red fibres (modified Gomori trichrome). mtDNA shows m.3243A>G mutation.',
    params: { glucose_mM: 5.0, oxygen_pct: 55.0, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 3.5, nutritional_state: 'fed', pathway: 'oxphos' },
    keyPoints: [
      'MELAS: most common mitochondrial disease; m.3243A>G in MT-TL1 (tRNA-Leu) → impaired oxidative phosphorylation',
      'Stroke-like episodes: not thromboembolic but mitochondrial angiopathy → vascular walls cannot produce ATP → ischaemia',
      'Ragged-red fibres: peripheral mitochondrial proliferation; subsarcolemmal accumulation visible on Gomori trichrome',
      'Maternal inheritance (mtDNA); variable penetrance due to heteroplasmy',
      'Management: avoid mitochondrial toxic drugs (metformin, valproate, linezolid); CoQ10, riboflavin, L-arginine (for strokes)',
    ],
    labs: { serum_lactate: '↑', plasma_amino: 'alanine ↑', mtDNA_mutation: '+', MRI: 'stroke-like FLAIR lesions', biopsy: 'RRF' },
  },
  {
    id: 'type2_diabetes',
    name: 'Type 2 Diabetes Mellitus',
    subtitle: 'Insulin Resistance with Relative Insulin Deficiency',
    icon: '🩺',
    color: '#22d3ee',
    category: 'Glucose Homeostasis',
    icd: 'E11',
    scenario: 'A 58-year-old obese man (BMI 35) has fasting glucose 12 mmol/L, HbA1c 9.2%, elevated fasting insulin (insulin resistance), and markedly elevated triglycerides. On OGTT, 2-hour glucose is 19 mmol/L. Glucagon suppression by insulin is lost.',
    params: { glucose_mM: 15.0, oxygen_pct: 100.0, insulin_fold: 3.0, glucagon_fold: 2.5, energy_demand: 1.2, nutritional_state: 'fasted', pathway: 'integrated' },
    keyPoints: [
      'Insulin resistance: PI3K pathway impaired → GLUT4 translocation fails in muscle/adipose → hyperglycaemia',
      'Hepatic insulin resistance: paradoxically insulin signalling through SREBP-1c is retained → lipogenesis proceeds',
      'Glucagon paradoxically NOT suppressed by hyperinsulinaemia → bihormonal defect drives hepatic glucose output',
      'Chronic hyperglycaemia → AGE formation → endothelial glycocalyx damage → micro/macrovascular disease',
      'Metformin: activates AMPK → phosphorylates TORC2 → reduces PEPCK/G6Pase gene expression',
    ],
    labs: { glucose: '↑↑', HbA1c: '↑↑', fasting_insulin: '↑', c_peptide: '↑', triglycerides: '↑↑' },
  },
  {
    id: 'fructose_malabsorption',
    name: 'Fructose Malabsorption',
    subtitle: 'Dietary Fructose Intolerance — GLUT5 Insufficiency',
    icon: '🍓',
    color: '#fb7185',
    category: 'Fructose Metabolism',
    icd: 'K90.4',
    scenario: 'A 28-year-old woman reports chronic bloating, abdominal pain, and diarrhoea specifically after eating fruits, honey, and HFCS-containing foods. Hydrogen breath test after fructose load is markedly positive at 60 minutes (>20 ppm rise). Her symptoms completely resolve on a low-FODMAP diet.',
    params: { glucose_mM: 8.0, oxygen_pct: 100, insulin_fold: 2.0, glucagon_fold: 0.8, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'glycolysis' },
    keyPoints: [
      'GLUT5 (SLC2A5) transports fructose across intestinal brush border; reduced GLUT5 activity = malabsorption',
      'Unabsorbed fructose reaches colon → fermented by bacteria → short-chain fatty acids + H₂/CO₂/CH₄ → bloating',
      'Distinct from hereditary fructose intolerance (which is metabolic, not absorptive)',
      'Low-FODMAP diet (Fermentable Oligosaccharides, Disaccharides, Monosaccharides, Polyols) is effective',
      'May coexist with IBS-D; breath test is diagnostic standard',
    ],
    labs: { H2_breath: '↑ (>20 ppm)', stool_acidity: '↑', serum_fructose: 'not measured routinely' },
  },
  {
    id: 'fanconi_bickel',
    name: 'Fanconi–Bickel Syndrome',
    subtitle: 'GLUT2 Deficiency — Renal Tubular Fanconi Syndrome',
    icon: '🫘',
    color: '#86efac',
    category: 'Glucose Transport Disorders',
    icd: 'E74.09',
    scenario: 'A 4-month-old has severe failure to thrive, rickets on X-ray, massive glycosuria despite euglycaemia, and hepatomegaly. Urine shows glucosuria + aminoaciduria + phosphaturia + bicarbonaturia. GLUT2 gene mutation identified on sequencing.',
    params: { glucose_mM: 4.5, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.5, energy_demand: 1.5, nutritional_state: 'fed', pathway: 'glycolysis' },
    keyPoints: [
      'GLUT2 is the high-Km, high-capacity glucose transporter in liver, intestine, kidney, and pancreatic β-cells',
      'Liver: GLUT2 deficiency → impaired glucose/galactose uptake → glycogen accumulates → hepatomegaly',
      'Kidney: GLUT2 is basolateral in proximal tubule → deficiency → glucose (+ other solutes) not reabsorbed → generalised Fanconi syndrome',
      'Pancreatic β-cells lose glucose sensing → impaired first-phase insulin → postprandial hyperglycaemia, then fasting hypoglycaemia',
      'Management: cornstarch, electrolyte replacement (K, PO₄, Na, HCO₃), vitamin D and phosphate for rickets',
    ],
    labs: { urine_glucose: '↑↑↑', amino_acids_urine: '↑↑', phosphate_urine: '↑↑', serum_phosphate: '↓', alkaline_phosphatase: '↑↑' },
  },

  // ── HMP Shunt Disorders ──────────────────────────────────────────
  {
    id: 'wernicke',
    name: "Wernicke's Encephalopathy",
    subtitle: 'Thiamine (B1) Deficiency — Transketolase Impairment',
    icon: '🧠',
    color: '#818cf8',
    category: 'HMP Shunt / Cofactor Deficiency',
    icd: 'E51.2',
    scenario: 'A 42-year-old with alcohol use disorder presents confused, with nystagmus, ophthalmoplegia (CN VI palsy), and ataxia. He has not eaten for 5 days. A&E nurse administers glucose infusion; symptoms worsen acutely. Thiamine is urgently administered — consciousness improves within 2 hours.',
    params: { glucose_mM: 6.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 2.0, nutritional_state: 'starved', pathway: 'hmp_shunt' },
    keyPoints: [
      'Thiamine (B1) as TPP is the essential cofactor for Transketolase (non-oxidative PPP), PDH complex, and α-KGDH complex',
      'Transketolase deficiency → PPP cannot regenerate F6P/G3P → impaired nucleotide synthesis + NADPH production',
      'Hallmark triad: Confusion + Ataxia + Ophthalmoplegia (CN VI palsy + nystagmus)',
      'CRITICAL: NEVER give dextrose before thiamine in alcoholic patients — glucose loading depletes last thiamine reserves → precipitates acute Wernicke\'s',
      'Erythrocyte Transketolase Activation Coefficient (ETKA) > 1.25 confirms thiamine deficiency',
      'Treatment: high-dose IV thiamine (Pabrinex) before any glucose. Korsakoff\'s (irreversible) develops if Wernicke\'s untreated.',
    ],
    labs: { thiamine_RBC: '↓↓', ETKA: '↑ (>1.25)', lactate: '↑ (PDH impaired)', MRI: 'mamillary body/periaqueductal signal' },
  },
  {
    id: 'transaldolase_def',
    name: 'Transaldolase Deficiency',
    subtitle: 'Non-Oxidative PPP Defect — Hepatic Cirrhosis in Infancy',
    icon: '🔬',
    color: '#6366f1',
    category: 'HMP Shunt / Cofactor Deficiency',
    icd: 'E74.8',
    scenario: 'A 6-month-old has progressive hepatomegaly, elevated transaminases, coagulopathy, and thrombocytopenia. Urine organic acids show elevations of sedoheptitol, erythritol, and arabitol. Liver biopsy shows cirrhosis. TALDO1 enzyme activity is absent.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.5, nutritional_state: 'fed', pathway: 'hmp_shunt' },
    keyPoints: [
      'Transaldolase (TALDO1) converts Sedoheptulose-7-P + G3P → Erythrose-4-P + Fructose-6-P in the non-oxidative PPP',
      'Deficiency → sedoheptulose-7-P, sedoheptitol, erythritol, arabitol accumulate → hepatotoxic polyol overload',
      'Presents with congenital liver disease: hepatosplenomegaly, cirrhosis, thrombocytopenia',
      'Unique biomarker: elevated urinary sugar alcohols (sedoheptitol) on urine organic acids/polyol screen',
      'Some improvement with dietary antioxidant supplementation (N-acetylcysteine); liver transplantation may be required',
    ],
    labs: { sedoheptitol: '↑↑ (urine)', AST_ALT: '↑↑', coagulation: '↓', platelets: '↓', TALDO1_activity: 'absent' },
  },

  // ── Glycogen Metabolism Disorders ───────────────────────────────
  {
    id: 'andersen',
    name: 'Andersen Disease',
    subtitle: 'GSD Type IV — Branching Enzyme (GBE1) Deficiency',
    icon: '🌲',
    color: '#4ade80',
    category: 'Glycogen Storage',
    icd: 'E74.09',
    scenario: 'A 9-month-old presents with failure to thrive, severe hepatomegaly, hardened liver on palpation, and progressive jaundice. Liver biopsy shows PAS-positive amylopectin-like inclusions. GBE1 enzyme activity is absent in liver and fibroblasts. Liver transplant is planned.',
    params: { glucose_mM: 4.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.5, energy_demand: 1.5, nutritional_state: 'fed', pathway: 'glycogenesis' },
    keyPoints: [
      'Branching enzyme (GBE1) creates α-1,6 branch points from α-1,4 chains in glycogen every 8–12 residues',
      'Deficiency → amylopectin-like glycogen (long unbranched chains, starch-like) → poorly soluble → hepatotoxic inclusions',
      'Presents as neonatal/infantile hepatic cirrhosis → portal hypertension → liver failure by 2 years if untreated',
      'Glycogen cannot be mobilised efficiently (branching increases outer chain density for phosphorylase access)',
      'Classic form: liver transplant is curative for hepatic phenotype (non-progressive neuromuscular form also exists)',
      'GBE1 mutations: autosomal recessive; GBE1 is same enzyme that creates amylopectin branches in starch metabolism',
    ],
    labs: { LFTs: '↑↑↑', PT: '↑↑', albumin: '↓', glycogen_structure: 'amylopectin-like inclusions', GBE1_activity: 'absent' },
  },
  {
    id: 'gsd0',
    name: 'GSD Type 0 (Glycogen Synthase Deficiency)',
    subtitle: 'GYS2 Deficiency — Empty Glycogen Stores',
    icon: '🪫',
    color: '#86efac',
    category: 'Glycogen Storage',
    icd: 'E74.09',
    scenario: 'A 7-year-old presents with early morning fasting hypoglycaemia, ketosis (not ketoacidosis), and poor growth. Surprisingly, post-prandial glucose spikes to 15 mmol/L after breakfast. Between meals, glucose falls precipitously. Liver glycogen content on biopsy is markedly reduced. GYS2 activity absent.',
    params: { glucose_mM: 2.5, oxygen_pct: 100, insulin_fold: 0.3, glucagon_fold: 3.0, energy_demand: 1.0, nutritional_state: 'starved', pathway: 'glycogenesis' },
    keyPoints: [
      'GYS2 (hepatic Glycogen Synthase) synthesises glycogen; deficiency → liver cannot store post-prandial glucose as glycogen',
      'Paradoxical presentation: Fasting hypoglycaemia (empty stores) + Post-prandial hyperglycaemia (glucose cannot be stored)',
      'Unlike classical GSDs: liver glycogen content is LOW (not high). Hepatomegaly is absent.',
      'Ketosis (not acidosis) during fasting: fatty acid mobilisation compensates for glucose deficit',
      'Management: frequent small meals, uncooked cornstarch at night; prognosis is generally good',
    ],
    labs: { glucose_fasting: '↓↓', glucose_post_prandial: '↑↑ (>10 mM)', ketones: '↑ (fasting)', lactate: 'normal', liver_glycogen: '↓↓ (biopsy)' },
  },
  {
    id: 'gsd9',
    name: 'GSD Type IX (Phosphorylase Kinase Deficiency)',
    subtitle: 'GSD IX — Most Common GSD; X-linked Hepatic Form',
    icon: '🔗',
    color: '#a3e635',
    category: 'Glycogen Storage',
    icd: 'E74.09',
    scenario: 'A 3-year-old boy has hepatomegaly, mildly elevated transaminases, and mild fasting hypoglycaemia. Unlike Von Gierke, lactate and uric acid are normal. By age 12, the hepatomegaly resolves spontaneously. Phosphorylase kinase activity in white cells is undetectable. His maternal uncle had the same childhood condition.',
    params: { glucose_mM: 3.5, oxygen_pct: 100, insulin_fold: 0.8, glucagon_fold: 2.5, energy_demand: 1.0, nutritional_state: 'fasted', pathway: 'glycogenolysis' },
    keyPoints: [
      'Phosphorylase kinase converts GP-b (inactive) → GP-a (active phosphorylated form); deficiency slows glycogenolysis',
      'X-linked PHKA2 mutations (liver alpha-subunit) = most common form; maternal transmission, males affected',
      'Mild course: glycogen accumulates in liver → hepatomegaly in childhood, generally resolves at puberty',
      'Differentiated from GSD Ia by normal lactate (GNG intact) and normal uric acid',
      'Glucagon test: liver glycogen not fully mobilisable → blunted glucose response but NOT absent (unlike GP deficiency)',
    ],
    labs: { glucose: '↓ mild', lactate: 'normal', uric_acid: 'normal', PhK_WBC: 'absent', AST_ALT: '↑ mild' },
  },

  // ── Fructose Metabolism Disorders ───────────────────────────────
  {
    id: 'essential_fructosuria',
    name: 'Essential Fructosuria',
    subtitle: 'Fructokinase (KHK) Deficiency — Benign Disorder',
    icon: '🍹',
    color: '#fde68a',
    category: 'Fructose Metabolism',
    icd: 'E74.11',
    scenario: 'A routine urine dipstick in a healthy 25-year-old shows positive reducing substances but is glucose-oxidase negative. The patient denies any symptoms. Dietary history reveals high fruit and fruit juice intake. Repeat testing on a fructose-free diet clears the urinuria. No treatment is required.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'fructose_metabolism' },
    keyPoints: [
      'Fructokinase (KHK) phosphorylates fructose → Fructose-1-P; deficiency → fructose cannot be trapped in cells',
      'Fructose accumulates in blood → excreted in urine (fructosuria). No metabolic consequences — fructose has no obligate pathway.',
      'Urine dipstick: reducing substance positive (fructose reduces copper reagent) but glucose-oxidase NEGATIVE (confirms it is not glucose)',
      'Completely asymptomatic and benign — no treatment required. Contrast with HFI (Aldolase B deficiency) which is life-threatening.',
      'Autosomal recessive inheritance; prevalence ~1:130,000. Often detected incidentally.',
    ],
    labs: { urine_reducing: '+', urine_glucose_oxidase: '−', serum_fructose: '↑ post-prandial', fructokinase_activity: 'absent/low' },
  },

  // ── Galactose Metabolism Disorders ──────────────────────────────
  {
    id: 'galactokinase_def',
    name: 'Galactokinase Deficiency',
    subtitle: 'GALK1 Deficiency — Cataracts Without Liver Disease',
    icon: '👁️',
    color: '#67e8f9',
    category: 'Galactose Metabolism',
    icd: 'E74.29',
    scenario: 'A 3-week-old breastfed neonate develops bilateral nuclear cataracts on newborn examination. Neonatal sepsis, jaundice, and hepatomegaly are all ABSENT. Urine shows reducing substances (galactose), confirmed on galactose quantitation. GALK1 enzyme activity is absent. A galactose-free diet leads to arrest of cataract progression.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'galactose_metabolism' },
    keyPoints: [
      'Galactokinase phosphorylates galactose → Gal-1-P; deficiency → galactose cannot enter the Leloir pathway',
      'Galactose → galactitol (via aldose reductase) → accumulates in lens → osmotic swelling → nuclear cataracts',
      'KEY DISTINCTION from classic galactosaemia: GALK deficiency produces NO Gal-1-P → no liver disease, no sepsis risk, no neurological damage',
      'Cataracts form rapidly in the newborn period (nuclear cataracts, unlike age-related cortical cataracts)',
      'Treatment: galactose-free diet (eliminate dairy). If started early, cataracts may regress; late diagnosis requires surgical lens removal.',
      'Differential: Galactose-reducing substances in urine in any neonate on dairy should trigger URGENT metabolic screen.',
    ],
    labs: { urine_galactose: '↑↑', GALK_activity: 'absent', ophthalmology: 'bilateral nuclear cataracts', LFTs: 'normal', sepsis: 'absent' },
  },
  {
    id: 'gale_deficiency',
    name: 'UDP-Galactose Epimerase Deficiency',
    subtitle: 'GALE Deficiency — Mild to Severe Spectrum',
    icon: '⚖️',
    color: '#5eead4',
    category: 'Galactose Metabolism',
    icd: 'E74.29',
    scenario: 'An infant found on newborn galactosaemia screen to have elevated total galactose is referred. Classic galactosaemia (GALT) has been excluded. GALE activity is absent in red blood cells. In this mild form, systemic tissues are unaffected (erythrocyte GALE deficiency only). A second patient from a consanguineous family has complete GALE absence — presents with fulminant neonatal galactosaemia despite a galactose-free diet.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'galactose_metabolism' },
    keyPoints: [
      'GALE converts UDP-Galactose ⇌ UDP-Glucose (bidirectional). NAD+ acts as catalytic cofactor (non-consumed).',
      'Unlike GALK and GALT deficiencies: GALE is ALSO required endogenously — even on galactose-free diet, cells must synthesise UDP-galactose for glycoproteins and glycolipids.',
      'MILD form (RBC-specific): benign — systemic GALE compensates; monitoring only, no dietary restriction.',
      'SEVERE form (generalised): paradoxically presents like classic galactosaemia even without dietary galactose — Gal-1-P and galactitol accumulate from internal synthesis.',
      'Complete GALE deficiency requires controlled galactose supplementation (UDP-galactose cannot be synthesised de novo) — galactose-free diet is CONTRAINDICATED in severe GALE deficiency.',
    ],
    labs: { total_galactose: '↑', GALT_activity: 'normal', GALE_activity: 'absent', Gal1P: '↑ (severe form only)', UDP_galactose: '↓ (severe)' },
  },

  // ── Amino Acid Disorders ─────────────────────────────────────────
  {
    id: 'pku',
    name: 'Phenylketonuria (PKU)',
    subtitle: 'Phenylalanine Hydroxylase (PAH) Deficiency',
    icon: '🧠',
    color: '#a78bfa',
    category: 'Amino Acid',
    icd: 'E70.1',
    scenario: 'Newborn screening (day 3): blood phenylalanine = 1800 µmol/L (ref < 120). The infant appears normal at birth. Without treatment, progressive intellectual disability, microcephaly, fair skin/hair (tyrosine deficiency → reduced melanin), and musty/mousy urine odour develop by 6 months.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'phenylalanine_tyrosine' },
    keyPoints: [
      'PAH converts Phe → Tyr using BH4. Deficiency → Phe accumulates → competitive inhibition of other aromatic AA transporters at BBB → neurotransmitter depletion',
      'Classic PKU: Phe > 1200 µmol/L. Mild HPA (hyperphenylalaninaemia): 120–600 µmol/L; may not need treatment',
      'BH4-responsive PKU (30% of patients): sapropterin (synthetic BH4) reduces Phe by acting as chaperone to stabilise mutant PAH protein',
      'Maternal PKU: if untreated pregnancy → Phe teratogenic to foetus (microcephaly, CHD, IUGR) even if foetus is not PKU',
      'Pegvaliase (PEGylated phenylalanine ammonia lyase, a bacterial enzyme) is a newer treatment for adults',
    ],
    labs: { phe: '↑↑↑ (>1200 µmol/L)', tyr: '↓', phe_tyr_ratio: '↑↑', urine_phenylketones: '↑', bh4_loading: 'responsive or not' },
  },
  {
    id: 'msud',
    name: 'Maple Syrup Urine Disease (MSUD)',
    subtitle: 'BCKDH Complex Deficiency',
    icon: '🍁',
    color: '#fb923c',
    category: 'Amino Acid',
    icd: 'E71.0',
    scenario: 'A 5-day-old neonate presents with poor feeding, encephalopathy, and a distinctive sweet/maple syrup odour of urine and earwax. Plasma amino acids show markedly elevated leucine (2400 µmol/L), isoleucine, and valine. Alloisoleucine is present (pathognomonic). Urine organic acids show branched-chain ketoacids.',
    params: { glucose_mM: 4.5, oxygen_pct: 100, insulin_fold: 0.8, glucagon_fold: 2.0, energy_demand: 2.0, nutritional_state: 'fasted', pathway: 'branched_chain_aa' },
    keyPoints: [
      'BCKDH complex (E1α/E1β/E2/E3) oxidatively decarboxylates branched-chain keto acids — same E3 as PDC and α-KGDH',
      'Leucine is primarily neurotoxic (inhibits brain PDC + causes cerebral oedema); target leucine < 300 µmol/L urgently',
      'Treatment: BCAA-restricted formula + emergency IV glucose/insulin to drive anabolism and lower BCKAs',
      'Thiamine-responsive MSUD (rare): high-dose thiamine (TPP cofactor) may partially restore BCKDH activity',
      'Alloisoleucine is pathognomonic — formed non-enzymatically from allo-isoleucine accumulation; not present in normal plasma',
      'Liver transplant is curative (BCKDH expressed in liver); widely used in classic MSUD',
    ],
    labs: { leucine: '↑↑↑', isoleucine: '↑↑↑', valine: '↑↑', alloisoleucine: '↑ (pathognomonic)', DNPH_urine: '↑ (ketoacids)', BCKAs_urine: '↑↑↑' },
  },
  {
    id: 'otc_deficiency',
    name: 'OTC Deficiency',
    subtitle: 'Ornithine Transcarbamylase Deficiency — X-linked UCD',
    icon: '🔱',
    color: '#f472b6',
    category: 'Amino Acid',
    icd: 'E72.4',
    scenario: 'A 3-day-old male neonate becomes increasingly lethargic, develops vomiting, and seizures. Ammonia = 850 µmol/L (ref < 50). Blood gas: pH 7.52, pCO₂ 22 (respiratory alkalosis — earliest sign of hyperammonaemia). Urine orotic acid is massively elevated. Plasma amino acids show elevated glutamine, low citrulline.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.5, energy_demand: 1.5, nutritional_state: 'fed', pathway: 'urea_cycle' },
    keyPoints: [
      'OTC (X-linked): catalyses carbamoyl-P + ornithine → citrulline in mitochondria. Deficiency → CP leaks → orotic acid (pyrimidine branch)',
      'Orotic aciduria distinguishes OTC deficiency from CPS-I/NAGS deficiency (both give high NH₃, low citrulline, NO orotic acid)',
      'Respiratory alkalosis is the first sign: NH₃ directly stimulates respiratory centre → hyperventilation → resp alkalosis',
      'Emergency: stop protein, IV glucose 10% (anti-catabolic), sodium benzoate + phenylbutyrate IV (scavengers), consider haemodialysis if NH₃ > 500',
      'Long-term: liver transplant is curative. Gene therapy in trials (OTC-AAVX vectors)',
      'Heterozygous females: protein aversion, migraine, episodic encephalopathy (triggered by illness/stress)',
    ],
    labs: { ammonia: '↑↑↑ (>500 µmol/L)', citrulline: '↓', orotic_acid: '↑↑↑', glutamine: '↑↑', pH: '↑ (resp alkalosis)', arginine: '↓' },
  },
  {
    id: 'tyrosinaemia1',
    name: 'Tyrosinaemia Type I',
    subtitle: 'Fumarylacetoacetase (FAH) Deficiency',
    icon: '🫀',
    color: '#4ade80',
    category: 'Amino Acid',
    icd: 'E70.2',
    scenario: 'A 3-month-old presents with failure to thrive, coagulopathy (INR 4.2), and hepatomegaly. Serum AFP is 250,000 U/mL (massively elevated). Urine succinylacetone detected on metabolic screen. The family is of French-Canadian origin. NTBC is started immediately.',
    params: { glucose_mM: 4.5, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.5, energy_demand: 1.5, nutritional_state: 'fed', pathway: 'phenylalanine_tyrosine' },
    keyPoints: [
      'FAH deficiency → succinylacetone + succinylacetoacetate accumulate → directly toxic to liver and kidney tubules',
      'Succinylacetone inhibits ALAD (porphobilinogen synthase) → 5-ALA accumulates → secondary acute intermittent porphyria episodes (neurovisceral crises)',
      'Massively elevated AFP indicates hepatocyte regeneration/injury and hepatocellular carcinoma risk (untreated: 40% lifetime HCC risk)',
      'NTBC (nitisinone): inhibits HPPD (2 steps above FAH) → prevents succinylacetone synthesis. Dramatically improves survival. Must combine with Phe/Tyr restricted diet',
      'Liver transplant formerly the only option; NTBC now first-line but does not eliminate HCC risk — surveillance essential',
      'High incidence in French-Canadians (Saguenay-Lac-Saint-Jean region, Quebec) due to founder effect',
    ],
    labs: { succinylacetone: '↑↑↑ (diagnostic)', AFP: '↑↑↑', INR: '↑↑', AST_ALT: '↑↑↑', ALA_urine: '↑ (porphyria)', tyrosine: '↑↑' },
  },

  // ── Lipid Disorders ──────────────────────────────────────────────
  {
    id: 'mcad_deficiency',
    name: 'MCAD Deficiency',
    subtitle: 'Medium-Chain Acyl-CoA Dehydrogenase Deficiency',
    icon: '⚡',
    color: '#facc15',
    category: 'Lipid',
    icd: 'E71.311',
    scenario: 'A previously well 18-month-old is brought to A&E after 16 hours of fasting (viral illness, poor feeding). He is unconscious with blood glucose of 1.1 mmol/L. Ketones are absent (urine dipstick negative). Acylcarnitine profile: massively elevated C8-carnitine (octanoylcarnitine). He responds to IV 10% dextrose.',
    params: { glucose_mM: 1.1, oxygen_pct: 100, insulin_fold: 0.2, glucagon_fold: 4.0, energy_demand: 2.0, nutritional_state: 'starved', pathway: 'fatty_acid_oxidation' },
    keyPoints: [
      'MCAD catalyses the first step of β-oxidation for medium-chain (C8–C12) fatty acids. Defect → cannot generate acetyl-CoA from FAs → no ketones + hypoglycaemia',
      'Hypoketotic hypoglycaemia is the hallmark: glucose is consumed, fat cannot be oxidised, ketones cannot be made',
      'C8 (octanoylcarnitine) and C8:1 are elevated on newborn MS/MS screen — now universally screened in developed countries',
      'Most common FAO disorder: ~1:10,000 in Northern Europeans. Single predominant mutation: c.985A>G (K304E, ~80% of alleles)',
      'Triggers: any fasting (illness, surgery, weaning) → do NOT fast longer than age-appropriate limits',
      'Prognosis: excellent with avoidance of fasting + sick day plans. Emergency: IV 10% dextrose at high rate',
    ],
    labs: { glucose: '↓↓ (<2 mmol/L)', ketones: '↓↓ (absent)', C8_carnitine: '↑↑↑', C8_1: '↑↑', NH3: '↑ (secondary)', LFTs: '↑ (metabolic crisis)' },
  },
  {
    id: 'dka',
    name: 'Diabetic Ketoacidosis (DKA)',
    subtitle: 'Type 1 DM — Uncontrolled Ketogenesis',
    icon: '🩺',
    color: '#f97316',
    category: 'Lipid',
    icd: 'E10.10',
    scenario: 'A 19-year-old type 1 diabetic presents with 2 days of vomiting, polyuria, and abdominal pain after missing insulin doses. pH 7.18, bicarb 9, glucose 32 mmol/L, serum ketones 7.2 mmol/L (ref < 0.6), anion gap 28. Physio: Kussmaul breathing.',
    params: { glucose_mM: 22.0, oxygen_pct: 100, insulin_fold: 0.05, glucagon_fold: 4.0, energy_demand: 1.5, nutritional_state: 'starved', pathway: 'ketogenesis' },
    keyPoints: [
      'No insulin → glucagon unopposed → lipolysis → massive FFA delivery to liver → HMGCS2 uninhibited (malonyl-CoA low, CPT-I active) → ketone production overwhelms buffering',
      'Anion gap metabolic acidosis: AG = Na − (Cl + HCO₃). In DKA, ketoacids (AcAc⁻, β-OHB⁻) are the unmeasured anions',
      'Kussmaul breathing: deep, laboured breathing to blow off CO₂ and compensate for metabolic acidosis (respiratory compensation)',
      'Fluid first (0.9% NaCl 1L/hr initially), then insulin infusion 0.1 units/kg/hr. Potassium — MUST be given before or with insulin (insulin drives K⁺ into cells; hypokalaemia → cardiac arrhythmia)',
      'DKA is resolved when: AG normalised, blood ketones < 0.6, pH > 7.3, and pt can eat/drink — not just when glucose normalises',
      'Cerebral oedema (rare, ~1% of paediatric DKA): risk increases with rapid fluid correction, young age, new-onset DM. Treat with IV mannitol',
    ],
    labs: { glucose: '↑↑↑ (>11 mM)', beta_OHB: '↑↑↑ (>3 mM)', pH: '↓↓ (<7.3)', bicarb: '↓↓ (<15)', anion_gap: '↑↑ (>16)', K: '↑ initially then ↓ with insulin' },
  },
  {
    id: 'familial_hypercholesterolaemia',
    name: 'Familial Hypercholesterolaemia (FH)',
    subtitle: 'LDLR Loss-of-Function — Premature CAD',
    icon: '❤️',
    color: '#84cc16',
    category: 'Lipid',
    icd: 'E78.01',
    scenario: 'A 42-year-old man presents with his first NSTEMI. Total cholesterol: 9.2 mmol/L, LDL-C: 7.8 mmol/L (untreated). Achilles tendon xanthomas and bilateral corneal arcus are noted on examination. His 16-year-old daughter has LDL-C of 6.1 mmol/L. Genetic testing confirms LDLR exon 4 deletion (pathogenic).',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'lipoprotein_metabolism' },
    keyPoints: [
      'LDLR mutations (>2000 variants) → impaired LDL clearance → lifelong LDL elevation from birth → accelerated atherosclerosis',
      'Heterozygous FH: ~1:250 prevalence (most common monogenic disorder). LDL 5–10 mmol/L. 50% risk MI by 50 (men), 60 (women) untreated',
      'Clinical signs: tendon xanthomas (Achilles, extensor tendons), corneal arcus < 45 years, xanthelasma',
      'Dutch Lipid Clinic Network (DLCN) or Simon Broome criteria for clinical diagnosis. Confirm with genetic testing',
      'Treatment: high-intensity statin + ezetimibe (combination achieves additional 15–20% LDL lowering). Add PCSK9 inhibitor (evolocumab/alirocumab) if targets not met (> 50% LDL reduction)',
      'Cascade screening: all first-degree relatives must be tested (1:2 chance of inheriting if parent affected)',
    ],
    labs: { LDL: '↑↑↑ (>5 mmol/L)', total_chol: '↑↑↑', TGs: 'normal', HDL: 'normal', LFTs: 'normal (before statin)', LDLR_gene: 'pathogenic variant' },
  },

  // ── Nucleotide Disorders ─────────────────────────────────────────
  {
    id: 'lesch_nyhan',
    name: 'Lesch-Nyhan Syndrome',
    subtitle: 'HGPRT Deficiency — X-linked Purine Disorder',
    icon: '🧬',
    color: '#67e8f9',
    category: 'Nucleotide',
    icd: 'E79.1',
    scenario: 'An 18-month-old boy is referred for developmental regression, progressive choreoathetosis, and unexplained self-biting of fingers and lips, resulting in significant tissue loss. Serum urate: 820 µmol/L. Orange crystal deposits seen in nappy at age 3 months (sodium urate). His maternal cousin had the same condition.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'purine_salvage' },
    keyPoints: [
      'HGPRT salvages hypoxanthine + guanine → IMP/GMP. Deficiency → no salvage → PRPP accumulates → drives de novo purine synthesis → massive urate overproduction',
      'Neurological features: dystonia, choreoathetosis, intellectual disability, and pathognomonic self-mutilation (not pain insensitivity — patients are distressed by their own biting)',
      'Gout and urate nephropathy: start allopurinol (XO inhibitor) early to prevent renal damage and tophi',
      'Allopurinol does NOT improve neurological features — neurological damage may be related to dopaminergic neuron dysfunction (HGPRT highly expressed in basal ganglia)',
      'X-linked: hemizygous males affected (complete); carrier females unaffected or partial (only if extreme X-inactivation)',
      'Diagnosis: HGPRT enzyme assay in erythrocytes; molecular confirmation of HPRT1 mutation',
    ],
    labs: { urate: '↑↑↑ (>700 µmol/L)', HGPRT_activity: 'absent', hypoxanthine: '↑', xanthine: '↑', creatinine: '↑ (if nephropathy)', orange_crystals_nappy: 'neonatal clue' },
  },
  {
    id: 'ada_scid',
    name: 'ADA-SCID',
    subtitle: 'Adenosine Deaminase Deficiency — First Gene Therapy Disease',
    icon: '🛡️',
    color: '#818cf8',
    category: 'Nucleotide',
    icd: 'D81.3',
    scenario: 'A 4-month-old presents with recurrent Pneumocystis jirovecii pneumonia, oral candidiasis, and failure to thrive. Lymphocyte count: 0.1 × 10⁹/L (severely lymphopaenic). Absent T, B, and NK cells on immunophenotyping. Adenosine deaminase activity is undetectable. Maternal HLA-matched bone marrow transplant is planned.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'purine_salvage' },
    keyPoints: [
      'ADA converts adenosine → inosine and deoxyadenosine → deoxyinosine. Deficiency → dATP accumulates in lymphocytes → RNR inhibition → no dNTP → lymphocyte death',
      'All lymphocyte lines affected (T, B, NK) — SCID presentation in infancy, susceptible to all pathogens including Pneumocystis, CMV, BCG dissemination',
      'First gene therapy disease (1990, Blaese/Anderson): modified retroviral vector expressing ADA transfected into patient T cells. Now superseded by haematopoietic stem cell gene therapy',
      'Enzyme replacement: pegademase bovine (PEG-ADA) — weekly IM injections of PEGylated bovine ADA. Effective but inferior to gene therapy/BMT',
      'Strimvelis (EMA-approved gene therapy): ex vivo retroviral vector correction of autologous HSCs. Curative in >90%',
      'Newborn screening for ADA-SCID now available via TRECs (T-cell receptor excision circles) on dried blood spot',
    ],
    labs: { ADA_activity: 'absent', lymphocytes: '↓↓↓ (<0.5)', dATP_RBCs: '↑↑↑', TRECs: 'absent', immunoglobulins: '↓ (maternal decline by 4mo)', CD3_CD4_CD8: 'absent' },
  },
  {
    id: 'gout_tls',
    name: 'Tumour Lysis Syndrome (TLS)',
    subtitle: 'Acute Urate Nephropathy — Xanthine Oxidase Crisis',
    icon: '💊',
    color: '#f43f5e',
    category: 'Nucleotide',
    icd: 'E79.0',
    scenario: 'A 35-year-old with newly diagnosed Burkitt lymphoma (LDH 3400 U/L) receives first-cycle cyclophosphamide/doxorubicin. 12 hours later: urate 920 µmol/L, potassium 6.8 mmol/L, phosphate 2.9 mmol/L, creatinine rising. ECG shows peaked T-waves. Rasburicase is given urgently.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 2.0, nutritional_state: 'fed', pathway: 'nucleotide_degradation' },
    keyPoints: [
      'TLS: massive tumour cell lysis → nuclear contents (purines, pyrimidines, K, PO₄) released → overwhelms normal disposal mechanisms',
      'Hyperuricaemia: XO converts hypoxanthine + xanthine → urate → precipitates in renal tubules at low pH → obstructive nephropathy',
      'The "4 Hs": Hyperuricaemia, Hyperkalaemia (cardiac arrhythmia), Hyperphosphataemia (→ calcium-phosphate precipitation → hypocalcaemia → tetany), and urate nephropathy (↑ Creatinine)',
      'Rasburicase (recombinant uricase): converts urate → allantoin (5–10× more soluble). Dramatically reduces urate within hours. Contraindicated in G6PD deficiency (H₂O₂ produced → haemolysis)',
      'Allopurinol prevents further urate synthesis but does NOT reduce already-elevated urate levels (give before chemotherapy, not during crisis)',
      'Aggressive IV hydration (3 L/m²/day) and urine alkalinisation to prevent urate crystal precipitation',
    ],
    labs: { urate: '↑↑↑ (>476 µmol/L)', potassium: '↑↑ (>6.0)', phosphate: '↑↑ (>2.1)', calcium: '↓', creatinine: '↑↑', LDH: '↑↑↑' },
  },

  // ── Amino Acid Disorders ──────────────────────────────────────────
  {
    id: 'pku',
    name: 'Phenylketonuria (PKU)',
    subtitle: 'PAH Deficiency — Hyperphenylalaninaemia',
    icon: '🧠',
    color: '#a78bfa',
    category: 'Amino Acid',
    icd: 'E70.0',
    scenario: 'Newborn screening detects phenylalanine 1400 µmol/L (normal <120) at day 5 of life. Sapropterin loading test shows 15% reduction. PAH mutation confirmed. Dietary management + BH4 supplementation initiated.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'phenylalanine_tyrosine' },
    keyPoints: [
      'PAH converts Phe → Tyr using tetrahydrobiopterin (BH4) cofactor. Deficiency → Phe accumulates → intellectual disability if untreated',
      'Elevated Phe inhibits LNAA transport at BBB → reduced brain Tyr/Trp → neurotransmitter deficit',
      'Treatment: low-Phe diet + Tyr supplementation (conditionally essential). Sapropterin (BH4) works in ~30% of PAH variants',
      'Pegvaliase (phenylalanine ammonia lyase): converts Phe → trans-cinnamic acid — non-dietary option for adults',
    ],
    labs: { phenylalanine: '↑↑↑ (>120 µmol/L)', tyrosine: '↓', Phe_Tyr_ratio: '↑↑', BH4_responsive: '~30%' },
  },
  {
    id: 'msud',
    name: 'Maple Syrup Urine Disease (MSUD)',
    subtitle: 'BCKDH Complex Deficiency — BCAA Toxicity',
    icon: '🍁',
    color: '#f59e0b',
    category: 'Amino Acid',
    icd: 'E71.0',
    scenario: 'A 4-day-old neonate deteriorates rapidly with hypertonia, hypotonia, poor feeding, and distinctive maple syrup odour. Plasma leucine 1280 µmol/L; alloisoleucine present (pathognomonic). BCKDH enzyme activity: <2% of normal.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.5, energy_demand: 1.5, nutritional_state: 'fed', pathway: 'branched_chain_aa' },
    keyPoints: [
      'BCKDH complex is irreversible; deficiency → BCAAs + toxic keto acids accumulate (α-KIC, α-KIV, α-KMV)',
      'Leucine is primary neurotoxin: inhibits LNAA transport → depletes brain Tyr/Trp → impairs myelination + cerebral oedema',
      'Maple syrup odour from sotolone (from α-KIV) — highly characteristic',
      'Acute: high-carbohydrate IV to suppress catabolism + protein restriction; dialysis if severe. Long-term: BCAA-restricted diet; liver transplant corrects hepatic defect',
    ],
    labs: { leucine: '↑↑↑', alloisoleucine: '+ (pathognomonic)', keto_acids: '+', pH: '↓' },
  },
  {
    id: 'otc_deficiency',
    name: 'OTC Deficiency',
    subtitle: 'X-Linked Ornithine Transcarbamylase Deficiency',
    icon: '⚠️',
    color: '#ef4444',
    category: 'Amino Acid',
    icd: 'E72.4',
    scenario: 'A 6-week-old boy: vomiting, lethargy, seizures. Ammonia: 840 µmol/L, respiratory alkalosis. Citrulline: low; urine orotic acid 850 µmol/mmol Cr (normal <5). OTC hemizygous mutation confirmed.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 2.0, energy_demand: 1.5, nutritional_state: 'fed', pathway: 'urea_cycle' },
    keyPoints: [
      'OTC catalyses: Ornithine + Carbamoyl-P → Citrulline (mitochondria). Deficiency → carbamoyl-P spills to cytoplasm',
      'Excess cytoplasmic carbamoyl-P → pyrimidine synthesis → orotic aciduria (distinguishes OTC from CPS-I deficiency which has no orotic acid)',
      'X-linked: hemizygous males severely affected. Carrier females range from asymptomatic to late-onset neuropsychiatric symptoms',
      'Acute: protein restriction + Na-benzoate/phenylacetate + dialysis if NH₃ >500 µmol/L. Long-term: liver transplant is curative',
    ],
    labs: { ammonia: '↑↑↑', orotic_acid: '↑↑↑', citrulline: '↓↓', arginine: '↓', pH: '↑ (resp alkalosis)' },
  },
  {
    id: 'homocystinuria',
    name: 'Classical Homocystinuria',
    subtitle: 'CBS Deficiency — Homocysteine & Thrombosis',
    icon: '🩸',
    color: '#f87171',
    category: 'Amino Acid',
    icd: 'E72.11',
    scenario: 'A 12-year-old with ectopia lentis (downward lens dislocation), Marfanoid habitus, intellectual disability, and first DVT. Total homocysteine: 185 µmol/L. Methionine: 850 µmol/L. CBS enzyme: <1% activity. B6-responsive variant.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'amino_acid_synthesis' },
    keyPoints: [
      'CBS converts homocysteine + serine → cystathionine → cysteine. Deficiency → homocysteine + methionine accumulate',
      'Homocysteine damages vascular endothelium → promotes platelet aggregation → thromboembolism (DVT, MI, stroke) even in teenagers',
      'Ectopia lentis (downward displacement) — contrast with Marfan syndrome (upward). Fibrillin cross-linking disrupted by homocysteine',
      'B6-responsive (50%): high-dose pyridoxine + folate + B12 reduce homocysteine. Betaine provides alternative remethylation pathway',
    ],
    labs: { homocysteine: '↑↑↑ (>100)', methionine: '↑↑', cysteine: '↓', thrombosis_risk: '↑↑↑' },
  },
  {
    id: 'alkaptonuria',
    name: 'Alkaptonuria',
    subtitle: 'HGD Deficiency — Ochronosis & Premature Arthritis',
    icon: '🟫',
    color: '#92400e',
    category: 'Amino Acid',
    icd: 'E70.29',
    scenario: 'A 42-year-old with severe OA of spine and large joints. Dark urine turns black on standing. Bluish-grey ear cartilage (ochronosis). HGD gene: homozygous p.Gly161Arg. Nitisinone (NTBC) trial discussed.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'phenylalanine_tyrosine' },
    keyPoints: [
      'HGD (homogentisate-1,2-dioxygenase) deficiency → HGA accumulates → polymerises to bluish-black alkapton pigment in connective tissues',
      'Ochronosis: pigment deposits in cartilage, tendons, sclera → makes cartilage brittle → early severe OA of spine/hips/knees',
      'Urine turns dark (black) on standing/alkalinisation. Dark nappies in infancy is an early clinical clue',
      'Nitisinone (NTBC): inhibits 4-HPPD upstream of HGA → dramatically reduces HGA levels. Treatment of choice',
    ],
    labs: { HGA_urine: '↑↑↑', urine_colour: 'darkens on standing', joint_Xray: 'dense OA + spinal calcification' },
  },
  {
    id: 'tyrosinaemia_1',
    name: 'Tyrosinaemia Type I (HT1)',
    subtitle: 'FAH Deficiency — Succinylacetone & Hepatocellular Damage',
    icon: '🔴',
    color: '#dc2626',
    category: 'Amino Acid',
    icd: 'E70.21',
    scenario: 'A 3-month-old: jaundice, coagulopathy (INR 4.2), hepatomegaly. Succinylacetone (SA): 380 µmol/L. AFP: 82,000 kU/L. FAH enzyme absent. NBS was SA-positive at birth — parents not followed up. Emergency NTBC + liver transplant listing.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 2.0, energy_demand: 1.5, nutritional_state: 'fed', pathway: 'phenylalanine_tyrosine' },
    keyPoints: [
      'FAH is the final step of Tyr catabolism; deficiency → FAA + succinylacetone (SA) accumulate',
      'SA inhibits ALA dehydratase → secondary porphyria crises + renal Fanconi syndrome',
      'SA alkylates hepatic DNA → hepatocellular carcinoma risk >30× by age 5 without NTBC treatment',
      'NTBC (nitisinone): inhibits 4-HPPD upstream → prevents SA production → reverses hepatic/renal damage dramatically',
      'NBS with SA at day 5 followed by immediate NTBC + restricted diet prevents ALL complications',
    ],
    labs: { succinylacetone: '↑↑↑', AFP: '↑↑↑', INR: '↑↑↑', tyrosine: '↑↑' },
  },

  // ── Additional Lipid Disorders ────────────────────────────────────
  {
    id: 'fh',
    name: 'Familial Hypercholesterolaemia (FH)',
    subtitle: 'LDLR Deficiency — Extreme LDL Elevation',
    icon: '🫀',
    color: '#f97316',
    category: 'Lipid',
    icd: 'E78.01',
    scenario: 'A 38-year-old with premature corneal arcus, bilateral Achilles tendon xanthomata, and a first MI. LDL: 7.8 mmol/L. Father had MI at 42. LDLR gene: pathogenic p.Cys352Arg (heterozygous FH).',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'cholesterol_synthesis' },
    keyPoints: [
      'LDLR deficiency → LDL cannot be cleared → accumulates in arterial walls → foam cells → atherosclerosis, tendon xanthomata',
      'Heterozygous FH (1:250 prevalence): LDL 5–10 mmol/L; premature CVD in 40–50s. Homozygous FH (1:300,000): CVD in childhood',
      'Statins: ↓HMGCR → ↓intracellular cholesterol → SREBP-2 activation → ↑LDLR expression (2–3× in hetFH) → 40–60% LDL reduction',
      'PCSK9 inhibitors (evolocumab/alirocumab): prevent PCSK9-LDLR degradation → additional 50–70% LDL reduction on top of statin',
    ],
    labs: { LDL: '↑↑↑ (>5.0 mmol/L)', total_cholesterol: '↑↑↑', Trig: 'normal', xanthomata: '+ tendon' },
  },
  {
    id: 'mcad',
    name: 'MCAD Deficiency',
    subtitle: 'Medium-Chain Acyl-CoA Dehydrogenase Deficiency — Hypoketotic Hypoglycaemia',
    icon: '⚡',
    color: '#facc15',
    category: 'Lipid',
    icd: 'E71.31',
    scenario: 'An 18-month-old comatose after 24-hour gastroenteritis. Glucose: 1.4 mmol/L, total ketones: 0.3 mmol/L (inappropriately low). Acylcarnitine profile: C8 ↑↑↑. ACADM gene: homozygous p.Lys304Glu. NBS positive at birth — not followed up.',
    params: { glucose_mM: 1.8, oxygen_pct: 100, insulin_fold: 0.3, glucagon_fold: 4.0, energy_demand: 2.0, nutritional_state: 'starved', pathway: 'fatty_acid_oxidation' },
    keyPoints: [
      'MCAD (medium-chain acyl-CoA dehydrogenase) β-oxidises C6–C12 fatty acids; deficiency blocks FAO at this stage',
      'During fasting/illness: glycogen depletes → FAO needed → MCAD block → no acetyl-CoA → no ketones → hypoketotic hypoglycaemia (the hallmark)',
      'C8/C10 acylcarnitines are toxic and inhibit gluconeogenesis + OXPHOS, compounding the hypoglycaemia',
      'Most common FAO disorder (1:8,000–12,000 Northern Europeans). Was a leading cause of SIDS before universal NBS. Excellent prognosis if diagnosed and managed early',
    ],
    labs: { glucose: '↓↓', ketones: 'inappropriately ↓', C8_acylcarnitine: '↑↑↑', C10: '↑↑' },
  },
  {
    id: 'refsum',
    name: 'Refsum Disease',
    subtitle: 'PHYH Deficiency — Phytanic Acid Accumulation',
    icon: '👁️',
    color: '#818cf8',
    category: 'Lipid',
    icd: 'G60.1',
    scenario: 'A 28-year-old with progressive ataxia since age 20, peripheral neuropathy, retinitis pigmentosa (night blindness), anosmia, sensorineural deafness. Phytanic acid: 680 µmol/L (normal <30). PHYH gene: homozygous p.Arg275Trp.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'fatty_acid_oxidation' },
    keyPoints: [
      'Phytanic acid (from dietary chlorophyll/dairy) undergoes α-oxidation (PHYH in peroxisomes) before β-oxidation. PHYH deficiency → phytanic acid accumulates',
      'Branched methyl group at Cα blocks direct β-oxidation — requires α-oxidation first to produce pristanic acid',
      'Classic tetrad: retinitis pigmentosa + cerebellar ataxia + peripheral polyneuropathy + elevated CSF protein without pleocytosis',
      'Treatment: eliminate dietary phytol sources (restrict ruminant fat, dairy, chlorophyll-rich vegetables). Plasmapheresis for acute crises',
    ],
    labs: { phytanic_acid: '↑↑↑ (>30 µmol/L)', CSF_protein: '↑↑', NCS: 'demyelinating + axonal' },
  },
  {
    id: 'smith_lemli_opitz',
    name: 'Smith-Lemli-Opitz Syndrome',
    subtitle: 'DHCR7 Deficiency — Last Step of Cholesterol Synthesis',
    icon: '🧫',
    color: '#84cc16',
    category: 'Lipid',
    icd: 'Q87.19',
    scenario: 'Male neonate with 2–3 toe syndactyly, microcephaly, cleft palate, ambiguous genitalia (46,XY), ASD, failure to thrive. Cholesterol: 0.8 mmol/L (♂). 7-DHC: 380 µmol/L. DHCR7: compound heterozygous loss-of-function.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'cholesterol_synthesis' },
    keyPoints: [
      'DHCR7 (7-dehydrocholesterol reductase) is the final step: 7-DHC → cholesterol. Deficiency → low cholesterol + 7-DHC accumulation',
      'Cholesterol is critical for Sonic Hedgehog signalling → multiple midline/structural defects; steroidogenesis → sex hormone + cortisol deficiency',
      'Photosensitivity: 7-DHC absorbs UV → reactive oxygen species → severe burns even from indoor lighting',
      'Treatment: dietary cholesterol supplementation. Simvastatin paradoxically may reduce 7-DHC by lowering upstream mevalonate flux',
    ],
    labs: { cholesterol: '↓↓', '7_DHC': '↑↑↑', testosterone: '↓ (46,XY)', multiple_malformations: '+' },
  },

  // ── Additional Nucleotide Disorders ──────────────────────────────
  {
    id: 'orotic_aciduria',
    name: 'Hereditary Orotic Aciduria',
    subtitle: 'UMPS Deficiency — Megaloblastic Anaemia Without Hyperammonaemia',
    icon: '🔬',
    color: '#67e8f9',
    category: 'Nucleotide',
    icd: 'E79.8',
    scenario: 'A 4-month-old: megaloblastic anaemia (Hb 68, MCV 105), failure to thrive, developmental delay. Ammonia: NORMAL. Urine orotic acid 2400 µmol/mmol Cr (normal <5). UMPS enzyme: nearly undetectable. Uridine supplementation → full anaemia resolution in 6 weeks.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.0, nutritional_state: 'fed', pathway: 'pyrimidine_synthesis' },
    keyPoints: [
      'UMPS (OPRT + OMP decarboxylase) deficiency → orotate accumulates; UMP synthesis fails',
      'Without UMP: CTP, dTMP, dCTP depleted → DNA/RNA synthesis fails → megaloblastic anaemia (like folate/B12 deficiency, but ammonia is NORMAL)',
      'Key distinction from OTC deficiency: orotic aciduria + hyperammonaemia in OTC; orotic aciduria + normal NH₃ in UMPS deficiency',
      'Treatment: exogenous uridine → uridine kinase converts Urd → UMP, bypassing the UMPS block. Dramatic, rapid clinical response',
    ],
    labs: { orotic_acid: '↑↑↑', ammonia: 'normal', MCV: '↑↑', Hb: '↓↓', citrulline: 'normal' },
  },
  {
    id: 'pnp_scid',
    name: 'PNP Deficiency (T-cell SCID)',
    subtitle: 'Purine Nucleoside Phosphorylase Deficiency — Selective T-cell Loss',
    icon: '🛡️',
    color: '#34d399',
    category: 'Nucleotide',
    icd: 'D81.5',
    scenario: 'A 9-month-old: recurrent PCP pneumonia, CMV retinitis, oral thrush. CD3+ T cells: 82/µL (normal 2000+). CD19+ B cells: 850/µL. Uric acid: <1.0 mg/dL (hypouricaemia — key clue). Deoxyinosine/deoxyguanosine elevated. PNP erythrocyte activity: <1%.',
    params: { glucose_mM: 5.0, oxygen_pct: 100, insulin_fold: 1.0, glucagon_fold: 1.0, energy_demand: 1.5, nutritional_state: 'fed', pathway: 'purine_salvage' },
    keyPoints: [
      'PNP cleaves inosine + guanosine → hypoxanthine/guanine + ribose-1-P. Deficiency → deoxyinosine + deoxyguanosine accumulate',
      'dGTP accumulates specifically in T cells (high deoxykinase activity) → inhibits RNR → blocks dNTP synthesis → T cell apoptosis',
      'Selective T-cell SCID (B cells intact) + hypouricaemia — contrasts with ADA-SCID (all lymphocytes affected, normal/high urate)',
      'Neurological features in 50%: pyramidal signs, ataxia, behavioural problems — may precede immunodeficiency',
      'Treatment: HSCT cures immunodeficiency; gene therapy (lentiviral PNP) in trials',
    ],
    labs: { uric_acid: '↓↓ (<1 mg/dL)', T_cells: '↓↓↓', B_cells: 'normal/↑', dGuo: '↑↑', PNP_activity: '<1%' },
  },
];

const CATEGORIES = [...new Set(CLINICAL_CASES.map(c => c.category))];

export default function ClinicalModule({ onNavigate }) {
  const [selected, setSelected] = useState(null);
  const [simResult, setSimResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeCategory, setActiveCategory] = useState('All');

  const runCase = async (c) => {
    setSelected(c);
    setSimResult(null);
    setLoading(true);
    try {
      const r = await runSimulation(c.params);
      setSimResult(r);
    } catch {
      // backend not running — show case info without simulation
    }
    setLoading(false);
  };

  const filtered = activeCategory === 'All'
    ? CLINICAL_CASES
    : CLINICAL_CASES.filter(c => c.category === activeCategory);

  return (
    <div style={{ padding: '1.5rem', maxWidth: 1100, margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '1rem', marginBottom: '0.4rem' }}>
          <h2 style={{ fontFamily: 'var(--font-sans)', margin: 0 }}>
            ✚ <span style={{ color: 'var(--cyan)' }}>Clinical</span> Integration Module
          </h2>
          <span style={{
            fontFamily: 'var(--font-mono)', fontSize: '0.72rem',
            color: 'var(--text-muted)', border: '1px solid var(--border)',
            padding: '2px 8px', borderRadius: 99,
          }}>{CLINICAL_CASES.length} disorders</span>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', margin: 0 }}>
          Carbohydrate, amino acid, lipid, and nucleotide metabolism disorders with live simulation overlays and clinical biochemistry interpretation
        </p>
      </div>

      {/* Category filter */}
      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginBottom: '1.25rem' }}>
        {['All', ...CATEGORIES].map(cat => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`btn btn-sm ${activeCategory === cat ? 'btn-primary' : 'btn-secondary'}`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Case grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(210px, 1fr))',
        gap: '0.75rem',
        marginBottom: '1.5rem',
      }}>
        {filtered.map(c => (
          <div
            key={c.id}
            id={`clinical-case-${c.id}`}
            className="card"
            style={{
              cursor: 'pointer',
              borderColor: selected?.id === c.id ? c.color + 'aa' : 'var(--border)',
              background: selected?.id === c.id ? `${c.color}0d` : 'var(--bg-card)',
              transition: 'all 0.2s ease',
              position: 'relative',
            }}
            onClick={() => runCase(c)}
            onMouseEnter={e => { e.currentTarget.style.borderColor = c.color + '66'; e.currentTarget.style.transform = 'translateY(-3px)'; e.currentTarget.style.boxShadow = `0 8px 24px ${c.color}20`; }}
            onMouseLeave={e => { if (selected?.id !== c.id) e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none'; }}
          >
            {/* ICD tag */}
            <div style={{
              position: 'absolute', top: 8, right: 10,
              fontFamily: 'var(--font-mono)', fontSize: '0.6rem',
              color: 'var(--text-muted)', letterSpacing: '0.05em',
            }}>{c.icd}</div>

            <div style={{ fontSize: '1.6rem', marginBottom: '0.5rem' }}>{c.icon}</div>
            <div style={{ fontWeight: 700, color: c.color, fontSize: '0.85rem', marginBottom: '0.2rem', lineHeight: 1.3 }}>
              {c.name}
            </div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', lineHeight: 1.4 }}>
              {c.subtitle}
            </div>
            <div style={{
              marginTop: '0.6rem', padding: '2px 7px', borderRadius: 99,
              fontSize: '0.67rem', fontWeight: 600, display: 'inline-block',
              background: `${c.color}12`, color: c.color,
              border: `1px solid ${c.color}30`,
            }}>{c.category}</div>
          </div>
        ))}
      </div>

      {/* Selected case detail */}
      {selected && (
        <div className="animate-in">
          <div className="card" style={{ borderColor: selected.color + '55', marginBottom: '1rem' }}>
            {/* Header row */}
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start', marginBottom: '1.25rem' }}>
              <div style={{
                width: 52, height: 52, flexShrink: 0,
                background: `${selected.color}18`, border: `1px solid ${selected.color}44`,
                borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '1.6rem',
              }}>{selected.icon}</div>
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap', marginBottom: '0.25rem' }}>
                  <h3 style={{ color: selected.color, margin: 0 }}>{selected.name}</h3>
                  <span style={{
                    fontFamily: 'var(--font-mono)', fontSize: '0.7rem',
                    padding: '2px 8px', borderRadius: 99,
                    background: `${selected.color}15`, color: selected.color,
                    border: `1px solid ${selected.color}35`,
                  }}>ICD {selected.icd}</span>
                  <span style={{
                    fontSize: '0.72rem', padding: '2px 8px', borderRadius: 99,
                    background: 'var(--bg-surface)', border: '1px solid var(--border)',
                    color: 'var(--text-muted)',
                  }}>{selected.category}</span>
                </div>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontStyle: 'italic' }}>
                  {selected.subtitle}
                </div>
              </div>
            </div>

            {/* Clinical scenario */}
            <div style={{ marginBottom: '1rem' }}>
              <div className="section-title">📋 Clinical Presentation</div>
              <div style={{
                background: 'var(--bg-surface)', border: '1px solid var(--border)',
                borderLeft: `3px solid ${selected.color}`,
                borderRadius: 8, padding: '0.85rem 1rem',
                color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.65,
              }}>
                {selected.scenario}
              </div>
            </div>

            {/* Key biochemical points */}
            <div style={{ marginBottom: '1rem' }}>
              <div className="section-title">⚗️ Biochemical Pathophysiology</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                {selected.keyPoints.map((p, i) => (
                  <div key={i} style={{
                    display: 'flex', gap: '0.75rem', alignItems: 'flex-start',
                    background: 'var(--bg-surface)', border: '1px solid var(--border)',
                    borderRadius: 8, padding: '0.65rem 0.85rem',
                    fontSize: '0.835rem', color: 'var(--text-secondary)',
                  }}>
                    <span style={{
                      fontFamily: 'var(--font-mono)', fontSize: '0.7rem',
                      color: selected.color, fontWeight: 700, flexShrink: 0, marginTop: 2,
                    }}>{String(i+1).padStart(2,'0')}</span>
                    {p}
                  </div>
                ))}
              </div>
            </div>

            {/* Lab findings */}
            {selected.labs && (
              <div style={{ marginBottom: '1rem' }}>
                <div className="section-title">🔬 Characteristic Lab Findings</div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {Object.entries(selected.labs).map(([key, val]) => (
                    <div key={key} style={{
                      background: 'var(--bg-surface)', border: '1px solid var(--border)',
                      borderRadius: 8, padding: '0.45rem 0.75rem',
                      fontSize: '0.78rem',
                    }}>
                      <span style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                        {key.replace(/_/g,' ')}
                      </span>
                      <span style={{ marginLeft: '0.4rem', fontWeight: 700, color: val.startsWith('↑') ? 'var(--red)' : val.startsWith('↓') ? 'var(--cyan)' : 'var(--green)' }}>
                        {val}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Simulation results */}
            {loading && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--cyan)', fontSize: '0.85rem' }}>
                <span className="spin">⬡</span> Running pathway simulation…
              </div>
            )}
            {simResult?.metrics && (
              <div>
                <div className="section-title">📊 Live Simulation Metrics</div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(110px, 1fr))', gap: '0.5rem' }}>
                  {[
                    { label: 'ATP Yield', value: simResult.metrics.atp_yield?.toFixed(1), unit: 'ATP', color: 'var(--cyan)' },
                    { label: 'Net Flux', value: (simResult.metrics.net_flux * 100).toFixed(0), unit: '%', color: 'var(--green)' },
                    { label: 'Lactate', value: (simResult.metrics.lactate_output * 100).toFixed(0), unit: '%', color: simResult.metrics.lactate_output > 0.5 ? 'var(--red)' : 'var(--text-secondary)' },
                    { label: 'NADH', value: simResult.metrics.nadh_produced?.toFixed(2), unit: '', color: 'var(--purple)' },
                  ].map(m => (
                    <div key={m.label} style={{
                      background: 'var(--bg-surface)', border: '1px solid var(--border)',
                      borderRadius: 10, padding: '0.75rem', textAlign: 'center',
                    }}>
                      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.4rem', fontWeight: 700, color: m.color }}>
                        {m.value}{m.unit && <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginLeft: 2 }}>{m.unit}</span>}
                      </div>
                      <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginTop: 2 }}>{m.label}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            <button id="btn-view-simulation" className="btn btn-primary" onClick={() => onNavigate('simulate')}>
              ⬡ View Full Simulation
            </button>
            <button id="btn-take-related-quiz" className="btn btn-secondary" onClick={() => onNavigate('quiz')}>
              ◆ Take the Quiz
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
