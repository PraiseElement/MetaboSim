"""
TCA (Citric Acid) Cycle kinetic simulation engine.

Models 8 enzymatic steps of the TCA cycle. Regulation based on:
- NADH/NAD+ ratio (product inhibition)
- ATP/ADP ratio (energy charge)
- Ca2+ (activated in exercising muscle)
- Substrate availability (acetyl-CoA from glycolysis/FAO)

Entry: Acetyl-CoA + Oxaloacetate (OAA)
Exit: 3 NADH, 1 FADH2, 1 GTP, 2 CO2 per turn
"""
from typing import Dict


def simulate_tca(params: Dict, glycolysis_result: Dict = None) -> Dict:
    """
    Simulate TCA cycle.

    Inputs come from glycolysis (acetyl-CoA from PDH) or from params directly.
    """
    o2 = params.get("oxygen_pct", 100.0) / 100.0
    demand = params.get("energy_demand", 1.0)
    state = params.get("nutritional_state", "fed")

    # Derive from glycolysis if available
    if glycolysis_result:
        acetyl_coa_input = glycolysis_result["metrics"]["pyruvate_output"]
    else:
        acetyl_coa_input = min(1.0, params.get("glucose_mM", 5.0) / 10.0) * 0.8

    # Ca2+ signal: high during exercise (demand > 2)
    ca2_signal = min(1.0, (demand - 1.0) / 4.0) if demand > 1.0 else 0.0

    # NADH back-pressure: high NADH slows TCA (product inhibition)
    # Hypoxia means NADH accumulates (ETC blocked)
    nadh_ratio = max(0.1, 1.0 - o2 * 0.6)  # 0 = fully oxidised, 1 = saturated

    # Energy charge: low when demand is high (more ADP available)
    energy_charge = max(0.2, 1.0 - demand * 0.15)

    # --- STEP-BY-STEP ---

    # 1. Citrate Synthase (CS) — condenses Acetyl-CoA + OAA → Citrate
    # Inhibited by citrate itself, NADH, succinyl-CoA
    cs_inhibition = 1.0 + (1.0 - energy_charge) * 0.5 + nadh_ratio * 1.5
    cs_flux = acetyl_coa_input * o2 / cs_inhibition

    # 2. Aconitase — Citrate → Isocitrate (near equilibrium)
    acn_flux = cs_flux * 0.97

    # 3. Isocitrate Dehydrogenase (IDH) — KEY regulatory
    # Activated by ADP/Ca2+, inhibited by ATP/NADH
    idh_activation = 1.0 + ca2_signal * 1.5 + (1.0 - energy_charge) * 1.2
    idh_inhibition = 1.0 + nadh_ratio * 2.0
    idh_flux = min(1.0, acn_flux * idh_activation / idh_inhibition)

    # 4. α-Ketoglutarate Dehydrogenase (AKGDH) — KEY regulatory
    # Similar to PDH; activated by Ca2+, inhibited by NADH/succinyl-CoA
    akgdh_inhibition = 1.0 + nadh_ratio * 1.8
    akgdh_activation = 1.0 + ca2_signal * 1.2
    akgdh_flux = min(1.0, idh_flux * akgdh_activation / akgdh_inhibition)

    # 5. Succinyl-CoA Synthetase — GTP synthesis (substrate level)
    scs_flux = akgdh_flux * 0.99

    # 6. Succinate Dehydrogenase (SDH) — FAD-dependent, directly in ETC (Complex II)
    # Inhibited by oxaloacetate
    oaa_inhibition = 1.0 + (1.0 - energy_charge) * 0.4
    sdh_flux = scs_flux / oaa_inhibition

    # 7. Fumarase — near equilibrium
    fum_flux = sdh_flux * 0.99

    # 8. Malate Dehydrogenase (MDH) — regenerates OAA
    # Inhibited by high NADH (thermodynamically disfavoured at high NADH)
    mdh_inhibition = 1.0 + nadh_ratio * 2.5
    mdh_flux = min(1.0, fum_flux / mdh_inhibition)

    # --- Outputs per turn ---
    turns = mdh_flux  # number of cycle turns (relative)
    nadh_tca = turns * 3.0     # 3 NADH per turn (IDH, AKGDH, MDH)
    fadh2_tca = turns * 1.0    # 1 FADH2 per turn (SDH)
    gtp_tca = turns * 1.0      # 1 GTP per turn
    co2_tca = turns * 2.0      # 2 CO2 per turn

    def _status(act):
        if act >= 0.7: return "active"
        elif act >= 0.35: return "allosteric"
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
        enzyme("CS",    "Citrate Synthase",                     cs_flux,    True,  ["OAA (+)", "Acetyl-CoA (+)", "NADH (−)", "Citrate (−)"],    _status(cs_flux)),
        enzyme("ACN",   "Aconitase",                            acn_flux,   False, [],                                                           _status(acn_flux)),
        enzyme("IDH",   "Isocitrate Dehydrogenase",             idh_flux,   True,  ["ADP (+)", "Ca²⁺ (+)", "ATP (−)", "NADH (−)"],              _status(idh_flux)),
        enzyme("AKGDH", "α-Ketoglutarate Dehydrogenase",        akgdh_flux, True,  ["Ca²⁺ (+)", "NADH (−)", "Succinyl-CoA (−)"],               _status(akgdh_flux)),
        enzyme("SCS",   "Succinyl-CoA Synthetase",              scs_flux,   False, [],                                                           _status(scs_flux)),
        enzyme("SDH",   "Succinate Dehydrogenase (Complex II)", sdh_flux,   True,  ["OAA (−)", "Fumarate (−)"],                                  _status(sdh_flux)),
        enzyme("FUM",   "Fumarase",                             fum_flux,   False, [],                                                           _status(fum_flux)),
        enzyme("MDH",   "Malate Dehydrogenase",                 mdh_flux,   True,  ["NADH (−)", "OAA (−)"],                                     _status(mdh_flux)),
    ]

    metabolites = [
        {"metabolite_id": "acetyl_coa", "name": "Acetyl-CoA",       "concentration": round(acetyl_coa_input, 3), "trend": "stable"},
        {"metabolite_id": "citrate",    "name": "Citrate",           "concentration": round(cs_flux * 0.6, 3),   "trend": "rising" if cs_flux > 0.7 else "stable"},
        {"metabolite_id": "isocitrate", "name": "Isocitrate",        "concentration": round(acn_flux * 0.4, 3),  "trend": "stable"},
        {"metabolite_id": "akg",        "name": "α-Ketoglutarate",   "concentration": round(idh_flux * 0.5, 3),  "trend": "stable"},
        {"metabolite_id": "succinate",  "name": "Succinate",         "concentration": round(scs_flux * 0.5, 3),  "trend": "stable"},
        {"metabolite_id": "malate",     "name": "Malate",            "concentration": round(fum_flux * 0.6, 3),  "trend": "stable"},
        {"metabolite_id": "oaa",        "name": "Oxaloacetate (OAA)","concentration": round(mdh_flux * 0.3, 3),  "trend": "falling" if mdh_flux < 0.3 else "stable"},
        {"metabolite_id": "nadh_tca",   "name": "NADH (TCA)",        "concentration": round(min(1.0, nadh_tca / 3.0), 3), "trend": "rising" if nadh_ratio > 0.6 else "stable"},
    ]

    metrics = {
        "atp_yield": round(gtp_tca, 2),
        "nadh_produced": round(nadh_tca, 2),
        "fadh2_produced": round(fadh2_tca, 2),
        "co2_released": round(co2_tca, 2),
        "net_flux": round(mdh_flux, 3),
        "pyruvate_output": 0.0,
        "lactate_output": 0.0,
        "glucose_consumed": 0.0,
    }

    notes = []
    if o2 < 0.2:
        notes.append("TCA cycle nearly halted: hypoxia prevents NADH reoxidation by ETC, causing severe product inhibition at IDH, AKGDH, and MDH.")
    if ca2_signal > 0.5:
        notes.append("High Ca²⁺ (exercise state) activates IDH and α-KGDH, accelerating the TCA cycle to match energy demand.")
    if nadh_ratio > 0.7:
        notes.append("NADH accumulation strongly inhibits the cycle — a feedback mechanism preventing runaway oxidation.")
    if acetyl_coa_input < 0.2:
        notes.append("Low acetyl-CoA input limits TCA flux. In starvation, ketone bodies can substitute as acetyl-CoA source.")

    warnings = []
    if mdh_flux < 0.1 and o2 < 0.3:
        warnings.append("TCA cycle severely impaired. ATP production will depend entirely on anaerobic glycolysis.")

    return {
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": metrics,
        "educational_notes": notes,
        "warnings": warnings,
    }
