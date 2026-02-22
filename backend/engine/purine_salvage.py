"""
Purine Salvage Pathways
Recovery of free purines (adenine, hypoxanthine, guanine) from nucleotide turnover

Key enzymes:
  APRT (adenine phosphoribosyltransferase): Adenine + PRPP → AMP
  HGPRT (hypoxanthine-guanine PR transferase): Hypoxanthine + PRPP → IMP; Guanine + PRPP → GMP
  Adenosine Kinase (AK): Adenosine + ATP → AMP + ADP
  5'-Nucleotidase (CD73/NT5E): AMP → Adenosine + Pi (ecto-enzyme, immunosuppressive)
  ADA (Adenosine Deaminase): Adenosine → Inosine + NH3

Energy cost comparison: Salvage uses 1 PRPP vs De Novo uses 5 ATP per purine
Critical: salvage is the MAJOR pathway in most tissues (except liver which does both)

Clinical: HGPRT deficiency → Lesch-Nyhan syndrome (male, severe neurological, self-mutilation)
          ADA deficiency → Severe Combined Immunodeficiency (SCID); first gene therapy target
          APRT deficiency → adenine → 2,8-dihydroxyadenine kidney stones
          CD73 over-expression in cancer → immunosuppression by adenosine
          Allopurinol: comp. inhibitor of xanthine oxidase; also activated by HGPRT → allopurinol-like
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


def simulate_purine_salvage(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # Purine turnover rate drives salvage substrate availability
    turnover_rate = min(0.5 + energy_demand * 0.2, 1.0)   # higher energy demand → more turnover
    prpp_avail    = min(glucose_mM / 5.0 * 0.5, 1.0)

    if nutr_state == "fasted" and glucagon_fold > 1.5:
        scenario = "fasted_high_salvage"
    elif energy_demand > 3:
        scenario = "exercise_high_salvage"
    else:
        scenario = "basal_purine_salvage"

    # HGPRT: Hypoxanthine/Guanine → IMP/GMP (most important salvage enzyme)
    hgprt_hx_flux = turnover_rate * prpp_avail * 0.70    # hypoxanthine → IMP
    hgprt_gua_flux = turnover_rate * prpp_avail * 0.40   # guanine → GMP
    imp_from_salvage = hgprt_hx_flux
    gmp_from_salvage = hgprt_gua_flux

    # APRT: Adenine salvage → AMP
    aprt_flux = turnover_rate * prpp_avail * 0.50
    amp_from_salvage = aprt_flux

    # Adenosine Kinase (AK): Adenosine → AMP (main pathway for adenosine clearance in most cells)
    ak_flux = turnover_rate * 0.60
    # ADA (Adenosine Deaminase): Adenosine → Inosine → Hypoxanthine (degradation route)
    ada_flux = turnover_rate * 0.25   # less flux than AK (salvage preferred over degradation)
    # 5'-Nucleotidase (CD73): AMP → Adenosine (balance of purine pool)
    cd73_flux = amp_from_salvage * 0.15   # normally low

    # ATP accounting: salvage uses only 1 PRPP = 2 ATP equivalent vs 5+ for de novo
    # But: adenosine kinase uses 1 ATP
    atp_invested = ak_flux * 1.0    # AK: Ado + ATP → AMP
    amp_net_gain = amp_from_salvage + imp_from_salvage * 0.8 + ak_flux  # purines recovered
    atp_yield    = 0.0   # effectively neutral (saves ATPs vs de novo, not direct gain)

    enzymes = [
        _enzyme("HGPRT", "Hypoxanthine-Guanine Phosphoribosyltransferase (HGPRT/HPRT1)",
                max(hgprt_hx_flux, hgprt_gua_flux), True,
                ["Hypoxanthine + PRPP → IMP; Guanine + PRPP → GMP",
                 "Most important salvage enzyme in brain and erythrocytes (no de novo)",
                 "HGPRT deficiency → Lesch-Nyhan Syndrome (X-linked):",
                 "  Complete deficiency: self-mutilation, severe choreoathetosis, gout, intellectual disability",
                 "  Partial def. (Kelley-Seegmiller): gout only, no neurological features",
                 "  Excess PRPP (not re-used for salvage) → feeds de novo synthesis → ↑uric acid",
                 "Allopurinol metabolite (oxypurinol) is converted by HGPRT → competes with its own substrate"],
                _status(max(hgprt_hx_flux, hgprt_gua_flux))),
        _enzyme("APRT", "Adenine Phosphoribosyltransferase (APRT)",
                aprt_flux, False,
                ["Adenine + PRPP → AMP",
                 "APRT deficiency: adenine accumulates → xanthine oxidase converts to 2,8-DHA (dihydroxyadenine)",
                 "2,8-DHA is insoluble → radio-opaque kidney stones; confused with uric acid stones",
                 "Distinguish: uric acid dissolves in NaOH, 2,8-DHA does not; MASS SPEC confirmatory"],
                _status(aprt_flux)),
        _enzyme("ADA", "Adenosine Deaminase (ADA)",
                ada_flux, True,
                ["Adenosine → Inosine + NH3 (deamination)",
                 "ADA DEFICIENCY → ADA-SCID: deoxyadenosine accumulates → phosphorylated → dATP",
                 "  dATP is toxic to lymphocytes (inhibits ribonucleotide reductase → blocked dNTP synthesis)",
                 "  All lymphocytes (T, B, NK) killed → profound SCID",
                 "HISTORICAL NOTE: ADA-SCID was the first disease treated with gene therapy (1990)",
                 "Modern treatment: PEG-ADA enzyme replacement, or gene therapy (lentiviral HSPC)"],
                _status(ada_flux)),
        _enzyme("AK", "Adenosine Kinase (AK / ADK)",
                ak_flux, True,
                ["Adenosine + ATP → AMP + ADP",
                 "Primary clearance route for adenosine in most tissues",
                 "Keeps intracellular adenosine low → maintains signalling functions",
                 "Under hypoxia/ischaemia: AK inhibited → adenosine accumulates → A1/A2 receptors → cardioprotective, neuroprotective"],
                _status(ak_flux)),
        _enzyme("CD73", "5'-Nucleotidase (CD73/NT5E, ecto-enzyme)",
                cd73_flux, True,
                ["AMP → Adenosine + Pi (extracellular, ecto-enzyme on cell surface)",
                 "Normally low activity; over-expressed in cancer → generates extracellular Adenosine",
                 "Extracellular Adenosine → A2A/A2B receptors on T cells → immunosuppression",
                 "CD73 inhibitors in clinical trials as cancer immunotherapy adjuncts (e.g., oleclumab)"],
                _status(cd73_flux)),
    ]

    metabolites = [
        {"metabolite_id": "hx",    "name": "Hypoxanthine (→ HGPRT)",   "concentration": round(turnover_rate * 0.6, 3), "trend": "falling" if hgprt_hx_flux > 0.3 else "rising"},
        {"metabolite_id": "gua",   "name": "Guanine (→ HGPRT)",        "concentration": round(turnover_rate * 0.4, 3), "trend": "falling" if hgprt_gua_flux > 0.2 else "rising"},
        {"metabolite_id": "aden",  "name": "Adenine (→ APRT)",         "concentration": round(turnover_rate * 0.3, 3), "trend": "falling" if aprt_flux > 0.2 else "rising"},
        {"metabolite_id": "adosn", "name": "Adenosine",                "concentration": round(ada_flux * 0.3 + cd73_flux * 0.5, 3),"trend": "stable"},
        {"metabolite_id": "inosn", "name": "Inosine",                  "concentration": round(ada_flux * 0.5, 3),     "trend": "stable"},
        {"metabolite_id": "amp_sv","name": "AMP (salvaged)",           "concentration": round(amp_from_salvage, 3),   "trend": "rising"},
        {"metabolite_id": "imp_sv","name": "IMP (from Hx salvage)",    "concentration": round(imp_from_salvage, 3),   "trend": "rising"},
    ]

    notes = [
        "Purine salvage saves significant energy: recovering hypoxanthine to IMP costs just 1 PRPP (≈ 2 ATP) vs 5 ATP for de novo synthesis of IMP. Salvage is the MAJOR pathway in most differentiated cells (erythrocytes, brain neurons, cardiac muscle) that have limited or no de novo capacity.",
        "Lesch-Nyhan Syndrome (HGPRT deficiency): X-linked, males only. The neurological phenotype (self-biting) is puzzling — not fully explained by uric acid because allopurinol treats the gout but NOT the neurological features. Current theory: disrupted dopaminergic signalling in basal ganglia (neurodevelopmental role of purines in dopamine regulation).",
        "ADA-SCID: textbook example of how enzyme deficiency → metabolite accumulation → selective lymphocyte toxicity. Deoxyadenosine → dATP in lymphocytes (they express deoxynucleoside kinases). dATP inhibits ribonucleotide reductase → all dNTP synthesis blocked → DNA synthesis stops → apoptosis. Other cells tolerate excess adenosine better.",
        "Ecto-CD73 in tumour immune evasion: cancer cells up-regulate CD73 → produce extracellular adenosine → binds A2A receptors on CD8+ T cells and NK cells → Gs→cAMP → PKA → T cell exhaustion, inhibited cytotoxicity. Combining anti-CD73 mAb with PD-1/PD-L1 checkpoint inhibition is a promising immunotherapy strategy.",
    ]

    warnings = []
    if hgprt_hx_flux < 0.1 and ada_flux > 0.5:
        warnings.append("Very low HGPRT flux with high ADA activity: Lesch-Nyhan-like pattern. Hypoxanthine not salvaged → feeds xanthine oxidase → elevated uric acid. dAdo accumulates → lymphotoxic (ADA-SCID-like co-presentation if ADA also impaired).")

    return {
        "pathway": "purine_salvage",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "atp_invested": round(atp_invested, 2),
            "atp_substrate_produced": 0.0,
            "net_flux": round(max(hgprt_hx_flux, hgprt_gua_flux), 3),
            "nadh_produced": 0.0,
            "fadh2_produced": 0.0,
            "co2_released": 0.0,
            "purines_salvaged": round(imp_from_salvage + gmp_from_salvage + amp_from_salvage, 2),
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": round(prpp_avail * 0.3, 2),
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
