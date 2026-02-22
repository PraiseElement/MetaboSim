"""
HMP Shunt (Hexose Monophosphate Shunt) / Pentose Phosphate Pathway (PPP)
Simulate the oxidative and non-oxidative phases.

Key outputs: NADPH (reducing power), Ribose-5-phosphate (nucleotide synthesis),
             and re-entry of carbon into glycolysis.
"""


def _enzyme(eid, name, flux, activity, is_reg, regs, status):
    return {
        "enzyme_id": eid, "enzyme_name": name,
        "flux": round(flux, 4), "activity": round(activity, 4),
        "is_regulated": is_reg, "regulators": regs, "status": status,
    }


def _status(x):
    if x >= 0.65: return "active"
    if x >= 0.30: return "allosteric"
    return "inhibited"


def simulate_hmp_shunt(params: dict) -> dict:
    glucose_mM   = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # ── Scenario detection ─────────────────────────────────────────
    if glucose_mM > 8 and insulin_fold > 1.5:
        scenario = "postprandial_hmp"
    elif glucagon_fold > 2 or nutr_state == "starved":
        scenario = "fasting_hmp"
    elif glucose_mM < 2:
        scenario = "hypoglycemia_hmp"
    else:
        scenario = "normal_hmp"

    glucose_factor  = min(glucose_mM / 5.0, 2.5)
    insulin_factor  = min(insulin_fold, 3.0)

    # Oxidative phase flux (NADPH-generating)
    oxidative_flux = 0.40 * glucose_factor * insulin_factor * (1.0 + 0.2 * energy_demand)
    oxidative_flux = max(0.05, min(oxidative_flux, 1.0))

    # Non-oxidative phase (carbon shuffling)
    nonox_flux = oxidative_flux * 0.7

    # G6PD — key regulatory enzyme
    nadph_factor = max(0.5, 1.0 - 0.3 / insulin_fold) if insulin_fold > 0 else 0.5
    g6pd_flux = oxidative_flux * nadph_factor
    g6pd_flux = max(0.05, min(g6pd_flux, 1.0))

    nadph_produced = 2.0 * oxidative_flux
    co2_released   = 1.0 * oxidative_flux

    enzymes = [
        _enzyme("G6PD",  "Glucose-6-Phosphate Dehydrogenase", g6pd_flux, g6pd_flux, True,
                ["-NADPH (product)", "+oxidative stress"], _status(g6pd_flux)),
        _enzyme("LAC",   "6-Phosphogluconolactonase (Lactonase)", oxidative_flux, oxidative_flux, False,
                [], _status(oxidative_flux)),
        _enzyme("6PGD",  "6-Phosphogluconate Dehydrogenase", oxidative_flux, oxidative_flux, True,
                ["-NADPH", "+6-phosphogluconate"], _status(oxidative_flux)),
        _enzyme("RPI",   "Ribose-5-Phosphate Isomerase", nonox_flux, nonox_flux, False,
                [], _status(nonox_flux)),
        _enzyme("RPE",   "Ribulose-5-Phosphate Epimerase", nonox_flux, nonox_flux, False,
                [], _status(nonox_flux)),
        _enzyme("TKT1",  "Transketolase (step 1)", nonox_flux, nonox_flux, True,
                ["requires TPP (Vitamin B1)"], _status(nonox_flux)),
        _enzyme("TALD",  "Transaldolase", nonox_flux * 0.9, nonox_flux * 0.9, False,
                [], _status(nonox_flux)),
        _enzyme("TKT2",  "Transketolase (step 2)", nonox_flux * 0.85, nonox_flux * 0.85, True,
                ["requires TPP (Vitamin B1)"], _status(nonox_flux)),
    ]

    metabolites = [
        {"metabolite_id": "G6P",   "name": "Glucose-6-Phosphate",        "concentration": round(glucose_factor * 0.85, 3), "trend": "stable"},
        {"metabolite_id": "6PGL",  "name": "6-Phosphoglucono-lactone",    "concentration": round(g6pd_flux * 0.40, 3),      "trend": "stable"},
        {"metabolite_id": "6PG",   "name": "6-Phosphogluconate",          "concentration": round(oxidative_flux * 0.55, 3), "trend": "stable"},
        {"metabolite_id": "RU5P",  "name": "Ribulose-5-Phosphate",        "concentration": round(oxidative_flux * 0.70, 3), "trend": "stable"},
        {"metabolite_id": "R5P",   "name": "Ribose-5-Phosphate",          "concentration": round(oxidative_flux * 0.60, 3), "trend": "stable"},
        {"metabolite_id": "X5P",   "name": "Xylulose-5-Phosphate",        "concentration": round(nonox_flux * 0.50, 3),     "trend": "stable"},
        {"metabolite_id": "S7P",   "name": "Sedoheptulose-7-Phosphate",   "concentration": round(nonox_flux * 0.45, 3),     "trend": "stable"},
        {"metabolite_id": "E4P",   "name": "Erythrose-4-Phosphate",       "concentration": round(nonox_flux * 0.40, 3),     "trend": "stable"},
        {"metabolite_id": "F6P",   "name": "Fructose-6-Phosphate",        "concentration": round(nonox_flux * 0.55, 3),     "trend": "stable"},
        {"metabolite_id": "G3P",   "name": "Glyceraldehyde-3-Phosphate",  "concentration": round(nonox_flux * 0.50, 3),     "trend": "stable"},
        {"metabolite_id": "NADPH", "name": "NADPH",                       "concentration": round(nadph_produced, 3),        "trend": "rising" if oxidative_flux > 0.5 else "stable"},
    ]

    notes = []
    warnings = []

    if g6pd_flux >= 0.65:
        notes.append("Active G6PD indicates high NADPH demand — consistent with lipogenesis or oxidative stress protection.")
    if oxidative_flux < 0.3:
        notes.append("Suppressed PPP: low NADPH may impair glutathione reduction -> increased RBC oxidative damage risk.")
    if nutr_state == "fed" and insulin_fold > 1.5:
        notes.append("Post-prandial: insulin upregulates G6PD transcription, channeling G6P toward NADPH for fatty acid synthesis.")
    if glucagon_fold > 2:
        notes.append("Fasting/glucagon: PPP suppressed; G6P redirected toward gluconeogenesis substrate supply.")
    notes.append("PPP is the sole source of NADPH in erythrocytes — G6PD deficiency causes haemolytic anaemia under oxidative stress.")
    notes.append("Ribose-5-phosphate from the PPP is essential for nucleotide (DNA/RNA) synthesis in proliferating cells.")

    if glucose_mM < 2:
        warnings.append("Hypoglycaemia: insufficient G6P substrate — NADPH and ribose-5-P production severely impaired.")

    return {
        "pathway": "hmp_shunt",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": 0.0,
            "net_flux": round(oxidative_flux, 3),
            "nadh_produced": 0.0,
            "fadh2_produced": 0.0,
            "nadph_produced": round(nadph_produced, 2),
            "co2_released": round(co2_released, 2),
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": round(g6pd_flux, 3),
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
