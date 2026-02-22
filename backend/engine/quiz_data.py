"""
MetaboSim Quiz Question Bank — 100+ questions across 5 pathways/topics.
Each question: id, question, options (list of 4), answer (0-indexed), explanation.
"""

QUIZ_QUESTIONS = {

# ─────────────────────────────────────────────────────────────
# GLYCOLYSIS  (25 questions)
# ─────────────────────────────────────────────────────────────
"glycolysis": [
  {"id":"g01","question":"Which enzyme is the primary pace-setter of glycolysis?",
   "options":["Hexokinase","Phosphofructokinase-1","Pyruvate Kinase","Aldolase"],
   "answer":1,"explanation":"PFK-1 catalyses the first truly irreversible, committed step and is the main allosteric control point, regulated by ATP, AMP, citrate, and fructose-2,6-bisphosphate."},

  {"id":"g02","question":"Under severe hypoxia, pyruvate is predominantly converted to:",
   "options":["Acetyl-CoA","Oxaloacetate","Lactate","Citrate"],
   "answer":2,"explanation":"LDH reduces pyruvate to lactate, regenerating NAD⁺ necessary to sustain glycolytic flux when the ETC cannot reoxidise NADH."},

  {"id":"g03","question":"Which molecule activates PFK-1 at high concentrations?",
   "options":["ATP","Citrate","AMP","Glucose-6-phosphate"],
   "answer":2,"explanation":"AMP signals low energy status and activates PFK-1 allosterically, driving more glucose through glycolysis to regenerate ATP."},

  {"id":"g04","question":"Net ATP yield from anaerobic glycolysis of one glucose molecule is:",
   "options":["0 ATP","2 ATP","4 ATP","38 ATP"],
   "answer":1,"explanation":"Glycolysis invests 2 ATP (HK, PFK-1) then generates 4 ATP (2×PGK + 2×PK), giving net 2 ATP per glucose."},

  {"id":"g05","question":"GAPDH is inhibited when which co-factor is depleted?",
   "options":["ATP","NAD⁺","NADPH","CoA"],
   "answer":1,"explanation":"GAPDH requires NAD⁺ to oxidise G3P to 1,3-BPG. In hypoxia, NADH accumulates and NAD⁺ is depleted, blocking GAPDH and halting glycolysis."},

  {"id":"g06","question":"Fructose-2,6-bisphosphate (F2,6BP) is a potent activator of PFK-1. Which hormone raises F2,6BP?",
   "options":["Glucagon","Epinephrine","Insulin","Cortisol"],
   "answer":2,"explanation":"Insulin activates PFK-2 (the kinase domain of the bifunctional enzyme), increasing F2,6BP, which allosterically activates PFK-1 and accelerates glycolysis."},

  {"id":"g07","question":"Pyruvate kinase is inhibited by which of the following?",
   "options":["Fructose-1,6-bisphosphate","AMP","Glucagon (via phosphorylation)","Insulin"],
   "answer":2,"explanation":"Glucagon activates PKA → phosphorylates liver pyruvate kinase → inactivation. This diverts PEP toward gluconeogenesis during fasting."},

  {"id":"g08","question":"The 'energy investment phase' of glycolysis consumes how many ATP?",
   "options":["1","2","3","4"],
   "answer":1,"explanation":"Two ATP are consumed: one by hexokinase (glucose → G6P) and one by PFK-1 (F6P → F1,6BP)."},

  {"id":"g09","question":"Which glycolytic enzyme is deficient in the most common cause of non-spherocytic haemolytic anaemia?",
   "options":["Hexokinase","Phosphoglucose Isomerase","Pyruvate Kinase","Enolase"],
   "answer":2,"explanation":"Pyruvate kinase deficiency is the most common glycolytic enzyme defect. RBCs depend entirely on glycolysis; PK deficiency depletes ATP, causing haemolysis."},

  {"id":"g10","question":"Which step of glycolysis is catalysed by phosphoglycerate mutase?",
   "options":["G6P → F6P","1,3-BPG → 3-PG","3-PG → 2-PG","2-PG → PEP"],
   "answer":2,"explanation":"PGM converts 3-phosphoglycerate to 2-phosphoglycerate by moving the phosphate group from carbon-3 to carbon-2."},

  {"id":"g11","question":"Aldolase cleaves fructose-1,6-bisphosphate into:",
   "options":["G6P + F6P","DHAP + Glyceraldehyde-3-phosphate","2-PG + PEP","Pyruvate + Acetyl-CoA"],
   "answer":1,"explanation":"Aldolase cleaves F1,6BP into two triose phosphates: dihydroxyacetone phosphate (DHAP) and glyceraldehyde-3-phosphate (G3P). TPI then inter-converts them."},

  {"id":"g12","question":"In McArdle disease (GSD V), which enzyme is deficient?",
   "options":["Liver glycogen phosphorylase","Muscle glycogen phosphorylase","Phosphofructokinase (muscle)","G6Pase"],
   "answer":1,"explanation":"McArdle disease is caused by myophosphorylase deficiency. Muscle cannot mobilise glycogen, causing exercise-induced cramps, myoglobinuria, and the 'second wind' phenomenon."},

  {"id":"g13","question":"During intense exercise, what happens to the AMP:ATP ratio in muscle?",
   "options":["AMP rises, activating PFK-1","AMP falls, inhibiting PFK-1","ATP rises, activating PGK","Citrate rises, inhibiting GAPDH"],
   "answer":0,"explanation":"Intense ATP hydrolysis raises ADP and AMP (via adenylate kinase: 2ADP → ATP + AMP). High AMP is a potent activator of PFK-1, accelerating glycolytic flux to match demand."},

  {"id":"g14","question":"Which metabolite accumulates proximal to an inhibited PFK-1 and can enter the pentose phosphate pathway?",
   "options":["F1,6BP","Pyruvate","Glucose-6-phosphate","1,3-BPG"],
   "answer":2,"explanation":"G6P accumulates when PFK-1 is inhibited (e.g. by ATP or citrate); it can be diverted into the HMP shunt for NADPH and ribose-5-phosphate production."},

  {"id":"g15","question":"Enolase converts 2-phosphoglycerate to PEP. Which ion is required as a cofactor?",
   "options":["Ca²⁺","Fe²⁺","Mg²⁺","Zn²⁺"],
   "answer":2,"explanation":"Enolase is a Mg²⁺-dependent metalloenzyme. It dehydrates 2-PG to phosphoenolpyruvate (PEP), which has very high phosphate-transfer potential."},

  {"id":"g16","question":"Citrate inhibits PFK-1 because it signals which metabolic state?",
   "options":["Low energy — activate glycolysis","Adequate acetyl-CoA — TCA is fed, slow glycolysis","High NADH — re-oxidise via ETC","High glucose — store as glycogen"],
   "answer":1,"explanation":"Citrate levels reflect TCA cycle saturation. When citrate is high, the cell has sufficient acetyl-CoA and energy; inhibiting PFK-1 reduces further glucose oxidation."},

  {"id":"g17","question":"Tarui disease (GSD VII) is caused by deficiency of which enzyme?",
   "options":["Muscle PFK","Liver PFK","Phosphoglycerate kinase","Phosphoglycerate mutase"],
   "answer":0,"explanation":"Tarui disease (GSD VII) is muscle phosphofructokinase deficiency, presenting like McArdle disease but also with haemolytic anaemia (RBCs also express the M subunit)."},

  {"id":"g18","question":"The substrate-level phosphorylation steps in glycolysis are catalysed by:",
   "options":["Hexokinase and PFK-1","GAPDH and Enolase","Phosphoglycerate kinase and Pyruvate kinase","PGM and Aldolase"],
   "answer":2,"explanation":"ATP is directly synthesised (substrate-level phosphorylation) at PGK (1,3-BPG → 3-PG) and PK (PEP → pyruvate). Both yield 2 ATP per glucose molecule."},

  {"id":"g19","question":"Which of the following CORRECTLY describes glucose entry into erythrocytes?",
   "options":["Via SGLT1 (active)","Via GLUT4 (insulin-dependent)","Via GLUT1 (constitutive)","Via GLUT2 (high-capacity)"],
   "answer":2,"explanation":"Erythrocytes use GLUT1 for constitutive, insulin-independent glucose transport. They have no mitochondria and rely solely on glycolysis for ATP."},

  {"id":"g20","question":"In the Cori cycle, lactate produced by muscle is converted back to glucose in the:",
   "options":["Kidney","Muscle","Liver","Heart"],
   "answer":2,"explanation":"The Cori cycle: muscle lactate → blood → liver, where LDH oxidises it to pyruvate, then gluconeogenesis regenerates glucose, which is released to blood for muscle uptake."},

  {"id":"g21","question":"Hexokinase is inhibited by its product. What is that product?",
   "options":["Fructose-6-phosphate","Glucose-1-phosphate","Glucose-6-phosphate","Fructose-1,6-bisphosphate"],
   "answer":2,"explanation":"G6P product-inhibits hexokinase (but NOT glucokinase/HK-IV). When G6P accumulates (e.g. PFK-1 blocked), HK is shut off, preventing futile glucose phosphorylation."},

  {"id":"g22","question":"Which vitamin deficiency directly impairs GAPDH and the PDH complex?",
   "options":["Vitamin B12","Niacin (B3)","Thiamine (B1)","Riboflavin (B2)"],
   "answer":1,"explanation":"NAD⁺ (derived from niacin/B3) is required by GAPDH. Thiamine (B1) is a cofactor for PDH and α-KGDH; riboflavin (B2) for FAD. But NAD⁺ for GAPDH specifically links to niacin."},

  {"id":"g23","question":"Phosphoglucose isomerase converts:",
   "options":["Glucose → G6P","G6P → F6P","F6P → F1,6BP","G3P → 1,3-BPG"],
   "answer":1,"explanation":"PGI interconverts G6P (aldose) and F6P (ketose) in a near-equilibrium reaction. It is not a major regulatory point."},

  {"id":"g24","question":"Which statement about glucokinase (HK-IV) is TRUE?",
   "options":["High affinity, saturated at physiological glucose","NOT inhibited by G6P, sigmoidal kinetics","Expressed in all cells","Activated by glucagon"],
   "answer":1,"explanation":"Glucokinase has a high Km (~10 mM), is not inhibited by G6P, shows sigmoidal kinetics (cooperativity), and acts as a glucose sensor in liver and pancreatic β-cells."},

  {"id":"g25","question":"2,3-BPG (bisphosphoglycerate) is primarily important for:",
   "options":["Activating PFK-1 in RBCs","Shifting the Hb-O₂ dissociation curve right","Inhibiting pyruvate kinase","Providing substrate for the TCA cycle"],
   "answer":1,"explanation":"2,3-BPG binds deoxyhaemoglobin, stabilising the T-state and reducing O₂ affinity (right-shift of the dissociation curve), facilitating O₂ delivery to tissues."},
],

# ─────────────────────────────────────────────────────────────
# TCA CYCLE  (22 questions)
# ─────────────────────────────────────────────────────────────
"tca_cycle": [
  {"id":"t01","question":"How many NADH molecules are produced per turn of the TCA cycle?",
   "options":["1","2","3","4"],
   "answer":2,"explanation":"3 NADH are produced at IDH, α-KGDH, and MDH steps. Plus 1 FADH₂ (SDH) and 1 GTP (SCS) per turn."},

  {"id":"t02","question":"Which ion activates IDH and α-KGDH during muscle contraction?",
   "options":["Na⁺","K⁺","Ca²⁺","Mg²⁺"],
   "answer":2,"explanation":"Ca²⁺ released during muscle contraction enters mitochondria, directly activating three TCA enzymes: pyruvate dehydrogenase, IDH, and α-KGDH — coupling contraction to energy production."},

  {"id":"t03","question":"SDH is unique among TCA enzymes because it:",
   "options":["Is located in the cytoplasm","Is also ETC Complex II","Generates GTP, not NADH","Requires biotin"],
   "answer":1,"explanation":"Succinate dehydrogenase is embedded in the inner mitochondrial membrane and donates electrons from FADH₂ directly to ubiquinone, serving as both TCA enzyme and ETC Complex II."},

  {"id":"t04","question":"Which TCA enzyme is activated by acetyl-CoA?",
   "options":["Isocitrate dehydrogenase","Citrate synthase","α-Ketoglutarate dehydrogenase","Succinyl-CoA synthetase"],
   "answer":1,"explanation":"Citrate synthase is allosterically inhibited by its product citrate and by ATP/NADH, but acetyl-CoA is its substrate — high acetyl-CoA drives citrate synthesis forward."},

  {"id":"t05","question":"Which metabolite directly inhibits citrate synthase AND isocitrate dehydrogenase?",
   "options":["AMP","Acetyl-CoA","NADH","Malate"],
   "answer":2,"explanation":"NADH signals high reduction state. It inhibits citrate synthase, IDH, and α-KGDH, slowing the cycle when the cell is energetically replete."},

  {"id":"t06","question":"The anaplerotic reaction replenishing TCA cycle intermediates from amino acids uses which enzyme?",
   "options":["Pyruvate carboxylase","Glutamate dehydrogenase","Aspartate transaminase","All of the above"],
   "answer":3,"explanation":"Multiple reactions feed the TCA cycle: PC (pyruvate → OAA), transamination of glutamate → α-ketoglutarate, aspartate → OAA (via AAT). All are anaplerotic."},

  {"id":"t07","question":"Per turn of the TCA cycle, how many CO₂ are released?",
   "options":["1","2","3","4"],
   "answer":1,"explanation":"Two CO₂ are released: one at isocitrate dehydrogenase (isocitrate → α-KG) and one at α-ketoglutarate dehydrogenase (α-KG → succinyl-CoA)."},

  {"id":"t08","question":"Which step of the TCA cycle produces GTP (or ATP) by substrate-level phosphorylation?",
   "options":["Citrate synthase","IDH","Succinyl-CoA synthetase","Malate dehydrogenase"],
   "answer":2,"explanation":"Succinyl-CoA synthetase (succinate thiokinase) converts succinyl-CoA + GDP + Pi → succinate + GTP + CoA. This is the only substrate-level phosphorylation in the TCA cycle."},

  {"id":"t09","question":"Fluoroacetate ('poison-1080') kills by accumulating as:",
   "options":["Fluoropyruvate inhibiting PDH","Fluorocitrate inhibiting aconitase","Fluoromalate inhibiting MDH","Fluorosuccinate inhibiting SDH"],
   "answer":1,"explanation":"Fluoroacetate is converted to fluoroacetyl-CoA, then condensed with OAA to form fluorocitrate, which irreversibly inhibits aconitase, blocking the TCA cycle and causing cardiac arrest."},

  {"id":"t10","question":"In MELAS syndrome, which complex of the ETC is most commonly impaired, causing TCA back-up?",
   "options":["Complex I","Complex II","Complex III","Complex V"],
   "answer":0,"explanation":"MELAS (m.3243A>G) impairs mitochondrial tRNA-Leu, reducing synthesis of all mtDNA-encoded ETC subunits — Complex I is most affected, causing NADH accumulation and TCA cycle arrest."},

  {"id":"t11","question":"Malate dehydrogenase catalyses: malate + NAD⁺ →",
   "options":["Fumarate + NADH","OAA + NADH","Citrate + NADH","Succinate + NAD⁺"],
   "answer":1,"explanation":"MDH oxidises malate to oxaloacetate (OAA), producing NADH. This reaction has a very unfavourable equilibrium but is driven forward by continuous OAA removal (to citrate synthase)."},

  {"id":"t12","question":"Where in the cell does the TCA cycle occur?",
   "options":["Cytoplasm","Outer mitochondrial membrane","Mitochondrial matrix","Intermembrane space"],
   "answer":2,"explanation":"The TCA cycle enzymes reside in the mitochondrial matrix, except SDH which is embedded in the inner mitochondrial membrane."},

  {"id":"t13","question":"Which TCA intermediate is a precursor for haem synthesis?",
   "options":["Citrate","Succinyl-CoA","α-Ketoglutarate","Isocitrate"],
   "answer":1,"explanation":"Succinyl-CoA condenses with glycine (via ALA synthase) to form δ-aminolevulinic acid (ALA), the committed first step of haem biosynthesis."},

  {"id":"t14","question":"α-Ketoglutarate is the carbon skeleton for which amino acid?",
   "options":["Aspartate","Alanine","Glutamate","Serine"],
   "answer":2,"explanation":"α-Ketoglutarate (α-KG) + NH₄⁺ → glutamate (via GDH). Glutamate is also the precursor for glutamine, proline, and arginine."},

  {"id":"t15","question":"Thiamine (B1) is a cofactor for which TCA enzyme?",
   "options":["Citrate synthase","Aconitase","α-Ketoglutarate dehydrogenase","Fumarase"],
   "answer":2,"explanation":"α-KGDH is a multienzyme complex (like PDH) requiring TPP (thiamine pyrophosphate), lipoic acid, CoA, FAD, and NAD⁺. Thiamine deficiency → Wernicke's encephalopathy."},

  {"id":"t16","question":"Citrate exported from mitochondria to cytoplasm serves as a precursor for:",
   "options":["Fatty acid synthesis","Glycolysis","Urea cycle","Haem synthesis"],
   "answer":0,"explanation":"In the fed state, excess citrate is exported by the citrate shuttle. In the cytoplasm, ATP-citrate lyase cleaves it to acetyl-CoA + OAA, providing cytoplasmic acetyl-CoA for lipogenesis."},

  {"id":"t17","question":"Which TCA intermediate is used for gluconeogenesis?",
   "options":["Acetyl-CoA","Citrate","Oxaloacetate (OAA)","Succinyl-CoA"],
   "answer":2,"explanation":"OAA is converted to PEP by PEPCK, the key gluconeogenic step. Note: acetyl-CoA CANNOT be used for net gluconeogenesis in mammals."},

  {"id":"t18","question":"The net equation for one turn of the TCA cycle: Acetyl-CoA + 3NAD⁺ + FAD + GDP + Pi + 2H₂O →",
   "options":["2CO₂ + 3NADH + FADH₂ + GTP + CoA + 3H⁺","CO₂ + 2NADH + FADH₂ + ATP + CoA","2CO₂ + 2NADH + 2FADH₂ + GTP","Pyruvate + 3NADH + GTP"],
   "answer":0,"explanation":"Per turn: 2 carbons enter as acetyl-CoA, 2 CO₂ leave, generating 3 NADH, 1 FADH₂, 1 GTP, and regenerating CoA. This feeds 10 electron pairs into the ETC."},

  {"id":"t19","question":"Which enzyme converts isocitrate to α-ketoglutarate and is inhibited by NADH and ATP?",
   "options":["Citrate synthase","Aconitase","Isocitrate dehydrogenase","Malate dehydrogenase"],
   "answer":2,"explanation":"IDH3 (mitochondrial, NAD⁺-dependent) is the regulated form. High NADH/ATP inhibits it; ADP and Ca²⁺ activate it, coupling TCA rate to energy demand."},

  {"id":"t20","question":"Succinyl-CoA is the product of which TCA enzyme?",
   "options":["SDH","Aconitase","α-Ketoglutarate dehydrogenase","Citrate synthase"],
   "answer":2,"explanation":"α-KGDH converts α-ketoglutarate → succinyl-CoA + CO₂ + NADH. This is the second decarboxylation step of the TCA cycle."},

  {"id":"t21","question":"Fumarase (fumarate hydratase) mutations are associated with:",
   "options":["McArdle disease","Hereditary leiomyomatosis and renal cell cancer (HLRCC)","Von Gierke disease","MELAS syndrome"],
   "answer":1,"explanation":"FH mutations (autosomal dominant) cause HLRCC. Fumarate accumulates, inhibiting prolyl hydroxylases → stabilises HIF-1α → pseudohypoxic drive → warburg-like metabolism and tumour growth."},

  {"id":"t22","question":"OAA is regenerated at the end of each TCA cycle by which enzyme?",
   "options":["Citrate synthase","Malate dehydrogenase","Fumarase","Succinate dehydrogenase"],
   "answer":1,"explanation":"MDH oxidises malate to regenerate OAA, completing the cycle. OAA then accepts another acetyl-CoA from citrate synthase to begin the next turn."},
],

# ─────────────────────────────────────────────────────────────
# OXIDATIVE PHOSPHORYLATION  (22 questions)
# ─────────────────────────────────────────────────────────────
"oxphos": [
  {"id":"o01","question":"What is the final electron acceptor in the mitochondrial ETC?",
   "options":["NAD⁺","FAD","Ubiquinone (CoQ)","O₂"],
   "answer":3,"explanation":"Complex IV (cytochrome c oxidase) transfers electrons from cytochrome c to O₂, reducing it to H₂O. O₂ is the terminal acceptor — its absence immediately halts ATP synthesis."},

  {"id":"o02","question":"Cyanide is lethal because it irreversibly inhibits:",
   "options":["Complex I","Complex II","Complex III","Complex IV"],
   "answer":3,"explanation":"CN⁻ binds the ferric iron (Fe³⁺) of cytochrome a3 in CIV, blocking O₂ reduction. The entire ETC backs up; NADH cannot be reoxidised; ATP synthesis stops."},

  {"id":"o03","question":"The P/O ratio for mitochondrial NADH oxidation is approximately:",
   "options":["1.0","1.5","2.5","3.8"],
   "answer":2,"explanation":"Modern chemiosmotic measurements give ~2.5 ATP per NADH (accounting for ATP synthase stoichiometry and the cost of ANT and Pi carrier transport across the inner membrane)."},

  {"id":"o04","question":"DNP (2,4-dinitrophenol) causes weight loss by acting as:",
   "options":["Complex I inhibitor","Proton gradient uncoupler","ATP synthase inhibitor","Cytochrome c releaser"],
   "answer":1,"explanation":"DNP is a lipid-soluble proton carrier. It shuttles H⁺ across the inner mitochondrial membrane without passing through ATP synthase, dissipating the PMF as heat instead of making ATP."},

  {"id":"o05","question":"Oligomycin inhibits mitochondrial ATP synthesis by binding:",
   "options":["Complex I (NADH dehydrogenase)","Complex III (bc₁)","Complex V (F₀ subunit of ATP synthase)","Cytochrome c"],
   "answer":2,"explanation":"Oligomycin blocks the c-ring (F₀ subunit) of ATP synthase, preventing proton flow through F₀ and thus ATP synthesis. It also causes PMF to build up, slowing the ETC."},

  {"id":"o06","question":"Rotenone (a pesticide) inhibits the ETC by blocking:",
   "options":["Complex I","Complex II","Complex III","Complex IV"],
   "answer":0,"explanation":"Rotenone blocks Complex I (NADH dehydrogenase) at the CoQ binding site, preventing electron transfer. It is a model for Parkinson's disease pathogenesis (striatal Complex I inhibition)."},

  {"id":"o07","question":"Antimycin A specifically inhibits:",
   "options":["NADH dehydrogenase (CI)","Ubiquinol-cytochrome c reductase (CIII)","Cytochrome c oxidase (CIV)","ATP synthase (CV)"],
   "answer":1,"explanation":"Antimycin A binds the Qᵢ site of Complex III, blocking the Q cycle and preventing electron transfer from ubiquinol to cytochrome c."},

  {"id":"o08","question":"How many ATP molecules does the F₁F₀ ATP synthase synthesise per complete rotation of the c-ring in humans?",
   "options":["2","3","8","10"],
   "answer":1,"explanation":"The human F₁ has 3 αβ pairs; each 120° rotation synthesises 1 ATP. The human c-ring has ~8 c-subunits, requiring ~2.7 H⁺ per ATP. Full 360° = 3 ATP."},

  {"id":"o09","question":"The proton-motive force (PMF) has two components. Which carries more energy in mitochondria?",
   "options":["ΔpH (chemical gradient)","ΔΨ (electrical membrane potential)","Equal contributions","ΔpH dominates only during exercise"],
   "answer":1,"explanation":"In mitochondria, the electrical component ΔΨ (~−180 mV) contributes ~70% of PMF. The chemical ΔpH (~1 unit) contributes the remaining ~30%."},

  {"id":"o10","question":"Cytochrome c is released from mitochondria during apoptosis. Which complex does it normally serve?",
   "options":["Complex I","Complex II","Complex III (as electron carrier to CIV)","Complex V"],
   "answer":2,"explanation":"Cytochrome c shuttles electrons from Complex III to Complex IV in the intermembrane space. Its release into the cytoplasm activates caspase-9 and initiates the intrinsic apoptotic pathway."},

  {"id":"o11","question":"The FADH₂ produced by the TCA cycle enters the ETC at which complex?",
   "options":["Complex I","Complex II","Complex III","Complex IV"],
   "answer":1,"explanation":"FADH₂ produced by succinate dehydrogenase (SDH = Complex II) directly reduces ubiquinone. This bypasses the H⁺-pumping step of Complex I, yielding ~1.5 ATP vs ~2.5 for NADH."},

  {"id":"o12","question":"What is the approximate total ATP yield from complete aerobic oxidation of one glucose?",
   "options":["8 ATP","18 ATP","30–32 ATP","68 ATP"],
   "answer":2,"explanation":"Modern estimates: glycolysis (2 ATP + 2 NADH→5), PDH (2 NADH→5), TCA (6 NADH→15 + 2 FADH₂→3 + 2 GTP) = ~30-32 ATP total (varies by shuttle used for cytoplasmic NADH)."},

  {"id":"o13","question":"Brown adipose tissue thermogenesis is driven by:",
   "options":["Increased Complex I activity","UCP1 (thermogenin) uncoupling","Extra ATP synthase","Increased FADH₂ production"],
   "answer":1,"explanation":"UCP1 (uncoupling protein 1) allows H⁺ to bypass ATP synthase, dissipating PMF as heat. Activated by free fatty acids and noradrenaline in cold exposure — critical for neonatal thermogenesis."},

  {"id":"o14","question":"Which shuttle transfers cytoplasmic NADH electrons into mitochondria in the heart?",
   "options":["Glycerol-3-phosphate shuttle (DHAP shuttle)","Malate-aspartate shuttle","Citrate shuttle","Carnitine shuttle"],
   "answer":1,"explanation":"The malate-aspartate shuttle transfers electrons at NADH equivalent, yielding ~2.5 ATP per cytoplasmic NADH (used in liver, heart, kidney). The glycerol-3-P shuttle yields only ~1.5 ATP."},

  {"id":"o15","question":"Leber hereditary optic neuropathy (LHON) is caused by mutations in:",
   "options":["Complex IV (nuclear-encoded)","Complex I (mtDNA-encoded subunits)","Cytochrome c (nuclear gene)","ANT (adenine nucleotide translocase)"],
   "answer":1,"explanation":"LHON arises from point mutations in mtDNA-encoded Complex I subunits (ND1, ND4, ND6 most common). Retinal ganglion cells are selectively vulnerable, causing painless central vision loss."},

  {"id":"o16","question":"What does the adenine nucleotide translocase (ANT) exchange across the inner mitochondrial membrane?",
   "options":["NADH for NAD⁺","ATP (out) for ADP (in)","H⁺ (out) for K⁺ (in)","Pi (in) for OH⁻ (out)"],
   "answer":1,"explanation":"ANT is the most abundant protein in the inner mitochondrial membrane. It exports ATP⁴⁻ and imports ADP³⁻, with the net electronegative charge movement driven by ΔΨ (ATP export is electrogenic)."},

  {"id":"o17","question":"In Leigh syndrome, MRI shows symmetric basal ganglia lesions. The most common cause is:",
   "options":["Pyruvate carboxylase deficiency","Complex I, IV, or V deficiency / SURF1 mutation","G6PD deficiency","Carnitine palmitoyltransferase deficiency"],
   "answer":1,"explanation":"Leigh syndrome (subacute necrotising encephalomyelopathy) is the most common childhood mitochondrial disease, most often caused by Complex I/IV deficiency or SURF1 (Complex IV assembly factor) mutations."},

  {"id":"o18","question":"How many protons does Complex I pump per 2 electrons transferred?",
   "options":["2","4","6","10"],
   "answer":1,"explanation":"Complex I pumps 4H⁺ per pair of electrons from NADH to CoQ."},

  {"id":"o19","question":"Azide (N₃⁻), like cyanide, inhibits the ETC at:",
   "options":["Complex I","Complex III","Complex IV","Complex V"],
   "answer":2,"explanation":"Azide binds Fe³⁺ of cytochrome a3 in Complex IV, similar to cyanide, blocking O₂ reduction and halting the ETC."},

  {"id":"o20","question":"The P/O ratio for FADH₂ oxidised via the ETC is approximately:",
   "options":["1.0","1.5","2.5","3.0"],
   "answer":1,"explanation":"FADH₂ enters the ETC at Complex II (bypassing CI's H⁺ pumping), so fewer protons are pumped per 2e⁻ → ~1.5 ATP per FADH₂."},

  {"id":"o21","question":"MERRF syndrome is associated with mutations causing deficiency of:",
   "options":["Complex I and IV (by mitochondrial tRNA mutations)","G6Pase","Pyruvate carboxylase","Adenylate kinase"],
   "answer":0,"explanation":"MERRF (myoclonic epilepsy with ragged-red fibres) is most often caused by the m.8344A>G mutation in MT-TK (tRNA-Lys), impairing translation of all mtDNA-encoded ETC subunits."},

  {"id":"o22","question":"The 'respiratory control ratio' (RCR) measures mitochondrial coupling. A high RCR means:",
   "options":["Poor coupling — protons leak freely","Tight coupling — ATP synthesis drives O₂ consumption","Maximum uncoupling by UCP1","Inhibition of Complex III"],
   "answer":1,"explanation":"A high RCR (state 3 / state 4 O₂ consumption) indicates that O₂ is consumed mainly when ADP is present (driving ATP synthesis) and very little H⁺ leaks — tightly coupled mitochondria."},
],

# ─────────────────────────────────────────────────────────────
# GLUCONEOGENESIS  (18 questions)
# ─────────────────────────────────────────────────────────────
"gluconeogenesis": [
  {"id":"n01","question":"Which enzyme catalyses pyruvate → OAA (first step of gluconeogenesis from pyruvate)?",
   "options":["PEPCK","Pyruvate Carboxylase","FBPase-1","G6Pase"],
   "answer":1,"explanation":"Pyruvate Carboxylase (PC) adds CO₂ to pyruvate using ATP and biotin. It is activated by acetyl-CoA, signalling that fatty acid oxidation is active and gluconeogenesis is needed."},

  {"id":"n02","question":"Deficiency of G6Pase causes Von Gierke disease. Which two processes are blocked?",
   "options":["Glycolysis and TCA","Glycogenolysis and Gluconeogenesis","Fatty acid oxidation and Ketogenesis","Urea cycle and TCA"],
   "answer":1,"explanation":"G6Pase is required to release free glucose from G6P. Without it, both glycogen breakdown and de novo glucose synthesis cannot produce blood glucose, causing severe hypoglycaemia."},

  {"id":"n03","question":"PEPCK is transcriptionally induced by:",
   "options":["Insulin","Glucagon (via cAMP-CREB) and Cortisol","Insulin and IGF-1","ATP and NADH"],
   "answer":1,"explanation":"PEPCK gene expression is strongly induced by glucagon (cAMP → PKA → CREB) and cortisol (GR), and powerfully repressed by insulin (via FOXO1 phosphorylation). This is a key fasting-state gene."},

  {"id":"n04","question":"Which of the following CANNOT serve as a net substrate for gluconeogenesis in humans?",
   "options":["Lactate","Glycerol","Acetyl-CoA","Alanine"],
   "answer":2,"explanation":"Acetyl-CoA cannot contribute net carbon to gluconeogenesis because the two carbons that enter the cycle as acetyl-CoA are both lost as CO₂ before OAA is regenerated. Odd-chain fatty acids (propionyl-CoA) can, however."},

  {"id":"n05","question":"FBPase-1 (fructose-1,6-bisphosphatase) is inhibited by:",
   "options":["Glucagon","AMP and Fructose-2,6-bisphosphate","ATP and Citrate","Insulin"],
   "answer":1,"explanation":"AMP (low energy) and F2,6BP (insulin-induced) both inhibit FBPase-1, blocking gluconeogenesis when energy is low or insulin is elevated. This opposes PFK-1/glycolysis reciprocally."},

  {"id":"n06","question":"The 'glucose-alanine cycle' transfers nitrogen from muscle to liver. Alanine is formed in muscle by:",
   "options":["Deamination of glutamate","Transamination of pyruvate with glutamate (ALT)","Reduction of pyruvate","Decarboxylation of aspartate"],
   "answer":1,"explanation":"ALT (alanine aminotransferase) transfers NH₂ from glutamate to pyruvate → alanine. In the liver, ALT reverses this → pyruvate (for GNG) + glutamate → urea (nitrogen disposal)."},

  {"id":"n07","question":"Which organ preferentially uses gluconeogenesis to supply glucose during prolonged fasting (>24 h)?",
   "options":["Muscle only","Liver and Kidney","Brain and Heart","Adipose only"],
   "answer":1,"explanation":"The liver is the primary site during early fasting. After 24–48 h, the kidney becomes increasingly important (up to 40% of GNG), particularly from glutamine."},

  {"id":"n08","question":"Metformin reduces hepatic glucose output primarily by inhibiting:",
   "options":["PEPCK directly","AMPK","Mitochondrial Complex I → activates AMPK → inhibits GNG gene expression","G6Pase directly"],
   "answer":2,"explanation":"Metformin's primary action is mild Complex I inhibition → raises intracellular AMP → activates AMPK → phosphorylates CRTC2 → reduces PEPCK/G6Pase transcription → less hepatic glucose output."},

  {"id":"n09","question":"Pyruvate carboxylase requires which vitamin as cofactor?",
   "options":["Thiamine (B1)","Biotin","Pyridoxal phosphate (B6)","Riboflavin (B2)"],
   "answer":1,"explanation":"Pyruvate carboxylase uses biotin as a prosthetic group to carry CO₂. Biotin is covalently attached to a lysine residue and acts as a CO₂ carrier between the biotin carboxylase and transcarboxylase domains."},

  {"id":"n10","question":"In fasting, which hormone promotes gluconeogenesis AND lipolysis simultaneously?",
   "options":["Insulin","Glucagon","Epinephrine","Both Glucagon and Epinephrine"],
   "answer":3,"explanation":"Both glucagon (hepatic) and epinephrine (hepatic + adipose) raise cAMP, activating PKA. PKA promotes glycogenolysis, GNG, and HSL-mediated lipolysis — coordinated mobilisation of energy stores."},

  {"id":"n11","question":"Which GNG enzyme is uniquely present in liver and kidney but absent in muscle?",
   "options":["PEPCK","FBPase-1","Glucose-6-phosphatase","Pyruvate carboxylase"],
   "answer":2,"explanation":"G6Pase is expressed only in liver, kidney, and intestine. Its absence in muscle means muscle cannot release free glucose into the blood (muscle glycogenolysis produces G6P used locally only)."},

  {"id":"n12","question":"During the 'Randle cycle', elevated fatty acid oxidation inhibits glycolysis in the heart by:",
   "options":["Directly inhibiting HK","Raising acetyl-CoA → activating PDH kinase → inactivating PDH","Depleting NAD⁺","Blocking GLUT4 translocation"],
   "answer":1,"explanation":"High β-oxidation → acetyl-CoA + NADH → acetyl-CoA activates PDH kinase → PDH is phosphorylated/inactivated → pyruvate cannot enter TCA → glycolysis backed up. This is the glucose-fatty acid (Randle) cycle."},

  {"id":"n13","question":"In amino acid catabolism, which amino acid is most directly glucogenic (converted to OAA)?",
   "options":["Leucine","Aspartate","Lysine","Alanine"],
   "answer":1,"explanation":"Aspartate is transaminated directly to OAA, feeding gluconeogenesis. Alanine → pyruvate → OAA (via PC). Leucine and lysine are purely ketogenic."},

  {"id":"n14","question":"Propionyl-CoA (from odd-chain fatty acids) enters GNG after conversion to:",
   "options":["Malonyl-CoA","Succinyl-CoA","Acetyl-CoA","OAA"],
   "answer":1,"explanation":"Propionyl-CoA → (via propionyl-CoA carboxylase + methylmalonyl-CoA mutase, requiring B12) → succinyl-CoA, which enters the TCA cycle and can yield OAA for gluconeogenesis."},

  {"id":"n15","question":"Which GSD directly impairs gluconeogenesis by blocking the bypass of phosphofructokinase?",
   "options":["GSD Ia (G6Pase deficiency)","GSD Ib (G6P translocase deficiency)","GSD I is the only one affecting GNG","FBPase-1 deficiency (GSD I-like)"],
   "answer":3,"explanation":"FBPase-1 deficiency (sometimes classified as GSD-like) blocks the gluconeogenic bypass of PFK-1. Patients present with fasting hypoglycaemia, lactic acidosis, and ketoacidosis — identical triggers to GSD Ia."},

  {"id":"n16","question":"PEPCK exists in two isoforms. The mitochondrial form (PEPCK-M) exports OAA as:",
   "options":["Malate or aspartate (after reduction/transamination)","Citrate","Acetyl-CoA","Succinyl-CoA"],
   "answer":0,"explanation":"Mitochondrial PEPCK converts OAA → PEP directly. In the cytoplasm, OAA (impermeant) must be shuttled as malate (via MDH) or aspartate (via AAT) before cytosolic PEPCK acts."},

  {"id":"n17","question":"Glycerol from lipolysis enters gluconeogenesis at which metabolite?",
   "options":["Pyruvate","Dihydroxyacetone phosphate (DHAP)","G6P","OAA"],
   "answer":1,"explanation":"Glycerol → (glycerol kinase) → glycerol-3-phosphate → (G3P dehydrogenase) → DHAP. DHAP is a gluconeogenic triose phosphate, fed directly into the reverse of glycolysis."},

  {"id":"n18","question":"Which nutrient status maximally activates gluconeogenesis?",
   "options":["Post-prandial (high insulin)","Prolonged fasting / starvation (low insulin, high glucagon, high cortisol)","High carbohydrate diet","Exercise with normal glucose"],
   "answer":1,"explanation":"Prolonged fasting maximally activates GNG: glucagon and cortisol induce PEPCK and G6Pase; insulin suppression removes inhibition; fatty acid oxidation provides ATP and acetyl-CoA to activate PC."},
],

# ─────────────────────────────────────────────────────────────
# CLINICAL / CARBOHYDRATE DISORDERS  (20 questions)
# ─────────────────────────────────────────────────────────────
"clinical": [
  {"id":"c01","question":"A neonate develops hypoglycaemia, hepatomegaly, and lactic acidosis. G6Pase activity is absent. Diagnosis?",
   "options":["Pompe disease","Von Gierke disease (GSD Ia)","McArdle disease","Galactosaemia"],
   "answer":1,"explanation":"GSD Ia = G6Pase deficiency, causing severe fasting hypoglycaemia (no glucose from glycogen or GNG), hepatomegaly (glycogen accumulation), lactic acidosis (G6P → glycolysis → lactate), hyperuricaemia, and hyperlipidaemia."},

  {"id":"c02","question":"An infant presents with hypertrophic cardiomyopathy, profound hypotonia, and absent acid alpha-glucosidase (GAA) activity. What is the diagnosis?",
   "options":["GSD III (Cori disease)","GSD II (Pompe disease)","GSD V (McArdle disease)","GSD VI (Hers disease)"],
   "answer":1,"explanation":"Pompe disease (GSD II) = lysosomal GAA deficiency. Glycogen accumulates in all cell lysosomes, most devastatingly in heart and skeletal muscle. Infantile-onset is rapidly fatal without ERT."},

  {"id":"c03","question":"Pyruvate kinase deficiency causes haemolytic anaemia because red blood cells:",
   "options":["Cannot synthesise NADPH","Cannot make ATP via oxidative phosphorylation, and glycolysis is the only ATP source","Accumulate G6P and undergo oxidative damage","Cannot import glucose via GLUT1"],
   "answer":1,"explanation":"Mature RBCs have no mitochondria. PK deficiency → cannot complete glycolysis → ATP depletion → Na/K-ATPase failure → RBC swells and lyses. Unique vulnerability of cells with no aerobic respiration."},

  {"id":"c04","question":"A 20-year-old develops haemolytic crisis after taking primaquine. G6PD activity is 8% of normal. Which pathway is critically impaired?",
   "options":["TCA cycle","Oxidative phosphorylation","Pentose phosphate pathway (HMP shunt)","Beta-oxidation"],
   "answer":2,"explanation":"G6PD generates NADPH via the HMP shunt. NADPH maintains reduced glutathione (GSH), protecting RBCs from oxidative damage. Without NADPH, H₂O₂ and oxidants denature Hb → Heinz bodies → haemolysis."},

  {"id":"c05","question":"Classic galactosaemia is caused by deficiency of galactose-1-phosphate uridyltransferase (GALT). Which complication is directly due to galactitol accumulation?",
   "options":["Lactic acidosis","Cataracts","Hepatomegaly","Hypoglycaemia"],
   "answer":1,"explanation":"Galactose → galactitol (by aldose reductase, which cannot be metabolised further). Galactitol accumulates in the lens → osmotic damage → cataracts. It also accumulates in the brain, causing neurological damage."},

  {"id":"c06","question":"Hereditary fructose intolerance (HFI) is caused by aldolase B deficiency. The mechanism of hypoglycaemia is:",
   "options":["Excess insulin secretion","Fructose-1-phosphate accumulates → inhibits phosphorylase and phosphoglucomutase → blocks glucose release","Fructose competes with glucose at GLUT2","Aldolase B normally activates glucokinase"],
   "answer":1,"explanation":"F1P traps inorganic phosphate, causing ATP depletion and secondarily inhibiting hepatic glycogen phosphorylase and PGM, blocking both glycogenolysis and gluconeogenesis → profound hypoglycaemia after fructose ingestion."},

  {"id":"c07","question":"A 25-year-old has exercise-induced myalgia, rhabdomyolysis, and myoglobinuria. Forearm exercise test shows no rise in venous lactate but normal ammonia rise. Diagnosis?",
   "options":["MELAS syndrome","McArdle disease (GSD V)","Mitochondrial myopathy (Complex I)","Phosphofructokinase deficiency (Tarui)"],
   "answer":1,"explanation":"McArdle disease hallmark: no lactate rise with exercise (muscle cannot use glycogen) but normal ammonia rise (purine nucleotide cycle intact). Classic history: 'second wind' after brief rest."},

  {"id":"c08","question":"In Type 2 Diabetes, which drug reduces hepatic glucose output by inhibiting SGLT2 in the kidney?",
   "options":["Metformin","Empagliflozin (SGLT2 inhibitor)","Sitagliptin (DPP-4 inhibitor)","Glipizide (sulfonylurea)"],
   "answer":1,"explanation":"SGLT2 inhibitors (gliflozins) block renal glucose reabsorption in the proximal tubule → glycosuria → lower blood glucose. They also reduce cardiovascular and renal mortality (EMPA-REG, CREDENCE trials)."},

  {"id":"c09","question":"A formula-fed neonate develops E. coli sepsis, jaundice, and lens clouding after milk introduction. Urine reducing substances are positive (not glucose). Most likely diagnosis?",
   "options":["Hereditary fructose intolerance","Galactosaemia (GALT deficiency)","G6PD deficiency","PK deficiency"],
   "answer":1,"explanation":"Classic galactosaemia triad: neonatal sepsis (impaired neutrophil function due to Gal-1-P), jaundice (liver damage), cataracts (galactitol). Reducing sugar in urine is galactose, not glucose."},

  {"id":"c10","question":"MELAS syndrome (m.3243A>G) most commonly presents with all EXCEPT:",
   "options":["Stroke-like episodes before age 40","Lactic acidosis","Ragged-red fibres on biopsy","Autosomal dominant inheritance"],
   "answer":3,"explanation":"MELAS is maternally inherited (mitochondrial DNA). The m.3243A>G mutation in MT-TL1 is inherited only from the mother. Penetrance varies with heteroplasmy level."},

  {"id":"c11","question":"Which enzyme deficiency causes the 'second wind' phenomenon and myoglobinuria on exertion?",
   "options":["Liver phosphorylase (GSD VI)","Myophosphorylase (GSD V)","Debranching enzyme (GSD III)","Phosphoglycerate mutase (GSD X)"],
   "answer":1,"explanation":"McArdle disease (myophosphorylase deficiency): initial cramps when glycogen cannot be used → rest → hepatic glucose rises in blood → muscles use blood glucose → 'second wind' improvement."},

  {"id":"c12","question":"Von Gierke disease characteristically shows hyperuricaemia because:",
   "options":["Increased purine synthesis from the HMP shunt using excess G6P → increased uric acid production","Kidneys fail to excrete uric acid","High lactate competes with urate for renal excretion","Both A and C"],
   "answer":3,"explanation":"G6P enters the HMP shunt → ribose-5-P → purine synthesis → uric acid. Additionally, high lactate and triglycerides compete with urate for renal secretion → hyperuricaemia from both overproduction and underexcretion."},

  {"id":"c13","question":"Fanconi–Bickel syndrome (GLUT2 deficiency) is distinguished from other GSDs by:",
   "options":["Cardiac involvement","Generalised renal tubular Fanconi syndrome (glycosuria + aminoaciduria + phosphaturia)","Muscle weakness only","Cataracts and liver disease"],
   "answer":1,"explanation":"GLUT2 is required for basolateral glucose export from the renal proximal tubule. Without it, glucose, amino acids, phosphate, bicarbonate, and urate are all lost in urine → generalised Fanconi syndrome."},

  {"id":"c14","question":"A patient with PDH complex deficiency presents with lactic acidosis. What is the lactate:pyruvate (L:P) ratio?",
   "options":["Normal (<20) — as both pyruvate and lactate rise proportionally","Markedly elevated (>25) — lactate rises much more","Decreased (<10)","L:P is not useful in PDH deficiency"],
   "answer":0,"explanation":"PDH deficiency causes both pyruvate AND lactate to rise together (pyruvate cannot be converted to acetyl-CoA → backs up → spills to LDH → lactate). L:P ratio remains normal (<20), distinguishing it from ETC defects where NADH accumulation increases the ratio."},

  {"id":"c15","question":"Which enzyme defect causes intermittent lactic acidosis, hypoglycaemia, and ketoacidosis specifically during fasting, and is treated with uncooked cornstarch?",
   "options":["PDH deficiency","FBPase-1 deficiency","G6Pase deficiency (Von Gierke)","Glycogen synthase deficiency"],
   "answer":1,"explanation":"FBPase-1 deficiency manifests during fasting when GNG is needed but blocked. Cornstarch (slowly-digested glucose polymer) prevents the need for GNG during prolonged fasting, preventing crises."},

  {"id":"c16","question":"GLUT1 deficiency syndrome (De Vivo disease) presents with:",
   "options":["Fasting hypoglycaemia","Low CSF glucose with normal blood glucose, drug-resistant epilepsy","Haemolytic anaemia","Exercise intolerance"],
   "answer":1,"explanation":"GLUT1 is the primary glucose transporter across the blood-brain barrier. Deficiency → brain glucose starvation → seizures (often starting in infancy), movement disorder, and intellectual disability. Key finding: CSF glucose <2.2 mM with normal plasma glucose."},

  {"id":"c17","question":"In 'Type B' lactic acidosis, which drug is the most common pharmaceutical cause?",
   "options":["Insulin","Metformin (especially in renal impairment)","Empagliflozin","Sitagliptin"],
   "answer":1,"explanation":"Metformin inhibits Complex I. In renal impairment, metformin accumulates → severe Complex I inhibition → NADH cannot be reoxidised → pyruvate → lactate → lactic acidosis. Contraindicated in CKD stage ≥3b."},

  {"id":"c18","question":"A child with Pompe disease would show normal findings in which test?",
   "options":["Acid alpha-glucosidase (GAA) activity in DBS","Forearm ischaemic exercise test (lactate)","Echocardiogram (infantile form)","Muscle biopsy (vacuoles with glycogen)"],
   "answer":1,"explanation":"The forearm exercise test assesses MUSCLE GLYCOGENOLYSIS (phosphorylase pathway). In Pompe disease, the glycolytic enzymes are normal — only lysosomal GAA is absent. Lactate WILL rise normally on the exercise test."},

  {"id":"c19","question":"Which GSD is characterised by 'limit dextrin' accumulation, normal lactate, and mildly elevated CK?",
   "options":["GSD Ia","GSD II","GSD III (Cori)","GSD V"],
   "answer":2,"explanation":"GSD III (Cori/debranching enzyme deficiency) accumulates limit dextrin (glycogen with very short outer chains). Gluconeogenesis is intact so lactate is normal (unlike GSD Ia). CK may be mildly elevated if muscle is involved (GSD IIIa)."},

  {"id":"c20","question":"Galactokinase deficiency causes a milder form of galactosuria with cataracts but WITHOUT liver disease because:",
   "options":["Galactose cannot be converted to galactitol","Gal-1-P does NOT accumulate (galactose → galactitol but not Gal-1-P)","Galactose enters the Leloir pathway via an alternative route","Galactokinase deficiency is only found in adults"],
   "answer":1,"explanation":"Galactokinase converts galactose → Gal-1-P. Without it, galactose accumulates → converted to galactitol by aldose reductase → cataracts. But Gal-1-P (the hepatotoxic metabolite) does NOT accumulate, so liver disease is absent."},
],

# ─────────────────────────────────────────────────────────────
# HMP SHUNT / PENTOSE PHOSPHATE PATHWAY  (10 questions)
# ─────────────────────────────────────────────────────────────
"hmp_shunt": [
  {"id":"h01","question":"G6PD catalyses the first step of the HMP shunt. What does it produce?",
   "options":["NADH + 6-Phosphogluconate","NADPH + 6-Phosphoglucono-δ-lactone","ATP + Ribose-5-phosphate","FADH₂ + CO₂"],
   "answer":1,"explanation":"G6PD (Glucose-6-Phosphate Dehydrogenase) oxidises G6P with NADP⁺ → 6-Phosphoglucono-δ-lactone + NADPH + H⁺. NADPH is crucial for reductive biosynthesis and antioxidant defence."},

  {"id":"h02","question":"G6PD deficiency causes haemolytic anaemia primarily because red blood cells cannot:",
   "options":["synthesise haemoglobin","produce ATP by glycolysis","regenerate reduced glutathione (GSH) via NADPH","carry out oxidative phosphorylation"],
   "answer":2,"explanation":"RBCs lack mitochondria. G6PD → NADPH → Glutathione reductase → reduced GSH ← H₂O₂ (deactivated by GPx). Without NADPH, H₂O₂ accumulates → Heinz bodies (denatured Hb) → haemolysis."},

  {"id":"h03","question":"Which vitamin cofactor is essential for Transketolase activity in the non-oxidative PPP?",
   "options":["Riboflavin (B2)","Niacin (B3)","Thiamine (B1 = TPP)","Pyridoxine (B6 = PLP)"],
   "answer":2,"explanation":"Transketolase requires thiamine pyrophosphate (TPP = Vitamin B1) as a prosthetic group. TPP stabilises the carbanion intermediate. Erythrocyte transketolase activation coefficient (ETKA) is the clinical test for thiamine deficiency."},

  {"id":"h04","question":"The oxidative phase of the HMP shunt produces, per glucose-6-phosphate oxidised:",
   "options":["2 NADH + 1 CO₂","2 NADPH + 1 CO₂","1 NADPH + 2 CO₂","2 ATP + 1 NADPH"],
   "answer":1,"explanation":"Two NADP⁺ → NADPH steps: (1) G6PD: G6P → 6-PGL + NADPH; (2) 6PGD: 6-PG → Ribulose-5-P + CO₂ + NADPH. Net: 2 NADPH + 1 CO₂ per G6P, with 0 ATP produced."},

  {"id":"h05","question":"Which of the following correctly pairs the PPP intermediate with its biosynthetic role?",
   "options":["NADPH → fatty acid synthesis","Ribose-5-Phosphate → cholesterol synthesis","Ribulose-5-Phosphate → haem synthesis","Erythrose-4-Phosphate → urea synthesis"],
   "answer":0,"explanation":"NADPH provides the reductive power for: fatty acid synthesis (ACC, FAS), cholesterol synthesis (HMG-CoA reductase), and glutathione regeneration. R5P is the scaffold for nucleotide (RNA/DNA) and NAD synthesis."},

  {"id":"h06","question":"Which drug most classically triggers haemolysis in G6PD-deficient individuals?",
   "options":["Penicillin","Primaquine","Metformin","Warfarin"],
   "answer":1,"explanation":"Primaquine (antimalarial) induces oxidative stress; G6PD-deficient RBCs cannot regenerate NADPH → GSH depletes → Heinz bodies → haemolysis. Other triggers: dapsone, fava beans, nitrofurantoin, infection."},

  {"id":"h07","question":"Transaldolase deficiency is diagnosed by elevated urinary:",
   "options":["Lactate and pyruvate","Sedoheptitol and erythritol","Galactitol and galactose","Fructose-1-phosphate and glyceraldehyde"],
   "answer":1,"explanation":"Transaldolase converts Sedoheptulose-7-P + G3P in the non-oxidative PPP. Deficiency → accumulation of sedoheptulose-7-P → reduced to sedoheptitol by aldose reductase. Elevated urinary sedoheptitol, erythritol, and arabitol are pathognomonic."},

  {"id":"h08","question":"The non-oxidative phase of the PPP is important in tissues with high cell proliferation primarily because it generates:",
   "options":["NADPH for antioxidant defence","ATP for anabolism","Ribose-5-Phosphate for nucleotide biosynthesis","Fructose-6-Phosphate for glycolysis"],
   "answer":2,"explanation":"Rapidly proliferating cells (e.g., cancer, lymphocytes) need R5P for nucleotide synthesis (DNA replication, mRNA). The non-oxidative PPP can produce R5P from F6P and G3P without the oxidative phase, allowing flexible demand."},

  {"id":"h09","question":"The erythrocyte transketolase activation coefficient (ETKA) is used to diagnose deficiency of which vitamin?",
   "options":["Vitamin B2 (Riboflavin)","Vitamin B1 (Thiamine)","Vitamin B6 (Pyridoxine)","Vitamin B12 (Cobalamin)"],
   "answer":1,"explanation":"ETKA measures TKT activity ± added TPP. A ratio (activated/basal) > 1.25 indicates TPP (thiamine) deficiency, as adding exogenous TPP substantially increases TKT activity when the baseline is sub-saturated."},

  {"id":"h10","question":"In which cell type is G6PD deficiency most clinically impactful, and why?",
   "options":["Hepatocytes — because they rely exclusively on NADPH for lipogenesis","Erythrocytes — they have no mitochondria and cannot regenerate NADPH by any other route","Neurons — high energy demand requires constant PPP activity","Muscle cells — exercise amplifies oxidative stress"],
   "answer":1,"explanation":"Mature RBCs have no nucleus or mitochondria. The PPP is their ONLY source of NADPH. NADPH is essential for glutathione regeneration via glutathione reductase. No PPP → no antioxidant defence → haemolysis."},
],

# ─────────────────────────────────────────────────────────────
# GLYCOGENESIS  (10 questions)
# ─────────────────────────────────────────────────────────────
"glycogenesis": [
  {"id":"gy01","question":"Glycogen Synthase forms which type of glycosidic bond to elongate glycogen chains?",
   "options":["β-1,4","α-1,6","α-1,4","β-1,6"],
   "answer":2,"explanation":"Glycogen Synthase adds UDP-glucose to the non-reducing end of glycogen via an α-1,4 glycosidic bond. The α-1,6 branch points are created by the Branching Enzyme (GBE1), which occurs separately."},

  {"id":"gy02","question":"Which intermediate is the direct glucose donor for Glycogen Synthase?",
   "options":["ADP-Glucose","GDP-Glucose","UDP-Glucose","G6P"],
   "answer":2,"explanation":"UDP-Glucose (uridine diphosphate glucose), formed by UDP-Glucose pyrophosphorylase from UTP + G1P, is the activated sugar donor. Glycogen Synthase transfers the glucose to glycogen, releasing UDP."},

  {"id":"gy03","question":"Glycogen Synthase is activated by dephosphorylation. Which signalling cascade phosphorylates and INACTIVATES it?",
   "options":["Insulin → PI3K → Akt → PP1 (activates GS)","Glucagon → cAMP → PKA → GSK-3 → phosphorylates GS","Epinephrine → cAMP → PKA → phosphorylates GS (directly)","Both B and C"],
   "answer":3,"explanation":"PKA (from glucagon/Epi cAMP) directly phosphorylates GS kinase and activates GSK-3, which further phosphorylates GS on multiple sites → inactivation. Insulin activates PP1 via Akt → dephosphorylates GS → activation."},

  {"id":"gy04","question":"GSD Type 0 (GYS2 deficiency) presents with which COMBINATION of findings?",
   "options":["Hepatomegaly + fasting hypoglycaemia + elevated lactate","Fasting hypoglycaemia + fasting ketosis + POST-PRANDIAL hyperglycaemia + NO hepatomegaly","Muscle cramps + exercise myoglobinuria + normal fasting glucose","Fasting hypoglycaemia + hyperuricaemia + lactic acidosis"],
   "answer":1,"explanation":"GYS2 (liver GS) deficiency: liver cannot store glucose as glycogen → post-prandial glucose spilt into blood (hyperglycaemia), then nothing to release during fasting → hypoglycaemia + ketosis. No glycogen accumulation → NO hepatomegaly."},

  {"id":"gy05","question":"The Branching Enzyme (GBE1) transfers how many glucose residues to create a new branch point?",
   "options":["At least 3","At least 6","Exactly 2","At least 11"],
   "answer":1,"explanation":"GBE1 cleaves ≥6 α-1,4-linked glucose residues from the outer chain and reattaches them via an α-1,6 bond, creating a new branch at least 4 residues from the last branch."},

  {"id":"gy06","question":"Which allosteric activator stimulates Glycogen Synthase directly (independent of covalent modification)?",
   "options":["ATP","AMP","Glucose-6-phosphate","Glucagon"],
   "answer":2,"explanation":"Glucose-6-phosphate allosterically activates GS even in its phosphorylated (usually inactive) form. Elevated G6P signals glucose is abundant → store it. This is important after a high-carbohydrate meal."},

  {"id":"gy07","question":"How many high-energy phosphate bonds are consumed per glucose unit stored as glycogen?",
   "options":["0 — glycogen synthesis is spontaneous","1 (only HK = ATP)","2 (HK uses 1 ATP; UGPPase uses 1 UTP ≈ 1 ATP)","3 (HK + PGM + GS each use ATP)"],
   "answer":2,"explanation":"Step 1: HK → G6P (1 ATP consumed). Step 2: PGM → G1P (no energy). Step 3: UGPPase → UDP-Glc (1 UTP consumed; PPi hydrolysed by pyrophosphatase). Total: 2 high-energy bonds per glucose. GS itself uses no ATP."},

  {"id":"gy08","question":"Andersen disease (GSD IV) is caused by deficiency of:",
   "options":["Glycogen Synthase (GYS2)","Branching Enzyme (GBE1)","Debranching Enzyme (AGL)","Glycogenin (GYG)"],
   "answer":1,"explanation":"GBE1 (Branching Enzyme) deficiency → long unbranched amylopectin-like glycogen accumulates → poorly water-soluble → triggers hepatotoxicity → cirrhosis by infancy. Liver transplant is curative."},

  {"id":"gy09","question":"Which primer is required to initiate glycogen synthesis de novo?",
   "options":["A free glucose molecule","Glycogenin (GYG) — a self-glucosylating protein","UDP-Glucose alone","A pre-existing 4-residue starch chain"],
   "answer":1,"explanation":"Glycogenin is a homodimeric glucosyltransferase that catalyses its own glucosylation (autocatalysis) to create a primer of 7 glucose residues. Glycogen Synthase then extends this primer."},

  {"id":"gy10","question":"Insulin promotes glycogenesis by simultaneously:",
   "options":["Inhibiting G6Pase and activating GS","Activating PP1 (which dephosphorylates/activates GS) AND inhibiting GSK-3 (via Akt)","Increasing cAMP and activating PKA","Activating PEPCK and increasing G1P availability"],
   "answer":1,"explanation":"Insulin → IRS-1 → PI3K → PIP3 → PDK1 → Akt phosphorylates GSK-3 (inactivating it) AND phosphorylates phosphodiesterase-3B (lowering cAMP). PP1 is activated → dephosphorylates GS → GS activation → glycogen synthesis."},
],

# ─────────────────────────────────────────────────────────────
# GLYCOGENOLYSIS  (10 questions)
# ─────────────────────────────────────────────────────────────
"glycogenolysis": [
  {"id":"gl01","question":"Glycogen Phosphorylase cleaves glucose from glycogen by:",
   "options":["Hydrolysis (using H₂O)","Phosphorolysis (using inorganic phosphate Pi)","Transfer to UDP","ATP-driven cleavage"],
   "answer":1,"explanation":"Phosphorylase uses Pi (inorganic phosphate) to cleave α-1,4 bonds → Glucose-1-Phosphate. This is phosphorolysis (not hydrolysis). The G1P product retains the phosphate from Pi — energetically superior as no ATP is spent."},

  {"id":"gl02","question":"Which vitamin serves as a covalently bound cofactor for Glycogen Phosphorylase?",
   "options":["Thiamine (B1)","Riboflavin (B2)","Pyridoxal-5-phosphate (PLP = B6)","Niacin (B3)"],
   "answer":2,"explanation":"PLP (pyridoxal-5-phosphate, derived from Vitamin B6) is covalently attached to Lys-680 of Glycogen Phosphorylase. It acts as a general acid-base catalyst in the phosphorolysis mechanism — an unusual role for PLP (not transamination here)."},

  {"id":"gl03","question":"The 'Second Wind' phenomenon in McArdle disease occurs because:",
   "options":["Muscle switches from aerobic to anaerobic metabolism","Hepatic glycogenolysis provides blood glucose that muscle can use via GLUT → glycolysis","Fatty acid oxidation is suddenly upregulated in muscle","Myosin is replaced by a more efficient isoform"],
   "answer":1,"explanation":"After first-wave fatigue (due to blocked muscle glycogenolysis), a brief rest allows hepatic glycogenolysis to raise plasma glucose. Muscles take up this circulating glucose via GLUT1/4 without needing their own GP → fatigue partially resolves."},

  {"id":"gl04","question":"Which hormone activates Glycogen Phosphorylase in BOTH liver and muscle via the cAMP-PKA cascade?",
   "options":["Insulin","Epinephrine","Glucagon (liver only)","Cortisol"],
   "answer":1,"explanation":"Epinephrine activates β-adrenoceptors in BOTH liver and muscle → adenylyl cyclase → cAMP → PKA → Phosphorylase Kinase → GP-a (active). Glucagon acts only on the liver (no glucagon receptors on skeletal muscle)."},

  {"id":"gl05","question":"Glucose uniquely inhibits Glycogen Phosphorylase a in LIVER but not in MUSCLE. Why is this physiologically important?",
   "options":["Muscle needs to continue glycogenolysis for local energy even when blood glucose is restored","Liver can sense blood glucose and stop releasing it when glucose is adequate","Glucose activates PKA in liver but not muscle","Liver GP-a requires AMP for activity"],
   "answer":1,"explanation":"Liver acts as a glucose buffer. When blood glucose rises (e.g. after a meal), glucose binds to liver GP-a allosterically → conformational change exposes the phosphorylation site → PP1 can dephosphorylate → GP-b (inactive) → glycogenolysis stops."},

  {"id":"gl06","question":"The Debranching Enzyme (AGL) has TWO activities. In what order do they act?",
   "options":["Glucosidase first, then transferase","Transferase first (moves 3 outer glucose residues), then glucosidase (releases 1 branch-point glucose)","They act simultaneously on separate substrates","AGL has only transferase activity; a separate glucosidase acts second"],
   "answer":1,"explanation":"After phosphorylase degrades the outer chain to 4 residues from a branch-point: (1) AGL transferase moves 3 of those residues to a nearby non-reducing end (α-1,4 bond); (2) AGL glucosidase hydrolyses the 1 remaining α-1,6 branch glucose → free glucose."},

  {"id":"gl07","question":"In the forearm ischaemic exercise test, which finding distinguishes McArdle's (GSD V) from a normal response?",
   "options":["Lactate rises, ammonia does not","Ammonia rises, but lactate does not rise","Both lactate and ammonia fail to rise","Lactate rises above 4 mmol/L"],
   "answer":1,"explanation":"Normal: both lactate (glycolysis) and ammonia (AMP deaminase — purine nucleotide cycle) rise with ischaemic exercise. McArdle's: myophosphorylase absent → muscle cannot use glycogen → no glycolysis → NO lactate rise. Ammonia still rises normally (purine cycle intact)."},

  {"id":"gl08","question":"AMP allosterically activates Glycogen Phosphorylase b specifically in MUSCLE. The significance is:",
   "options":["Allows muscle to mobilise glycogen without waiting for hormone signalling when energy demand is high","AMP inhibits phosphorylase kinase, directly activating phosphorylase","AMP replacement for calcium in the calmodulin activation","AMP is an allosteric inhibitor, not activator"],
   "answer":0,"explanation":"During intense exercise, muscle AMP rises rapidly (ATP → ADP → AMP via adenylate kinase). High AMP directly activates GP-b → G1P production → glycolysis → ATP regeneration. This is a rapid, hormone-independent mechanism for energy sensing."},

  {"id":"gl09","question":"GSD Type VI (Hers disease) affects which isoform of Glycogen Phosphorylase?",
   "options":["Liver phosphorylase (PYGL)","Muscle phosphorylase (PYGM)","Brain phosphorylase (PYGB)","Both liver and muscle (PYGL + PYGM)"],
   "answer":0,"explanation":"Hers disease = hepatic Glycogen Phosphorylase (PYGL) deficiency. Unlike McArdle (PYGM = muscle), Hers presents with hepatomegaly and mild fasting hypoglycaemia — usually resolves spontaneously at puberty."},

  {"id":"gl10","question":"Phosphorylase Kinase (PhK) is unique in responding to BOTH hormonal AND mechanical signals. The mechanical signal is:",
   "options":["Mechanical stretch → opens ATP channels","Ca²⁺ released during muscle contraction → binds calmodulin δ-subunit of PhK → activates PhK","AMP generated by ATP hydrolysis → allosterically activates PhK","Myosin-actin binding → activates a PhK adaptor protein"],
   "answer":1,"explanation":"PhK consists of 4 subunits (α, β, γ, δ). The δ-subunit IS calmodulin. Ca²⁺ released from SR during contraction binds δ-calmodulin → activates PhK → activates GP-a → glycogenolysis begins within milliseconds of muscle contraction."},
],

# ─────────────────────────────────────────────────────────────
# FRUCTOSE METABOLISM  (10 questions)
# ─────────────────────────────────────────────────────────────
"fructose_metabolism": [
  {"id":"f01","question":"Unlike hexokinase (acting on glucose), fructokinase (KHK) is NOT regulated by its product. What is the clinical consequence?",
   "options":["Fructose is converted very slowly in liver","Fructose floods the liver in high doses without negative feedback → rapid ATP and Pi depletion","Fructose cannot be metabolised — it appears in urine","KHK product inhibition is actually present — this premise is incorrect"],
   "answer":1,"explanation":"HK is product-inhibited by G6P → self-regulating. KHK has no such brake → flooded with fructose → rapid F1P accumulation → Pi trapping → ATP depletion → uric acid production (from AMP catabolism) and hepatotoxicity."},

  {"id":"f02","question":"Fructose uniquely bypasses PFK-1 regulation. The metabolic consequence in hepatic fructose metabolism is:",
   "options":["Slower entry of carbons into glycolysis","Unregulated carbon entry beyond PFK-1 → excess pyruvate, acetyl-CoA → lipogenesis (VLDL-TG) and uric acid","Fructose enters glycolysis at the level of F6P (before PFK-1)","Fructose is entirely converted to galactose"],
   "answer":1,"explanation":"Glucose is regulated by PFK-1 (the pace-setter). Fructose bypasses PFK-1 (entering as DHAP + G3P via Aldolase B). This unregulated entry provides uncontrolled acetyl-CoA → de novo lipogenesis → hepatic steatosis, hypertriglyceridaemia, and uric acid production."},

  {"id":"f03","question":"In Hereditary Fructose Intolerance (HFI), WHICH enzyme is deficient?",
   "options":["Fructokinase (KHK)","Aldolase B","Triokinase","Phosphoglucose Isomerase"],
   "answer":1,"explanation":"Aldolase B deficiency causes HFI. F1P (product of KHK) CANNOT be cleaved → accumulates → traps Pi → ATP depletion → inhibits phosphorylase and PGM → blocks glycogenolysis and GNG → profound hypoglycaemia when fructose is ingested."},

  {"id":"f04","question":"Which urine test finding is characteristic of hereditary fructose intolerance AFTER fructose ingestion?",
   "options":["Glucose in urine (renal tubular glucose leak)","Reducing substances in urine (fructose), NOT detected by glucose-oxidase strip","Galactose and galactitol in urine","Lactate and pyruvate in urine"],
   "answer":1,"explanation":"F1P accumulates → phosphate trapping → ATP collapse. Excess fructose (not metabolised) spills into urine as reducing substance (positive copper-reagent test), but glucose-oxidase strip is negative (specific for glucose). Positive Clinitest negative Clinistix pattern."},

  {"id":"f05","question":"A child with HFI develops an instinctive aversion to sweet foods. The mechanism is:",
   "options":["Bitter taste receptors activated by fructose-1-phosphate","The hypoglycaemia and vomiting after fructose ingestion creates conditioned aversion — protective learned behaviour","Genetic mutation affecting GLUT5 reduces fructose palatability","Aldolase B is expressed in taste buds and changes sweet perception"],
   "answer":1,"explanation":"HFI children learn by association: eating sweet foods (containing fructose/sucrose/sorbitol) → vomiting, abdominal pain, hypoglycaemia. This creates a powerful conditioned avoidance. Clinically, this may delay diagnosis as children self-protect."},

  {"id":"f06","question":"Sorbitol (found in 'sugar-free' products) is dangerous for HFI patients because:",
   "options":["Sorbitol competitively inhibits aldolase B","Sorbitol is converted to fructose by sorbitol dehydrogenase in liver → raises F1P → same hypoglycaemia risk as fructose","Sorbitol directly inhibits glycogen phosphorylase","Sorbitol is converted to galactose in the lens"],
   "answer":1,"explanation":"Sorbitol → fructose (sorbitol dehydrogenase) → KHK → F1P → same cascade as dietary fructose. HFI patients must avoid fructose AND sorbitol AND sucrose (sucrose = glucose + fructose). 'Sugar-free' labels using sorbitol are hazardous."},

  {"id":"f07","question":"Net ATP yield from hepatic fructose catabolism to pyruvate (compared to glucose) is approximately the same, but the key COST difference is:",
   "options":["Fructose uses 3 ATP in the investment phase vs 2 for glucose","Fructose requires 2 ATP (KHK + Triokinase) but produces the same 4 per 2 trioses = net 2 ATP (same as glucose net 2 ATP from glycolysis)","Fructose produces 6 ATP (2 more than glucose) per molecule","Fructose bypasses both ATP-investing steps in glycolysis"],
   "answer":1,"explanation":"Glucose glycolysis: invest 2 ATP (HK + PFK-1), produce 4 → net 2. Fructose: invest 2 ATP (KHK + Triokinase), produce 4 → net 2. Same net yield, but different regulatory control — fructose has NO PFK-1 gate."},

  {"id":"f08","question":"Fructose-1-phosphate (F1P) accumulation in HFI depletes intracellular phosphate. This causes a SECONDARY inhibition of:",
   "options":["Hexokinase and PFK-1","Aldolase A and triose phosphate isomerase","Glycogen Phosphorylase (phosphate-dependent) AND Phosphoglucomutase → blocks glycogenolysis","ATP synthase in mitochondria"],
   "answer":2,"explanation":"Pi depletion impairs Glycogen Phosphorylase (needs Pi for phosphorolysis) and PGM (a Pi-carrying enzyme). This blocks glycogenolysis AND gluconeogenesis at G1P→G6P step → liver cannot release glucose → severe hypoglycaemia after fructose."},

  {"id":"f09","question":"Essential fructosuria (KHK deficiency) is distinguished from HFI (Aldolase B deficiency) by:",
   "options":["Severe post-prandial hypoglycaemia in KHK deficiency vs mild symptoms in HFI","Benign fructosuria in KHK deficiency; severe hypoglycaemia, liver disease in HFI","KHK deficiency causes cataracts; HFI causes haemolytic anaemia","Both conditions require strict fructose restriction"],
   "answer":1,"explanation":"KHK deficiency = essential fructosuria: fructose cannot be phosphorylated → cannot be trapped → excreted in urine → benign and asymptomatic. HFI (Aldolase B deficiency): fructose IS phosphorylated to F1P but cannot be cleaved → F1P traps Pi → disaster."},

  {"id":"f10","question":"In which cellular location does fructose PRIMARILY enter glycolysis after aldolase B cleavage?",
   "options":["As F6P at the PGI step","As DHAP (enters via TPI → G3P) and Glyceraldehyde (phosphorylated by Triokinase → G3P)","As G6P at the HK step","As Pyruvate directly"],
   "answer":1,"explanation":"Aldolase B cleaves F1P → DHAP + Glyceraldehyde. DHAP is directly isomerised to G3P by TPI. Glyceraldehyde is phosphorylated to G3P by Triokinase (ATP used). Both trioses then continue from G3P → pyruvate in the second half of glycolysis."},
],

# ─────────────────────────────────────────────────────────────
# GALACTOSE METABOLISM  (10 questions)
# ─────────────────────────────────────────────────────────────
"galactose_metabolism": [
  {"id":"gal01","question":"Which enzyme catalyses the first step of galactose metabolism in the Leloir pathway?",
   "options":["GALT (galactose-1-P uridylyltransferase)","GALE (UDP-galactose 4-epimerase)","GALK (galactokinase)","Phosphoglucomutase"],
   "answer":2,"explanation":"Galactokinase (GALK1) phosphorylates galactose → Galactose-1-Phosphate using 1 ATP. This is the committed first step, trapping galactose inside the cell for further metabolism."},

  {"id":"gal02","question":"Classic galactosaemia (GALT deficiency) is most immediately life-threatening to neonates because of:",
   "options":["Hypoglycaemia from impaired glycogenolysis","Neonatal E. coli sepsis due to impaired neutrophil function from Gal-1-P accumulation","Cataracts causing blindness","Haemolytic anaemia from osmotic RBC damage"],
   "answer":1,"explanation":"Gal-1-P accumulates in galactosaemia. It impairs neutrophil phagocytic function → profound susceptibility to E. coli sepsis in the first week of life. Sepsis is THE most common cause of neonatal death in undiagnosed galactosaemia. Cataracts and liver disease are also present."},

  {"id":"gal03","question":"Galactitol is formed from galactose by which enzyme, and it accumulates primarily in which tissue to cause which complication?",
   "options":["Aldose reductase → galactitol → lens → cataracts","Sorbitol dehydrogenase → galactitol → liver → cirrhosis","Galactokinase → galactitol → kidney → tubular damage","GALE → galactitol → brain → encephalopathy"],
   "answer":0,"explanation":"Aldose reductase (present in lens, nerve, kidney) converts galactose to galactitol using NADPH. Galactitol cannot be further metabolised in the lens → osmotic water entry → lens swelling → nuclear cataracts. This occurs in BOTH GALK and GALT deficiency."},

  {"id":"gal04","question":"GALT catalyses the exchange: Galactose-1-P + UDP-Glucose → Glucose-1-P + UDP-Galactose. This reaction requires:",
   "options":["ATP and Mg²⁺","A ping-pong mechanism through a histidine-uridylyl intermediate; no external cofactor","NADP⁺ as electron acceptor","GTP and CoA"],
   "answer":1,"explanation":"GALT uses a ping-pong bi-bi mechanism: (1) UDP is transferred from UDP-Glucose to His186 of GALT → enzyme-uridylyl intermediate (ping); (2) Gal-1-P attacks the intermediate → UDP-Galactose released and G1P formed (pong). No external cofactors."},

  {"id":"gal05","question":"GALE (UDP-Galactose Epimerase) is unique compared to GALK and GALT in that its deficiency can paradoxically be worsened by:",
   "options":["High-protein diet","Galactose restriction (because UDP-galactose is also synthesised endogenously via GALE for glycan biosynthesis)","High-fat ketogenic diet","Insulin therapy"],
   "answer":1,"explanation":"GALE converts UDP-Gal ⇌ UDP-Glc in both directions. Complete GALE deficiency = cannot synthesise UDP-galactose from UDP-glucose. UDP-galactose is essential for glycoprotein and glycolipid synthesis. Strict galactose-free diet deprive even the endogenous source → must supplement controlled galactose."},

  {"id":"gal06","question":"Which galactose disorder presents with cataracts ONLY (no liver disease, no sepsis)?",
   "options":["Classic galactosaemia (GALT deficiency)","Galactokinase deficiency (GALK1 deficiency)","GALE deficiency (severe form)","Fanconi–Bickel syndrome"],
   "answer":1,"explanation":"GALK1 deficiency: galactose cannot be phosphorylated. Galactose → galactitol (aldose reductase) → cataracts. No Gal-1-P is formed → no hepatotoxicity, no neutrophil impairment, no sepsis. Milder than GALT deficiency."},

  {"id":"gal07","question":"Glucose-1-Phosphate produced at the end of the Leloir pathway enters which metabolic pathway FIRST?",
   "options":["Directly enters glycolysis at the G3P step","Converted to G6P by Phosphoglucomutase → then glycolysis, glycogen synthesis, or PPP","Directly enters the TCA cycle","Converted to UDP-Glucose and recycled back"],
   "answer":1,"explanation":"G1P → (Phosphoglucomutase, PGM) → G6P. G6P is the metabolic branch-point: it can enter glycolysis, glycogen synthesis (via G1P again → UDP-Glc), or the PPP. PGM catalyses a near-equilibrium reversible reaction."},

  {"id":"gal08","question":"Newborn screening for galactosaemia typically measures TOTAL galactose (including Gal-1-P) in dried blood spot. A positive screen should be treated by:",
   "options":["Immediate liver biopsy","Emergency phlebotomy to reduce Gal-1-P","Immediate withdrawal of all galactose-containing feeds (dairy) + confirmatory enzyme testing","Starting enzyme replacement therapy"],
   "answer":2,"explanation":"Act URGENTLY: switch from breast milk/formula to galactose-free formula (e.g. soya-based). Confirmatory GALT enzyme testing on DBS follows. Do NOT wait — neonatal E. coli sepsis can occur within days. Galactosaemia screening is part of expanded newborn screening in most developed countries."},

  {"id":"gal09","question":"Long-term complications of classic galactosaemia despite dietary treatment include all EXCEPT:",
   "options":["Cognitive impairment and learning difficulties","Primary ovarian insufficiency (POI) in females","Progressive liver cirrhosis in adulthood","Cataracts if poorly controlled"],
   "answer":2,"explanation":"With dietary treatment, liver disease and cataracts are largely preventable. However, Gal-1-P continues to be produced endogenously (GALT cannot process any galactose from internal sources) → low-level toxicity → cognitive impairments, speech difficulties, and POI in females occur despite best dietary management."},

  {"id":"gal10","question":"The Leloir pathway for galactose metabolism is named after Luis Federico Leloir, who received the 1970 Nobel Prize in Chemistry. The KEY biochemical innovation he identified was:",
   "options":["The role of UDP-galactose as an activated sugar donor","The existence of the galactosidase enzyme","The identification of galactose as a monosaccharide","The discovery that galactose is an epimer of glucose"],
   "answer":0,"explanation":"Leloir discovered nucleotide sugars (UDP-glucose, UDP-galactose, etc.) as the activated intermediates in carbohydrate interconversions. Before Leloir's work, it was unclear how galactose was converted to glycolytic substrates. His Nobel Prize-winning work established nucleotide sugars as universal glycosyl donors."},
],

# ─── Amino Acid Catabolism ───────────────────────────────────────────────────
"amino_acid_catabolism": [
  {"id":"aac01","question":"Which enzyme catalyses the transfer of an amino group from alanine to α-ketoglutarate?","options":["GDH","ALT (Alanine transaminase)","AST","PDC"],"answer":1,"explanation":"ALT (alanine aminotransferase) transfers the amino group from Ala to α-KG, producing pyruvate + glutamate. Elevated ALT is a hallmark of hepatocellular damage."},
  {"id":"aac02","question":"Glutamate dehydrogenase (GDH) releases nitrogen as:","options":["Urea","NH₃ (ammonium)","Carbamoyl phosphate","Aspartate"],"answer":1,"explanation":"GDH oxidatively deaminates glutamate → α-KG + NH₃. The NH₃ enters the urea cycle (in liver) or is excreted (in kidney)."},
  {"id":"aac03","question":"Pyruvate dehydrogenase complex (PDC) requires which vitamin as a cofactor?","options":["Vitamin B12","Thiamine (B1)","Riboflavin only","Biotin"],"answer":1,"explanation":"PDC requires TPP (from B1/thiamine), lipoate, CoA, FAD, and NAD+. Thiamine deficiency → PDC failure → pyruvate and lactate accumulate → Wernicke's encephalopathy."},
  {"id":"aac04","question":"Glucogenic amino acids are those whose carbon skeletons can be converted to:","options":["Acetyl-CoA only","Oxaloacetate or other TCA intermediates → glucose","Acetoacetate or acetyl-CoA","Ketone bodies directly"],"answer":1,"explanation":"Glucogenic AAs enter TCA as OAA, α-KG, succinyl-CoA, fumarate, or as pyruvate, all of which can be used for gluconeogenesis."},
  {"id":"aac05","question":"Which amino acid is BOTH glucogenic AND ketogenic?","options":["Alanine","Leucine","Phenylalanine","Isoleucine"],"answer":2,"explanation":"Phe/Tyr yield fumarate (glucogenic) and acetoacetate (ketogenic). Leucine is purely ketogenic. Isoleucine is also both. Phe is a classic exam example."},
  {"id":"aac06","question":"Aminotransferase reactions require which coenzyme?","options":["NAD+","Pyridoxal phosphate (PLP, B6)","Biotin","Cobalamin (B12)"],"answer":1,"explanation":"PLP (pyridoxal phosphate, the active form of B6) forms a Schiff base with the amino acid substrate in all aminotransferase reactions."},
  {"id":"aac07","question":"Propionyl-CoA carboxylase (PCC) deficiency causes accumulation of:","options":["Methylmalonyl-CoA","Propionyl-CoA → propionic acid","Isovaleric acid","Homocysteine"],"answer":1,"explanation":"PCC converts propionyl-CoA → methylmalonyl-CoA. PCC deficiency → propionic acidaemia: metabolic acidosis, hyperammonaemia, and elevated propionylcarnitine (C3) on acylcarnitine profile."},
  {"id":"aac08","question":"Which is the ONLY purely ketogenic amino acid?","options":["Isoleucine","Phenylalanine","Leucine","Tyrosine"],"answer":2,"explanation":"Leucine is cleaved entirely to acetyl-CoA and acetoacetate — it cannot contribute to gluconeogenesis. Lys is the other purely ketogenic AA."},
],

# ─── Urea Cycle ──────────────────────────────────────────────────────────────
"urea_cycle": [
  {"id":"uc01","question":"CPS-I differs from CPS-II in that CPS-I:","options":["Is cytoplasmic and uses glutamine","Is mitochondrial and uses NH₃, activated by NAG","Uses glutamine and produces carbamoyl-P for pyrimidines","Is found only in kidney"],"answer":1,"explanation":"CPS-I (urea cycle) is mitochondrial, uses free NH₃, and is allosterically activated by N-acetylglutamate (NAG). CPS-II (pyrimidine synthesis) is cytoplasmic and uses glutamine."},
  {"id":"uc02","question":"N-Acetylglutamate (NAG) is synthesised from glutamate and acetyl-CoA by NAGS. What activates NAGS?","options":["Urea","Citrulline","Arginine","Fumarate"],"answer":2,"explanation":"Arginine allosterically activates NAGS, creating a positive feedback loop: as urea cycle flux rises, arginine (its intermediate) stimulates more NAG → more CPS-I activity."},
  {"id":"uc03","question":"OTC deficiency is the most common urea cycle disorder. It is:","options":["Autosomal recessive, affects females more","X-linked; males severely affected, females variably","Autosomal dominant; presents in adults","Mitochondrial inheritance"],"answer":1,"explanation":"OTC deficiency is X-linked. Hemizygous males have severe neonatal hyperammonaemia. Heterozygous females have variable expression (Lyon effect / X-inactivation); some have protein aversion."},
  {"id":"uc04","question":"Orotic acid accumulates in OTC deficiency because:","options":["OTC normally degrades orotic acid","Excess carbamoyl-P leaks to cytoplasm → enters pyrimidine synthesis","Arginine accumulates and inhibits pyrimidine catabolism","Urea inhibits UMP synthase"],"answer":1,"explanation":"Without OTC, carbamoyl phosphate cannot be condensed with ornithine. It leaks out of mitochondria into the cytoplasm where CPS-II/CAD pathway converts it to carbamoyl-aspartate → orotic acid. Urinary orotic acid is a key diagnostic marker for OTC deficiency."},
  {"id":"uc05","question":"The urea cycle net ATP cost per urea molecule is:","options":["0 ATP","1 ATP","3 ATP (2 from CPS-I + 1 from ASS)","6 ATP"],"answer":2,"explanation":"CPS-I uses 2 ATP (forms carbamoyl-P); ASS uses 1 ATP (as PPi). Total = 3 high-energy phosphate bonds consumed per urea synthesised."},
  {"id":"uc06","question":"Fumarate is a byproduct of which urea cycle step?","options":["CPS-I","OTC","ASS (argininosuccinate synthetase)","ASL (argininosuccinate lyase)"],"answer":3,"explanation":"ASL cleaves argininosuccinate → arginine + fumarate. Fumarate enters the TCA cycle (→ malate → OAA), linking the urea cycle and TCA cycle (the 'Krebs bicycle')."},
  {"id":"uc07","question":"Treatment of hyperammonaemia in urea cycle disorders commonly includes sodium benzoate and sodium phenylbutyrate. Their mechanism is:","options":["They directly activate CPS-I","They conjugate with glycine and glutamine to excrete nitrogen in urine","They inhibit glutaminase to reduce NH₃ production","They donate carbamoyl phosphate"],"answer":1,"explanation":"Benzoate conjugates with glycine → hippurate (excreted); phenylbutyrate → phenylacetate conjugates with glutamine → phenylacetylglutamine (excreted). Each excreted molecule removes 1–2 nitrogen atoms, bypassing the urea cycle."},
  {"id":"uc08","question":"Arginase-1 deficiency presents differently from other UCDs because:","options":["It causes severe neonatal hyperammonaemia like OTC deficiency","It presents later with progressive spastic diplegia and cognitive decline; hyperammonaemia is mild","It causes orotic aciduria","It is the only AR urea cycle disorder"],"answer":1,"explanation":"Arginase-1 deficiency causes arginine accumulation (neurotoxic). Patients develop progressive neurological deterioration (spastic diplegia, intellectual disability) without severe neonatal hyperammonaemia. Arginine restriction is the treatment."},
],

# ─── Phenylalanine & Tyrosine ────────────────────────────────────────────────
"phenylalanine_tyrosine": [
  {"id":"pt01","question":"PKU (phenylketonuria) is caused by deficiency of:","options":["Tyrosine hydroxylase","Phenylalanine hydroxylase (PAH)","Fumarylacetoacetase (FAH)","Homogentisate oxidase"],"answer":1,"explanation":"PAH converts Phe to Tyr using BH4 as cofactor. PAH deficiency → Phe accumulates → phenylketones in urine. Treated by Phe-restricted diet + BH4 supplementation (sapropterin) in BH4-responsive PKU."},
  {"id":"pt02","question":"Biopterin (BH4) is a cofactor for PAH. BH4 deficiency (not PAH deficiency) causes:","options":["Classic PKU with normal BH4 response","Malignant hyperphenylalaninaemia with neurological deterioration despite diet","Tyrosinaemia type I","Albinism"],"answer":1,"explanation":"BH4 is also required for tyrosine hydroxylase (dopamine synthesis) and tryptophan hydroxylase (serotonin). BH4 deficiency depletes neurotransmitters → severe neurological deterioration not corrected by Phe restriction alone. Requires BH4 + neurotransmitter precursor supplementation."},
  {"id":"pt03","question":"Tyrosinaemia type I is caused by deficiency of FAH (fumarylacetoacetase). The toxic metabolite is:","options":["Tyrosine","Succinylacetone","Homogentisate","p-Hydroxyphenylpyruvate"],"answer":1,"explanation":"FAH deficiency → succinylacetone accumulates. Succinylacetone inhibits porphobilinogen synthase (ALAD) → secondary porphyria crisis. Also directly hepatotoxic. Treatment: NTBC (nitisinone) inhibits upstream HPPD, preventing succinylacetone production."},
  {"id":"pt04","question":"Catecholamine synthesis from tyrosine begins with which enzyme?","options":["DOPA decarboxylase","PAH","Tyrosine hydroxylase (TH)","DBH (dopamine β-hydroxylase)"],"answer":2,"explanation":"TH converts Tyr → L-DOPA (rate-limiting step of catecholamine synthesis). It requires BH4. L-DOPA → Dopamine (DOPA decarboxylase) → Noradrenaline (DBH) → Adrenaline (PNMT in adrenal medulla)."},
  {"id":"pt05","question":"Alkaptonuria is caused by deficiency of:","options":["PAH","Homogentisate 1,2-dioxygenase","FAH","DOPA decarboxylase"],"answer":1,"explanation":"Homogentisate accumulates → excreted in urine (darkens on standing to black/brown — alkapton). Deposits in cartilage/joints (ochronosis) cause arthritis. The disease described by Archibald Garrod as an 'inborn error of metabolism' in 1902."},
  {"id":"pt06","question":"Melanin is synthesised from tyrosine by:","options":["PAH","Tyrosinase (in melanosomes)","DBH","Tyrosine aminotransferase"],"answer":1,"explanation":"Tyrosinase (CuII-dependent) converts Tyr → DOPA → DOPAquinone, leading to melanin polymers. Tyrosinase deficiency → oculocutaneous albinism (OCA) type I."},
  {"id":"pt07","question":"The product of phenylalanine catabolism that enters the TCA cycle as a glucogenic substrate is:","options":["Acetoacetate","Fumarate","Pyruvate","Malate"],"answer":1,"explanation":"Tyr catabolism (TAT → HPPD → HGO → FAH) produces fumarate (glucogenic) and acetoacetate (ketogenic). Fumarate enters TCA; acetoacetate is a ketone body."},
  {"id":"pt08","question":"Newborn screening for PKU measures:","options":["Urinary phenylketones","Blood phenylalanine by tandem mass spectrometry (MS/MS)","Hair tyrosine","Urine biopterin"],"answer":1,"explanation":"Modern NBS uses MS/MS to quantify Phe (and Phe:Tyr ratio) from dried blood spots. Guthrie bacterial inhibition assay was historical. MS/MS also detects Tyr disorders and other aminoacidopathies simultaneously."},
],

# ─── BCAA Catabolism ─────────────────────────────────────────────────────────
"branched_chain_aa": [
  {"id":"bc01","question":"MSUD (Maple Syrup Urine Disease) is caused by deficiency of:","options":["BCAT (branched-chain aminotransferase)","BCKDH (branched-chain α-keto acid dehydrogenase complex)","Isovaleryl-CoA dehydrogenase","Propionyl-CoA carboxylase"],"answer":1,"explanation":"BCKDH is the E1 component requiring TPP (thiamine). Deficiency → accumulation of branched-chain keto acids (especially the leucine-derived α-ketoisocaproate) → sweet urine odour, neonatal encephalopathy. Treat: BCAA-restricted diet + thiamine."},
  {"id":"bc02","question":"Which BCAA is most toxic in MSUD?","options":["Valine","Leucine","Isoleucine","All equally"],"answer":1,"explanation":"Leucine (and its keto acid α-ketoisocaproate) is most neurotoxic, inhibiting pyruvate dehydrogenase and brain energy metabolism. Emergency management targets lowering leucine first."},
  {"id":"bc03","question":"Isovaleric acidaemia is caused by deficiency of:","options":["BCKDH","Isovaleryl-CoA dehydrogenase (IVD)","Methylmalonyl-CoA mutase","3-Methylcrotonyl-CoA carboxylase"],"answer":1,"explanation":"IVD catalyses the dehydrogenation of isovaleryl-CoA (from Leu catabolism). Deficiency → isovaleric acid accumulates → 'sweaty feet' odour + metabolic acidosis + hyperammonaemia."},
  {"id":"bc04","question":"Methylmalonic acidaemia (MMA) is caused by deficiency of methylmalonyl-CoA mutase, which requires:","options":["Thiamine (B1)","Cobalamin (B12, adenosylcobalamin)","Biotin","Pyridoxal phosphate"],"answer":1,"explanation":"Methylmalonyl-CoA mutase requires adenosylcobalamin (B12 cofactor). Deficiency → methylmalonic acid accumulates → metabolic acidosis, hyperammonaemia, renal damage (methylmalonate is nephrotoxic). B12 supplementation helps in responsive forms."},
  {"id":"bc05","question":"BCAA catabolism in muscle generates nitrogen primarily as:","options":["Free NH₃ released to blood","Alanine (via glucose-alanine cycle)","Glutamine and alanine","Urea directly"],"answer":2,"explanation":"Muscle lacks a full urea cycle. Branched-chain amino groups are transferred to glutamate (via BCAT), then to pyruvate (ALT) → alanine, which transports N safely to the liver (glucose-alanine cycle). Glutamine also carries N to liver/kidney."},
  {"id":"bc06","question":"The glucose-alanine cycle links BCAA catabolism in muscle to gluconeogenesis in liver. In this cycle, liver releases:","options":["BCAA","Glucose (from alanine-derived pyruvate)","Glutamine","Glutamate"],"answer":1,"explanation":"Liver takes up alanine → ALT converts it to pyruvate + glutamate → pyruvate enters gluconeogenesis → glucose released to blood → muscle uses glucose. This elegantly cycles carbon and nitrogen between muscle and liver."},
  {"id":"bc07","question":"BCKDH is regulated identically to PDC. Which kinase inactivates it?","options":["AMPK","BCKDH kinase (BDK)","PKA","PDK1"],"answer":1,"explanation":"BCKDH kinase (BDK) phosphorylates and inactivates BCKDH. BDK is inhibited by BCKA (the substrates) — so when BCKAs accumulate, they relieve BDK inhibition of BCKDH, activating catabolism. Thiamine deficiency impairs both BCKDH and PDC."},
  {"id":"bc08","question":"Propionic acidaemia results from PCC deficiency. Propionyl-CoA can also arise from catabolism of:","options":["Valine and isoleucine only","Val, Ile, Met, Thr, and odd-chain fatty acids","Leucine","Lysine"],"answer":1,"explanation":"Propionyl-CoA is produced from Val, Ile, Met, Thr (glucogenic BCAA catabolism), and from β-oxidation of odd-chain fatty acids. PCC deficiency causes a combined amino acid + fatty acid catabolism disorder."},
],

# ─── Fatty Acid Oxidation ────────────────────────────────────────────────────
"fatty_acid_oxidation": [
  {"id":"fo01","question":"Which enzyme is the rate-limiting gatekeeper of mitochondrial fatty acid oxidation?","options":["ACSL (Acyl-CoA synthetase)","CPT-I (Carnitine Palmitoyl Transferase I)","MCAD","β-Hydroxyacyl-CoA dehydrogenase"],"answer":1,"explanation":"CPT-I is inhibited by malonyl-CoA (the first product of fatty acid synthesis), creating reciprocal regulation: when FA synthesis is active (insulin-stimulated), FA oxidation is blocked. CPT-I deficiency causes hypoketotic hypoglycaemia."},
  {"id":"fo02","question":"MCAD deficiency classically presents as:","options":["Neonatal cardiomyopathy","Hypoketotic hypoglycaemia during fasting, with C8 acylcarnitine elevated","Lactic acidosis with normal blood glucose","Myoglobinuria after exercise"],"answer":1,"explanation":"MCAD (medium-chain acyl-CoA dehydrogenase) deficiency is the commonest FAO disorder. C8 (octanoylcarnitine) on newborn MS/MS screen is diagnostic. Fasting triggers hypoglycaemia because glucose usage continues without ketone backup. Avoid fasting; carnitine supplementation."},
  {"id":"fo03","question":"How many acetyl-CoA molecules are produced from one palmitate (C16)?","options":["6","7","8","16"],"answer":2,"explanation":"β-Oxidation of palmitate (C16) requires 7 cycles, cleaving off 2 carbons each cycle → 8 acetyl-CoA. Formula: n/2 acetyl-CoA for an n-carbon fatty acid."},
  {"id":"fo04","question":"Each cycle of β-oxidation produces:","options":["1 NADH + 1 ATP","1 FADH₂ + 1 NADH + 1 Acetyl-CoA","2 FADH₂ + 1 Acetyl-CoA","1 NADH + 1 FADH₂ only"],"answer":1,"explanation":"One β-oxidation cycle: acyl-CoA dehydrogenase (→ FADH₂), enoyl-CoA hydratase, β-hydroxyacyl-CoA dehydrogenase (→ NADH), thiolase (→ acetyl-CoA). No direct ATP produced; FADH₂ and NADH feed ETC."},
  {"id":"fo05","question":"The energy cost to activate a fatty acid to fatty acyl-CoA is:","options":["1 ATP → 1 ADP + Pi","1 ATP → AMP + PPi (= 2 ATP equivalents)","2 NADH","No cost"],"answer":1,"explanation":"Acyl-CoA Synthetase (ACSL) couples ATP → AMP + PPi (pyrophosphate). PPi is immediately hydrolysed by pyrophosphatase → 2 Pi (drives reaction forward). Net cost = 2 ATP equivalents (since AMP must be doubly phosphorylated back to ATP by adenylate kinase + ATP)."},
  {"id":"fo06","question":"Malonyl-CoA inhibits CPT-I. Malonyl-CoA is produced by:","options":["FAS (Fatty Acid Synthase)","ACC (Acetyl-CoA carboxylase), activated by insulin","AMPK directly","Citrate synthase"],"answer":1,"explanation":"ACC (acetyl-CoA carboxylase) converts acetyl-CoA → malonyl-CoA. Insulin activates ACC; AMPK phosphorylates and inactivates ACC. This means when energy is abundant (insulin high), CPT-I is inhibited and FA oxidation is suppressed."},
  {"id":"fo07","question":"Jamaican vomiting sickness (from unripe ackee fruit) inhibits which enzyme?","options":["CPT-I","MCAD","SCAD","β-Hydroxyacyl-CoA dehydrogenase (HADH)"],"answer":1,"explanation":"Hypoglycin A (from unripe ackee) is metabolised to MCPA-CoA, which irreversibly inhibits MCAD (and several other acyl-CoA dehydrogenases). Clinically mimics MCAD deficiency: vomiting, hypoketotic hypoglycaemia, potentially fatal."},
  {"id":"fo08","question":"In β-oxidation of an unsaturated fatty acid (e.g. oleate, C18:1 Δ9), an additional enzyme is required:","options":["Enoyl-CoA isomerase","A second thiolase","MCAD instead of LCAD","An extra NADPH"],"answer":0,"explanation":"The double bond in oleate is in the cis configuration at Δ9. After 3 cycles of β-oxidation, cis-Δ3-enoyl-CoA appears. Enoyl-CoA isomerase converts it to trans-Δ2-enoyl-CoA (the normal β-oxidation substrate). Odd-numbered double bonds: need 2,4-dienoyl-CoA reductase additionally."},
],

# ─── Ketogenesis ─────────────────────────────────────────────────────────────
"ketogenesis": [
  {"id":"kg01","question":"Ketogenesis occurs exclusively in:","options":["Astrocytes","Hepatocyte mitochondria","Skeletal muscle","Kidney cortex"],"answer":1,"explanation":"Only liver mitochondria contain sufficient HMGCS2 (mitochondrial HMG-CoA synthase) and HMGCL for ketogenesis. The liver paradoxically CANNOT utilise ketone bodies (lacks SCOT)."},
  {"id":"kg02","question":"Why can the liver not use its own ketone bodies?","options":["Lacks BDH1","Lacks SCOT (succinyl-CoA oxoacid transferase)","Lacks acetyl-CoA","Lacks thiolase"],"answer":1,"explanation":"SCOT (OXCT1) is absent in adult liver. SCOT activates acetoacetate by transferring CoA from succinyl-CoA → AcAcCoA. Without SCOT, the liver cannot re-activate acetoacetate for TCA entry."},
  {"id":"kg03","question":"In alcoholic ketoacidosis, blood β-OHB is very high but urine ketostix is negative/weakly positive. This is because:","options":["Ketostix measures only β-OHB","Ethanol-induced high NADH drives BDH1 to convert all AcAc → β-OHB; ketostix measures AcAc only","Methanol interferes with the test","Alcohol depletes ketones"],"answer":1,"explanation":"Ethanol metabolism produces massive NADH → BDH1 equilibrium shifts to β-OHB production. Standard ketostix (nitroprusside) detects acetoacetate only. β-OHB is not detected → falsely negative. Always measure serum β-OHB directly in suspected alcoholic ketoacidosis."},
  {"id":"kg04","question":"DKA management: insulin is the primary treatment because it:","options":["Directly neutralises ketone bodies","Restores glucose uptake AND suppresses lipolysis and hepatic ketogenesis","Activates SCOT in peripheral tissues","Provides bicarbonate"],"answer":1,"explanation":"Insulin simultaneously restores glucose utilisation in peripheral tissues, inhibits hormone-sensitive lipase (reduces FFA supply to liver), and suppresses glucagon (reducing malonyl-CoA depletion and HMGCS2 expression). Bicarbonate is reserved for pH < 6.9."},
  {"id":"kg05","question":"The ketogenic diet (used in epilepsy) works by providing ketones as brain fuel while restricting:","options":["Fat","Protein only","Carbohydrates (to suppress insulin and raise glucagon)","Sodium"],"answer":2,"explanation":"The ketogenic diet is very high fat, very low carbohydrate. Low carbs → low insulin → high glucagon → CPT-I uninhibited → FA oxidation → ketones. Ketones provide > 60% of brain energy after adaptation. Mechanism of seizure reduction is multifactorial."},
  {"id":"kg06","question":"HMGCS2 is activated (post-translationally) by:","options":["Insulin-mediated phosphorylation","SIRT3-mediated desuccinylation","AMPK-mediated phosphorylation","mTOR pathway"],"answer":1,"explanation":"SIRT3 (mitochondrial deacylase) removes succinyl groups from HMGCS2 lysine residues during fasting → HMGCS2 is activated. This NAD+-dependent sirtuin activation links energy sensing (NAD+ levels rise in fasting) to ketogenesis induction."},
],

# ─── Fatty Acid Synthesis ─────────────────────────────────────────────────────
"fatty_acid_synthesis": [
  {"id":"fs01","question":"The rate-limiting enzyme of de novo lipogenesis (DNL) is:","options":["Fatty Acid Synthase (FASN)","Acetyl-CoA Carboxylase (ACC)","ATP Citrate Lyase (ACLY)","Malic enzyme"],"answer":1,"explanation":"ACC converts acetyl-CoA → malonyl-CoA (committing carbon to FA synthesis). ACC is activated by insulin (dephosphorylation), citrate (allosteric), and inhibited by AMPK (phosphorylation) and malonyl-CoA's product (palmitate-CoA)."},
  {"id":"fs02","question":"Acetyl-CoA for fatty acid synthesis is generated in mitochondria but cannot cross the inner membrane. It exits as:","options":["Malonyl-CoA","Citrate (via citrate shuttle) → regenerated by ACLY in cytoplasm","Acetyl-carnitine","Acetate only"],"answer":1,"explanation":"Citrate synthase condenses OAA + AcCoA → citrate in mitochondria. Citrate crosses the inner membrane via CIC (citrate carrier). ACLY (ATP citrate lyase) cleaves cytoplasmic citrate → OAA + AcCoA. ACLY is the key link between TCA and lipogenesis."},
  {"id":"fs03","question":"How many malonyl-CoA molecules are used to synthesise one palmitate (C16) from acetyl-CoA?","options":["6","7","8","14"],"answer":1,"explanation":"Palmitate synthesis: 1 acetyl-CoA (starter) + 7 malonyl-CoA (each adds 2C after CO2 loss) = 16C. FASN catalyses all 7 condensation-reduction cycles."},
  {"id":"fs04","question":"Malonyl-CoA has a dual role: it is the substrate for FAS AND it:","options":["Activates CPT-I","Inhibits CPT-I (preventing FA entry into mitochondria for oxidation)","Activates AMPK","Stimulates ketogenesis"],"answer":1,"explanation":"This reciprocal regulation ensures that FA synthesis and FA oxidation do not run simultaneously (futile cycle). When insulin is high and malonyl-CoA is elevated, CPT-I is blocked → FA oxidation stops; synthesis proceeds."},
  {"id":"fs05","question":"NADPH for FA synthesis is primarily supplied by:","options":["Complex I (NADH→NADPH)","HMP shunt (G6PD) and malic enzyme","Isocitrate dehydrogenase","Glutamate dehydrogenase"],"answer":1,"explanation":"Two NADPH per cycle (for β-ketoacyl reduction + enoyl reduction). Total 14 NADPH for palmitate. Sources: G6PD (HMP shunt, oxidative phase: 2 NADPH per G6P) and malic enzyme (malate → pyruvate + NADPH, cytoplasmic)."},
  {"id":"fs06","question":"Non-alcoholic fatty liver disease (NAFLD) is linked to increased DNL because:","options":["Fat intake alone overwhelms the liver","Hyperinsulinaemia (insulin resistance) activates SREBP-1c → upregulates ACC and FASN","Glucagon directly activates FASN","Fructose exclusively causes hepatic fat accumulation"],"answer":1,"explanation":"Insulin resistance → compensatory hyperinsulinaemia → hepatic insulin signalling for lipogenesis remains intact (selective insulin resistance) → SREBP-1c transcription factor activates ACC, FASN, SCD-1 → excess TG synthesis → NAFLD."},
],

# ─── Cholesterol Synthesis ────────────────────────────────────────────────────
"cholesterol_synthesis": [
  {"id":"cs01","question":"The rate-limiting enzyme of cholesterol synthesis and the primary target of statins is:","options":["Squalene synthase","HMG-CoA Reductase (HMGCR)","Mevalonate kinase","Lanosterol synthase"],"answer":1,"explanation":"HMGCR converts HMG-CoA → mevalonate. It is under tight feedback control by cholesterol (via SCAP-SREBP-2 pathway) and is the target of statins (competitive inhibitors), which reduce LDL-C by 30–55%."},
  {"id":"cs02","question":"Statins reduce plasma LDL not only by direct cholesterol synthesis inhibition but mainly by:","options":["Activating LPL","Upregulating hepatic LDLR via SCAP/SREBP-2 pathway","Blocking PCSK9 secretion","Increasing HDL cholesterol directly"],"answer":1,"explanation":"Statins deplete hepatic cholesterol → SCAP-INSIG complex releases SCAP bound to SREBP-2 → SREBP-2 translocates to nucleus → transcribes LDLR → more LDL receptors on hepatocytes → increased LDL clearance from plasma."},
  {"id":"cs03","question":"Smith-Lemli-Opitz (SLO) syndrome is caused by deficiency of:","options":["HMGCR","DHCR7 (7-dehydrocholesterol reductase)","Mevalonate kinase","CYP51A1"],"answer":1,"explanation":"DHCR7 converts 7-dehydrocholesterol → cholesterol (last step). Deficiency → 7-DHC accumulates + cholesterol deficient → multiple congenital abnormalities (2nd/3rd toe syndactyly, intellectual disability, holoprosencephaly). Diagnose: elevated 7-DHC in plasma."},
  {"id":"cs04","question":"Non-sterol products of the mevalonate pathway include all EXCEPT:","options":["Coenzyme Q10 (ubiquinone)","Dolichol (for N-glycosylation)","Farnesyl pyrophosphate (for protein prenylation)","Arachidonic acid (eicosanoid precursor)"],"answer":3,"explanation":"Arachidonic acid is an omega-6 fatty acid (from membrane phospholipids), not from the mevalonate pathway. CoQ10, dolichol, and geranylgeranyl/farnesyl pyrophosphate (for small GTPase prenylation like Ras, Rho) are all derived from mevalonate."},
  {"id":"cs05","question":"PCSK9 inhibitors (evolocumab, alirocumab) lower LDL by:","options":["Directly inhibiting HMGCR","Preventing PCSK9 from binding LDLR → LDLR is not degraded → more surface LDLR","Activating LPL","Reducing intestinal cholesterol absorption"],"answer":1,"explanation":"PCSK9 binds surface LDLR after LDL delivery to lysosomes → targets LDLR for lysosomal degradation instead of recycling. Anti-PCSK9 mAbs prevent this → LDLR recycles to cell surface → further 50–60% LDL reduction on top of statins."},
  {"id":"cs06","question":"Bile acid synthesis from cholesterol uses cholesterol as substrate and is regulated by FXR (farnesoid X receptor). When bile acids are abundant:","options":["FXR activates CYP7A1 (increases bile acid synthesis)","FXR inhibits CYP7A1 via SHP → reduces cholesterol conversion to bile acids","FXR activates HMGCR","FXR stimulates PCSK9 production"],"answer":1,"explanation":"FXR (activated by bile acids) → induces SHP (short heterodimer partner) → SHP represses LRH-1 → LRH-1 normally transactivates CYP7A1 → CYP7A1 (rate-limiting for bile acid synthesis) is suppressed. Classic negative feedback loop."},
],

# ─── Lipoprotein Metabolism ───────────────────────────────────────────────────
"lipoprotein_metabolism": [
  {"id":"lp01","question":"Lipoprotein lipase (LPL) cleaves TG from circulating lipoproteins. LPL is activated by:","options":["ApoB-100","ApoC-II (on chylomicrons and VLDL)","ApoE","ApoA-I"],"answer":1,"explanation":"ApoC-II is the obligate activator of LPL. LPL deficiency or ApoC-II deficiency → severe hypertriglyceridaemia, eruptive xanthomas, pancreatitis. ApoC-III inhibits LPL (counter-regulatory)."},
  {"id":"lp02","question":"Familial Hypercholesterolaemia (FH) is most commonly caused by:","options":["PCSK9 loss-of-function","LDLR loss-of-function mutations","LPL deficiency","ApoB deficiency"],"answer":1,"explanation":"LDLR mutations (>2000 known) cause most FH. Heterozygous FH: LDL 5–10 mmol/L, tendon xanthomas, premature CAD. Homozygous FH: LDL > 13 mmol/L, aortic stenosis in childhood. ApoB mutations also cause FH-like phenotype."},
  {"id":"lp03","question":"HDL performs reverse cholesterol transport (RCT). The rate-limiting step of RCT is:","options":["LPL-mediated TG hydrolysis","LCAT (lecithin-cholesterol acyltransferase) — converts free cholesterol on HDL to cholesterol esters","ApoE mediating HDL clearance","CETP transferring CE from HDL to LDL"],"answer":1,"explanation":"LCAT (activated by ApoA-I) esterifies free cholesterol on nascent HDL → cholesterol esters → form HDL core → HDL matures from disc to sphere → can transport more cholesterol. LCAT deficiency → corneal opacities, anaemia (abnormal RBC membranes), renal failure."},
  {"id":"lp04","question":"PCSK9 gain-of-function mutations cause:","options":["Low LDL","Familial hypercholesterolaemia phenotype (elevated LDL)","Hypertriglyceridaemia","HDL deficiency"],"answer":1,"explanation":"PCSK9 GoF → excessive LDLR degradation → reduced LDL clearance → FH phenotype. Conversely, PCSK9 LoF mutations (some West Africans) → very low lifelong LDL → 90% reduction in CHD risk (landmark natural experiment supporting PCSK9 inhibitor development)."},
  {"id":"lp05","question":"Tangier disease is caused by mutations in:","options":["LDLR","ABCA1 (ATP-binding cassette transporter A1)","LPL","CETP"],"answer":1,"explanation":"ABCA1 exports cholesterol from macrophages to lipid-poor ApoA-I (forming nascent HDL). ABCA1 loss-of-function → cholesterol accumulates in macrophages (foam cells) → lipid-laden tonsillar tissue (orange tonsils — pathognomonic), peripheral neuropathy, very low HDL."},
  {"id":"lp06","question":"The ApoE ε4 allele is the strongest genetic risk factor for late-onset Alzheimer's disease. In lipoprotein metabolism, ApoE primarily mediates:","options":["LPL activation","Receptor-mediated clearance of chylomicron remnants and IDL via LDLR/LRP1","LCAT activation","HDL biogenesis"],"answer":1,"explanation":"ApoE (especially ApoE3/E4 on chylomicron remnants and VLDL/IDL) binds LDLR and LRP1 on hepatocytes → remnant clearance. ApoE4 also impairs amyloid-β clearance in brain → AD risk. ApoE2 → dysbetalipoproteinaemia (type III hyperlipidaemia) due to poor receptor binding."},
  {"id":"lp07","question":"Ezetimibe reduces LDL by:","options":["Inhibiting HMGCR","Inhibiting NPC1L1 (Niemann-Pick C1-Like 1) in the intestinal brush border → less cholesterol absorption","Activating bile acid synthesis","Blocking CETP"],"answer":1,"explanation":"NPC1L1 mediates dietary and biliary cholesterol absorption at the enterocyte brush border. Ezetimibe selectively inhibits this transporter → 15–20% additional LDL reduction. Highly effective combined with statins (IMPROVE-IT trial)."},
],

# ─── Purine Synthesis ─────────────────────────────────────────────────────────
"purine_synthesis": [
  {"id":"ps01","question":"The rate-limiting step of purine de novo synthesis is catalysed by:","options":["IMPDH","PPAT (PRPP amidotransferase)","ADSS","ATIC"],"answer":1,"explanation":"PPAT (AKA GPAT) catalyses PRPP + Gln → phosphoribosylamine (PRA) — the committed first step. It is feedback-inhibited by AMP, ADP, GMP, and GDP (end-product inhibition)."},
  {"id":"ps02","question":"Mycophenolate mofetil (MMF) suppresses the immune system by inhibiting:","options":["PPAT","IMPDH (inosine monophosphate dehydrogenase)","ADSL","DHFR"],"answer":1,"explanation":"IMPDH converts IMP → XMP → GMP branch rate-limiting step. Lymphocytes rely heavily on IMPDH2 for GTP synthesis; other cells use salvage. MMF → MPA → non-competitive IMPDH inhibitor → lymphocyte depletion. Used in transplant, lupus nephritis."},
  {"id":"ps03","question":"Methotrexate inhibits purine synthesis by:","options":["Directly inhibiting PPAT","Inhibiting DHFR → depleting THF → blocking formyl-THF donors for GART and ATIC","Blocking PRPP synthesis","Inhibiting IMPDH"],"answer":1,"explanation":"Methotrexate (MTX) competitively inhibits DHFR → polyglutamated MTX stays in cell → THF depleted → 10-formyl-THF unavailable for steps 3 and 9 of purine synthesis (GART, ATIC) → purine starvation → cell death."},
  {"id":"ps04","question":"The purine ring is built upon which sugar-phosphate backbone?","options":["Ribose-5-phosphate (R5P) provided by HMP shunt","Deoxyribose-phosphate","Mannose-6-phosphate","Fructose-6-phosphate"],"answer":0,"explanation":"PRPP (phosphoribosyl pyrophosphate) is formed from R5P (via PRPS: R5P + 2ATP → PRPP). For purines, PRPP is the first substrate; the ring is built ON PRPP. For pyrimidines, PRPP is added AFTER the ring is complete (at UMPS step)."},
  {"id":"ps05","question":"AMP and GMP cross-regulate their own synthesis to maintain balance. Which is correct?","options":["High AMP inhibits IMPDH (GMP branch); high GMP inhibits ADSS (AMP branch)","High AMP inhibits ADSS; high GMP inhibits IMPDH","Both inhibit PPAT equally","Neither inhibits the other's branch"],"answer":0,"explanation":"Cross-regulation: excess AMP → inhibits ADSS (prevents more AMP from IMP), pushing IMP to GMP branch; excess GMP → inhibits IMPDH (prevents more GMP from IMP), pushing IMP to AMP branch. Elegant balancing mechanism."},
  {"id":"ps06","question":"IMP is the branch point for AMP vs GMP synthesis. AMP synthesis requires GTP as energy source; GMP synthesis requires ATP. This ensures:","options":["Both branches always run at maximum rate","Balance: when purine pools are high, synthesis of either requires use of the other, creating natural cross-regulation","GMP is always made in excess","AMP synthesis is faster"],"answer":1,"explanation":"This reciprocal energy requirement adds another layer of balance: AMP synthesis (ADSS) uses GTP → depletes GMP slightly → relieves GMP inhibition of IMPDH → GMP branch can recover, and vice versa."},
],

# ─── Pyrimidine Synthesis ─────────────────────────────────────────────────────
"pyrimidine_synthesis": [
  {"id":"pyr01","question":"The key difference between pyrimidine and purine de novo synthesis is:","options":["Purines use PRPP first; pyrimidines build the ring first then add PRPP (via UMPS)","Both pathways are identical","Pyrimidines use more ATP","Purines build the ring on an amino acid scaffold"],"answer":0,"explanation":"Purines: PRPP is attached first (step 1, PPAT), then the imidazole+pyrimidine ring is elaborated on the ribose backbone. Pyrimidines: ring is assembled first (CAD steps), then PRPP is added at UMPS (OPRT). This is a classic exam distinction."},
  {"id":"pyr02","question":"DHODH is unique among pyrimidine synthesis enzymes because:","options":["It uses ATP","It is the only mitochondrial enzyme in the pathway","It requires PRPP","It only works in kidney"],"answer":1,"explanation":"DHODH (dihydroorotate dehydrogenase) is embedded in the inner mitochondrial membrane and oxidises DHO → orotate using CoQ (ubiquinone) as electron acceptor, coupling pyrimidine synthesis to the ETC. Leflunomide/teriflunomide inhibit DHODH."},
  {"id":"pyr03","question":"5-Fluorouracil (5-FU) is activated to 5-FdUMP, which then inhibits TYMS by:","options":["Competitive inhibition with dUMP","Forming a covalent ternary complex with TYMS and 5,10-methylene-THF (irreversible)","Depleting folate","Inhibiting DHFR"],"answer":1,"explanation":"5-FdUMP forms a covalent ternary complex (5-FdUMP + TYMS + CH₂-THF) → TYMS irreversibly trapped → no dTMP synthesis → thymineless death. Leucovorin (folinic acid → CH₂-THF) potentiates 5-FU by stabilising this complex."},
  {"id":"pyr04","question":"Leflunomide is used in rheumatoid arthritis; its active metabolite teriflunomide is used in multiple sclerosis. Both work by:","options":["Inhibiting IMPDH","Inhibiting DHODH → depleting pyrimidines in rapidly dividing lymphocytes","Inhibiting TYMS","Blocking CAD (CPS-II)"],"answer":1,"explanation":"Brain-infiltrating lymphocytes in MS and synovial lymphocytes in RA rely on pyrimidine de novo synthesis. DHODH inhibition specifically targets these high-turnover lymphocyte populations while sparing resting cells that use salvage."},
  {"id":"pyr05","question":"Hereditary orotic aciduria (UMPS deficiency) is treated with:","options":["Allopurinol","Uridine supplementation (bypasses the UMPS defect)","Leucovorin","NTBC"],"answer":1,"explanation":"UMPS (OPRT + OMP decarboxylase) converts orotate → UMP. Exogenous uridine bypasses the defect: uridine → UMP (via uridine kinase). This corrects the megaloblastic anaemia and reduces orotic acid excretion. Distinguish from OTC deficiency which also causes orotic aciduria but has hyperammonaemia."},
  {"id":"pyr06","question":"DPYD (dihydropyrimidine dehydrogenase) deficiency is clinically relevant because:","options":["It causes uracil kidney stones","It causes severe 5-FU toxicity (as 5-FU is normally degraded by DPYD)","It causes orotic aciduria","It causes megaloblastic anaemia"],"answer":1,"explanation":"DPYD is the rate-limiting enzyme of pyrimidine catabolism. ~5% Caucasians have heterozygous DPYD variants. Reduced DPYD → 5-FU accumulates → severe bone marrow suppression, mucositis, diarrhoea. CPIC recommends DPYD genotyping before fluoropyrimidine therapy."},
],

# ─── Purine Salvage ───────────────────────────────────────────────────────────
"purine_salvage": [
  {"id":"sv01","question":"HGPRT (hypoxanthine-guanine phosphoribosyltransferase) salvages hypoxanthine and guanine using:","options":["ATP","PRPP (phosphoribosyl pyrophosphate)","SAM","CDP"],"answer":1,"explanation":"HGPRT: Hx + PRPP → IMP + PPi; Gua + PRPP → GMP + PPi. PRPP is consumed (unlike de novo synthesis where PRPP is the backbone). This is energetically efficient: 1 PRPP (≈2 ATP) vs 5 ATP for de novo IMP."},
  {"id":"sv02","question":"Lesch-Nyhan syndrome (HGPRT deficiency) is characterised by all EXCEPT:","options":["Uric acid overproduction and gout","Self-mutilating behaviour (lip/finger biting)","Spastic cerebral palsy and choreoathetosis","Hepatosplenomegaly and jaundice"],"answer":3,"explanation":"Lesch-Nyhan: gout (hyperuricaemia), dystonia/choreoathetosis, intellectual disability, and compulsive self-mutilation. Hepatosplenomegaly is NOT a feature. The neurological features are not corrected by allopurinol (which treats gout only)."},
  {"id":"sv03","question":"ADA-SCID (adenosine deaminase deficiency) causes SCID because:","options":["Adenosine activates T cell apoptosis directly","dATP accumulates and inhibits ribonucleotide reductase → blocks dNTP synthesis → lymphocyte death","ADA normally produces thymine","NH₃ from ADA toxifies lymphocytes"],"answer":1,"explanation":"ADA deficiency → deoxyAdenosine accumulates → phosphorylated to dATP in lymphocytes (high deoxynucleoside kinase activity) → dATP inhibits RNR (ribonucleotide reductase) → all dNTP synthesis blocked → DNA synthesis impossible → apoptosis. T, B, and NK cells all affected."},
  {"id":"sv04","question":"APRT deficiency causes kidney stones composed of:","options":["Uric acid","2,8-Dihydroxyadenine (2,8-DHA)","Cystine","Calcium oxalate"],"answer":1,"explanation":"Without APRT, adenine cannot be salvaged → xanthine oxidase converts adenine → 2,8-dihydroxyadenine (2,8-DHA). Highly insoluble → radiopaque kidney stones. Mimic uric acid stones clinically but do NOT dissolve with allopurinol/alkalinisation. Mass spec identification is essential."},
  {"id":"sv05","question":"Adenosine kinase (AK) is the primary route for intracellular adenosine clearance. Under ischaemia, AK is inhibited, which:","options":["Causes adenosine toxicity","Allows adenosine to accumulate → acts on A1/A2 receptors → cardioprotective/neuroprotective signalling","Depletes ATP stores rapidly","Activates purine de novo synthesis"],"answer":1,"explanation":"Ischaemia → ATP → ADP → AMP → adenosine (by 5'-NT). High adenosine → A1 receptors on cardiac myocytes → reduced heart rate, preconditioning. A2 receptors on coronary vessels → vasodilation. This adenosine surge is an endogenous cardioprotective mechanism exploited by adenosine in AVNRT treatment."},
],

# ─── Nucleotide Degradation ───────────────────────────────────────────────────
"nucleotide_degradation": [
  {"id":"nd01","question":"Xanthine oxidase (XO) catalyses the final two steps of purine degradation. Its end-product in humans is:","options":["Allantoin","Xanthine","Uric acid","Hypoxanthine"],"answer":2,"explanation":"Humans lack uricase (unlike most mammals), so uric acid is the final end-product of purine catabolism. Normal serum urate: < 6.0 mg/dL (women), < 7.0 mg/dL (men). Above 6.8 mg/dL → supersaturation → crystal deposition."},
  {"id":"nd02","question":"Allopurinol reduces uric acid because it is:","options":["A uricase enzyme replacement","Converted to oxypurinol by XO, which then inhibits XO irreversibly","A competitive inhibitor of HGPRT","A direct xanthine chelator"],"answer":1,"explanation":"Allopurinol (xanthine analogue) is a 'suicide substrate': XO oxidises it to oxypurinol (alloxanthine), which remains tightly bound to the reduced form of XO → irreversible inactivation. Hypoxanthine and xanthine accumulate instead (more soluble than urate)."},
  {"id":"nd03","question":"Rasburicase is used for tumour lysis syndrome (TLS). Its mechanism is:","options":["Inhibits XO","Recombinant uricase — converts urate → allantoin (soluble, excreted)","Chelates uric acid","Inhibits purine de novo synthesis"],"answer":1,"explanation":"Humans evolved to lose uricase (possibly as an antioxidant advantage — urate is an antioxidant). Rasburicase re-introduces uricase activity: urate → allantoin (5–10× more soluble). Given prophylactically/therapeutically in TLS (haematological malignancies post-chemotherapy) to prevent acute urate nephropathy. Contraindicated in G6PD deficiency (H₂O₂ generated)."},
  {"id":"nd04","question":"PNP (purine nucleoside phosphorylase) deficiency causes selective T-cell SCID because:","options":["PNP is only expressed in T cells","dGTP accumulates specifically in T cells (high deoxynucleoside kinase levels) → inhibits RNR → T cell death","PNP deficiency directly destroys the thymus","B cells undergo apoptosis via Fas pathway"],"answer":1,"explanation":"Unlike ADA-SCID where all lymphocytes die, PNP deficiency affects T cells preferentially. dGuanosine accumulates → phosphorylated → dGTP toxic to T cells (T cells have high TdK/7 kinase activity). B cells tolerate dGuanosine better. Clinical: normal Ig levels initially but absent T cells and cellular immunity."},
  {"id":"nd05","question":"Gout is characterised by monosodium urate (MSU) crystal deposition. The classic joint affected in podagra is:","options":["Knee","First metatarsophalangeal (MTP) joint (big toe)","Ankle","Wrist"],"answer":1,"explanation":"First MTP joint is the classic site due to combination of high pressure, low temperature (periphery), and local trauma → urate supersaturation and crystallisation. Colchicine (microtubule inhibitor → blocks neutrophil migration) is the first-line acute treatment."},
  {"id":"nd06","question":"Febuxostat differs from allopurinol in that:","options":["It inhibits HGPRT not XO","It is a non-purine selective XO inhibitor; does not require HGPRT activation and is renally safe","It is a uricase","It blocks renal urate secretion"],"answer":1,"explanation":"Allopurinol is a purine analogue (requires activation by HGPRT → oxypurinol). Febuxostat is a non-purine, selective XO inhibitor → works even in HGPRT-deficient patients (e.g. Lesch-Nyhan). More potent than standard allopurinol doses. Use with caution in cardiovascular disease (CARES trial signal)."},
  {"id":"nd07","question":"DPYD genotyping before 5-FU/capecitabine is recommended because DPYD variants cause:","options":["Reduced 5-FU activation → treatment failure","Reduced 5-FU catabolism → drug accumulation → severe toxicity (myelosuppression, mucositis)","Increased orotic acid","Reduced uridine availability"],"answer":1,"explanation":"~5% of Caucasians carry heterozygous DPYD loss-of-function variants (most common: DPYD*2A, c.2846A>T). CPIC/DPWG guidelines recommend dose reduction 25–50% in heterozygotes; avoid in homozygotes. Testing prevents life-threatening fluoropyrimidine toxicity."},
],


# ─── Integrated Metabolism (Cross-Pathway) ───────────────────────────────────
"integrated_metabolism": [
  {"id":"im01","question":"After an overnight fast, which is the PRIMARY source of blood glucose in healthy adults?","options":["Hepatic glycogenolysis","Gluconeogenesis from alanine","Intestinal absorption","Renal glucose production"],"answer":0,"explanation":"After 8–12 hours of fasting, hepatic glycogen stores (≈70–80 g) supply most blood glucose via glycogenolysis. After 24–48 hours, glycogen is depleted and gluconeogenesis (mainly from alanine, lactate, glycerol) becomes dominant. This transition is the basis of the Cori cycle."},

  {"id":"im02","question":"The Cori cycle shuttles lactate from muscle to liver. This cycle:","options":["Generates net ATP across the whole body","Is ATP-negative overall but allows muscle to work anaerobically while liver bears the gluconeogenic cost","Produces glucose without any energy expenditure","Is only active in aerobic exercise"],"answer":1,"explanation":"In the Cori cycle: muscle converts glucose → lactate (anaerobic glycolysis) gaining 2 ATP; liver converts lactate → glucose (gluconeogenesis) costing 6 ATP. Net: −4 ATP across the body. This is why sustained anaerobic exercise can continue temporarily — liver absorbs the energetic debt."},

  {"id":"im03","question":"Malonyl-CoA is made by ACC1 in the cytoplasm. Its dual role in metabolism is:","options":["Substrate for cholesterol and ketone body synthesis","Substrate for fatty acid elongation AND allosteric inhibitor of CPT1 (preventing simultaneous β-oxidation)","Activator of AMPK","Inhibitor of acetyl-CoA carboxylase"],"answer":1,"explanation":"Malonyl-CoA is the carbon donor for FASN (fatty acid synthesis) and simultaneously inhibits CPT1 at the outer mitochondrial membrane, preventing acyl-CoA entry into the mitochondria. This ensures fatty acid synthesis and oxidation cannot run at the same time — a key metabolic switch."},

  {"id":"im04","question":"During DKA (diabetic ketoacidosis), blood pH falls because:","options":["Glucose acidifies directly","Ketone bodies (acetoacetate, β-OHB) are weak acids that donate H⁺ in the buffer range, overwhelming bicarbonate","High lactate displaces bicarbonate","Hyperglycaemia directly causes acidosis"],"answer":1,"explanation":"Acetoacetate (pKa 3.8) and β-hydroxybutyrate (pKa 4.7) partially dissociate at physiological pH, consuming bicarbonate buffer → anion gap metabolic acidosis. The high anion gap (Na⁺ − Cl⁻ − HCO₃⁻ > 12) is accounted for by the accumulating ketoanions."},

  {"id":"im05","question":"The glucose-alanine cycle (Felig cycle) connects muscle and liver. The muscle exports alanine because:","options":["Alanine is the only amino acid that can cross the blood-muscle barrier","BCAA catabolism in muscle generates amino groups (via BCAT) that are transaminated onto pyruvate → alanine for safe nitrogen transport to liver","Alanine is synthesised de novo in muscle","Glutamine is unavailable during exercise"],"answer":1,"explanation":"During exercise/fasting: BCAAs catabolised in muscle → amino groups transferred to α-KG → glutamate → then transaminated to pyruvate (ALT) → alanine. Alanine carries nitrogen safely to liver for urea cycle + provides pyruvate carbon for gluconeogenesis. A two-way glucose-alanine shuttle."},

  {"id":"im06","question":"Insulin and glucagon are 'reciprocal' regulators. Which combination is correct?","options":["Insulin activates glycolysis; glucagon activates glycolysis","Insulin: activates GS, PFK-2, PK; glucagon: activates GP, PEPCK, FBPase-2 (phosphatase domain)","Glucagon activates GS; insulin activates GP","Both activate ACC"],"answer":1,"explanation":"Insulin promotes anabolic storage (glycogenesis, glycolysis, lipogenesis, protein synthesis). Glucagon promotes catabolic release (glycogenolysis, gluconeogenesis, β-oxidation, ketogenesis). The bifunctional PFK-2/FBPase-2 enzyme is the classic example: insulin phosphatase activates PFK-2 domain (↑F2,6BP → glycolysis); glucagon/PKA activates FBPase-2 domain (↓F2,6BP → gluconeogenesis)."},

  {"id":"im07","question":"AMPK (AMP-activated protein kinase) is the 'master energy sensor'. When activated (low energy), AMPK simultaneously:","options":["Activates FA synthesis and inhibits β-oxidation","Inhibits ACC1 (↓malonyl-CoA → ↑FAO), HMGCR, and glycogen synthase; activates CPT1, glucose uptake (GLUT4)","Activates protein synthesis","Stimulates cholesterol synthesis"],"answer":1,"explanation":"AMPK is activated when AMP:ATP ratio rises. It phosphorylates and INACTIVATES: ACC1 (→↓malonyl-CoA→↑FAO), HMGCR (↓cholesterol synthesis), GS (↓glycogenesis), PFKFB3 (in some contexts). It activates catabolic processes. Metformin and AICAR (exercise training) work partly via AMPK. Exercise training adapts this response."},

  {"id":"im08","question":"Why can the brain survive on ketone bodies during prolonged starvation but NOT on fatty acids?","options":["Fatty acids are too large to be catabolised","The blood-brain barrier is impermeable to fatty acids; ketone bodies (water-soluble, small) cross freely","Neurons lack mitochondria","Neurons cannot perform β-oxidation due to absence of CPT1 in brain"],"answer":1,"explanation":"Long-chain fatty acids are bound to albumin and cannot cross the intact blood-brain barrier. Ketone bodies (β-hydroxybutyrate, acetoacetate) are small, water-soluble, monocarboxylates (MCT1/MCT2 transporters) → cross BBB freely → neurons/astrocytes perform ketolysis (SCOT + thiolase) → acetyl-CoA → TCA. Brain adapts to use 75% ketones after 3–4 weeks of starvation."},

  {"id":"im09","question":"Phenylketonuria (PKU) is treated with diet + medications. The dietary principle is:","options":["Eliminate all protein","Restrict phenylalanine (Phe) intake while ensuring sufficient tyrosine supplementation (Tyr becomes essential)","Enhance phenylalanine catabolism with B6","High fat diet to reduce glucose dependency"],"answer":1,"explanation":"PAH converts Phe → Tyr; its deficiency makes Tyr conditionally essential. Treatment: restrict dietary Phe (avoid high-protein foods) + supplement Tyr + use of large neutral amino acid (LNAA) competition at gut/BBB to reduce Phe uptake. Sapropterin (BH4 cofactor) helps ~25–30% of patients with PKU."},

  {"id":"im10","question":"The NADPH produced by the HMP shunt is essential for:","options":["Glycolysis","Oxidative burst of neutrophils (via NADPH oxidase) AND reductive biosynthesis (fatty acid synthesis, cholesterol synhesis, GSH regeneration)","ATP synthesis","Glycogenesis"],"answer":1,"explanation":"NADPH from G6PD/6PGD (PPP) has two key roles: (1) Reductive anabolism: FA synthesis (FASN), cholesterol synthesis (HMGCR), and steroid hydroxylations. (2) Antioxidant defence: GR reduces GSSG→2GSH using NADPH; NADPH oxidase generates O₂·⁻ for neutrophil killing. Paradox: G6PD deficiency = reduced pathogen killing capacity but also protects against malaria."},

  {"id":"im11","question":"In the fed (postprandial) state, the liver simultaneously runs FA synthesis. What prevents futile cycling with FAO?","options":["FAO occurs only in fasted state due to a transcription switch that takes hours","Malonyl-CoA (product of FA synthesis) immediately inhibits CPT1 → prevents FA entry into mitochondria — acute metabolic switch, no transcription delay needed","Glucagon suppresses FAO enzymes","AMPK inactivates both CPT1 and ACC1 together"],"answer":1,"explanation":"The CPT1–malonyl-CoA switch is elegantly rapid: insulin → dephosphorylates/activates ACC1 → malonyl-CoA rises → CPT1 inhibited → FAO stops within minutes. Simultaneously FASN makes new FA from the acetyl-CoA pool. This is a post-translational regulatory switch, not a transcription-level switch."},

  {"id":"im12","question":"Metformin's primary mechanism for lowering blood glucose involves:","options":["Increasing insulin secretion from β-cells","Inhibiting hepatic complex I (ETC) → ↑AMP:ATP → AMPK activation → inhibits PEPCK and G6Pase (gluconeogenesis)","Blocking intestinal glucose absorption","Directly inhibiting glycogen phosphorylase"],"answer":1,"explanation":"Metformin enters hepatocytes via OCT1 transporter → inhibits Complex I (mildly) → ↑ADP/AMP ratio → AMPK activation → TORC2 phosphorylation (CREB co-activator) → ↓PEPCK and G6Pase gene expression → ↓hepatic glucose output. Also via ACC1 phosphorylation → ↓malonyl-CoA → metabolic effects. Does NOT stimulate insulin secretion → no hypoglycaemia alone."},

  {"id":"im13","question":"Which metabolic pathway is active during the absorptive state that is NOT active during the post-absorptive state?","options":["Gluconeogenesis","β-Oxidation","De novo fatty acid synthesis (lipogenesis)","Glycogenolysis"],"answer":2,"explanation":"Absorptive (fed): high insulin → glycolysis active, FA synthesis active, glycogenesis active. Post-absorptive (fasted): glucagon dominant → glycogenolysis, gluconeogenesis, β-oxidation, ketogenesis active. FA synthesis is uniquely an absorptive-state pathway — it requires excess acetyl-CoA, high NADPH, and active ACC1 (dephosphorylated by insulin)."},

  {"id":"im14","question":"Hyperammonaemia is dangerous because ammonia crosses the blood-brain barrier and:","options":["Directly inhibits ATP synthase","Is incorporated into α-KG → glutamate (via GDH) → glutamine (via GS) → depleting α-KG from TCA → impaired brain energy metabolism + astrocyte swelling","Oxidises NADH directly","Activates caspases in neurons"],"answer":1,"explanation":"In astrocytes, NH₃ + α-KG (GDH) → glutamate; then Glu + NH₃ (GS) → glutamine. Glutamine accumulates in astrocytes → osmotic swelling → cerebral oedema. Also, α-KG is removed from TCA → impaired TCA flux → ATP deficit. Treatment: lactulose, rifaximin (↓gut NH₃), sodium benzoate/phenylacetate (alternative nitrogen disposal), liver transplant."},

  {"id":"im15","question":"Statins lower LDL by inhibiting HMGCR. They also upregulate LDLR through:","options":["Direct LDLR activation","Reduced intracellular cholesterol → INSIG releases SCAP → SCAP escorts SREBP-2 to Golgi → S1P/S2P cleavage → nuclear SREBP-2 → ↑LDLR gene transcription","PKA-mediated LDLR phosphorylation","Reduced PCSK9 secretion"],"answer":1,"explanation":"This is the statin paradox/synergism: statins reduce intracellular cholesterol → cell senses cholesterol deficit → SCAP-SREBP-2 pathway activated → LDLR upregulated → more LDL cleared from plasma. The SLCO1B1 polymorphism affects statin hepatic uptake (via OATP1B1 transporter) — a major cause of statin myopathy."},

  {"id":"im16","question":"During exercise, which fuel transitions occur in order of increasing exercise duration?","options":["Ketones → glucose → fatty acids","Creatine phosphate → glycogen (anaerobic) → blood glucose → fatty acids → (if prolonged) ketones","Fatty acids → glucose → glycogen","Blood glucose → fatty acids → creatine phosphate"],"answer":1,"explanation":"Substrate hierarchy during exercise: (1) 0–10 sec: creatine phosphate (CP) + ATP stores. (2) 10 sec–2 min: anaerobic glycolysis from muscle glycogen. (3) 2 min–30 min: aerobic glycolysis + FA oxidation (increasing FA contribution). (4) 30+ min: FA oxidation dominant; liver glycogenolysis + gluconeogenesis maintain blood glucose. (5) Starvation: ketone bodies supplement."},

  {"id":"im17","question":"One-carbon metabolism (folate cycle) connects amino acid metabolism to nucleotide synthesis. The key intersection is:","options":["NADH from glutamate oxidation","5,10-methylene-THF (CH₂-THF) from serine catabolism (SHMT) used in dTMP synthesis (TYMS) and as formyl-THF donor in purine synthesis","PRPP from the PPP pathway","Acetyl-CoA from amino acid catabolism"],"answer":1,"explanation":"Serine + THF → glycine + CH₂-THF (SHMT). CH₂-THF is used: (1) TYMS: dUMP + CH₂-THF → dTMP + DHF (pyrimidine synthesis). (2) MTHFR: CH₂-THF → 5-methyl-THF → methionine cycle (homocysteine remethylation). (3) After oxidation → 10-formyl-THF → purine ring carbons C2 and C8 (GART, ATIC). MTX, pemetrexed block this nexus."},

  {"id":"im18","question":"Urea cycle defects (e.g. OTC deficiency) typically present with hyperammonaemia AND orotic aciduria. Why orotic acid?","options":["Urea cycle enzymes also degrade pyrimidines","Excess carbamoyl phosphate (CP) that cannot enter the urea cycle spills into the cytoplasm → enters pyrimidine synthesis → orotic acid overproduction (CPS-II not saturated)","Orotic acid is a direct by-product of ammonia","Hyperammonaemia inhibits orotic acid degradation"],"answer":1,"explanation":"OTC deficiency → carbamoyl phosphate accumulates in mitochondria → leaks into cytoplasm → enters pyrimidine synthesis pathway (CAD: CPS-II + ATCase + DHOase) → orotate/orotic acid overproduction → orotic aciduria. This feature helps differentiate OTC deficiency (orotic aciduria +) from CPS-I deficiency (orotic aciduria −, as no CP is made)."},

  {"id":"im19","question":"Which metabolic abnormality is shared between pyruvate carboxylase deficiency AND OTC deficiency?","options":["Hyperuricaemia","Lactic acidosis","Orotic aciduria","Ketosis"],"answer":1,"explanation":"Pyruvate carboxylase deficiency: pyruvate → cannot form OAA → TCA depleted → acetyl-CoA accumulates → ketosis + lactic acidosis. OTC deficiency: hyperammonaemia → overwhelming transamination → α-KG consumed → TCA impairment → lactic acidosis. Both can have lactic acidosis from TCA failure, though mechanisms differ."},

  {"id":"im20","question":"Glucose-6-phosphate is a metabolic nexus — it can enter 5 different pathways. Which set is correct?","options":["Glycolysis, TCA, urea cycle, β-oxidation, pentose phosphate pathway","Glycolysis (PFK-1 → onward), glycogenesis (UDPase-G→glycogen), HMP shunt (G6PD), gluconeogenesis (reverse via G6Pase), and glucose export (G6Pase in liver/kidney)","Glycolysis, oxidative phosphorylation, fatty acid synthesis, protein synthesis, nucleotide synthesis","Transamination, deamination, urea cycle, gluconeogenesis, glycolysis"],"answer":1,"explanation":"G6P is a true metabolic nexus: (1) Glycolysis (→F6P via PGI). (2) Glycogenesis (→G1P via PGM → UDP-glucose → glycogen). (3) HMP shunt (→6-phosphogluconate via G6PD → NADPH + R5P). (4) Gluconeogenesis in reverse (G6Pase releases free glucose — liver/kidney only). G6Pase deficiency (Von Gierke) blocks the last step, trapping cells as G6P."},
],

"amino_acid_catabolism": [
  {"id":"aac01","question":"Which amino acid is purely ketogenic?","options":["Valine","Leucine","Isoleucine","Methionine"],"answer":1,"explanation":"Leucine is the only purely ketogenic amino acid. Valine is glucogenic; isoleucine is mixed."},
  {"id":"aac02","question":"Transamination requires which vitamin cofactor?","options":["Thiamine (B1)","Pyridoxal phosphate (B6)","Cobalamin (B12)","Biotin"],"answer":1,"explanation":"PLP (B6) is the cofactor for all aminotransferases. B6 deficiency impairs all transaminations simultaneously."},
  {"id":"aac03","question":"The glucose-alanine cycle nitrogen carrier from muscle to liver is:","options":["Glutamine","Alanine (pyruvate carbon + amino nitrogen)","Aspartate","Urea"],"answer":1,"explanation":"Muscle ALT: pyruvate + Glu to Ala. Liver ALT: Ala + alpha-KG to pyruvate + Glu. Pyruvate feeds gluconeogenesis; glutamate nitrogen enters urea cycle."},
  {"id":"aac04","question":"Homocysteine is remethylated to methionine using:","options":["Biotin + CO2","5-methylTHF + methylcobalamin (B12)","SAM directly","PLP"],"answer":1,"explanation":"Methionine synthase (MTR) transfers methyl from 5-methylTHF to homocysteine. Requires methylcobalamin (B12). MTHFR provides 5-methylTHF. CBS (B6) shunts Hcy to cysteine."}
],
"urea_cycle": [
  {"id":"uc01","question":"CPS1 obligate activator is:","options":["ATP","N-acetylglutamate (NAG)","Ornithine","Arginine"],"answer":1,"explanation":"NAG is essential allosteric activator of CPS1. NAG synthase is stimulated by arginine - positive feedback ensuring urea cycle matches nitrogen load."},
  {"id":"uc02","question":"OTC deficiency has orotic aciduria because:","options":["OTC degrades orotate","Carbamoyl phosphate leaks to cytoplasm, enters pyrimidine synthesis via CPS-II/CAD, producing orotic acid","Ammonia stimulates orotate synthesis","Orotic acid is a urea metabolite"],"answer":1,"explanation":"CPS-I deficiency: no orotic aciduria (no carbamoyl-P made). OTC deficiency: carbamoyl-P accumulates, spills to cytoplasm, CPS-II uses it to produce orotic acid."},
  {"id":"uc03","question":"Net ATP cost to produce one urea molecule:","options":["1 ATP","2 ATP","3 ATP equivalents","5 ATP"],"answer":2,"explanation":"CPS1: 2 ATP. ASS: 1 ATP (to AMP+PPi). Total 3 ATP equivalents (4 phosphoanhydride bonds per urea)."}
],
"phenylalanine_tyrosine": [
  {"id":"pt01","question":"PKU causes intellectual disability because:","options":["Phe is directly neurotoxic only","High Phe occupies LNAA BBB transporter, blocks Trp/Tyr entry, depletes monoamine neurotransmitters; toxic metabolites add damage","Lack of tyrosine reduces brain melanin","PAH normally makes ATP"],"answer":1,"explanation":"Phe competes with large neutral AAs at BBB. Tryptophan (serotonin) and tyrosine (dopamine/NA) starved in brain. Phenylpyruvate + phenylacetate are neurotoxic."},
  {"id":"pt02","question":"Alkaptonuria (HGD deficiency) characteristic feature:","options":["Neonatal crisis","Urine turns dark on standing; ochronosis in connective tissues in adulthood","Maple syrup odour","Cholestatic jaundice"],"answer":1,"explanation":"HGD deficiency: homogentisate oxidises on air exposure to dark benzoquinone pigment. Ochronosis: pigment deposits in cartilage/tendons - arthropathy in adulthood. Urine dark on standing is diagnostic."},
  {"id":"pt03","question":"Catecholamine order from tyrosine:","options":["Tyr to DOPA to adrenaline to dopamine","Tyr to DOPA to dopamine to noradrenaline to adrenaline (PNMT in adrenal medulla)","Phe to dopamine to noradrenaline","Tyr to tyramine to adrenaline"],"answer":1,"explanation":"TH (BH4): Tyr to L-DOPA. AADC: L-DOPA to dopamine. DβH: dopamine to noradrenaline. PNMT (cortisol-induced, adrenal medulla only): noradrenaline to adrenaline."}
],
"branched_chain_aa": [
  {"id":"bcaa01","question":"MSUD (BCKDH deficiency) dietary restriction:","options":["All protein","Leucine, isoleucine, and valine (the three BCAAs)","Phenylalanine","Arginine"],"answer":1,"explanation":"BCKDH is committed step for all 3 BCAAs. All three keto acids accumulate. Leu is most toxic (mTORC1 activation). Restrict all 3 BCAAs."},
  {"id":"bcaa02","question":"Isovaleric acidaemia (IVD deficiency) odour:","options":["Maple syrup","Sweaty feet (isovaleric acid/isovalerylglycine)","Cabbage","Musty"],"answer":1,"explanation":"IVD deficiency: isovaleryl-CoA accumulates, isovaleric acid released. Treatment: glycine + carnitine (conjugate toxic acyl-CoA for renal excretion)."},
  {"id":"bcaa03","question":"MUT deficiency (methylmalonic acidaemia) cofactor:","options":["Biotin","Adenosylcobalamin (B12)","PLP (B6)","Thiamine (B1)"],"answer":1,"explanation":"MUT (methylmalonyl-CoA mutase) requires adenosylcobalamin (AdoCbl, mitochondrial B12). B12 deficiency or cbl transport defects impair MUT."},
  {"id":"bcaa04","question":"PCC deficiency secondary hyperammonaemia because:","options":["PCC activates CPS1","Propionyl-CoA/propionate inhibits CPS1, urea cycle fails","Valine/isoleucine toxic to liver","PCC makes NAG"],"answer":1,"explanation":"Propionyl-CoA and propionate directly inhibit CPS1. Secondary hyperammonaemia complicates propionic acidaemia."}
],
"fatty_acid_oxidation": [
  {"id":"fao01","question":"CPT1 is gatekeeper of FAO. It is inhibited by:","options":["Palmitoyl-CoA","Malonyl-CoA (product of ACC1 in FA synthesis)","AMPK","Carnitine"],"answer":1,"explanation":"When insulin high: ACC1 active, malonyl-CoA rises, CPT1 blocked. Prevents futile FAO+synthesis cycling. AMPK inhibits ACC1, malonyl-CoA falls, CPT1 active."},
  {"id":"fao02","question":"Each beta-oxidation cycle yields:","options":["2 NADH","1 FADH2 + 1 NADH + 1 acetyl-CoA (chain shortened 2C)","1 ATP directly","2 acetyl-CoA"],"answer":1,"explanation":"Acyl-CoA dehydrogenase (FADH2), enoyl-CoA hydratase, 3-hydroxyacyl-CoA dehydrogenase (NADH), thiolase (acetyl-CoA). Net per turn: 1 FADH2 + 1 NADH + 1 acetyl-CoA."},
  {"id":"fao03","question":"MCAD deficiency causes hypoketotic hypoglycaemia because:","options":["MCAD blocks ketone utilisation","Medium-chain FA cannot be oxidised, no acetyl-CoA, liver cannot make ketones via HMG-CoA pathway","MCAD makes ketones","Glucose transport is impaired"],"answer":1,"explanation":"FAO feeds acetyl-CoA to ketogenesis. MCAD block: C6-12 FAs not oxidised, acetyl-CoA falls, ketogenesis impossible. Brain/heart starve for both glucose and ketones."}
],
"fatty_acid_synthesis": [
  {"id":"fas01","question":"ACC1 (committed step FA synthesis) activated by:","options":["AMPK","Citrate + insulin (dephosphorylation)","Acyl-CoA","cAMP"],"answer":1,"explanation":"Citrate (excess acetyl-CoA signal) allosterically activates ACC1. Insulin dephosphorylates/activates ACC1. AMPK phosphorylates/inhibits ACC1. Product palmitoyl-CoA inhibits."},
  {"id":"fas02","question":"Cytoplasmic NADPH for FA synthesis from:","options":["Complex I reverse","HMP shunt (G6PD + 6PGD) and malic enzyme","Isocitrate dehydrogenase","Fumarase"],"answer":1,"explanation":"G6PD in HMP shunt produces 2 NADPH per G6P. Malic enzyme (ME1): malate + NADP+ to pyruvate + CO2 + NADPH. FASN requires 14 NADPH per palmitate."}
],
"ketogenesis": [
  {"id":"keto01","question":"Which organ synthesises ketones but cannot use them?","options":["Skeletal muscle","Liver (lacks SCOT/OXCT1)","Kidney","Heart"],"answer":1,"explanation":"Liver mitochondria make ketones (HMG-CoA pathway) but lacks SCOT. Cannot use own ketones - exports them for brain, heart, kidney, muscle during starvation."},
  {"id":"keto02","question":"DKA: uncontrolled ketogenesis driven by:","options":["High insulin + glucagon","Absent insulin (HSL unrestrained, massive FFA) + dominant glucagon (low malonyl-CoA, CPT1 active, TCA depleted by gluconeogenesis) = HMG-CoA overflow","Excess dietary fat","Hyperglycaemia activating HMGCS2"],"answer":1,"explanation":"Insulin absence: adipose HSL releases massive FFAs. Glucagon: inhibits ACC1, malonyl-CoA falls, CPT1 activates. OAA diverted to gluconeogenesis, TCA cannot use acetyl-CoA, overflows to ketones."}
],
"cholesterol_synthesis": [
  {"id":"chol01","question":"Statins increase LDLR expression via:","options":["Direct LDLR gene activation","Low intracellular cholesterol, SCAP escorts SREBP-2 to Golgi, S1P/S2P cleave it, nuclear SREBP-2 upregulates LDLR transcription","PKA-mediated LDLR phosphorylation","Reduced PCSK9 secretion"],"answer":1,"explanation":"Statin mechanism: inhibit HMGCR, intracellular cholesterol falls, INSIG releases SCAP-SREBP-2, Golgi cleavage, nuclear SREBP-2 upregulates LDLR. More LDLR = more LDL-C cleared from plasma."},
  {"id":"chol02","question":"Smith-Lemli-Opitz (DHCR7 deficiency) causes:","options":["Excess cholesterol causing atherosclerosis","7-dehydrocholesterol accumulation + cholesterol deficiency, impaired hedgehog signalling, polydactyly, intellectual disability","LDLR dysfunction","Adrenal insufficiency alone"],"answer":1,"explanation":"DHCR7 final step: 7-DHC to cholesterol. Deficiency: 7-DHC (toxic) accumulates + cholesterol deficient. Impairs hedgehog signalling (requires cholesterol conjugation). Features: 2-3 toe syndactyly, polydactyly, intellectual disability."}
],
"lipoprotein_metabolism": [
  {"id":"lipo01","question":"Which lipoprotein transports dietary fat from intestine?","options":["VLDL","Chylomicrons","LDL","IDL"],"answer":1,"explanation":"Chylomicrons: assembled in enterocytes, secreted into lymph then blood. Carry dietary TG. LPL in capillaries hydrolyses TG. Remnants go to liver via ApoE receptor."},
  {"id":"lipo02","question":"Familial Hypercholesterolaemia (FH) caused by:","options":["HMGCR overactivity","LDLR loss-of-function, LDL not cleared, elevated plasma LDL-C, premature atherosclerosis","PCSK9 deficiency","Excess dietary cholesterol"],"answer":1,"explanation":"FH: LDLR mutations. Heterozygous: LDL 2x elevated. Homozygous: 4-6x, MI in teens. Treatment: statins (increase LDLR via SREBP-2) + PCSK9 inhibitors (prevent LDLR degradation)."},
  {"id":"lipo03","question":"ApoC-II activates:","options":["LCAT","LPL (lipoprotein lipase)","CETP","Hepatic lipase"],"answer":1,"explanation":"ApoC-II is essential LPL cofactor. LPL hydrolyses TG in chylomicrons/VLDL in capillaries. ApoC-II deficiency: type I hyperlipoproteinaemia (same as LPL deficiency)."}
],
"purine_synthesis": [
  {"id":"pur01","question":"De novo purine ring is assembled on:","options":["Free adenine","PRPP (phosphoribosylpyrophosphate) - the activated ribose scaffold","IMP directly","Glutamine"],"answer":1,"explanation":"11 steps assemble the purine ring on PRPP using Gln, Gly, formyl-THF, aspartate, CO2. IMP is the first complete purine, branches to AMP or GMP."},
  {"id":"pur02","question":"Allopurinol inhibits xanthine oxidase by:","options":["Competitive inhibition only","Being oxidised to oxypurinol (alloxanthine) which tightly inhibits XO (suicide-substrate mechanism)","Chelating molybdenum cofactor","Blocking xanthine transport"],"answer":1,"explanation":"Allopurinol is oxidised by XO to oxypurinol, which remains tightly bound to reduced XO - mechanism-based inhibition. Less uric acid produced. Febuxostat: non-purine XO inhibitor."},
  {"id":"pur03","question":"PRPP amidotransferase (PPAT, committed step) inhibited by:","options":["PRPP","AMP and GMP (end-product feedback)","Glutamine","Ribose-5-phosphate"],"answer":1,"explanation":"End-product feedback: AMP, GMP, IMP inhibit PPAT. PRPP activates PPAT (substrate-level). Matches de novo synthesis to cellular purine demand."}
],
"pyrimidine_synthesis": [
  {"id":"pyrim01","question":"First enzyme complex assembling pyrimidine ring:","options":["UMPS","CAD (CPS-II + ATCase + DHOase) - trifunctional cytoplasmic enzyme","DHODH (mitochondrial)","PRPS1"],"answer":1,"explanation":"CAD assembles carbamoyl-phosphate + aspartate into dihydroorotate. DHODH (inner mitochondrial membrane, links to CoQ/Complex III) oxidises to orotate. UMPS adds PRPP to make UMP."},
  {"id":"pyrim02","question":"5-FU kills cancer cells by:","options":["Inhibiting DHODH","Being converted to 5-F-dUMP, irreversibly inhibiting TYMS (thymidylate synthase), blocking dTMP synthesis","Inhibiting RNR directly","Blocking CPS-II"],"answer":1,"explanation":"5-FU to 5-fluoro-dUMP (FUMP): covalent ternary complex with TYMS + CH2-THF. Suicide inhibition. dTMP cannot be made, dTTP deficiency, DNA strand breaks. Leucovorin enhances 5-FU by providing more CH2-THF."},
  {"id":"pyrim03","question":"Hereditary orotic aciduria (UMPS deficiency) features:","options":["Hyperammonaemia","Megaloblastic anaemia + orotic crystals in urine, NO hyperammonaemia","Gout-like joint disease","Immune deficiency"],"answer":1,"explanation":"UMPS deficiency: orotate accumulates, cannot make UMP, pyrimidine starvation, megaloblastic anaemia. No hyperammonaemia (urea cycle intact). Contrast OTC deficiency: orotic aciduria + hyperammonaemia. Treatment: uridine supplementation."}
],
"purine_salvage": [
  {"id":"salv01","question":"Lesch-Nyhan syndrome (HGPRT deficiency):","options":["Hypouricaemia","Severe gout/hyperuricaemia + neurological features (self-mutilation, choreoathetosis) - X-linked males","SCID","Megaloblastic anaemia"],"answer":1,"explanation":"HGPRT salvages hypoxanthine (to IMP) and guanine (to GMP). Without salvage: bases degraded to uric acid, massive hyperuricaemia. Neurological: dopaminergic dysfunction in basal ganglia, compulsive self-biting pathognomonic."},
  {"id":"salv02","question":"ADA deficiency causes SCID because:","options":["Adenosine kills macrophages only","Deoxyadenosine accumulates, dATP expands, inhibits RNR, blocks DNA synthesis in lymphocytes (both T and B cells)","ADA deficiency prevents T-cell homing","dATP activates caspases"],"answer":1,"explanation":"ADA deaminates (deoxy)adenosine to (deoxy)inosine. Deficiency: deoxyadenosine, dATP up, RNR inhibition (all dNTPs blocked), lymphocyte DNA synthesis arrested, combined T+B SCID. First gene therapy target (1990)."}
],
"nucleotide_degradation": [
  {"id":"nd01","question":"Humans cannot degrade uric acid further because:","options":["Kidneys efficiently excrete xanthine","Humans lack uricase (pseudogene) so uric acid is the final purine catabolic product","Gout is adaptive","Uric acid is an antioxidant"],"answer":1,"explanation":"Most mammals: uricase converts urate to allantoin (soluble). Humans: URC1 gene is pseudogene. Uric acid poorly soluble at plasma concentrations (Ksp 6.8 mg/dL). Hyperuricaemia: gout, nephrolithiasis, tophi."},
  {"id":"nd02","question":"PNP deficiency: selective T-cell SCID (vs ADA = combined T+B) because:","options":["PNP expressed only in T-cells","Deoxyguanosine/dGTP accumulates, RNR inhibited in T-cells; B-cells partially spared due to different rescue pathways","PNP deficiency causes autoimmunity not SCID","Guanosine activates T-cell apoptosis"],"answer":1,"explanation":"PNP cleaves purine nucleosides. Deficiency: deoxyguanosine, dGTP up, RNR inhibited predominantly in T-cells. B cells partially spared (different deoxynucleoside kinase balance). Contrast ADA: deoxyadenosine toxicity affects both T and B cells."}
]

}