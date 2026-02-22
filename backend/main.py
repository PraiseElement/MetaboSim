"""
MetaboSim FastAPI Backend

Endpoints:
  GET  /                      - health check
  GET  /api/scenarios         - list all scenario presets
  GET  /api/pathways          - list available pathways
  POST /api/simulate          - run simulation with given parameters
  GET  /api/quiz/{pathway}    - get quiz questions for a pathway
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
import time
import os

from models.simulation import SimulationRequest, SimulationResult
from engine.glycolysis import simulate_glycolysis
from engine.tca_cycle import simulate_tca
from engine.oxphos import simulate_oxphos
from engine.gluconeogenesis import simulate_gluconeogenesis
from engine.hmp_shunt import simulate_hmp_shunt
from engine.glycogenesis import simulate_glycogenesis
from engine.glycogenolysis import simulate_glycogenolysis
from engine.fructose_metabolism import simulate_fructose_metabolism
from engine.galactose_metabolism import simulate_galactose_metabolism
# Amino acid metabolism
from engine.amino_acid_catabolism import simulate_amino_acid_catabolism
from engine.urea_cycle import simulate_urea_cycle
from engine.phenylalanine_tyrosine import simulate_phenylalanine_tyrosine
from engine.branched_chain_aa import simulate_branched_chain_aa
from engine.amino_acid_synthesis import simulate_amino_acid_synthesis
# Lipid metabolism
from engine.fatty_acid_oxidation import simulate_fatty_acid_oxidation
from engine.fatty_acid_synthesis import simulate_fatty_acid_synthesis
from engine.ketogenesis import simulate_ketogenesis
from engine.cholesterol_synthesis import simulate_cholesterol_synthesis
from engine.lipoprotein_metabolism import simulate_lipoprotein_metabolism
# Nucleotide metabolism
from engine.purine_synthesis import simulate_purine_synthesis
from engine.pyrimidine_synthesis import simulate_pyrimidine_synthesis
from engine.purine_salvage import simulate_purine_salvage
from engine.nucleotide_degradation import simulate_nucleotide_degradation
from engine.scenarios import SCENARIOS
from engine.quiz_data import QUIZ_QUESTIONS

app = FastAPI(
    title="MetaboSim API",
    description="Interactive metabolic pathway simulation engine for biochemistry education.",
    version="2.0.0",
)

# CORS — in production set ALLOWED_ORIGINS env var to your Vercel URL(s)
# e.g. ALLOWED_ORIGINS=https://metabosim.vercel.app,https://metabosim-*.vercel.app
_raw_origins = os.environ.get("ALLOWED_ORIGINS", "")
ALLOWED_ORIGINS: list[str] = (
    [o.strip() for o in _raw_origins.split(",") if o.strip()]
    if _raw_origins
    else ["*"]  # permissive for local dev
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app" if not _raw_origins else None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PATHWAYS = {
    "glycolysis": {
        "id": "glycolysis",
        "name": "Glycolysis",
        "description": "The 10-step breakdown of glucose to pyruvate, generating ATP and NADH.",
        "steps": 10,
        "location": "Cytoplasm",
        "net_atp": "2 (anaerobic) / 7 (aerobic per glucose, from NADH)",
    },
    "gluconeogenesis": {
        "id": "gluconeogenesis",
        "name": "Gluconeogenesis",
        "description": "Synthesis of glucose from non-carbohydrate precursors: lactate, amino acids, glycerol.",
        "steps": 11,
        "location": "Cytoplasm + Mitochondria (PC step)",
        "net_atp": "−6 ATP consumed per glucose",
    },
    "tca_cycle": {
        "id": "tca_cycle",
        "name": "TCA (Citric Acid) Cycle",
        "description": "The 8-step cycle oxidising acetyl-CoA to CO₂ while reducing NAD⁺ and FAD.",
        "steps": 8,
        "location": "Mitochondrial matrix",
        "net_atp": "1 GTP + 3 NADH + 1 FADH₂ per turn",
    },
    "oxphos": {
        "id": "oxphos",
        "name": "Oxidative Phosphorylation",
        "description": "The ETC (Complexes I–IV) and ATP synthase (Complex V) generating the bulk of cellular ATP.",
        "steps": 5,
        "location": "Inner mitochondrial membrane",
        "net_atp": "~26–28 ATP per glucose (from NADH/FADH₂)",
    },
    "hmp_shunt": {
        "id": "hmp_shunt",
        "name": "HMP Shunt (Pentose Phosphate)",
        "description": "Oxidative and non-oxidative phases producing NADPH and ribose-5-phosphate from G6P.",
        "steps": 8,
        "location": "Cytoplasm",
        "net_atp": "No ATP — produces 2 NADPH + 1 CO₂ per G6P (oxidative phase)",
    },
    "glycogenesis": {
        "id": "glycogenesis",
        "name": "Glycogenesis",
        "description": "Synthesis of glycogen from glucose, regulated by insulin and glucagon.",
        "steps": 5,
        "location": "Cytoplasm (liver + muscle)",
        "net_atp": "−2 high-energy phosphates per glucose residue stored",
    },
    "glycogenolysis": {
        "id": "glycogenolysis",
        "name": "Glycogenolysis",
        "description": "Breakdown of glycogen to glucose-1-phosphate, regulated by glucagon and epinephrine.",
        "steps": 4,
        "location": "Cytoplasm (liver + muscle)",
        "net_atp": "+3 ATP advantage (glycogen glucose vs free glucose)",
    },
    "fructose_metabolism": {
        "id": "fructose_metabolism",
        "name": "Fructose Metabolism",
        "description": "Hepatic fructolysis via Fructokinase and Aldolase B, bypassing PFK-1 regulation.",
        "steps": 5,
        "location": "Cytoplasm (liver)",
        "net_atp": "~4 ATP per fructose (via triose phosphate entry to glycolysis)",
    },
    "galactose_metabolism": {
        "id": "galactose_metabolism",
        "name": "Galactose Metabolism",
        "description": "Leloir pathway converting galactose to glucose-1-phosphate for glycolysis or glycogenesis.",
        "steps": 4,
        "location": "Cytoplasm (liver)",
        "net_atp": "~3.8 ATP per galactose",
    },
    "integrated": {
        "id": "integrated",
        "name": "Integrated (All)",
        "description": "Combined glycolysis + TCA cycle + oxidative phosphorylation.",
        "steps": 23,
        "location": "Cytoplasm + Mitochondria",
        "net_atp": "~30–32 ATP per glucose (complete aerobic oxidation)",
        "domain": "carbohydrate",
    },
    # ── Amino Acid Metabolism ───────────────────────────────────────────────────
    "amino_acid_catabolism": {
        "id": "amino_acid_catabolism",
        "name": "Amino Acid Catabolism",
        "description": "Transamination (ALT/AST), GDH, and TCA entry points for all 20 amino acids.",
        "steps": 5,
        "location": "Cytoplasm + Mitochondria",
        "net_atp": "Variable — glucogenic/ketogenic carbon skeleton yields differ by AA",
        "domain": "amino_acid",
    },
    "urea_cycle": {
        "id": "urea_cycle",
        "name": "Urea Cycle",
        "description": "5-step conversion of NH₃ + CO₂ + aspartate → urea in periportal hepatocytes.",
        "steps": 5,
        "location": "Mitochondria (CPS-I, OTC) + Cytoplasm (ASS, ASL, Arginase)",
        "net_atp": "−3 ATP per urea molecule (energy cost of nitrogen excretion)",
        "domain": "amino_acid",
    },
    "phenylalanine_tyrosine": {
        "id": "phenylalanine_tyrosine",
        "name": "Phenylalanine & Tyrosine",
        "description": "PAH (PKU), catecholamine synthesis, melanin, and degradation via FAH (tyrosinaemia).",
        "steps": 8,
        "location": "Cytoplasm + ER + Mitochondria",
        "net_atp": "0 direct — mixed gluco/ketogenic (fumarate + acetoacetate)",
        "domain": "amino_acid",
    },
    "branched_chain_aa": {
        "id": "branched_chain_aa",
        "name": "BCAA Catabolism",
        "description": "Val/Leu/Ile catabolism via BCAT and BCKDH; MSUD, isovaleric acidaemia, MMA.",
        "steps": 6,
        "location": "Mitochondria (muscle and liver)",
        "net_atp": "0 direct — products enter TCA as acetyl-CoA or succinyl-CoA",
        "domain": "amino_acid",
    },
    "amino_acid_synthesis": {
        "id": "amino_acid_synthesis",
        "name": "Amino Acid Synthesis",
        "description": "Non-essential AA biosynthesis: GS (Gln), PHGDH (Ser/Gly), AS (Asn), ALT (Ala).",
        "steps": 6,
        "location": "Cytoplasm + Mitochondria",
        "net_atp": "−1 to −2 ATP per AA synthesised (GS, AS)",
        "domain": "amino_acid",
    },
    # ── Lipid Metabolism ────────────────────────────────────────────────────────
    "fatty_acid_oxidation": {
        "id": "fatty_acid_oxidation",
        "name": "β-Oxidation (FA Oxidation)",
        "description": "Palmitoyl-CoA (C16) → 8 Acetyl-CoA via 7 cycles; CPT-I gate; MCAD deficiency.",
        "steps": 5,
        "location": "Mitochondrial matrix (CPT-I on inner mito membrane)",
        "net_atp": "−2 activation + 0 substrate-level; 7 FADH₂ + 7 NADH → ~106 ATP full oxidation",
        "domain": "lipid",
    },
    "fatty_acid_synthesis": {
        "id": "fatty_acid_synthesis",
        "name": "Fatty Acid Synthesis (DNL)",
        "description": "De novo lipogenesis: ACC (malonyl-CoA) + FAS complex → palmitate; −7 ATP, −14 NADPH.",
        "steps": 4,
        "location": "Cytoplasm (liver, adipose)",
        "net_atp": "−7 ATP + 14 NADPH per palmitate",
        "domain": "lipid",
    },
    "ketogenesis": {
        "id": "ketogenesis",
        "name": "Ketogenesis & Ketolysis",
        "description": "Hepatic HMGS2 → acetoacetate/β-OHB; DKA vs physiological ketosis; SCOT ketolysis.",
        "steps": 5,
        "location": "Hepatocyte mitochondria (production); extrahepatic (utilisation)",
        "net_atp": "0 direct from ketogenesis; ~22 ATP per acetoacetate during ketolysis",
        "domain": "lipid",
    },
    "cholesterol_synthesis": {
        "id": "cholesterol_synthesis",
        "name": "Cholesterol Synthesis",
        "description": "Mevalonate pathway: HMGCR (statin target), MVK, DHCR7 (SLO), FPP → CoQ/dolichol.",
        "steps": 5,
        "location": "ER + Cytoplasm (liver)",
        "net_atp": "−18 ATP + 16 NADPH per cholesterol synthesised",
        "domain": "lipid",
    },
    "lipoprotein_metabolism": {
        "id": "lipoprotein_metabolism",
        "name": "Lipoprotein Metabolism",
        "description": "LPL, LDLR, PCSK9, LCAT, ABCA1 — FH, LPL deficiency, statin/PCSK9i pharmacology.",
        "steps": 6,
        "location": "Plasma + Liver + Peripheral tissues",
        "net_atp": "0 direct — transport/remodelling process",
        "domain": "lipid",
    },
    # ── Nucleotide Metabolism ───────────────────────────────────────────────────
    "purine_synthesis": {
        "id": "purine_synthesis",
        "name": "Purine De Novo Synthesis",
        "description": "PRPP → IMP → AMP/GMP; IMPDH (mycophenolate target), ADSS/ADSL, MTX mechanism.",
        "steps": 5,
        "location": "Cytoplasm",
        "net_atp": "−5 ATP per IMP; −6 per AMP; −7 per GMP",
        "domain": "nucleotide",
    },
    "pyrimidine_synthesis": {
        "id": "pyrimidine_synthesis",
        "name": "Pyrimidine De Novo Synthesis",
        "description": "CAD → DHODH (leflunomide/teriflunomide) → UMPS → UMP/CTP; TYMS (5-FU), DHFR (MTX).",
        "steps": 6,
        "location": "Cytoplasm + Mitochondria (DHODH)",
        "net_atp": "~−5 ATP per CTP; DHODH regenerates CoQ",
        "domain": "nucleotide",
    },
    "purine_salvage": {
        "id": "purine_salvage",
        "name": "Purine Salvage",
        "description": "HGPRT (Lesch-Nyhan), APRT (2,8-DHA stones), ADA (SCID), CD73 (tumour immunity).",
        "steps": 5,
        "location": "Cytoplasm",
        "net_atp": "~0 net (saves 4 ATP vs de novo per purine)",
        "domain": "nucleotide",
    },
    "nucleotide_degradation": {
        "id": "nucleotide_degradation",
        "name": "Nucleotide Degradation",
        "description": "XO (allopurinol/febuxostat/TLS/gout), PNP (T-cell SCID), DPYD (5-FU toxicity).",
        "steps": 5,
        "location": "Cytoplasm + Liver",
        "net_atp": "0 direct — purines degraded to uric acid",
        "domain": "nucleotide",
    },
}

# QUIZ_QUESTIONS imported from engine/quiz_data.py (107 questions across 5 topics)


def _detect_scenario(params: dict) -> str:
    o2 = params.get("oxygen_pct", 100)
    glucose = params.get("glucose_mM", 5.0)
    insulin = params.get("insulin_fold", 1.0)
    glucagon = params.get("glucagon_fold", 1.0)
    demand = params.get("energy_demand", 1.0)
    state = params.get("nutritional_state", "fed")

    if o2 <= 10:
        return "lactic_acidosis" if demand > 2.5 else "hypoxia"
    if state == "starved":
        return "starvation"
    if state == "fasted" and glucagon > 2.0:
        return "fasting"
    if demand >= 4.0:
        return "exercise"
    if glucose > 11.0:
        return "type2_diabetes"
    return "normal_fed"


@app.get("/")
def health():
    return {"status": "ok", "service": "MetaboSim API", "version": "2.0.0"}


@app.get("/api/pathways")
def get_pathways():
    return {"pathways": list(PATHWAYS.values())}


@app.get("/api/scenarios")
def get_scenarios():
    return {"scenarios": SCENARIOS}


@app.post("/api/simulate")
def simulate(request: SimulationRequest) -> Dict[str, Any]:
    params = request.model_dump()
    pathway = params.get("pathway", "glycolysis")

    scenario = _detect_scenario(params)

    all_results: Dict[str, Any] = {
        "scenario_detected": scenario,
        "pathway": pathway,
    }

    # Always run glycolysis as the entry point
    glyc = simulate_glycolysis(params)

    if pathway == "glycolysis":
        all_results.update(glyc)

    elif pathway == "tca_cycle":
        tca = simulate_tca(params, glycolysis_result=glyc)
        all_results.update(tca)

    elif pathway == "oxphos":
        tca = simulate_tca(params, glycolysis_result=glyc)
        oxp = simulate_oxphos(params, glycolysis_result=glyc, tca_result=tca)
        all_results.update(oxp)

    elif pathway == "gluconeogenesis":
        gng = simulate_gluconeogenesis(params)
        all_results.update(gng)

    elif pathway == "integrated":
        # Run all pathways and combine
        tca = simulate_tca(params, glycolysis_result=glyc)
        oxp = simulate_oxphos(params, glycolysis_result=glyc, tca_result=tca)
        gng = simulate_gluconeogenesis(params)

        all_enzymes = glyc["enzymes"] + tca["enzymes"] + oxp["enzymes"] + gng["enzymes"]
        all_metabolites = glyc["metabolites"] + tca["metabolites"] + oxp["metabolites"] + gng["metabolites"]
        all_notes = list(set(glyc["educational_notes"] + tca["educational_notes"] + oxp["educational_notes"] + gng["educational_notes"]))
        all_warnings = list(set(glyc["warnings"] + tca["warnings"] + oxp["warnings"] + gng["warnings"]))

        # Sum ATP yields
        total_atp = (
            glyc["metrics"]["atp_yield"]
            + tca["metrics"]["atp_yield"]
            + oxp["metrics"]["atp_yield"]
        )

        all_results["enzymes"] = all_enzymes
        all_results["metabolites"] = all_metabolites
        all_results["educational_notes"] = all_notes
        all_results["warnings"] = all_warnings
        all_results["metrics"] = {
            "atp_yield": round(total_atp, 2),
            "nadh_produced": round(glyc["metrics"]["nadh_produced"] + tca["metrics"]["nadh_produced"], 2),
            "fadh2_produced": round(tca["metrics"]["fadh2_produced"], 2),
            "co2_released": round(tca["metrics"]["co2_released"], 2),
            "net_flux": round(glyc["metrics"]["net_flux"], 3),
            "pyruvate_output": round(glyc["metrics"]["pyruvate_output"], 3),
            "lactate_output": round(glyc["metrics"]["lactate_output"], 3),
            "glucose_consumed": round(glyc["metrics"]["glucose_consumed"], 3),
        }
    elif pathway == "hmp_shunt":
        hmp = simulate_hmp_shunt(params)
        all_results.update(hmp)

    elif pathway == "glycogenesis":
        gys = simulate_glycogenesis(params)
        all_results.update(gys)

    elif pathway == "glycogenolysis":
        gyl = simulate_glycogenolysis(params)
        all_results.update(gyl)

    elif pathway == "fructose_metabolism":
        fru = simulate_fructose_metabolism(params)
        all_results.update(fru)

    elif pathway == "galactose_metabolism":
        gal = simulate_galactose_metabolism(params)
        all_results.update(gal)

    # ── Amino Acid Metabolism ──────────────────────────────────────────────────
    elif pathway == "amino_acid_catabolism":
        all_results.update(simulate_amino_acid_catabolism(params))

    elif pathway == "urea_cycle":
        all_results.update(simulate_urea_cycle(params))

    elif pathway == "phenylalanine_tyrosine":
        all_results.update(simulate_phenylalanine_tyrosine(params))

    elif pathway == "branched_chain_aa":
        all_results.update(simulate_branched_chain_aa(params))

    elif pathway == "amino_acid_synthesis":
        all_results.update(simulate_amino_acid_synthesis(params))

    # ── Lipid Metabolism ───────────────────────────────────────────────────────
    elif pathway == "fatty_acid_oxidation":
        all_results.update(simulate_fatty_acid_oxidation(params))

    elif pathway == "fatty_acid_synthesis":
        all_results.update(simulate_fatty_acid_synthesis(params))

    elif pathway == "ketogenesis":
        all_results.update(simulate_ketogenesis(params))

    elif pathway == "cholesterol_synthesis":
        all_results.update(simulate_cholesterol_synthesis(params))

    elif pathway == "lipoprotein_metabolism":
        all_results.update(simulate_lipoprotein_metabolism(params))

    # ── Nucleotide Metabolism ──────────────────────────────────────────────────
    elif pathway == "purine_synthesis":
        all_results.update(simulate_purine_synthesis(params))

    elif pathway == "pyrimidine_synthesis":
        all_results.update(simulate_pyrimidine_synthesis(params))

    elif pathway == "purine_salvage":
        all_results.update(simulate_purine_salvage(params))

    elif pathway == "nucleotide_degradation":
        all_results.update(simulate_nucleotide_degradation(params))

    else:
        raise HTTPException(status_code=400, detail=f"Unknown pathway: {pathway}")

    return all_results


@app.get("/api/quiz/{pathway}")
def get_quiz(pathway: str):
    questions = QUIZ_QUESTIONS.get(pathway)
    if questions is None:
        raise HTTPException(status_code=404, detail=f"No quiz found for pathway: {pathway}")
    # Don't expose answers in the GET response
    sanitized = []
    for q in questions:
        sanitized.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
        })
    return {"pathway": pathway, "questions": sanitized}


@app.post("/api/quiz/{pathway}/check")
def check_answer(pathway: str, body: Dict[str, Any]):
    question_id = body.get("question_id")
    submitted = body.get("answer_index")

    questions = QUIZ_QUESTIONS.get(pathway, [])
    for q in questions:
        if q["id"] == question_id:
            correct = q["answer"]
            is_correct = submitted == correct
            return {
                "correct": is_correct,
                "correct_index": correct,
                "explanation": q["explanation"],
            }

    raise HTTPException(status_code=404, detail="Question not found")
