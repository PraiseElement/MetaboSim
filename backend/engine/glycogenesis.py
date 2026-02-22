"""
Glycogenesis — Glycogen Synthesis Pathway
Glucose -> G6P -> G1P -> UDP-glucose -> Glycogen

Key enzymes: Hexokinase/Glucokinase, Phosphoglucomutase,
             UDP-glucose pyrophosphorylase, Glycogen Synthase, Branching Enzyme
Regulated by: Insulin (activates GS via PP1), Glucagon/Epinephrine (inhibit via PKA)
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


def simulate_glycogenesis(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # ── Scenario ───────────────────────────────────────────────────
    if insulin_fold > 2.0 and glucose_mM > 6:
        scenario = "postprandial_glycogenesis"
    elif glucagon_fold > 2.0 or nutr_state in ("fasted", "starved"):
        scenario = "fasting_glycogenesis_inhibited"
    elif insulin_fold > 1.2:
        scenario = "insulin_stimulated"
    else:
        scenario = "basal_glycogenesis"

    glucose_factor  = min(glucose_mM / 5.0, 3.0)
    gs_insulin_act  = min(insulin_fold, 4.0)
    gs_glucagon_inh = max(0.1, 1.0 - 0.35 * (glucagon_fold - 1.0)) if glucagon_fold > 1 else 1.0
    energy_factor   = max(0.2, 1.5 - 0.3 * energy_demand)

    gs_flux = 0.55 * glucose_factor * gs_insulin_act * gs_glucagon_inh * energy_factor
    gs_flux = max(0.05, min(gs_flux, 1.0))

    early_flux = min(gs_flux * 1.15, 1.0)
    atp_yield  = -2.0 * gs_flux   # 2 high-energy phosphates consumed per glucose stored

    enzymes = [
        _enzyme("HK",    "Hexokinase / Glucokinase", min(early_flux, 1.0), min(early_flux, 1.0), True,
                ["-G6P (HK only)", "+glucose (GK sigmoidal)"], _status(early_flux)),
        _enzyme("PGM",   "Phosphoglucomutase", early_flux * 0.95, early_flux * 0.95, False,
                ["requires glucose-1,6-bisphosphate cofactor"], _status(early_flux)),
        _enzyme("UGPP",  "UDP-Glucose Pyrophosphorylase", gs_flux * 1.05, gs_flux * 1.05, False,
                ["driven by pyrophosphate hydrolysis (irreversible)"], _status(gs_flux)),
        _enzyme("GS",    "Glycogen Synthase", gs_flux, gs_flux, True,
                ["+insulin (dephosphorylation via PP1)", "-glucagon/Epi (PKA->phosphorylation)",
                 "+glucose-6-P (allosteric)"], _status(gs_flux)),
        _enzyme("BE",    "Branching Enzyme (Amylo-transglucosylase)", gs_flux * 0.30, gs_flux * 0.30, False,
                ["transfers >=6 glucose units to alpha-1,6 branch points"],
                "active" if gs_flux > 0.3 else "allosteric"),
    ]

    metabolites = [
        {"metabolite_id": "glucose",    "name": "Blood Glucose",          "concentration": round(min(glucose_factor, 1.0), 3), "trend": "stable"},
        {"metabolite_id": "g6p_gs",     "name": "Glucose-6-Phosphate",    "concentration": round(early_flux * 0.90, 3),        "trend": "stable"},
        {"metabolite_id": "g1p_gs",     "name": "Glucose-1-Phosphate",    "concentration": round(early_flux * 0.70, 3),        "trend": "stable"},
        {"metabolite_id": "udpglc",     "name": "UDP-Glucose",            "concentration": round(gs_flux * 0.80, 3),           "trend": "stable"},
        {"metabolite_id": "glycogen",   "name": "Glycogen (n+1 residues)","concentration": round(gs_flux, 3),                  "trend": "rising" if gs_flux > 0.5 else "stable"},
        {"metabolite_id": "udp",        "name": "UDP (released)",         "concentration": round(gs_flux * 0.75, 3),           "trend": "stable"},
        {"metabolite_id": "utp",        "name": "UTP (consumed)",         "concentration": round(max(0.1, 1.0 - gs_flux * 0.5), 3), "trend": "falling" if gs_flux > 0.4 else "stable"},
    ]

    notes = []
    warnings = []

    if scenario == "postprandial_glycogenesis":
        notes.append("Post-prandial: insulin activates PP1 which dephosphorylates glycogen synthase -> active form promotes glycogen deposition.")
    if scenario == "fasting_glycogenesis_inhibited":
        notes.append("Fasting: glucagon -> PKA -> phosphorylates glycogen synthase -> inactive. Glycogenolysis dominates.")
    if gs_flux < 0.2:
        warnings.append("Glycogen synthase activity very low — nearly no glycogen being synthesised.")
    notes.append("Each glucose added to glycogen costs 1 ATP (hexokinase) + 1 UTP (UGPPase) = 2 high-energy phosphate bonds per glucose residue.")
    notes.append("Von Gierke disease (GSD Ia): G6Pase deficiency causes G6P accumulation, paradoxically stimulating GS -> massive glycogen accumulation despite hypoglycaemia.")
    notes.append("Glycogen synthase kinase-3 (GSK-3) is a major inhibitory kinase; insulin/Akt phosphorylates and inactivates GSK-3, disinhibiting GS.")

    if glucagon_fold > 3:
        warnings.append("Extreme glucagonaemia: glycogen synthase maximally phosphorylated — synthesis blocked.")

    return {
        "pathway": "glycogenesis",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "net_flux": round(gs_flux, 3),
            "nadh_produced": 0.0,
            "fadh2_produced": 0.0,
            "co2_released": 0.0,
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": round(early_flux, 3),
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
