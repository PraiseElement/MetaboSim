"""
Gluconeogenesis simulation engine.

Models the reverse pathway from pyruvate/OAA/lactate to glucose.
Only active when metabolic state favours glucose synthesis:
- Fasted/starved state
- High glucagon
- Low insulin

Key bypass enzymes (not reversible in glycolysis):
1. Pyruvate Carboxylase (PC):  Pyruvate + CO2 → OAA  (mito)
2. PEPCK:                      OAA → PEP + CO2
3. FBPase-1:                   F1,6BP → F6P  (inhibited by F2,6BP, AMP)
4. G6Pase:                     G6P → Glucose (liver/kidney only)
"""
from typing import Dict


def simulate_gluconeogenesis(params: Dict) -> Dict:
    o2 = params.get("oxygen_pct", 100.0) / 100.0
    insulin = params.get("insulin_fold", 1.0)
    glucagon = params.get("glucagon_fold", 1.0)
    demand = params.get("energy_demand", 1.0)
    state = params.get("nutritional_state", "fed")

    # Gluconeogenesis is active in fasted/starved, suppressed by insulin
    gng_drive = 0.0
    if state == "fasted":
        gng_drive = 0.6
    elif state == "starved":
        gng_drive = 1.0
    else:
        gng_drive = 0.1

    gng_drive *= max(0.1, glucagon / max(0.1, insulin))
    gng_drive = min(1.0, gng_drive)

    # Substrate availability: lactate and amino acids as gluconeogenic precursors
    lactate_as_substrate = min(1.0, (1.0 - o2) * 0.7 + 0.2)  # more lactate during hypoxia
    alanine_substrate = 0.3 if state in ("fasted", "starved") else 0.1
    substrate = min(1.0, lactate_as_substrate + alanine_substrate)

    # --- STEP-BY-STEP ---

    # 1. Lactate Dehydrogenase (LDH) reverse — Lactate → Pyruvate (Cori cycle)
    ldh_r_flux = substrate * gng_drive * 0.9

    # 2. Pyruvate Carboxylase (PC) — Pyruvate → OAA; requires biotin, ATP
    # Activated by acetyl-CoA (signals fat oxidation is occurring)
    acetyl_coa_signal = 0.4 if state in ("fasted", "starved") else 0.15
    pc_activation = 1.0 + acetyl_coa_signal * 2.0
    pc_flux = ldh_r_flux * min(1.0, pc_activation) * gng_drive

    # 3. PEPCK — OAA → PEP + CO2; induced by glucagon/cortisol
    # Main rate-control step in GNG
    pepck_induction = min(2.0, glucagon * 0.8 + 0.4)
    pepck_inhibition = max(1.0, insulin * 0.8)
    pepck_flux = pc_flux * pepck_induction / pepck_inhibition

    # 4-7. Reverse glycolytic enzymes (PK, ENO, PGM, PGK) — running in reverse
    rev_flux = pepck_flux * 0.95

    # 8. FBPase-1 — F1,6BP → F6P
    # Inhibited by AMP (high demand) and F2,6BP (insulin-driven)
    amp_inhibition = 1.0 + min(1.0, (demand - 1.0) * 0.5)
    f26bp_inhibition = 1.0 + insulin * 0.8
    fbpase_flux = rev_flux / (amp_inhibition * f26bp_inhibition)

    # 9. PGI (reverse) — F6P → G6P
    pgi_r_flux = fbpase_flux * 0.98

    # 10. G6Pase — G6P → Glucose; only in liver and kidney
    g6pase_flux = pgi_r_flux * gng_drive * 0.95

    # Glucose output
    glucose_output = g6pase_flux

    # ATP cost: GNG costs 6 ATP per glucose (4 ATP + 2 GTP equivalent)
    atp_cost = g6pase_flux * 6.0

    def _status(act):
        if act >= 0.6: return "active"
        elif act >= 0.3: return "allosteric"
        else: return "inhibited"

    def enzyme(eid, name, flux, regulated, regulators, status):
        return {
            "enzyme_id": eid,
            "enzyme_name": name,
            "flux": round(flux, 3),
            "activity": round(flux, 3),
            "is_regulated": regulated,
            "regulators": regulators,
            "status": status,
        }

    enzymes = [
        enzyme("LDH_R",  "LDH (reverse, Cori cycle)",  ldh_r_flux,   True,  ["Lactate (+)", "O₂ (−, competes)"],                         _status(ldh_r_flux)),
        enzyme("PC",     "Pyruvate Carboxylase",         pc_flux,      True,  ["Acetyl-CoA (+)", "Biotin (cofactor)", "ATP required"],      _status(pc_flux)),
        enzyme("PEPCK",  "PEPCK",                        pepck_flux,   True,  ["Glucagon (+)", "Cortisol (+)", "Insulin (−)"],              _status(pepck_flux)),
        enzyme("REV",    "Reverse Glycolytic Steps",     rev_flux,     False, ["Glycolytic intermediates"],                                 _status(rev_flux)),
        enzyme("FBP1",   "FBPase-1",                     fbpase_flux,  True,  ["AMP (−)", "F2,6BP (−, insulin-driven)", "Glucagon (+)"],   _status(fbpase_flux)),
        enzyme("PGI_R",  "PGI (reverse)",                pgi_r_flux,   False, [],                                                          _status(pgi_r_flux)),
        enzyme("G6PASE", "Glucose-6-Phosphatase",        g6pase_flux,  True,  ["Liver/kidney specific", "Glucose-6-P (+)"],                 _status(g6pase_flux)),
    ]

    metabolites = [
        {"metabolite_id": "lactate_gng", "name": "Lactate (precursor)",  "concentration": round(lactate_as_substrate, 3), "trend": "falling" if gng_drive > 0.5 else "stable"},
        {"metabolite_id": "pyruvate_gng","name": "Pyruvate (GNG)",        "concentration": round(ldh_r_flux * 0.6, 3),    "trend": "stable"},
        {"metabolite_id": "oaa_gng",     "name": "OAA",                   "concentration": round(pc_flux * 0.5, 3),       "trend": "stable"},
        {"metabolite_id": "pep",         "name": "PEP",                   "concentration": round(pepck_flux * 0.6, 3),    "trend": "stable"},
        {"metabolite_id": "g6p_gng",     "name": "G6P (GNG)",             "concentration": round(pgi_r_flux * 0.4, 3),   "trend": "stable"},
        {"metabolite_id": "gng_glucose", "name": "New Glucose (output)",  "concentration": round(glucose_output, 3),      "trend": "rising" if glucose_output > 0.3 else "stable"},
    ]

    metrics = {
        "atp_yield": round(-atp_cost, 2),  # negative: GNG consumes ATP
        "nadh_produced": 0.0,
        "fadh2_produced": 0.0,
        "co2_released": round(-pepck_flux * 1.0, 2),  # CO2 released at PEPCK
        "net_flux": round(g6pase_flux, 3),
        "pyruvate_output": 0.0,
        "lactate_output": round(-ldh_r_flux * 0.5, 3),  # lactate consumed
        "glucose_consumed": round(-glucose_output, 3),    # glucose produced (negative = production)
    }

    notes = []
    if gng_drive > 0.6:
        notes.append("Gluconeogenesis is highly active. The liver is synthesising glucose from lactate (Cori cycle), alanine, and glycerol.")
    if pepck_flux > 0.5:
        notes.append("PEPCK is the main flux-controlling enzyme in GNG, transcriptionally induced by glucagon and cortisol during fasting.")
    if state == "fasted" and insulin < 0.5:
        notes.append("Low insulin removes F2,6BP production, releasing FBPase-1 from inhibition — a key feedforward switch into gluconeogenic mode.")
    if fbpase_flux < 0.1 and demand > 3.0:
        notes.append("AMP inhibits FBPase-1. During heavy exercise, even if glucagon is high, this prevents wasteful futile cycling.")
    if state == "fed":
        notes.append("In the fed state, high insulin suppresses PEPCK transcription and maintains high F2,6BP, keeping glycolysis dominant and GNG suppressed.")

    warnings = []
    if g6pase_flux < 0.05 and gng_drive > 0.5:
        warnings.append("GNG pathway is active but glucose release is blocked — could indicate G6Pase deficiency (Von Gierke disease model).")

    return {
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": metrics,
        "educational_notes": notes,
        "warnings": warnings,
    }
