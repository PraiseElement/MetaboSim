"""
Galactose Metabolism — Leloir Pathway
Dietary galactose -> Gal-1-P -> G1P -> G6P -> Glycolysis / Glycogenesis

Key enzymes: Galactokinase (GALK), GALT (galactose-1-phosphate uridylyltransferase),
             UDP-galactose-4-epimerase (GALE), Phosphoglucomutase (PGM)
Disorders: Classic Galactosaemia (GALT deficiency), Galactokinase deficiency, GALE deficiency
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


def simulate_galactose_metabolism(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # Use glucose_mM as proxy for dietary carbohydrate/lactose load
    galactose_factor = min(glucose_mM / 5.0, 2.5)

    # ── Scenario ───────────────────────────────────────────────────
    if galactose_factor > 1.5 and nutr_state == "fed":
        scenario = "high_galactose_load"
    elif nutr_state in ("fasted", "starved"):
        scenario = "fasted_galactose"
    elif insulin_fold > 2 and galactose_factor > 1:
        scenario = "postprandial_galactose"
    else:
        scenario = "normal_galactose"

    # ── Enzyme fluxes ──────────────────────────────────────────────
    galk_flux = 0.65 * galactose_factor
    galk_flux = max(0.05, min(galk_flux, 1.0))

    # GALT: Gal-1-P + UDP-glucose -> G1P + UDP-galactose
    galt_flux = galk_flux * 0.90
    galt_flux = max(0.05, min(galt_flux, 1.0))

    # GALE: UDP-galactose <-> UDP-glucose (bidirectional)
    gale_flux = galt_flux * 0.95

    # PGM: G1P -> G6P
    pgm_flux = galt_flux * 0.92

    # Downstream into glycolysis/glycogenesis
    downstream = pgm_flux * min(0.6 + 0.2 * insulin_fold, 1.0)
    downstream = max(0.05, min(downstream, 1.0))

    # ATP accounting (substrate-level phosphorylation only — ETC NOT counted here):
    #  - GALK consumes 1 ATP (galactose → Gal-1-P)
    #  - Downstream glycolysis produces 2 net substrate-level ATP per galactose unit
    #  - Net: 2 produced − 1 invested = ~1 ATP net per galactose
    #  - NADH (via GAPDH downstream) goes to OxPhos only — not counted here
    atp_substrate_produced = downstream * 2.0            # substrate-level glycolysis ATP only
    atp_invested           = galk_flux * 1.0             # GALK costs 1 ATP
    atp_yield              = atp_substrate_produced - atp_invested
    nadh_produced = downstream * 2.0    # 2 NADH per galactose unit via glycolysis (→ OxPhos)

    # Galactitol accumulates if GALT-equivalent flux < GALK flux (toxic in lens)
    galactitol_risk = max(0, galk_flux - galt_flux * 0.95)

    enzymes = [
        _enzyme("GALK",   "Galactokinase", galk_flux, galk_flux, False,
                ["consumes ATP", "deficiency = Galactokinase deficiency (cataracts only, no liver disease)",
                 "galactitol builds up via aldose reductase"], _status(galk_flux)),
        _enzyme("GALT",   "Galactose-1-P Uridylyltransferase (GALT)", galt_flux, galt_flux, True,
                ["deficiency = Classic Galactosaemia (autosomal recessive)",
                 "Gal-1-P accumulates -> hepatocyte toxicity",
                 "+UDP-glucose (substrate)"], _status(galt_flux)),
        _enzyme("GALE",   "UDP-Galactose-4-Epimerase", gale_flux, gale_flux, True,
                ["bidirectional — provides UDP-galactose for glycoprotein synthesis",
                 "GALE deficiency: mild (RBC only) to severe (fulminant neonatal)"],
                _status(gale_flux)),
        _enzyme("PGM3",   "Phosphoglucomutase", pgm_flux, pgm_flux, False,
                ["near-equilibrium"], _status(pgm_flux)),
        _enzyme("G6Pdwn", "G6P -> Glycolysis / Glycogenesis", downstream, downstream, True,
                ["+insulin (-> glycogenesis)", "+glucagon (-> glycolysis -> gluconeogenesis)"],
                _status(downstream)),
    ]

    metabolites = [
        {"metabolite_id": "galactose",  "name": "Galactose",               "concentration": round(galactose_factor, 3),     "trend": "stable"},
        {"metabolite_id": "gal1p",      "name": "Galactose-1-Phosphate",   "concentration": round(galk_flux * 0.80, 3),     "trend": "rising" if galt_flux < galk_flux * 0.85 else "stable"},
        {"metabolite_id": "udpgal",     "name": "UDP-Galactose",           "concentration": round(galt_flux * 0.70, 3),     "trend": "stable"},
        {"metabolite_id": "udpglc_gal", "name": "UDP-Glucose",            "concentration": round(gale_flux * 0.75, 3),     "trend": "stable"},
        {"metabolite_id": "g1p_gal",    "name": "Glucose-1-Phosphate",    "concentration": round(galt_flux * 0.85, 3),     "trend": "stable"},
        {"metabolite_id": "g6p_gal",    "name": "Glucose-6-Phosphate",    "concentration": round(pgm_flux * 0.80, 3),      "trend": "stable"},
        {"metabolite_id": "galactitol", "name": "Galactitol (lens toxic)","concentration": round(galactitol_risk * 0.60, 3),"trend": "rising" if galactitol_risk > 0.1 else "stable"},
        {"metabolite_id": "pyruvate_gal","name": "Pyruvate",              "concentration": round(downstream * 0.65, 3),    "trend": "stable"},
    ]

    notes = []
    warnings = []

    notes.append("Galactose is metabolised via the Leloir pathway in the liver, converting it to G6P for glycolysis or glycogenesis.")
    notes.append("UDP-galactose from GALE is essential for glycoprotein and glycolipid synthesis — complete GALE deficiency is lethal even on a galactose-free diet.")
    notes.append("Classic galactosaemia (GALT deficiency): Gal-1-P accumulates -> liver failure, intellectual disability, ovarian failure. Treatment: strict galactose-free diet from birth.")

    if galk_flux > 0.6 and galt_flux < 0.3:
        warnings.append("Gal-1-P accumulating (GALT-like suppression) — risk of hepatocellular toxicity and galactitol lens accumulation -> cataracts.")
    if scenario == "high_galactose_load":
        notes.append("High galactose load (heavy dairy intake in neonates): GALK flux may outstrip GALT capacity — neonatal screening (Beutler test) is critical.")
    if nutr_state == "fasted":
        notes.append("Fasting: endogenous galactose from glycoprotein turnover still enters the Leloir pathway — galactose restriction alone is insufficient in galactosaemia.")

    if galactitol_risk > 0.2:
        warnings.append("Elevated galactitol risk: accumulation in lens -> cataracts are likely. Galactitol cannot be metabolised and builds up irreversibly.")

    return {
        "pathway": "galactose_metabolism",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "atp_invested": round(atp_invested, 2),
            "atp_substrate_produced": round(atp_substrate_produced, 2),
            "net_flux": round(galt_flux, 3),
            "nadh_produced": round(nadh_produced, 2),
            "fadh2_produced": 0.0,
            "co2_released": round(downstream * 0.4, 2),
            "pyruvate_output": round(downstream * 0.65, 3),
            "lactate_output": 0.0,
            "glucose_consumed": round(galactose_factor, 3),
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
