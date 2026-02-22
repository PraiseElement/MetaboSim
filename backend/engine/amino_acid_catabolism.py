"""
Amino Acid Catabolism Pathway
Transamination, deamination, and TCA entry points for 9 amino acid groups.

Key enzymes: ALT, AST, GDH, PDC, PCC, BCAT
Clinical: PKU, MSUD, HCU, urea cycle disorders (connect to downstream pathways)
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


# Entry points for each AA group into TCA / central metabolism
AA_TCA_ENTRIES = {
    "Ala, Cys, Gly, Ser, Thr":  "Pyruvate     → Acetyl-CoA via PDH",
    "Leu, Lys":                  "Acetyl-CoA   (purely ketogenic)",
    "Ile, Trp, Thr":             "Acetyl-CoA + Succinyl-CoA",
    "Val, Met, Ile":             "Succinyl-CoA via propionyl-CoA / PCC",
    "Asp, Asn":                  "Oxaloacetate (OAA)",
    "Glu, Gln, Pro, Arg, His":  "α-Ketoglutarate (via GDH / transamination)",
    "Phe, Tyr":                  "Fumarate + Acetoacetate (mixed gluco/keto)",
}


def simulate_amino_acid_catabolism(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # Protein mobilisation increases with fasting / glucagon
    protein_catab = min(glucagon_fold / 2.0 + (0.5 if nutr_state == "fasted" else 0.0), 2.0)
    # Insulin suppresses catabolism
    protein_catab *= max(0.3, 1.0 - (insulin_fold - 1.0) * 0.2)
    protein_catab = max(0.1, min(protein_catab, 1.0))

    # Scenario
    if nutr_state == "fasted" and glucagon_fold > 1.5:
        scenario = "fasted_protein_catabolism"
    elif energy_demand > 3:
        scenario = "high_energy_aa_catabolism"
    elif protein_catab < 0.3:
        scenario = "anabolic_low_catabolism"
    else:
        scenario = "basal_aa_catabolism"

    # --- Enzyme fluxes ---
    # Alanine aminotransferase (ALT): Ala + αKG ⇌ Pyr + Glu
    alt_flux = protein_catab * 0.70
    # Aspartate aminotransferase (AST): Asp + αKG ⇌ OAA + Glu
    ast_flux = protein_catab * 0.65
    # Glutamate dehydrogenase (GDH): Glu → αKG + NH4+
    gdh_flux = protein_catab * 0.60
    # Pyruvate dehydrogenase complex (PDC) for glucogenic entry
    pdc_flux = alt_flux * 0.80
    # Propionyl-CoA carboxylase (PCC) — odd-chain / Val/Met/Ile → succinyl-CoA
    pcc_flux = protein_catab * 0.30

    # --- ATP accounting (substrate-level from resulting TCA entry) ---
    # Glucogenic AAs entering pyruvate → glycolysis-equivalent ATP via PK
    # No direct substrate-level ATP from transamination itself
    # We report equiv. substrate-level ATP from glucogenic portion
    atp_substrate = pdc_flux * 1.0      # Each glucogenic unit eventually ≥1 substrate ATP via phosphoenolpyruvate
    atp_invested  = protein_catab * 0.0 # Transamination itself is ATP-neutral (PLP-dependent, reversible)
    atp_yield     = atp_substrate - atp_invested

    # Reducing equivalents: GDH oxidation of Glu → NADH
    nadh_produced = gdh_flux * 1.0   # 1 NADH per Glu → αKG oxidation
    # Nitrogen load
    nh3_produced  = gdh_flux * 1.0   # NH3 must be excreted → urea cycle

    enzymes = [
        _enzyme("ALT", "Alanine Aminotransferase (ALT / GPT)",
                alt_flux, True,
                ["+Glucagon (↑ protein catabolism)", "+Fasting state",
                 "−Insulin (suppresses overall catabolism)",
                 "PLP (Vit B6) cofactor — REQUIRED"],
                _status(alt_flux)),
        _enzyme("AST", "Aspartate Aminotransferase (AST / GOT)",
                ast_flux, True,
                ["+Glucagon", "+Fasting",
                 "PLP (Vit B6) cofactor — REQUIRED",
                 "Elevated in hepatocellular damage (liver panel marker)"],
                _status(ast_flux)),
        _enzyme("GDH", "Glutamate Dehydrogenase (GDH)",
                gdh_flux, True,
                ["+ADP, AMP, leucine (allosteric activators — low energy)",
                 "−NADH, GTP, ATP (product inhibition — energy surplus)",
                 "Mitochondrial matrix; links AA catabolism to TCA"],
                _status(gdh_flux)),
        _enzyme("PDC", "Pyruvate Dehydrogenase Complex (PDC)",
                pdc_flux, True,
                ["+ADP, CoA, NAD+ (activated by low energy)",
                 "−NADH, Acetyl-CoA, ATP (product inhibition)",
                 "−PDK (phosphorylation by PDH kinase → inactive)",
                 "+Ca2+ during exercise"],
                _status(pdc_flux)),
        _enzyme("PCC", "Propionyl-CoA Carboxylase (PCC)",
                pcc_flux, False,
                ["Biotin cofactor required",
                 "Converts propionyl-CoA (from Val/Met/Ile, odd-chain FA) → methylmalonyl-CoA → succinyl-CoA",
                 "Deficiency → propionic acidaemia"],
                _status(pcc_flux)),
    ]

    metabolites = [
        {"metabolite_id": "ala",    "name": "Alanine",           "concentration": round(alt_flux * 0.8, 3),   "trend": "falling" if alt_flux > 0.5 else "stable"},
        {"metabolite_id": "glu",    "name": "Glutamate",         "concentration": round(gdh_flux * 0.9, 3),   "trend": "stable"},
        {"metabolite_id": "akg",    "name": "α-Ketoglutarate",   "concentration": round(gdh_flux * 0.7, 3),   "trend": "rising" if gdh_flux > 0.5 else "stable"},
        {"metabolite_id": "oaa_aa", "name": "Oxaloacetate",      "concentration": round(ast_flux * 0.6, 3),   "trend": "stable"},
        {"metabolite_id": "pyr_aa", "name": "Pyruvate",          "concentration": round(pdc_flux * 0.5, 3),   "trend": "stable"},
        {"metabolite_id": "nh3",    "name": "Ammonia (NH₃)",     "concentration": round(nh3_produced * 0.4, 3),"trend": "rising" if nh3_produced > 0.4 else "stable"},
        {"metabolite_id": "urea_m", "name": "Urea (output)",     "concentration": round(nh3_produced * 0.3, 3),"trend": "rising"},
    ]

    notes = [
        "Transamination (ALT/AST) transfers α-amino groups to α-ketoglutarate, forming glutamate. Pyridoxal phosphate (Vitamin B6) is the essential cofactor — deficiency impairs all transamination reactions.",
        "Glutamate dehydrogenase (GDH) is the critical NH₃-release step: Glu → α-KG + NH₄⁺. NH₄⁺ is toxic at high concentrations → must be converted to urea (liver urea cycle) for excretion.",
        "Carbon skeletons of glucogenic amino acids enter TCA at: pyruvate (Ala, Cys, Gly, Ser), OAA (Asp, Asn), α-KG (Glu, Gln, Pro, Arg, His), succinyl-CoA (Val, Met, Ile), or fumarate (Phe, Tyr).",
        "Alanine-glucose cycle (Cahill cycle): muscle pyruvate + glutamate → alanine (via ALT) → alanine exported to liver → liver converts back to glucose via GNG, releasing alanine nitrogen as urea.",
        "Purely ketogenic amino acids (Leu, Lys) yield only acetyl-CoA — they CANNOT be converted to glucose. Useful for ketone body synthesis in fasting.",
    ]
    warnings = []
    if nh3_produced > 0.5:
        warnings.append(f"High NH₃ production ({nh3_produced:.2f} units) — ensure urea cycle capacity is adequate. Hyperammonaemia → encephalopathy if urea cycle is impaired (OTC deficiency, N-acetylglutamate synthase deficiency).")
    if nutr_state == "fasted" and glucagon_fold > 2:
        warnings.append("Prolonged fasting with high glucagon: extensive muscle protein catabolism for glucose production. Risk of muscle wasting and elevated urea nitrogen.")

    return {
        "pathway": "amino_acid_catabolism",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "atp_invested": round(atp_invested, 2),
            "atp_substrate_produced": round(atp_substrate, 2),
            "net_flux": round(protein_catab, 3),
            "nadh_produced": round(nadh_produced, 2),
            "fadh2_produced": 0.0,
            "co2_released": round(pdc_flux * 0.5, 2),
            "nitrogen_load": round(nh3_produced, 2),
            "pyruvate_output": round(pdc_flux * 0.7, 3),
            "lactate_output": 0.0,
            "glucose_consumed": 0.0,
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
