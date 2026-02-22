"""
Urea Cycle
5-step cycle converting NH3 + CO2 + aspartate into urea for nitrogen excretion.
Occurs in periportal hepatocytes (steps 1-2 in mitochondria, steps 3-5 in cytoplasm).

Key enzymes: CPS-I, OTC, ASS, ASL, Arginase
Activation: N-Acetylglutamate (NAG) activates CPS-I
Clinical disorders: CPS-I def., OTC def. (X-linked, most common), ASS def. (citrullinaemia),
                   ASL def. (argininosuccinic aciduria), Arginase def. (hyperargininaemia)
ATP cost: 3 per cycle (2 ATP for CPS-I + 1 ATP equivalent for ASS via AMP→AMP+PPi = 2 ATP)
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


def simulate_urea_cycle(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")
    oxygen_pct    = params.get("oxygen_pct", 100)

    # Nitrogen load drives urea cycle activity
    protein_load = min((glucagon_fold / 2.0) + (0.5 if nutr_state == "fasted" else 0.0), 2.0)
    # High protein diet / fasting → high nitrogenous load
    nh3_load = max(0.1, min(protein_load * 0.7, 1.0))

    # NAG (N-acetylglutamate) availability: made from Glu + Acetyl-CoA by NAG synthase
    # High Glu (high protein catabolism) → high NAG → CPS-I activation
    nag_level = min(nh3_load * 1.1, 1.0)

    # Scenario
    if nh3_load > 0.6 and nutr_state == "fasted":
        scenario = "high_protein_fasted"
    elif insulin_fold > 2 and nutr_state == "fed":
        scenario = "fed_low_urea"
    elif energy_demand > 3:
        scenario = "exercise_increased_urea"
    else:
        scenario = "basal_urea_cycle"

    # --- Enzyme fluxes ---
    # Step 1 (mitochondria): NH3 + HCO3- + 2 ATP → carbamoyl-P   [CPS-I]
    cps1_flux = nh3_load * nag_level * 0.85
    cps1_flux = max(0.05, min(cps1_flux, 1.0))

    # Step 2 (mitochondria): Ornithine + Carbamoyl-P → Citrulline  [OTC] - X-linked gene
    otc_flux  = cps1_flux * 0.92

    # Step 3 (cytoplasm): Citrulline + Aspartate + ATP → Argininosuccinate  [ASS]
    ass_flux  = otc_flux * 0.90

    # Step 4 (cytoplasm): Argininosuccinate → Arginine + Fumarate  [ASL]
    asl_flux  = ass_flux * 0.95

    # Step 5 (cytoplasm, mainly liver): Arginine + H2O → Ornithine + Urea  [Arginase-1]
    arg1_flux = asl_flux * 0.98

    # Urea produced (main output) and ornithine recycled
    urea_output   = arg1_flux
    fumarate_out  = asl_flux      # enters TCA cycle → helps TCA run → NADH
    # Fumarate injection → can be converted to malate → OAA → aspartate (for next cycle turn)

    # --- ATP cost ---
    # CPS-I: consumes 2 ATP per carbamoyl-P
    # ASS: consumes 1 ATP (→ AMP + PPi, equivalent to 2 ATP hydrolysis high-energy)
    # Total: ~3 ATP per urea molecule (net cost, not benefit)
    atp_invested = cps1_flux * 3.0   # 2 CPS-I + 1 ASS (×2 for AMP = effectively 3)
    atp_yield    = -atp_invested       # Negative: urea cycle COSTS energy

    # NADH: minimal direct from urea cycle itself (fumarate → TCA gives indirect NADH)
    nadh_produced = fumarate_out * 0.5  # Indirect: fumarate → malate → OAA (MDH, NADH)

    enzymes = [
        _enzyme("CPS1", "Carbamoyl-Phosphate Synthetase I (CPS-I)",
                cps1_flux, True,
                ["+N-Acetylglutamate (NAG) — OBLIGATORY allosteric activator",
                 "NAG made by NAG synthase (activated by Arg, Glu)",
                 "−High energy charge (ATP inhibits above certain threshold)",
                 "Mitochondrial; CPS-II is cytoplasmic (pyrimidine synthesis, NOT urea cycle)"],
                _status(cps1_flux)),
        _enzyme("OTC", "Ornithine Transcarbamylase (OTC)",
                otc_flux, False,
                ["X-linked gene (Xp21.1) — most common urea cycle disorder",
                 "OTC deficiency: hyperammonaemia, spares females (heterozygous) but severe in males",
                 "Citrulline + ornithine antiporter (ORNT1) exports citrulline from mitochondria"],
                _status(otc_flux)),
        _enzyme("ASS", "Argininosuccinate Synthetase (ASS)",
                ass_flux, False,
                ["Rate-limiting step of cytoplasmic phase",
                 "ASS deficiency → Classical Citrullinaemia type I",
                 "Consumes 1 ATP → AMP + PPi (equivalent to 2 ATP)",
                 "Incorporates aspartate = provides the 2nd nitrogen of urea"],
                _status(ass_flux)),
        _enzyme("ASL", "Argininosuccinate Lyase (ASL)",
                asl_flux, False,
                ["ASL deficiency → Argininosuccinic aciduria",
                 "Releases fumarate → enters TCA (gluconeogenic precursor)",
                 "Arginine becomes available here — critical for NO synthesis"],
                _status(asl_flux)),
        _enzyme("ARG1", "Arginase-1 (Liver)",
                arg1_flux, True,
                ["+Arginine (substrate)",
                 "−Ornithine product inhibition at high levels",
                 "Arginase-1 def. → hyperargininaemia (spastic diplegia, intellectual disability)",
                 "Arginase-2 in kidney/brain for local arginine metabolism"],
                _status(arg1_flux)),
    ]

    metabolites = [
        {"metabolite_id": "nh3_uc",    "name": "Ammonia (NH₃, input)",   "concentration": round(nh3_load, 3),        "trend": "falling"},
        {"metabolite_id": "carp_uc",   "name": "Carbamoyl-Phosphate",    "concentration": round(cps1_flux * 0.6, 3), "trend": "stable"},
        {"metabolite_id": "citr_uc",   "name": "Citrulline",             "concentration": round(otc_flux * 0.5, 3),  "trend": "stable"},
        {"metabolite_id": "argsuc_uc", "name": "Argininosuccinate",      "concentration": round(ass_flux * 0.3, 3),  "trend": "stable"},
        {"metabolite_id": "arg_uc",    "name": "Arginine",               "concentration": round(asl_flux * 0.6, 3),  "trend": "stable"},
        {"metabolite_id": "orn_uc",    "name": "Ornithine (recycled)",   "concentration": round(arg1_flux * 0.7, 3), "trend": "stable"},
        {"metabolite_id": "urea_uc",   "name": "Urea (output)",          "concentration": round(urea_output, 3),     "trend": "rising"},
        {"metabolite_id": "fum_uc",    "name": "Fumarate (→ TCA)",       "concentration": round(fumarate_out * 0.4, 3),"trend": "stable"},
    ]

    notes = [
        "TWO nitrogen atoms are incorporated into urea: (1) NH₃ from amino acid catabolism via GDH → CPS-I, and (2) aspartate → argininosuccinate → ASL. This is why aspartate is an essential substrate.",
        "OTC deficiency (X-linked): the most common urea cycle disorder. Males are severely affected (no functioning allele); females are carriers but can show partial deficiency. Orotic acid is elevated in urine (carbamoyl-P builds up → pyrimidine synthesis).",
        "N-Acetylglutamate (NAG) is the OBLIGATORY allosteric activator of CPS-I. NAG is made from Glu + Acetyl-CoA by NAG synthase, which is activated by arginine. Deficiency of NAG synthase → hyperammonaemia responsive to N-carbamoylglutamate.",
        "ASL releases fumarate, which enters the TCA cycle — the 'aspartate-argininosuccinate shunt' connects the urea cycle to TCA, enabling gluconeogenesis under fasting conditions.",
        "Hyperammonaemia clinical presentation: vomiting, lethargy, encephalopathy, brain oedema. NH₃ is directly neurotoxic — impairs glutamate neurotransmission and promotes cerebral oedema. Treatment: arginine supplementation to drive the cycle, nitrogen scavengers (sodium benzoate, phenylbutyrate).",
    ]
    warnings = []
    if nh3_load > 0.7:
        warnings.append(f"High ammonia load ({nh3_load:.2f}) detected — hyperammonaemia risk. Normal plasma NH₃ < 50 µmol/L; >200 µmol/L → encephalopathy.")
    if cps1_flux < 0.2:
        warnings.append("Very low CPS-I flux — possible NAG deficiency, CPS-I enzyme deficiency, or severe energy depletion. Urea cycle cannot clear nitrogen load.")

    return {
        "pathway": "urea_cycle",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),             # Negative — cycle costs 3 ATP per turn
            "atp_invested": round(atp_invested, 2),
            "atp_substrate_produced": 0.0,
            "net_flux": round(cps1_flux, 3),
            "nadh_produced": round(nadh_produced, 2),
            "fadh2_produced": 0.0,
            "co2_released": round(cps1_flux * 1.0, 2),   # 1 CO2 fixed per CPS-I step
            "nitrogen_load": round(nh3_load, 2),
            "urea_produced": round(urea_output, 2),
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": 0.0,
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
