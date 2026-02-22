"""
Fructose Metabolism Pathway
Dietary fructose -> Fructose-1-phosphate -> DHAP + Glyceraldehyde -> Glycolysis

Key enzymes: Fructokinase (KHK), Aldolase B, Triokinase, GAPDH, PK
Clinical disorders: HFI (Aldolase B deficiency), Essential Fructosuria (KHK deficiency)
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


def simulate_fructose_metabolism(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # Use glucose_mM as proxy for dietary carbohydrate/fructose load
    fructose_factor = min(glucose_mM / 5.0, 2.5)

    # ── Scenario ───────────────────────────────────────────────────
    if fructose_factor > 1.5 and nutr_state == "fed":
        scenario = "high_fructose_load"
    elif glucagon_fold > 2 or nutr_state == "fasted":
        scenario = "fasted_fructose"
    elif energy_demand > 3:
        scenario = "high_demand_fructose"
    else:
        scenario = "normal_fructose"

    # ── Fructokinase is NOT regulated by hormones ──────────────────
    fk_flux = 0.70 * fructose_factor
    fk_flux = max(0.05, min(fk_flux, 1.0))

    # Aldolase B cleaves F1P -> DHAP + glyceraldehyde
    aldob_flux = fk_flux * 0.85
    aldob_flux = max(0.05, min(aldob_flux, 1.0))

    # Triokinase converts glyceraldehyde -> G3P
    triokinase_flux = aldob_flux * 0.90

    # DHAP and G3P enter glycolysis
    glycolysis_entry = (aldob_flux * 0.50 + triokinase_flux * 0.50)

    # ATP accounting (substrate-level phosphorylation only — ETC/OxPhos is NOT included here):
    #  - KHK consumes 1 ATP (traps fructose as F1P)
    #  - Triokinase consumes 1 ATP (converts glyceraldehyde → G3P)
    #  - Investment total: 2 ATP per fructose (fk_flux * 2)
    #  - PGK + PK together produce 4 ATP for 2 trioses → 2 ATP net per fructose
    #  - Net substrate-level: 2 produced − 2 invested = ~0 (same as glucose)
    #  - NADH from GAPDH goes to OxPhos — NOT counted here to avoid double-counting
    atp_substrate_produced = glycolysis_entry * 2.0   # 2 net substrate ATP per fructose (PGK+PK)
    atp_invested           = fk_flux * 2.0            # KHK + Triokinase
    atp_yield              = atp_substrate_produced - atp_invested
    nadh_produced = glycolysis_entry * 2.0    # 2×GAPDH per fructose (1 per triose)
    co2_released  = glycolysis_entry * 0.5
    lactate_out   = 0.1 if energy_demand < 2 else glycolysis_entry * 0.3
    uric_acid_out = fk_flux * 0.30  # Pi depletion -> purine catabolism

    enzymes = [
        _enzyme("KHK",    "Fructokinase (KHK-C)", fk_flux, fk_flux, False,
                ["NOT regulated by insulin/glucagon", "traps fructose in liver irreversibly",
                 "ATP consumption -> Pi depletion at high fructose loads"], _status(fk_flux)),
        _enzyme("ALDOB",  "Aldolase B", aldob_flux, aldob_flux, True,
                ["deficiency = Hereditary Fructose Intolerance (HFI)",
                 "F1P accumulation -> Pi depletion -> ATP collapse"], _status(aldob_flux)),
        _enzyme("TK",     "Triokinase (glyceraldehyde kinase)", triokinase_flux, triokinase_flux, False,
                ["phosphorylates glyceraldehyde -> G3P -> glycolysis"], _status(triokinase_flux)),
        _enzyme("GAPDH",  "GAPDH -> Pyruvate Kinase (glycolytic entry)", glycolysis_entry, glycolysis_entry, True,
                ["both DHAP and G3P enter at this stage", "bypasses PFK-1 regulation"], _status(glycolysis_entry)),
        _enzyme("PK2",    "Pyruvate Kinase", glycolysis_entry * 0.90, glycolysis_entry * 0.90, True,
                ["+F1,6BP (fructolytic flux feeds forward)", "+ADP"], _status(glycolysis_entry)),
    ]

    metabolites = [
        {"metabolite_id": "fructose",   "name": "Fructose",                   "concentration": round(fructose_factor, 3),       "trend": "stable"},
        {"metabolite_id": "f1p",        "name": "Fructose-1-Phosphate",       "concentration": round(fk_flux * 0.80, 3),        "trend": "rising" if fk_flux > 0.6 else "stable"},
        {"metabolite_id": "dhap_fr",    "name": "DHAP",                       "concentration": round(aldob_flux * 0.55, 3),     "trend": "stable"},
        {"metabolite_id": "ga",         "name": "Glyceraldehyde",             "concentration": round(aldob_flux * 0.45, 3),     "trend": "stable"},
        {"metabolite_id": "g3p_fr",     "name": "Glyceraldehyde-3-Phosphate", "concentration": round(triokinase_flux * 0.80, 3),"trend": "stable"},
        {"metabolite_id": "pyruvate_fr","name": "Pyruvate",                   "concentration": round(glycolysis_entry * 0.75, 3),"trend": "stable"},
        {"metabolite_id": "atp_fr",     "name": "ATP (net produced)",         "concentration": round(min(atp_yield / 5.0, 1.0), 3), "trend": "stable"},
        {"metabolite_id": "uric_acid",  "name": "Uric Acid",                  "concentration": round(uric_acid_out, 3),         "trend": "rising" if fk_flux > 0.6 else "stable"},
    ]

    notes = []
    warnings = []

    notes.append("Fructose bypasses PFK-1 — the major regulatory checkpoint of glycolysis — leading to unregulated carbon flow into the metabolic network.")
    notes.append("High fructose -> rapid ATP consumption by fructokinase -> Pi depletion -> purine catabolism -> uric acid elevation (hyperuricaemia, gout risk).")
    notes.append("Hepatic fructose preferentially flows to de novo lipogenesis (DNL) and triglyceride synthesis rather than oxidation.")

    if fk_flux > 0.7:
        warnings.append("High fructokinase flux: significant Pi depletion risk -> impaired oxidative phosphorylation -> transient hepatic ATP crisis.")
    if scenario == "high_fructose_load":
        notes.append("High fructose load: liver overwhelmed — excess carbon diverted to DNL -> hepatic steatosis, hypertriglyceridaemia risk.")
    if glucagon_fold > 2:
        notes.append("Fasting with fructose: fructose carbon can be directed toward gluconeogenesis (via DHAP/G3P), increasing hepatic glucose output.")

    return {
        "pathway": "fructose_metabolism",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "atp_invested": round(atp_invested, 2),
            "atp_substrate_produced": round(atp_substrate_produced, 2),
            "net_flux": round(fk_flux, 3),
            "nadh_produced": round(nadh_produced, 2),
            "fadh2_produced": 0.0,
            "co2_released": round(co2_released, 2),
            "pyruvate_output": round(glycolysis_entry * 0.75, 3),
            "lactate_output": round(lactate_out, 3),
            "glucose_consumed": round(fructose_factor, 3),
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
