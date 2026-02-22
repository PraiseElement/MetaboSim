"""
Phenylalanine & Tyrosine Metabolism
Phe → Tyr (PAH) → catecholamines + melanin + fumarate + acetoacetate

Key enzymes: PAH (BH4), TAT, HPD, HGD, Tyrosinase, TH, AADC, DBH, PNMT
Clinical: PKU (PAH def.), Tyrosinaemia type I/II/III, Alkaptonuria (HGD),
          Oculocutaneous albinism (tyrosinase), Catecholamine excess (phaeochromocytoma)
ATP yields: Mixed glucogenic (fumarate) + ketogenic (acetoacetate); net ~0 direct
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


def simulate_phenylalanine_tyrosine(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # Dietary Phe load (proxy = glucose_mM as 'substrate availability')
    phe_load = min(glucose_mM / 5.0, 2.0) * 0.6
    phe_load = max(0.1, min(phe_load, 1.0))

    # Scenario
    if phe_load > 0.7:
        scenario = "high_phe_load"
    elif energy_demand > 3:
        scenario = "high_demand_catecholamines"
    elif nutr_state == "fasted" and glucagon_fold > 1.5:
        scenario = "fasted_phe_catabolism"
    else:
        scenario = "normal_phe_tyr_metabolism"

    # BH4 (tetrahydrobiopterin) availability — limits PAH
    bh4_avail = min(0.9, 0.5 + energy_demand * 0.1)

    # --- Enzyme fluxes ---
    # Step 1: Phe → Tyr (PAH, BH4-dependent) — PKU if absent
    pah_flux = phe_load * bh4_avail * 0.85
    pah_flux = max(0.05, min(pah_flux, 1.0))

    # Branch 1: Tyr → catecholamines (adrenal/brain)
    th_flux  = pah_flux * 0.25    # Tyrosine Hydroxylase (TH): Tyr → DOPA; rate-limiting for catecholamines
    aadc_flux = th_flux * 0.90    # AADC: DOPA → Dopamine
    dbh_flux  = aadc_flux * 0.60  # DBH: Dopamine → Noradrenaline
    pnmt_flux = dbh_flux * 0.40   # PNMT: NA → Adrenaline (adrenal medulla only)

    # Branch 2: Tyr → melanin (melanocytes)
    tyrosinase_flux = pah_flux * 0.10

    # Branch 3: Tyr → catabolism to fumarate + acetoacetate (liver)
    tat_flux  = pah_flux * 0.55    # TAT: Tyr → p-hydroxyphenylpyruvate
    hpd_flux  = tat_flux * 0.90    # HPD: HPPA → homogentisate
    hgd_flux  = hpd_flux * 0.90    # HGD: homogentisate → maleylacetoacetate  (Alkaptonuria if absent)
    fah_flux  = hgd_flux * 0.85    # FAH: fumarylacetoacetate → fumarate + acetoacetate (Tyr-I if absent)

    # Fumarate → TCA (glucogenic), acetoacetate → ketone body (ketogenic)
    fumarate_out   = fah_flux * 0.5   # glucogenic portion
    acetoacetate_out = fah_flux * 0.5  # ketogenic portion

    # --- ATP accounting ---
    # PAH uses BH4 (not ATP directly); BH4 regeneration costs 1 NADPH per cycle
    # Fumarate entry into TCA → eventually generates NADH (via MDH/malate)
    # No direct substrate-level ATP
    atp_yield    = 0.0
    atp_invested = pah_flux * 0.0   # BH4 regeneration costs NADPH not ATP
    nadh_produced = fumarate_out * 0.5  # indirect from TCA entry

    enzymes = [
        _enzyme("PAH", "Phenylalanine Hydroxylase (PAH)",
                pah_flux, True,
                ["+BH4 (tetrahydrobiopterin) — REQUIRED cofactor",
                 "−High Phe (substrate inhibition at excess)",
                 "PAH deficiency → PKU (phenylketonuria): Phe accumulates, inhibits LNAA transport to brain",
                 "BH4 also required by TH, TPH — explains NTX-like features in BH4-deficient PKU"],
                _status(pah_flux)),
        _enzyme("TH", "Tyrosine Hydroxylase (TH)",
                th_flux, True,
                ["+BH4-dependent (same cofactor as PAH)",
                 "Rate-limiting step in catecholamine biosynthesis",
                 "−Catecholamine product inhibition (dopamine/NA feedback)",
                 "+cAMP/PKA phosphorylation (stress response)"],
                _status(th_flux)),
        _enzyme("AADC", "Aromatic L-Amino Acid Decarboxylase (AADC)",
                aadc_flux, False,
                ["PLP (Vit B6) cofactor",
                 "Converts both DOPA→Dopamine AND 5-HTP→Serotonin",
                 "AADC deficiency → severe combined catecholamine+serotonin deficiency"],
                _status(aadc_flux)),
        _enzyme("DBH", "Dopamine β-Hydroxylase (DBH)",
                dbh_flux, False,
                ["Copper + Vitamin C (ascorbate) cofactors",
                 "Located in catecholamine storage vesicles (vesicular enzyme)",
                 "Converts Dopamine → Noradrenaline (also called norepinephrine)"],
                _status(dbh_flux)),
        _enzyme("TAT", "Tyrosine Aminotransferase (TAT)",
                tat_flux, True,
                ["+Glucocorticoids (induce TAT transcription — fasting response)",
                 "PLP cofactor",
                 "TAT deficiency → Tyrosinaemia type II (Richner-Hanhart syndrome): corneal erosions, palmoplantar keratoderma"],
                _status(tat_flux)),
        _enzyme("HGD", "Homogentisate Dioxygenase (HGD)",
                hgd_flux, False,
                ["HGD deficiency → Alkaptonuria: homogentisate accumulates, excreted in urine (darkens on standing)",
                 "Ochronosis: dark pigmentation of cartilage, sclerae",
                 "First inborn error of metabolism described (Garrod, 1902)"],
                _status(hgd_flux)),
        _enzyme("FAH", "Fumarylacetoacetase (FAH)",
                fah_flux, False,
                ["FAH deficiency → Tyrosinaemia type I (hepatorenal syndrome)",
                 "Fumarylacetoacetate + succinylacetone accumulate → hepatocellular damage, renal tubular dysfunction, hepatocellular carcinoma risk",
                 "Treatment: NTBC (nitisinone) inhibits HPD → reduces toxic intermediates"],
                _status(fah_flux)),
        _enzyme("TYR", "Tyrosinase (melanocytes)",
                tyrosinase_flux, False,
                ["Copper-containing enzyme",
                 "Converts Tyr → DOPA → DOPAquinone → melanin",
                 "Tyrosinase deficiency → Oculocutaneous Albinism type I (OCA1): no melanin",
                 "Also responsible for browning of cut apples or potatoes"],
                _status(tyrosinase_flux)),
    ]

    metabolites = [
        {"metabolite_id": "phe",    "name": "Phenylalanine",      "concentration": round(phe_load, 3),             "trend": "falling" if pah_flux > 0.4 else "rising"},
        {"metabolite_id": "tyr",    "name": "Tyrosine",           "concentration": round(pah_flux * 0.6, 3),       "trend": "stable"},
        {"metabolite_id": "dopa",   "name": "DOPA",               "concentration": round(th_flux * 0.5, 3),        "trend": "stable"},
        {"metabolite_id": "da",     "name": "Dopamine",           "concentration": round(aadc_flux * 0.55, 3),     "trend": "stable"},
        {"metabolite_id": "na",     "name": "Noradrenaline",      "concentration": round(dbh_flux * 0.6, 3),       "trend": "stable"},
        {"metabolite_id": "hga",    "name": "Homogentisate",      "concentration": round(hgd_flux * 0.3, 3),       "trend": "stable" if hgd_flux > 0.3 else "rising"},
        {"metabolite_id": "fum_pt", "name": "Fumarate (→ TCA)",  "concentration": round(fumarate_out, 3),         "trend": "stable"},
        {"metabolite_id": "acac_pt","name": "Acetoacetate",       "concentration": round(acetoacetate_out, 3),     "trend": "stable"},
    ]

    notes = [
        "PKU (Phenylketonuria): PAH deficiency → Phe accumulates → competitively inhibits large neutral amino acid (LNAA) transport at the blood-brain barrier → brain Tyr/Trp deficiency → impaired dopamine and serotonin synthesis → intellectual disability. Treatment: Phe-restricted diet ± BH4 supplementation (sapropterin for responsive variants) ± LNAA therapy.",
        "BH4 (tetrahydrobiopterin) is cofactor for PAH (Phe→Tyr), TH (Tyr→DOPA), TPH (Trp→5-HTP). BH4 deficiency (GCH1, PTS, QDPR mutations) → 'malignant hyperphenylalaninaemia' — diet alone insufficient; need neurotransmitter precursors (DOPA + 5-HTP).",
        "Alkaptonuria: Homogentisate accumulates → urine turns dark on standing (oxidation). Ochronosis (bluish-black pigmentation) in cartilage/sclerae from prolonged HGA polymer accumulation. Arthropathy similar to OA. Nitisinone (NTBC) now used.",
        "Catecholamine synthesisis pathway: Tyr → DOPA → Dopamine → Noradrenaline → Adrenaline. Rate-limited by TH. Stored in vesicles in adrenal medulla + sympathetic nerve terminals.",
        "Tyr is a conditionally essential amino acid: essential only when dietary Phe is insufficient OR PAH is non-functional (as in PKU). It must then be provided directly in the diet.",
    ]

    warnings = []
    if phe_load > 0.7 and scenario == "high_phe_load":
        warnings.append(f"High phenylalanine load ({phe_load:.2f}): without adequate PAH activity, Phe will accumulate. Risk of PKU-like metabolic phenotype. Plasma Phe > 360 µmol/L is the diagnostic threshold.")
    if pah_flux < 0.2:
        warnings.append("Low PAH flux: Phe hydroxylation severely impaired. Check for PKU, BH4 deficiency, or combined Phe overload. Phenylketones (phenylpyruvate, phenylacetate, phenyllactate) will accumulate.")

    return {
        "pathway": "phenylalanine_tyrosine",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "atp_invested": 0.0,
            "atp_substrate_produced": 0.0,
            "net_flux": round(pah_flux, 3),
            "nadh_produced": round(nadh_produced, 2),
            "fadh2_produced": 0.0,
            "co2_released": round(tat_flux * 0.3, 2),
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": 0.0,
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
