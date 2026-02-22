"""
Nucleotide Degradation (Purine Catabolism → Uric Acid)
AMP/GMP/IMP → adenosine/inosine → hypoxanthine/guanine → xanthine → uric acid

Key enzymes:
  5'-Nucleotidase: AMP → Adenosine
  ADA: Adenosine → Inosine
  PNP (Purine Nucleoside Phosphorylase): Inosine → Hypoxanthine; Guanosine → Guanine
  XO (Xanthine Oxidase): Hypoxanthine → Xanthine → Uric Acid (produces H2O2/O2•-)

Pyrimidine catabolism (brief):
  UMP → Uridine → Uracil → β-alanine + NH3 + CO2 (maleic/fumaric acid pathway)
  CMP → Cytidine → Uracil (via deamination)
  dTMP → Thymine → β-aminoisobutyrate + NH3 + CO2

Clinical:
  Gout: uric acid > 6.8 mg/dL → crystals in joints, kidneys
  XO deficiency → Xanthinuria: low uric acid, xanthine stones
  PNP deficiency → selective T cell SCID (dGuo toxic to T cells)
  Allopurinol (xanthine oxidase competitive inhibitor): gout treatment
  Febuxostat (non-purine XO inhibitor): gout treatment, safe in PRPP excess
  Rasburicase (recombinant uricase): acute hyperuricaemia in tumour lysis syndrome
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


def simulate_nucleotide_degradation(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # Nucleotide turnover increases with: high energy demand (ATP used), fasting, tissue damage
    turnover_rate = min(energy_demand * 0.4 + (0.3 if nutr_state == "fasted" else 0.1), 1.0)
    # High protein/purine diet also increases load
    dietary_purines = min(glucose_mM / 5.0 * 0.5, 0.8)   # proxy for dietary purine load
    total_nt_load   = min(turnover_rate + dietary_purines * 0.3, 1.0)

    if total_nt_load > 0.7:
        scenario = "high_purine_load_gout_risk"
    elif energy_demand > 3:
        scenario = "exercise_high_atp_turnover"
    elif nutr_state == "fasted":
        scenario = "fasted_nucleotide_degradation"
    else:
        scenario = "basal_nucleotide_degradation"

    # --- AMP/GMP degradation cascade ---
    nt5e_flux = total_nt_load * 0.80    # 5'-NT: AMP → Adenosine
    ada2_flux = nt5e_flux  * 0.75       # ADA: Adenosine → Inosine
    pnp_hx_flux = ada2_flux * 0.90      # PNP: Inosine → Hypoxanthine + Ribose-1P
    pnp_gua_flux = (total_nt_load * 0.30) * 0.80  # PNP: Guanosine → Guanine

    # Xanthine oxidase steps
    xo_hx_flux  = pnp_hx_flux   * 0.85   # XO: Hypoxanthine → Xanthine
    xo_xan_flux = xo_hx_flux    * 0.95   # XO: Xanthine → Uric Acid
    xo_gua_flux = pnp_gua_flux  * 0.80   # XO: Guanine → Xanthine (via guanine deaminase)
    uric_acid_production = xo_xan_flux + xo_gua_flux

    # Pyrimidine degradation
    dhu_flux = total_nt_load * 0.20    # Dihydrouracil dehydrogenase (DPYD): Uracil → DHU
    beta_ala_out = dhu_flux * 0.6      # β-alanine product (excreted or used for carnosine synthesis)

    # H2O2 and superoxide production by XO (important for oxidative stress)
    rox_prod = (xo_hx_flux + xo_xan_flux) * 0.5   # ROS produced per XO cycle (O2•- or H2O2)

    # ATP accounting: degradation produces no direct ATP
    # However: PNP produces ribose-1-phosphate (→ ribose-5-P → glycolysis — small energy recovery)
    atp_yield    = 0.0
    atp_invested = 0.0

    enzymes = [
        _enzyme("XO", "Xanthine Oxidase / Xanthine Dehydrogenase (XO / XDH)",
                xo_hx_flux, True,
                ["KEY enzyme: oxidises Hypoxanthine → Xanthine → Uric Acid",
                 "XO form: uses O2 → superoxide (O2•-) + H2O2 (ROS production — oxidative stress)",
                 "XDH form: uses NAD+ → NADH (less harmful in normal state; becomes XO under ischaemia)",
                 "TARGET OF ALLOPURINOL: competitive inhibitor (allopurinol → alloxanthine/oxypurinol, non-competitive)",
                 "TARGET OF FEBUXOSTAT: potent non-purine XO inhibitor; no activation by HGPRT",
                 "Rasburicase: recombinant uricase converts Urate → Allantoin (soluble); not available endogenously in humans"],
                _status(xo_hx_flux)),
        _enzyme("PNP", "Purine Nucleoside Phosphorylase (PNP)",
                pnp_hx_flux, False,
                ["Inosine → Hypoxanthine + Ribose-1P; Guanosine → Guanine + Ribose-1P",
                 "PNP DEFICIENCY → selective T cell deficiency (NOT B cells initially):",
                 "  dGuanosine accumulates → phosphorylated by kinases → dGTP toxic to T cells",
                 "  T cell SCID with near-normal Ig (unlike ADA-SCID which affects all lymphocytes)",
                 "Forodesine (immucillin-H): potent PNP inhibitor in clinical trials for T cell malignancies"],
                _status(pnp_hx_flux)),
        _enzyme("ADA2", "Adenosine Deaminase (ADA, degradation role)",
                ada2_flux, False,
                ["Adenosine → Inosine + NH3",
                 "Deficiency → SCID (same enzyme as in salvage — but operating in degradation mode)",
                 "Note: ADA2 (separate gene, CECR1) → ADA2 deficiency: vasculitis, strokes, immunodeficiency"],
                _status(ada2_flux)),
        _enzyme("NT5E", "5'-Nucleotidase (CD73 / NT5E, nuclear + cytoplasmic forms)",
                nt5e_flux, True,
                ["AMP → Adenosine + Pi",
                 "Initiates degradation cascade or generates extracellular adenosine (CD73 ecto-enzyme)",
                 "Elevated during ischaemia — releases purines for signalling + degradation"],
                _status(nt5e_flux)),
        _enzyme("DPYD", "Dihydropyrimidine Dehydrogenase (DPYD)",
                dhu_flux, True,
                ["Rate-limiting enzyme of pyrimidine catabolism: Uracil → DHU",
                 "DPYD deficiency (SNP DPYDc.1905+1G>A, Caucasian): 5-FU accumulates → severe toxicity",
                 "Before 5-FU administration, DPYD genotyping now recommended (EU guidance 2020)"],
                _status(dhu_flux)),
    ]

    metabolites = [
        {"metabolite_id": "adosn_d","name": "Adenosine",                    "concentration": round(ada2_flux * 0.3, 3),   "trend": "stable"},
        {"metabolite_id": "inosn_d","name": "Inosine",                      "concentration": round(pnp_hx_flux * 0.4, 3), "trend": "stable"},
        {"metabolite_id": "hx_d",   "name": "Hypoxanthine",                 "concentration": round(xo_hx_flux * 0.3, 3),  "trend": "falling" if xo_hx_flux > 0.3 else "rising"},
        {"metabolite_id": "xan_d",  "name": "Xanthine",                     "concentration": round(xo_xan_flux * 0.3, 3), "trend": "stable"},
        {"metabolite_id": "ua",     "name": "Uric Acid (plasma)",           "concentration": round(uric_acid_production, 3),"trend": "rising" if total_nt_load > 0.5 else "stable"},
        {"metabolite_id": "ros_d",  "name": "ROS (from XO)",               "concentration": round(rox_prod, 3),           "trend": "rising" if xo_hx_flux > 0.5 else "stable"},
        {"metabolite_id": "bala_d", "name": "β-Alanine (pyrimidine catab.)","concentration": round(beta_ala_out, 3),      "trend": "stable"},
    ]

    notes = [
        "Uric acid is uniquely insoluble (pKa 5.4) at physiological pH. Normal plasma urate < 6.0 (women), < 7.0 mg/dL (men). Supersaturation at > 6.8 mg/dL → monosodium urate crystal deposition → gout. Crystals in joints: acute inflammatory arthritis (podagra — 1st MTP joint). In kidney: urate nephrolithiasis.",
        "Allopurinol pharmacology: a 'suicide substrate' → hydroxylated by XO to oxypurinol (alloxanthine), which binds XO tightly (non-competitive, slowly reversible). Requires HGPRT for mild anti-gout efficacy. No HGPRT (Lesch-Nyhan) → allopurinol reduces uric acid but doesn't affect neurological features. Febuxostat is HGPRT-independent.",
        "Tumour Lysis Syndrome (TLS): rapid destruction of tumour cells (post-chemotherapy) → massive purine/pyrimidine release → acute hyperuricaemia + hyperkalaemia + hyperphosphataemia + hypocalcaemia. Urate crystals → AKI. Prevention/treatment: rasburicase (recombinant uricase; converts UA → allantoin, water-soluble) + allopurinol + vigorous IV hydration.",
        "XO as source of ROS in ischaemia-reperfusion injury: normally XDH form (uses NAD+); proteolytic cleavage during ischaemia → XO form (uses O2). On reperfusion, O2 floods in → massive superoxide burst → oxidative tissue injury (heart, intestine, kidney). XO inhibitors (allopurinol) tested as cardioprotective agents.",
        "DPYD pharmacogenomics: ~5% Caucasians are heterozygous DPYD-deficient → 5-FU metabolised slowly → drug accumulates → severe toxicity (diarrhoea, neutropenia, stomatitis, mucositis, cardiac toxicity). CPIC Guidelines recommend DPYD genotyping before any fluoropyrimidine (5-FU, capecitabine). Dose reduce 25–50% in heterozygotes; avoid in homozygotes.",
    ]

    warnings = []
    if uric_acid_production > 0.7:
        warnings.append(f"High uric acid production ({round(uric_acid_production,2)} units): Gout risk elevated. Ensure adequate hydration (dilutes urate), consider allopurinol or febuxostat if sustained. Avoid high-purine foods (organ meat, shellfish, beer).")
    if rox_prod > 0.5:
        warnings.append(f"Elevated ROS from XO activity ({round(rox_prod,2)} units): significant oxidative stress. XO-derived superoxide can trigger inflammation, endothelial damage, and ischaemia-reperfusion injury. Consider antioxidant support and XO inhibitor therapy.")

    return {
        "pathway": "nucleotide_degradation",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": 0.0,
            "atp_invested": 0.0,
            "atp_substrate_produced": 0.0,
            "net_flux": round(xo_hx_flux, 3),
            "nadh_produced": 0.0,
            "fadh2_produced": 0.0,
            "co2_released": round(dhu_flux * 0.5, 2),   # pyrimidine catabolism CO2
            "uric_acid_produced": round(uric_acid_production, 2),
            "ros_produced": round(rox_prod, 2),
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": 0.0,
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
