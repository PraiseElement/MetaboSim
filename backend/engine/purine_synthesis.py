"""
Purine De Novo Synthesis
IMP synthesis from scratch: 10 steps from PRPP + ATP + Gln + Gly + Asp + 10-formyl-THF + CO2

Key enzymes: PPAT (step 1, Gln-PRPP → PRA), GART, PFAS, ADSS, ADSL, ATIC, IMPDH (IMP→XMP→GMP)
AMP branch: ADSS + ADSL: IMP + Asp + GTP → AMP
GMP branch: IMPDH: IMP + NAD → XMP → GMP synthetase (requires ATP)

Stoichiometry per IMP: 5 ATP (4 from PPAT, GART, PFAS, FGARS, ATICS) + 2 NADPH + Gln (×2) + Gly + Asp
Per AMP from IMP: +1 GTP → AMP (+ fumarate)
Per GMP from IMP: +1 ATP + NAD → GMP (via IMP→XMP→GMP)
Note: Cross-regulation: excess AMP inhibits ADSS; excess GMP inhibits IMPDH

Clinical: MYF inhibitors target IMPDH (mycophenolate — immunosuppression),
          Azathioprine/6-MP (prodrug → 6-thio-IMP → poisons IMPDH + DNA),
          Methotrexate/pemetrexed (DHFR/MTHFD inhibitors → block 10-formyl-THF supply)
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


def simulate_purine_synthesis(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # PRPP availability drives purine synthesis (HMP shunt provides R5P → PRPP via PRPS)
    prpp_avail = min(glucose_mM / 5.0 * 0.7, 1.0)
    # Proliferating cells need more purines (e.g. rapid growth, immune activation)
    growth_demand = min(energy_demand * 0.5, 1.0)
    # Salvage pathway partially feeds back (when purines abundant → inhibit PPAT)
    salvage_feedback = 0.2   # normal modest feedback

    # De novo synthesis strongly inhibited when AMP/GMP/ADP/GDP are abundant
    amp_gmp_level = max(0.3, min(0.8 - growth_demand * 0.3, 0.9))  # inverse of demand

    if growth_demand > 0.7:
        scenario = "high_growth_purine_synthesis"
    elif nutr_state == "fasted":
        scenario = "fasted_reduced_synthesis"
    elif prpp_avail < 0.3:
        scenario = "prpp_limited_synthesis"
    else:
        scenario = "basal_purine_synthesis"

    # Main flux
    ppat_flux  = prpp_avail * (1.0 - amp_gmp_level * 0.6) * (1.0 - salvage_feedback)
    ppat_flux  = max(0.05, min(ppat_flux, 1.0))

    gart_flux  = ppat_flux * 0.90    # GART: 3 enzymes (GAR transformylase, PRA synthetase, AIRS)
    pfas_flux  = gart_flux * 0.90    # PFAS (PFAS multifunctional: FGAM synthetase + FGAM amidotransferase)
    atic_flux  = pfas_flux * 0.85    # ATIC: IMP cyclohydrolase — last step to IMP
    imp_produced = atic_flux

    # AMP branch: IMP + Asp + GTP → adenylosuccinate → AMP + fumarate
    adss_flux = imp_produced * 0.45   # ADSS: uses GTP
    adsl_flux = adss_flux * 0.90      # ADSL: releases fumarate
    amp_produced = adsl_flux

    # GMP branch: IMP → XMP (IMPDH, NAD-dependent) → GMP (GMP synthetase, ATP)
    impdh_flux = imp_produced * 0.45   # IMPDH: rate-limiting for GMP; target of MPA
    gmps_flux  = impdh_flux * 0.88     # GMP Synthetase
    gmp_produced = gmps_flux

    # ATP accounting per purine synthesised (de novo is VERY expensive)
    atp_per_imp   = 5.0   # PPAT (1) + GART (1) + PFAS (1) + FGARS (1) + ATIC-kinase-equiv (1)
    gtp_per_amp   = 1.0   # ADSS uses GTP
    atp_per_gmp   = 1.0   # GMP synthetase uses ATP
    atp_invested  = atp_per_imp * imp_produced + gtp_per_amp * amp_produced + atp_per_gmp * gmp_produced
    atp_yield     = -atp_invested

    # NADPH: 2 per 10-formyl-THF recycled (DHFR) — indirect, from folate cycle
    nadph_consumed = gart_flux * 0.3   # approximate DHFR cost for THF regeneration

    enzymes = [
        _enzyme("PPAT", "PRPP Amidotransferase (PPAT / GPAT)",
                ppat_flux, True,
                ["Rate-limiting step of purine de novo synthesis",
                 "+PRPP (substrate; from HMP shunt: R5P + 2 ATP via PRPS)",
                 "+Gln (substrate/N-donor)",
                 "−AMP, ADP, GMP, GDP (end-product feedback — purines inhibit their own synthesis)",
                 "Inhibited by 6-thioguanine / 6-MP after metabolic activation"],
                _status(ppat_flux)),
        _enzyme("GART", "GART / PFAS (Multifunctional purine enzymes)",
                gart_flux, False,
                ["GART catalyses 3 reactions (trifunctional); uses Gly, THF-formyl donor, Gln",
                 "PFAS catalyses 2 reactions; uses Gln as N-donor",
                 "Methotrexate blocks DHFR → THF depleted → formyl-THF supply blocked → GART stalls"],
                _status(gart_flux)),
        _enzyme("IMPDH", "IMP Dehydrogenase (IMPDH1/2)",
                impdh_flux, True,
                ["Rate-limiting step for GMP branch",
                 "+NAD+ (substrate; IMP → XMP + NADH)",
                 "−GMP/GDP (feedback inhibition)",
                 "TARGET OF MYCOPHENOLATE (MPA / MMF): non-competitive inhibitor → immunosuppression in transplant",
                 "IMPDH2 over-expressed in cancer (high GTP demand for proliferation)",
                 "Azathioprine/6-MP prodrug → 6-thio-IMP → potently inhibits IMPDH"],
                _status(impdh_flux)),
        _enzyme("ADSS", "Adenylosuccinate Synthetase (ADSS)",
                adss_flux, True,
                ["IMP → Adenylosuccinate: uses GTP (not ATP!) + Asp",
                 "Reciprocal regulation: excess AMP inhibits ADSS; excess GMP inhibits IMPDH",
                 "This cross-regulation maintains AMP:GMP balance"],
                _status(adss_flux)),
        _enzyme("ADSL", "Adenylosuccinate Lyase (ADSL)",
                adsl_flux, False,
                ["Adenylosuccinate → AMP + Fumarate",
                 "ADSL deficiency → Adenylosuccinate lyase deficiency (ADSL def.):",
                 "  SAICAr and succinyladenosine accumulate → autism, seizures, intellectual disability"],
                _status(adsl_flux)),
    ]

    metabolites = [
        {"metabolite_id": "prpp",  "name": "PRPP (5-Phosphoribosyl-PP)", "concentration": round(prpp_avail * 0.5, 3),    "trend": "falling" if ppat_flux > 0.4 else "stable"},
        {"metabolite_id": "imp",   "name": "IMP (Inosine Monophosphate)", "concentration": round(imp_produced * 0.3, 3), "trend": "stable"},
        {"metabolite_id": "amp_de","name": "AMP (de novo)",              "concentration": round(amp_produced, 3),        "trend": "rising" if adsl_flux > 0.3 else "stable"},
        {"metabolite_id": "gmp_de","name": "GMP (de novo)",              "concentration": round(gmp_produced, 3),        "trend": "rising" if gmps_flux > 0.3 else "stable"},
        {"metabolite_id": "xmp",   "name": "XMP (intermediate)",         "concentration": round(impdh_flux * 0.2, 3),    "trend": "stable"},
    ]

    notes = [
        "Purine de novo synthesis is a 10-step pathway that builds the purine ring atom by atom from PRPP using Gly, Gln, Asp, CO2, and one-carbon donors from folate (10-formyl-THF). Extremely expensive: 5 ATP per IMP; 6 total for AMP; 7 total for GMP.",
        "IMP is the branch point: AMP branch uses GTP (ADSS), while GMP branch uses ATP (GMP synthetase). Cross-regulation: high AMP → inhibit ADSS (stops making more AMP); high GMP → inhibit IMPDH (stops making more GMP). This elegantly balances AMP:GMP ratios.",
        "Methotrexate mechanism: competitive DHFR inhibitor → polyglutamated MTX stays in cell → DHFR inhibited → THF depleted → 10-formyl-THF depleted → GART (step 3 + step 9 of purine synthesis) stalled; also TYMS (dTMP synthesis) blocked. Cancer cells die from purine + pyrimidine starvation. Used in ALL, lymphoma, RA, psoriasis.",
        "Mycophenolate (MMF): prodrug → MPA (mycophenolic acid) → non-competitive IMPDH inhibitor → GMP depleted. Lymphocytes (~T and B cells) RELY on IMPDH2 for GTP synthesis; other cells can use salvage. MPA selectively suppresses T/B cell proliferation → used for transplant immunosuppression, anti-GBM disease, lupus nephritis.",
        "Gout prevention connection: PRPP over-production (PRPS1 gain-of-function) or HGPRT deficiency (→ excess PRPP) → over-production of IMP → degraded to uric acid → hyperuricaemia → gout. Allopurinol inhibits xanthine oxidase (same pathway).",
    ]

    warnings = []
    if impdh_flux < 0.2:
        warnings.append("IMPDH severely suppressed: consistent with mycophenolate therapy or severe lymphocyte depletion. GTP pools will be critically low — impacts all GTP-requiring processes (G-proteins, tubulin polymerisation, EF-Tu/G translation, signal transduction).")
    if ppat_flux < 0.1 and growth_demand > 0.5:
        warnings.append("PPAT flux very low despite high cell growth demand: PRPP-limited or severe end-product inhibition. Cells may upregulate purine salvage to compensate.")

    return {
        "pathway": "purine_synthesis",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "atp_invested": round(atp_invested, 2),
            "atp_substrate_produced": 0.0,
            "net_flux": round(ppat_flux, 3),
            "nadh_produced": round(impdh_flux * 1.0, 2),   # IMPDH: IMP→XMP produces NADH
            "fadh2_produced": 0.0,
            "nadph_consumed": round(nadph_consumed, 2),
            "co2_released": 0.0,
            "amp_produced": round(amp_produced, 2),
            "gmp_produced": round(gmp_produced, 2),
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": round(prpp_avail * 0.5, 2),   # R5P diverted from HMP
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
