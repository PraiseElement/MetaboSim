"""
Cholesterol Synthesis (Mevalonate Pathway)
Acetyl-CoA → Mevalonate → Squalene → Cholesterol

Key rate-limiting enzyme: HMG-CoA Reductase (HMGCR) — target of statins
Stoichiometry per cholesterol: 18 ATP + 16 NADPH consumed (very expensive)
Intermediates: Isoprene units (IPP,DMAPP) → farnesyl-PP → squalene → lanosterol → cholesterol
Side products: Dolichol (glycoprotein synthesis), Ubiquinone (CoQ, ETC), Farnesyl/Geranylgeranyl
               (protein prenylation of Ras, Rho — explains pleiotropic statin effects beyond lipid)
Regulation: SREBP-2 (sterol response element; low cholesterol → active), INSIG, SCAP
Clinical: Familial Hypercholesterolaemia (LDL receptor), Statins (HMGCR competitive inhibitors),
          Mevalonic aciduria (MVK def.), Smith-Lemli-Opitz (DHCR7 def.)
"""


def _enzyme(eid, name, flux, is_reg, regs, status):
    return {
        "enzyme_id": eid, "enzyme_name": name,
        "flux": round(flux, 4), "activity": round(flux, 4),
        "is_regulated": is_reg, "regulators": regs, "status": status,
    }


def _status(x):
    if x >= 0.65: return "active"
    if x >= 0.30: return "allosteric"
    return "inhibited"


