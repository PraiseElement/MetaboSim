"""
Glycolysis kinetic simulation engine.

Models the 10-step glycolytic pathway using simplified Michaelis-Menten
kinetics with allosteric regulation rules. Returns flux rates and metabolite
levels for each reaction step.

Regulatory logic is based on classical biochemistry:
- Hexokinase (HK): inhibited by G6P product
- Phosphoglucose isomerase (PGI): near-equilibrium
- Phosphofructokinase-1 (PFK-1): KEY regulatory step
    - Activated by: AMP, ADP, fructose-2,6-bisphosphate (F2,6BP; insulin-dependent)
    - Inhibited by: ATP, citrate (high energy / TCA activity)
- Glyceraldehyde-3-phosphate dehydrogenase (GAPDH): requires NAD+
- Phosphoglycerate kinase (PGK): substrate-level ATP synthesis
- Pyruvate kinase (PK): activated by F1,6BP, inhibited by ATP, alanine
"""
import numpy as np
from typing import Dict, Tuple, List


# Michaelis-Menten helper: v = Vmax * S / (Km + S)
def mm(S: float, Vmax: float, Km: float) -> float:
    return Vmax * max(S, 0.0) / (Km + max(S, 0.0))


def simulate_glycolysis(params: Dict) -> Dict:
    """
    Simulate glycolysis given physiological parameters.

    Parameters (all from SimulationRequest):
        glucose_mM      : plasma glucose concentration
        oxygen_pct      : O2 availability (0-100%)
        insulin_fold    : insulin relative to basal
        glucagon_fold   : glucagon relative to basal
        energy_demand   : ATP demand multiplier
        nutritional_state: 'fed', 'fasted', 'starved'

    Returns:
        dict with 'enzymes', 'metabolites', 'metrics'
    """
    glucose = params.get("glucose_mM", 5.0)
    o2 = params.get("oxygen_pct", 100.0) / 100.0
    insulin = params.get("insulin_fold", 1.0)
    glucagon = params.get("glucagon_fold", 1.0)
    demand = params.get("energy_demand", 1.0)
    state = params.get("nutritional_state", "fed")

    # --- Derived regulatory signals ---
    # AMP level rises when energy demand is high
    amp_signal = min(1.0, demand / 3.0)
    # ATP inhibitory signal (high when demand is low)
    atp_signal = max(0.0, 1.0 - amp_signal * 0.7)
    # Citrate rises with high TCA / fatty acid oxidation (fasted)
    citrate_signal = 0.3 if state in ("fasted", "starved") else 0.1
    # F2,6BP increases with insulin (promotes glycolysis)
    f26bp_signal = min(1.0, insulin * 0.5)
    # NAD+ availability limited by hypoxia (NADH can't be reoxidized)
    nad_available = min(1.0, 0.2 + o2 * 0.8)

    # ----- STEP-BY-STEP FLUX CALCULATIONS -----

    # 1. Hexokinase (HK) / Glucokinase
    hk_activity = mm(glucose, 1.0, 0.1) * (1.0 - 0.3 * (1.0 / (1.0 + glucose)))
    hk_flux = hk_activity * min(1.0, insulin * 0.6 + 0.4)

    # 2. Phosphoglucose Isomerase (PGI) — near equilibrium
    pgi_flux = hk_flux * 0.98

    # 3. Phosphofructokinase-1 (PFK-1) — KEY regulated step
    pfk_activation = (1.0 + amp_signal * 2.0 + f26bp_signal * 1.5)
    pfk_inhibition = (1.0 + atp_signal * 1.5 + citrate_signal * 2.0)
    pfk_activity = min(1.0, pgi_flux * pfk_activation / pfk_inhibition)
    pfk_flux = pfk_activity

    # 4. Aldolase — cleaves F1,6BP into DHAP + G3P
    ald_flux = pfk_flux * 0.97

    # 5. Triose Phosphate Isomerase (TPI) — equilibrium
    tpi_flux = ald_flux

    # 6. Glyceraldehyde-3-P Dehydrogenase (GAPDH) — NAD+ dependent
    gapdh_flux = tpi_flux * nad_available

    # 7. Phosphoglycerate Kinase (PGK) — first ATP synthesis
    pgk_flux = gapdh_flux * 0.99

    # 8. Phosphoglycerate Mutase (PGM) — near equilibrium
    pgm_flux = pgk_flux * 0.99

    # 9. Enolase — near equilibrium
    eno_flux = pgm_flux * 0.99

    # 10. Pyruvate Kinase (PK) — second ATP synthesis
    # Activated by F1,6BP (proportional to PFK flux), inhibited by ATP
    pk_activation = 1.0 + pfk_flux * 1.2
    pk_inhibition = 1.0 + atp_signal * 0.8
    # Glucagon/fasting inhibits PK (promotes gluconeogenesis)
    pk_gs_inhibition = 1.0 + (glucagon - 1.0) * 0.5 if glucagon > 1.0 else 1.0
    pk_activity = min(1.0, eno_flux * pk_activation / (pk_inhibition * pk_gs_inhibition))
    pk_flux = pk_activity

    # --- Pyruvate fate ---
    # Under hypoxia: pyruvate → lactate (LDH)
    # Under aerobic: pyruvate → acetyl-CoA (PDH)
    hypoxia_factor = max(0.0, 1.0 - o2)
    lactate_output = pk_flux * hypoxia_factor * 0.9
    pdc_flux = pk_flux * (1.0 - hypoxia_factor * 0.85)  # pyruvate dehydrogenase

    # --- ATP yield (per glucose) ---
    # Glycolysis only performs SUBSTRATE-LEVEL phosphorylation:
    #   Investment phase:  2 ATP consumed (HK + PFK-1)
    #   Payoff phase:      4 ATP produced (2×PGK + 2×PK)
    #   Net:               2 ATP per glucose
    #
    # The 2 NADH produced by GAPDH are REDUCING EQUIVALENTS, not ATP.
    # They are passed to the ETC (OxPhos), which converts them to ATP there.
    # To avoid double-counting, we do NOT add NADH→ATP here.
    substrate_atp_produced = 4.0 * pk_flux    # 2×PGK + 2×PK
    substrate_atp_invested = 2.0 * hk_flux    # HK + PFK-1
    total_atp = substrate_atp_produced - substrate_atp_invested

    # NADH produced in glycolysis proper
    nadh_glycolysis = 2.0 * gapdh_flux

    # --- Metabolite levels (relative 0-1) ---
    g6p = max(0.0, min(1.0, hk_flux * 0.8 - pfk_flux * 0.6))
    f16bp = max(0.0, min(1.0, pfk_flux * 0.7))
    g3p = max(0.0, min(1.0, tpi_flux * 0.5 - gapdh_flux * 0.4))
    pyruvate = max(0.0, min(1.0, pk_flux * 0.6 - pdc_flux * 0.5))
    lactate = min(1.0, lactate_output * 1.5)

    # --- Build enzyme states ---
    def enzyme(eid, name, flux, activity, regulated, regulators, status):
        return {
            "enzyme_id": eid,
            "enzyme_name": name,
            "flux": round(flux, 3),
            "activity": round(activity, 3),
            "is_regulated": regulated,
            "regulators": regulators,
            "status": status,
        }

    def _status(act):
        if act >= 0.7:
            return "active"
        elif act >= 0.4:
            return "allosteric"
        else:
            return "inhibited"

    enzymes = [
        enzyme("HK",    "Hexokinase",                          hk_flux,    hk_activity,   True,  ["G6P (−)", "Insulin (+)"],                        _status(hk_activity)),
        enzyme("PGI",   "Phosphoglucose Isomerase",            pgi_flux,   pgi_flux,      False, [],                                                  _status(pgi_flux)),
        enzyme("PFK1",  "Phosphofructokinase-1",               pfk_flux,   pfk_activity,  True,  ["AMP (+)", "F2,6BP (+)", "ATP (−)", "Citrate (−)"], _status(pfk_activity)),
        enzyme("ALD",   "Aldolase",                            ald_flux,   ald_flux,      False, [],                                                  _status(ald_flux)),
        enzyme("TPI",   "Triose Phosphate Isomerase",          tpi_flux,   tpi_flux,      False, [],                                                  _status(tpi_flux)),
        enzyme("GAPDH", "Glyceraldehyde-3-P Dehydrogenase",    gapdh_flux, gapdh_flux,    True,  ["NAD⁺ (required)", "O₂ availability"],              _status(gapdh_flux)),
        enzyme("PGK",   "Phosphoglycerate Kinase",             pgk_flux,   pgk_flux,      False, [],                                                  _status(pgk_flux)),
        enzyme("PGM",   "Phosphoglycerate Mutase",             pgm_flux,   pgm_flux,      False, [],                                                  _status(pgm_flux)),
        enzyme("ENO",   "Enolase",                             eno_flux,   eno_flux,      False, [],                                                  _status(eno_flux)),
        enzyme("PK",    "Pyruvate Kinase",                     pk_flux,    pk_activity,   True,  ["F1,6BP (+)", "ATP (−)", "Glucagon (−)", "Alanine (−)"], _status(pk_activity)),
        enzyme("LDH",   "Lactate Dehydrogenase",               lactate_output, lactate_output, True, ["Pyruvate (+)", "NADH (+)", "O₂ (−)"],         _status(lactate_output) if o2 < 0.5 else "active" if o2 < 0.8 else "inhibited"),
        enzyme("PDH",   "Pyruvate Dehydrogenase Complex",      pdc_flux,   pdc_flux,      True,  ["O₂ required", "NADH (−)", "Acetyl-CoA (−)"],      _status(pdc_flux)),
    ]

    metabolites = [
        {"metabolite_id": "glucose",  "name": "Glucose",             "concentration": round(min(1.0, glucose/10.0), 3), "trend": "stable"},
        {"metabolite_id": "g6p",      "name": "Glucose-6-Phosphate", "concentration": round(g6p, 3),     "trend": "rising" if g6p > 0.5 else "stable"},
        {"metabolite_id": "f16bp",    "name": "Fructose-1,6-BP",     "concentration": round(f16bp, 3),   "trend": "rising" if pfk_flux > 0.7 else "stable"},
        {"metabolite_id": "g3p",      "name": "G3P",                 "concentration": round(g3p, 3),     "trend": "stable"},
        {"metabolite_id": "pyruvate", "name": "Pyruvate",            "concentration": round(pyruvate, 3),"trend": "rising" if pyruvate > 0.5 else "stable"},
        {"metabolite_id": "lactate",  "name": "Lactate",             "concentration": round(lactate, 3), "trend": "rising" if lactate > 0.4 else "stable"},
        {"metabolite_id": "atp",      "name": "ATP",                 "concentration": round(min(1.0, total_atp/10.0), 3), "trend": "stable"},
        {"metabolite_id": "nadh",     "name": "NADH",                "concentration": round(min(1.0, nadh_glycolysis/2.0 * (1.0 - o2 * 0.7)), 3), "trend": "rising" if o2 < 0.4 else "stable"},
    ]

    metrics = {
        "atp_yield": round(total_atp, 2),
        # ATP breakdown (for report)
        "atp_invested": round(substrate_atp_invested, 2),      # HK + PFK-1
        "atp_substrate_produced": round(substrate_atp_produced, 2),  # PGK + PK
        "nadh_produced": round(nadh_glycolysis, 2),            # → passed to OxPhos
        "fadh2_produced": 0.0,
        "co2_released": 0.0,
        "net_flux": round(pk_flux, 3),
        "pyruvate_output": round(pdc_flux, 3),
        "lactate_output": round(lactate_output, 3),
        "glucose_consumed": round(hk_flux, 3),
    }

    # --- Educational notes ---
    notes = []
    if o2 < 0.3:
        notes.append("Severe hypoxia: NADH cannot be reoxidised via ETC, blocking GAPDH. Cells switch to anaerobic glycolysis, generating lactate to regenerate NAD⁺.")
    if lactate_output > 0.5:
        notes.append("High lactate production. In clinical settings, persistent lactate > 2 mmol/L defines lactic acidaemia. If pH also falls, this is lactic acidosis.")
    if pfk_activity < 0.3:
        notes.append("PFK-1 is strongly inhibited — either by high ATP (energy surplus) or citrate (TCA is active). Glycolysis is downregulated appropriately.")
    if state == "fasted" and glucagon > 1.2:
        notes.append("Glucagon inhibits Pyruvate Kinase, diverting PEP toward gluconeogenesis instead of completing glycolysis.")
    if insulin > 2.0:
        notes.append("High insulin promotes F2,6BP synthesis, strongly activating PFK-1 and accelerating glycolytic flux.")
    if demand > 3.0:
        notes.append("High energy demand increases AMP:ATP ratio, allosterically activating PFK-1 and accelerating ATP regeneration.")

    warnings = []
    if glucose < 2.0:
        warnings.append("Glucose critically low (< 2 mM). Real hypoglycaemia triggers counter-regulatory hormone release.")
    if lactate_output > 0.7 and o2 < 0.3:
        warnings.append("Risk of lactic acidosis: very high lactate with severe hypoxia.")

    return {
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": metrics,
        "educational_notes": notes,
        "warnings": warnings,
    }
