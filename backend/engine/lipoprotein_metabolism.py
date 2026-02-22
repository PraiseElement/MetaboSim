"""
Lipoprotein Metabolism
Chylomicrons (dietary fat) → VLDL → IDL → LDL and HDL pathways

Key enzymes: LPL (lipoprotein lipase), HTGL, LCAT, CETP, LDLR, PCSK9, ApoE, ApoB
Clinical: FH (familial hypercholesterolaemia — LDLR mutations), FH type II (ApoB),
          LPL deficiency (type I hyperTG), abetalipoproteinaemia (MTP),
          PCSK9-inhibitor therapy, Tangier disease (ABCA1)
ATP: 0 net direct from lipoprotein metabolism (transport/remodelling process)
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


def simulate_lipoprotein_metabolism(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # Dietary fat load → chylomicron production (postprandial)
    dietary_fat = min(glucose_mM / 5.0, 1.5) if nutr_state == "fed" else 0.1
    # VLDL production driven by hepatic TG synthesis (DNL, re-esterification)
    vldl_production = min(insulin_fold * 0.35 + dietary_fat * 0.2, 1.0)

    if nutr_state == "fed" and dietary_fat > 0.8:
        scenario = "postprandial_lipaemia"
    elif nutr_state == "fasted" and glucagon_fold > 1.5:
        scenario = "fasted_vldl_predominance"
    elif insulin_fold < 0.3:
        scenario = "insulin_deficient_hypertg"
    else:
        scenario = "basal_lipoprotein_metabolism"

    # --- Lipoprotein Processing Cascade ---
    # Chylomicron TG hydrolysis by LPL in capillaries (muscle, adipose, heart)
    lpl_flux = dietary_fat * 0.80 * min(insulin_fold * 0.6, 1.0)  # Insulin activates LPL
    # Chylomicron remnants → liver → cleared by ApoE receptors
    cm_remnant_flux = lpl_flux * 0.90

    # VLDL secretion from liver
    vldl_flux = vldl_production

    # VLDL lipolysis by LPL → IDL → LDL (ApoB100 retained, cholesterol-enriched)
    vldl_lpl_flux = vldl_flux * 0.75
    idl_flux      = vldl_lpl_flux * 0.90
    # HTGL (hepatic TG lipase): IDL → LDL (further TG hydrolysis → small, dense LDL)
    htgl_flux = idl_flux * 0.80
    ldl_prod  = htgl_flux

    # LDL clearance by LDLR (liver, max 70% LDL cleared)
    ldlr_flux = ldl_prod * 0.70   # Normal LDLR
    # FH: LDLR reduced → LDL accumulates
    plasma_ldl = ldl_prod * (1.0 - 0.70)   # residual plasma LDL after receptor clearance

    # PCSK9: degrades LDLR after LDL uptake → less surface LDLR → more plasma LDL
    pcsk9_activity = 0.30   # normal PCSK9 constitutive activity

    # HDL pathway: RCT (Reverse Cholesterol Transport)
    # ABCA1 effluxes cholesterol from macrophages → nascent HDL
    abca1_flux = 0.40 * (1.0 / max(insulin_fold, 0.5))   # HDL benefits from lower insulin
    # LCAT: esterifies free cholesterol on HDL → mature HDL3 → HDL2
    lcat_flux = abca1_flux * 0.75
    # CETP: transfers CE from HDL to VLDL/LDL (reduces HDL, a target of failed drugs)
    cetp_flux = lcat_flux * 0.50

    enzymes = [
        _enzyme("LPL", "Lipoprotein Lipase (LPL)",
                lpl_flux, True,
                ["+Insulin (induces LPL expression in adipose, muscle, heart)",
                 "+ApoCII (obligatory activator on chylomicrons/VLDL — deficiency = hyperTG)",
                 "−ApoCIII (inhibitor — elevated in insulin resistance → hypertriglyceridaemia)",
                 "LPL deficiency (type I) → massive hyperTG, pancreatitis, eruptive xanthomata",
                 "Anchored to capillary endothelium via GPIHBP1"],
                _status(lpl_flux)),
        _enzyme("LDLR", "LDL Receptor (LDLR, liver)",
                ldlr_flux, True,
                ["+SREBP-2 (low intracellular cholesterol → LDLR transcription)",
                 "+Statins (HMGCR inhibition → low intracellular chol → SREBP-2 active → LDLR up)",
                 "−PCSK9 (degrades LDLR after internalisation → fewer recycled to surface)",
                 "FH: loss-of-function LDLR mutations → markedly elevated LDL-C, premature MI",
                 "Heterozygous FH: 1:250–500; TC ~350–450 mg/dL; MI by 40s–50s",
                 "Homozygous FH: 1:1,000,000; TC > 600 mg/dL; MI in childhood"],
                _status(ldlr_flux)),
        _enzyme("PCSK9", "PCSK9 (Proprotein Convertase Subtilisn/Kexin 9)",
                pcsk9_activity, True,
                ["Serine protease that binds LDLR → targets it for lysosomal degradation",
                 "Higher PCSK9 → fewer surface LDLR → elevated plasma LDL",
                 "PCSK9 inhibitors (evolocumab, alirocumab): mAbs → block PCSK9-LDLR binding",
                 "→ LDLR recycled → markedly lower LDL (50–65% reduction on top of statins)",
                 "Gain-of-function PCSK9 mutation → ADH (Autosomal Dominant Hypercholesterolaemia)"],
                _status(pcsk9_activity)),
        _enzyme("LCAT", "Lecithin-Cholesterol Acyltransferase (LCAT)",
                lcat_flux, False,
                ["Esterifies free cholesterol (FC) on HDL surface → cholesterol ester (CE)",
                 "CE moves to HDL core → HDL matures (nascent discoidal → HDL3 → HDL2)",
                 "ApoAI activates LCAT",
                 "LCAT deficiency → Fish-eye disease: corneal opacity + HDL very low"],
                _status(lcat_flux)),
        _enzyme("ABCA1", "ATP-Binding Cassette A1 (ABCA1, macrophages/liver)",
                abca1_flux, True,
                ["Effluxes cholesterol + phospholipids from macrophages → lipid-poor ApoAI",
                 "Initiates reverse cholesterol transport (RCT)",
                 "ABCA1 deficiency → Tangier disease: orange tonsils, HDL near zero, neuropathy",
                 "+LXR activation (oxysterols) → ABCA1 transcription"],
                _status(abca1_flux)),
        _enzyme("HTGL", "Hepatic Triglyceride Lipase (HTGL)",
                htgl_flux, False,
                ["Converts IDL → LDL (removes TG from IDL to make small, dense LDL)",
                 "Also remodels HDL2 → HDL3 (smaller particles)",
                 "High HTGL + high CETP → atherogenic small dense LDL pattern"],
                _status(htgl_flux)),
    ]

    metabolites = [
        {"metabolite_id": "cm",    "name": "Chylomicrons (postprandial)", "concentration": round(dietary_fat * 0.5, 3),   "trend": "rising" if dietary_fat > 0.5 else "falling"},
        {"metabolite_id": "vldl",  "name": "VLDL (liver-secreted)",       "concentration": round(vldl_flux * 0.5, 3),    "trend": "rising" if nutr_state == "fasted" else "stable"},
        {"metabolite_id": "ldl",   "name": "LDL (plasma)",                "concentration": round(plasma_ldl, 3),         "trend": "rising" if ldlr_flux < 0.5 else "stable"},
        {"metabolite_id": "hdl",   "name": "HDL (mature)",                "concentration": round(lcat_flux * 0.6, 3),    "trend": "stable"},
        {"metabolite_id": "cm_rem","name": "Chylomicron Remnants",        "concentration": round(cm_remnant_flux * 0.3, 3),"trend": "falling"},
        {"metabolite_id": "tg_pl", "name": "Plasma Triglycerides",        "concentration": round(vldl_flux * 0.7 + dietary_fat * 0.3, 3),"trend": "rising" if lpl_flux < 0.4 else "stable"},
    ]

    notes = [
        "Lipoprotein order: Chylomicrons (largest, least dense, highest TG) → VLDL → IDL → LDL (smallest, densest, most cholesterol) → lipoproteins get progressively smaller and denser as TG is removed by LPL/HTGL.",
        "ApoB is the key structural apolipoprotein: ApoB-48 on chylomicrons (truncated, intestine), ApoB-100 on VLDL/IDL/LDL (full-length, liver). ApoB-100 mutation (ApoB 3500 mutation) → LDLR cannot bind → Familial Ligand-Defective ApoB100 (FH type II).",
        "PCSK9 inhibitor mechanism: PCSK9 normally binds LDLR during LDL endocytosis, causing LDLR degradation in lysosomes instead of recycling. Monoclonal antibodies (evolocumab, alirocumab) block this → LDLR is recycled → more surface LDLR → dramatically reduced plasma LDL (50–70% reduction). Now standard care in high-risk CV disease.",
        "LPL deficiency (type I hyperlipoproteinaemia): without LPL, chylomicrons and VLDL accumulate → plasma TG > 1000 mg/dL → acute pancreatitis risk. Creamy plasma (lipaemic serum), eruptive xanthomata on buttocks/elbows. Genetic: APOC2 (cofactor) or LPL mutations. No statins work here; treated with low-fat diet, fibrates.",
        "Reverse Cholesterol Transport (RCT): key anti-atherogenic pathway. Macrophage foam cell cholesterol → ABCA1 efflux → lipid-poor ApoAI → LCAT → mature HDL → SR-BI in liver → cholesterol excreted in bile. HDL-C as a biomarker of RCT capacity (though not causal — CETP inhibitor trials failed despite raising HDL).",
    ]

    warnings = []
    if dietary_fat > 0.8 and lpl_flux < 0.4:
        warnings.append("High dietary fat with low LPL activity: risk of severe hypertriglyceridaemia. Plasma TG > 500 mg/dL → acute pancreatitis risk. Restrict fat intake, consider fibrates or omega-3 therapy.")
    if ldlr_flux < 0.3:
        warnings.append(f"Severely reduced LDLR activity (flux {round(ldlr_flux,2)}): consistent with Familial Hypercholesterolaemia (FH) or PCSK9 GOF mutation. Plasma LDL will be markedly elevated → premature atherosclerosis. Statin + ezetimibe + PCSK9 inhibitor indicated.")

    return {
        "pathway": "lipoprotein_metabolism",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": 0.0,
            "atp_invested": 0.0,
            "atp_substrate_produced": 0.0,
            "net_flux": round(lpl_flux, 3),
            "nadh_produced": 0.0,
            "fadh2_produced": 0.0,
            "co2_released": 0.0,
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": 0.0,
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