def simulate_cholesterol_synthesis(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # Cholesterol synthesis is primarily a fed/hepatic process
    # SREBP-2: low intra-ER cholesterol → SCAP/INSIG releases SREBP-2 → nucleus → HMGCR transcription
    chol_demand = max(0.2, 0.7 - params.get("glucose_mM", 5.0) * 0.02)  # less demand if diet provides cholesterol
    # Insulin activates SREBP-1c and HMGCR dephosphorylation → more synthesis in fed state
    insulin_effect = min(insulin_fold * 0.4, 1.0)
    # Statins: we model statin use implicitly as parameter (energy_demand proxy for statin inhibition)
    statin_effect  = max(0.0, (energy_demand - 1.5) * 0.3)   # high energy_demand reduces HMGCR

    hmgcr_activity = min(0.9, chol_demand + insulin_effect * 0.2 - statin_effect)
    hmgcr_activity = max(0.05, hmgcr_activity)

    if nutr_state == "fed" and insulin_fold > 2:
        scenario = "fed_high_cholesterol_synthesis"
    elif nutr_state == "fasted":
        scenario = "fasted_reduced_synthesis"
    elif hmgcr_activity < 0.3:
        scenario = "statin_inhibited"
    else:
        scenario = "basal_cholesterol_synthesis"

    # --- Enzyme fluxes ---
    hmgcr_flux  = hmgcr_activity         # HMGCR: HMG-CoA → Mevalonate (rate-limiting, 2 NADPH)
    mvk_flux    = hmgcr_flux * 0.90      # Mevalonate Kinase: Mevalonate → Mevalonate-5P
    pmvk_flux   = mvk_flux * 0.90        # Phosphomevalonate Kinase
    mvd_flux    = pmvk_flux * 0.90       # MVD: Mevalonate-PP → IPP (decarboxylation)
    fps_flux    = mvd_flux * 0.50        # FPP Synthase: IPP+DMAPP → GPP → FPP
    sqle_flux   = fps_flux * 0.85        # Squalene synthase (FPP→squalene, 1 NADPH)
    cas1_flux   = sqle_flux * 0.80       # Lanosterol synthase
    dhcr7_flux  = cas1_flux * 0.85       # DHCR7 (7-dehydrocholesterol reductase): last step

    cholesterol_produced = dhcr7_flux

    # Side product fluxes (from FPP branch point)
    dolichol_flux    = fps_flux * 0.10   # for N-glycosylation
    ubiquinone_flux  = fps_flux * 0.10   # for ETC Complex I
    prenylation_flux = fps_flux * 0.15   # for Ras/Rho GTPases protein prenylation

    # ATP and NADPH costs
    # Per cholesterol: ~18 ATP + 16 NADPH (from various kinase steps and HMGCR)
    atp_invested = 18.0 * cholesterol_produced
    nadph_consumed = 16.0 * cholesterol_produced
    atp_yield = -atp_invested   # Very negative — cholesterol synthesis is costly

    enzymes = [
        _enzyme("HMGCR", "HMG-CoA Reductase (HMGCR)",
                hmgcr_flux, True,
                ["RATE-LIMITING enzyme of cholesterol synthesis",
                 "+SREBP-2 transcriptional induction (low intracellular cholesterol)",
                 "+Insulin (promotes dephosphorylation → active form)",
                 "−AMPK (phosphorylates → INACTIVE; energy depletion)",
                 "−Cholesterol (end-product feedback via INSIG-SCAP-SREBP-2 axis)",
                 "TARGET OF STATINS: competitive inhibitors at mevalonate binding site",
                 "Statins reduce LDL by 30–60%; also upregulate LDL receptor (LDLR) → clears plasma LDL"],
                _status(hmgcr_flux)),
        _enzyme("MVK", "Mevalonate Kinase (MVK)",
                mvk_flux, False,
                ["Mevalonate → Mevalonate-5-phosphate (2 ATP total for MVK+PMVK)",
                 "MVK deficiency → Mevalonic aciduria: elevated mevalonate + periodic fever",
                 "Also: Hyperimmunoglobulinaemia D with periodic fever syndrome (HIDS, partial MVK def.)"],
                _status(mvk_flux)),
        _enzyme("SQLE", "Squalene Epoxidase (SQLE)",
                sqle_flux, True,
                ["Converts Squalene → 2,3-oxidosqualene (uses O2, NADPH)",
                 "Secondary regulatory enzyme after HMGCR",
                 "Target of some antifungal drugs (e.g., terbinafine — fungal SQLE inhibitor)"],
                _status(sqle_flux)),
        _enzyme("DHCR7", "7-Dehydrocholesterol Reductase (DHCR7)",
                dhcr7_flux, False,
                ["Last step: 7-dehydrocholesterol → Cholesterol",
                 "DHCR7 deficiency → Smith-Lemli-Opitz Syndrome (SLO): multiple malformations",
                 "7-DHC also substrate for Vitamin D synthesis (Vitamin D3 precursor)"],
                _status(dhcr7_flux)),
        _enzyme("FPS", "Farnesyl Pyrophosphate Synthase (FPPS)",
                fps_flux, True,
                ["Branch point: FPP can go to cholesterol OR non-sterol products",
                 "FPP → Squalene (cholesterol route)",
                 "FPP → Dolichol (N-glycoprotein synthesis), Ubiquinone (CoQ, ETC), Farnesyl (Ras)",
                 "Bisphosphonates (anti-osteoporosis) inhibit FPPS → block osteoclast prenylation → apoptosis"],
                _status(fps_flux)),
    ]

    metabolites = [
        {"metabolite_id": "hmgcoa_c", "name": "HMG-CoA (input)",         "concentration": round(hmgcr_flux * 0.8, 3),   "trend": "falling"},
        {"metabolite_id": "meval_c",  "name": "Mevalonate",              "concentration": round(mvk_flux * 0.5, 3),     "trend": "stable"},
        {"metabolite_id": "ipp_c",    "name": "Isopentenyl-PP (IPP)",    "concentration": round(mvd_flux * 0.5, 3),     "trend": "stable"},
        {"metabolite_id": "fpp_c",    "name": "Farnesyl-PP (FPP)",       "concentration": round(fps_flux * 0.6, 3),     "trend": "stable"},
        {"metabolite_id": "squalene", "name": "Squalene",                "concentration": round(sqle_flux * 0.4, 3),    "trend": "stable"},
        {"metabolite_id": "chol_c",   "name": "Cholesterol (produced)",  "concentration": round(cholesterol_produced, 3),"trend": "rising" if hmgcr_flux > 0.5 else "stable"},
        {"metabolite_id": "dolichol", "name": "Dolichol (N-glycosylation)","concentration": round(dolichol_flux, 3),   "trend": "stable"},
        {"metabolite_id": "uq_c",     "name": "Ubiquinone (CoQ, ETC)",   "concentration": round(ubiquinone_flux, 3),    "trend": "stable"},
    ]

    notes = [
        f"Cholesterol synthesis at {round(hmgcr_activity*100)}% HMGCR activity: ~{round(cholesterol_produced,2)} units synthesised. ATP cost: ~{round(atp_invested,1)} ATP. NADPH consumed: ~{round(nadph_consumed,1)}. This is one of the most energy-expensive biosynthetic processes in the body.",
        "Statin pharmacology: competitive inhibitors of HMGCR, binding with Ki ~100-fold lower than the natural substrate HMG-CoA. Reduced intracellular cholesterol → SCAP escorts SREBP-2 from ER to Golgi → cleavage → active SREBP-2 → upregulates LDLR transcription → more LDL cleared from plasma. This receptor upregulation accounts for 70% of the LDL-lowering effect.",
        "Non-sterol products of the mevalonate pathway explain statin 'pleiotropic effects': reduced Ras/Rho prenylation → anti-inflammatory, antiproliferative, plaque-stabilising effects. These occur at lower statin doses and partially explain cardiovascular protection beyond LDL reduction.",
        "SREBP-SCAP-INSIG axis (master regulator): When ER cholesterol is low → INSIG releases SCAP → SCAP escorts SREBP-2 to Golgi → S1P + S2P proteases cleave SREBP-2 → active fragment enters nucleus → HMGCR, LDLR, PCSK9 transcription increases. When ER cholesterol is high → INSIG retains SCAP-SREBP-2 in ER → synthesis suppressed.",
        "Smith-Lemli-Opitz (SLO): DHCR7 deficiency → 7-DHC accumulates, cholesterol depleted → multiple congenital anomalies (2nd/3rd toe syndactyly pathognomonic, microcephaly, ASD). Severity correlates with residual DHCR7 activity. Treat with cholesterol supplementation. Incidence ~1:20,000.",
    ]

    warnings = []
    if cholesterol_produced > 0.7:
        warnings.append(f"Very high cholesterol synthesis ({round(cholesterol_produced*100)}% of max). Combined with dietary intake, plasma cholesterol may be markedly elevated. LDL-C risk if LDLR expression is also reduced (FH).")
    if hmgcr_flux < 0.1 and energy_demand > 2:
        warnings.append("Very low HMGCR flux: statin-equivalent suppression. Critical — ubiquinone (CoQ10) synthesis is also reduced. Prolonged statin use at very high doses may cause statin myopathy (CoQ10 depletion in muscle).")

    return {
        "pathway": "cholesterol_synthesis",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "atp_invested": round(atp_invested, 2),
            "atp_substrate_produced": 0.0,
            "net_flux": round(hmgcr_flux, 3),
            "nadh_produced": 0.0,
            "fadh2_produced": 0.0,
            "nadph_consumed": round(nadph_consumed, 2),
            "co2_released": 0.0,
            "cholesterol_synthesised": round(cholesterol_produced, 2),
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": 0.0,
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
