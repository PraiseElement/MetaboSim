"""
Oxidative Phosphorylation (OxPhos) simulation engine.

Models the electron transport chain (Complexes I-IV) and ATP synthase (Complex V).
Inputs: NADH and FADH2 from glycolysis and TCA cycle.
Outputs: ATP (via P/O ratios), H2O, O2 consumption.

Regulation:
- Substrate (NADH/FADH2) availability
- O2 as terminal electron acceptor
- ADP availability (drives ATP synthase)
- Proton motive force (PMF)
- Inhibitors: CN-, CO, oligomycin (educational simulations)
"""
from typing import Dict


def simulate_oxphos(params: Dict, glycolysis_result: Dict = None, tca_result: Dict = None) -> Dict:
    """Run the ETC + ATP synthase simulation."""

    o2 = params.get("oxygen_pct", 100.0) / 100.0
    demand = params.get("energy_demand", 1.0)

    # ADP availability drives ATP synthase (high demand = more ADP available)
    adp_available = min(1.0, demand / 3.0 + 0.3)

    # Collect reducing equivalents from upstream
    if glycolysis_result:
        nadh_cyto = glycolysis_result["metrics"]["nadh_produced"]    # cytoplasmic NADH
    else:
        nadh_cyto = 2.0 * 0.8  # estimate

    if tca_result:
        nadh_mito = tca_result["metrics"]["nadh_produced"]    # mitochondrial NADH
        fadh2 = tca_result["metrics"]["fadh2_produced"]
    else:
        nadh_mito = 6.0 * 0.8
        fadh2 = 2.0 * 0.8

    # Cytoplasmic NADH carries less energy (malate-aspartate shuttle: ~2.5 ATP, glycerol-3-P shuttle: ~1.5 ATP)
    # We use the malate-aspartate shuttle (2.5 ATP per NADH) as default
    total_nadh_equiv = nadh_mito + nadh_cyto * 0.9  # slight efficiency loss crossing membrane

    # --- Complex I (NADH:ubiquinone oxidoreductase) ---
    # NADH → NAD+ + 2e → pumps 4H+ across inner membrane
    c1_flux = min(1.0, total_nadh_equiv / 8.0) * o2
    c1_activity = c1_flux

    # --- Complex II (Succinate dehydrogenase) ---
    # FADH2 → FAD + 2e → does NOT pump protons
    c2_flux = min(1.0, fadh2 / 2.0) * o2
    c2_activity = c2_flux

    # --- Complex III (bc1 complex) ---
    # Ubiquinol → ubiquinone; pumps 4H+
    c3_input = (c1_flux + c2_flux) * 0.95
    c3_flux = c3_input * o2 * 0.97

    # --- Complex IV (Cytochrome c oxidase) ---
    # 4e + O2 → H2O; pumps 2H+; rate-limiting in hypoxia
    # Km for O2 is very low (~0.1 µM) but becomes rate-limiting at near-zero O2
    o2_effect = o2 / (0.01 + o2)  # tight sigmoid: near-full activity at 10% O2
    c4_flux = c3_flux * o2_effect * 0.98

    # Proton motive force (PMF) — drives Complex V
    pmf = (c1_flux * 4 + c2_flux * 0 + c3_flux * 4 + c4_flux * 2) / 12.0
    pmf_adjusted = min(1.0, pmf)

    # --- Complex V (ATP Synthase) ---
    # Rate depends on PMF and ADP/Pi availability
    atp_synthase_flux = pmf_adjusted * adp_available * o2

    # --- ATP yield calculation ---
    # P/O ratios: NADH (mito) = 2.5, NADH (cyto, mal-asp shuttle) ≈ 2.5, FADH2 = 1.5
    atp_from_nadh_mito = nadh_mito * 2.5 * atp_synthase_flux
    atp_from_nadh_cyto = nadh_cyto * 2.5 * atp_synthase_flux * 0.9
    atp_from_fadh2 = fadh2 * 1.5 * atp_synthase_flux
    total_atp_oxphos = atp_from_nadh_mito + atp_from_nadh_cyto + atp_from_fadh2

    o2_consumed = c4_flux * 0.5  # relative units

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
        enzyme("CI",   "Complex I (NADH Dehydrogenase)",      c1_flux,          True,  ["NADH (+)", "O₂ required", "Rotenone (−)"],         _status(c1_flux)),
        enzyme("CII",  "Complex II (Succinate DH)",           c2_flux,          True,  ["FADH₂ (+)", "OAA (−)"],                             _status(c2_flux)),
        enzyme("CIII", "Complex III (bc₁ complex)",           c3_flux,          True,  ["Ubiquinol (+)", "Antimycin A (−)"],                  _status(c3_flux)),
        enzyme("CIV",  "Complex IV (Cytochrome c Oxidase)",   c4_flux,          True,  ["O₂ (critical)", "CN⁻ (−)", "CO (−)"],               _status(c4_flux)),
        enzyme("CV",   "Complex V (ATP Synthase)",            atp_synthase_flux, True,  ["PMF (+)", "ADP/Pi (+)", "Oligomycin (−)"],          _status(atp_synthase_flux)),
    ]

    metabolites = [
        {"metabolite_id": "nadh_pool",  "name": "Mitochondrial NADH",  "concentration": round(min(1.0, nadh_mito / 6.0), 3), "trend": "stable"},
        {"metabolite_id": "fadh2_pool", "name": "FADH₂ Pool",          "concentration": round(min(1.0, fadh2 / 2.0), 3),    "trend": "stable"},
        {"metabolite_id": "ubiquinol",  "name": "Ubiquinol (QH₂)",     "concentration": round(c2_flux * 0.7 + c1_flux * 0.3, 3), "trend": "stable"},
        {"metabolite_id": "cytc",       "name": "Cytochrome c (red.)",  "concentration": round(c3_flux * 0.8, 3),             "trend": "stable"},
        {"metabolite_id": "pmf",        "name": "Proton Motive Force",  "concentration": round(pmf_adjusted, 3),              "trend": "rising" if atp_synthase_flux < 0.3 else "stable"},
        {"metabolite_id": "atp_oxphos", "name": "ATP (OxPhos output)",  "concentration": round(min(1.0, total_atp_oxphos / 30.0), 3), "trend": "stable"},
        {"metabolite_id": "o2_consumed","name": "O₂ Consumed",          "concentration": round(o2_consumed, 3),               "trend": "rising" if demand > 2 else "stable"},
    ]

    metrics = {
        "atp_yield": round(total_atp_oxphos, 2),
        "nadh_produced": 0.0,
        "fadh2_produced": 0.0,
        "co2_released": 0.0,
        "net_flux": round(atp_synthase_flux, 3),
        "pyruvate_output": 0.0,
        "lactate_output": 0.0,
        "glucose_consumed": 0.0,
    }

    notes = []
    if o2 < 0.1:
        notes.append("Anoxia: ETC completely blocked. Complex IV has no O₂ as terminal acceptor. PMF collapses → ATP synthase stops → only anaerobic glycolysis sustains life.")
    if o2 < 0.5:
        notes.append("Partial hypoxia: Complex IV rate limited by O₂. PMF is partially maintained but ATP yield is significantly reduced.")
    if demand > 3.5:
        notes.append("High energy demand depletes ADP quickly into ATP, but ADP is also required to drive ATP synthase. Cells upregulate ETC enzymes via PGC-1α signaling over time.")
    if atp_synthase_flux > 0.8:
        notes.append("ATP synthase running near maximum capacity — the system is efficiently converting the proton gradient into usable energy.")
    if c4_flux < 0.2:
        notes.append("Complex IV severely inhibited. CO and cyanide (CN⁻) bind Complex IV irreversibly — this is the mechanism of CO and cyanide poisoning.")

    warnings = []
    if o2 < 0.2 and demand > 2.0:
        warnings.append("Critical mismatch: high energy demand with near-zero O₂. Cellular energy crisis imminent.")

    return {
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": metrics,
        "educational_notes": notes,
        "warnings": warnings,
    }
