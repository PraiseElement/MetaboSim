"""
Branched-Chain Amino Acid (BCAA) Catabolism
Val (glucogenic) → succinyl-CoA
Leu (ketogenic only) → 2 acetyl-CoA (+ HMG-CoA → acetoacetate)
Ile (mixed) → acetyl-CoA + propionyl-CoA → succinyl-CoA

Key enzymes: BCAT (PLP), BCKDH (TPP — Maple Syrup Urine Disease), IVD (Leu), MCC (Leu),
             HMGCL (Leu→ketogenic), MCCD (Val/Ile), PCC (propionyl-CoA→methylmalonyl-CoA)
Clinical: MSUD (BCKDH), Isovaleric acidaemia (IVD), Propionic acidaemia (PCC),
          Methylmalonic acidaemia (MUT, AdoCbl transport)
NOTE: BCAAss are catabolised primarily in muscle (BCAT rich there), NOT liver
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


def simulate_branched_chain_aa(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # BCAA catabolism increases with energy demand (exercise → muscle catabolism)
    bcaa_load = min(energy_demand / 2.0 + (0.3 if nutr_state == "fasted" else 0.0), 2.0)
    # Insulin suppresses BCKDH (promotes protein anabolism)
    bcaa_load *= max(0.3, 1.0 - (insulin_fold - 1.0) * 0.15)
    bcaa_load = max(0.1, min(bcaa_load, 1.0))

    # Scenario
    if energy_demand > 3 and nutr_state == "fasted":
        scenario = "exercise_fasting_bcaa_catabolism"
    elif insulin_fold > 2:
        scenario = "fed_low_bcaa_catabolism"
    elif bcaa_load > 0.7:
        scenario = "high_bcaa_oxidation"
    else:
        scenario = "basal_bcaa_catabolism"

    # --- Step 1: BCAT (Branched-Chain Aminotransferase) ---
    # Val + αKG → KIV + Glu | Leu + αKG → KIC + Glu | Ile + αKG → KMV + Glu
    # PLP cofactor; reversible; abundant in muscle (BCAT2)
    bcat_flux = bcaa_load * 0.90

    # --- Step 2: BCKDH complex (Branched-Chain α-Ketoacid Dehydrogenase) ---
    # KIV/KIC/KMV → isovaleryl-CoA/isobutyryl-CoA/α-methylbutyryl-CoA + CO2 + NADH
    # TPP (Vit B1) + lipoate + CoA + FAD + NAD+ cofactors
    # RATE-LIMITING step; MSUD if deficient
    # BCKDH kinase phosphorylates → INACTIVE (high energy, high BCAA product)
    # BCKDH phosphatase → ACTIVE
    bckdh_activity = min(0.9, bcaa_load * 0.95 / (1.0 + (insulin_fold - 1.0) * 0.3))
    bckdh_flux = bcat_flux * bckdh_activity

    # NADH produced (same as PDH/αKGDH — decarboxylative oxidation)
    bckdh_nadh = bckdh_flux * 1.0   # 1 NADH + 1 CO2 per keto acid decarboxylation

    # --- Branch: Leucine (ketogenic only) ---
    # isovaleryl-CoA → methylcrotonyl-CoA → methylglutaconyl-CoA → HMG-CoA → acetyl-CoA + acetoacetate
    ivd_flux  = bckdh_flux * 0.33    # IVD (Isovaleryl-CoA Dehydrogenase): FAD-dependent
    ivd_fadh2 = ivd_flux * 1.0
    mcc_flux  = ivd_flux * 0.85      # MCC (Methylcrotonyl-CoA Carboxylase): biotin-dependent
    hmgcl_leu_flux = mcc_flux * 0.80 # HMGCL: HMG-CoA → acetyl-CoA + acetoacetate
    leu_acetyl_coa = hmgcl_leu_flux * 2.0  # 2 acetyl-CoA per Leu (purely ketogenic)
    leu_ketones    = hmgcl_leu_flux * 1.0  # acetoacetate produced

    # --- Branch: Valine (glucogenic) → propionyl-CoA → succinyl-CoA ---
    # isobutyryl-CoA → methylmalonyl-CoA → succinyl-CoA (via PCC + MUT)
    pcc_val_flux = bckdh_flux * 0.33    # propionyl-CoA carboxylase; biotin
    mut_flux     = pcc_val_flux * 0.90  # Methylmalonyl-CoA Mutase; adenosylcobalamin (B12)
    val_succinyl = mut_flux              # → succinyl-CoA → TCA (glucogenic)

    # --- Branch: Isoleucine (mixed) → acetyl-CoA + propionyl-CoA ---
    ile_flux = bckdh_flux * 0.33
    ile_acetyl_coa = ile_flux * 0.5
    ile_propionyl  = ile_flux * 0.5   # → succinyl-CoA via PCC+MUT

    # Total CoA products
    total_acetyl_coa = leu_acetyl_coa + ile_acetyl_coa
    total_succinyl   = val_succinyl + ile_propionyl * mut_flux / max(pcc_val_flux, 0.01)
    total_fadh2      = ivd_fadh2       # from IVD step (one per Leu)
    total_nadh       = bckdh_nadh + total_acetyl_coa * 0.5   # approx additional

    # ATP accounting (substrate-level only — direct):
    # No substrate-level ATP from BCAA catabolism itself
    # All ATP comes from acetyl-CoA entering TCA + OxPhos
    atp_yield    = 0.0
    atp_invested = 0.0    # No direct ATP consumed in BCAA catabolism steps

    enzymes = [
        _enzyme("BCAT2", "Branched-Chain Aminotransferase (BCAT2, muscle)",
                bcat_flux, True,
                ["PLP (Vit B6) cofactor required",
                 "Abundant in muscle: responsible for peripheral BCAA deamination",
                 "Liver has minimal BCAT → BCKAs absorbed from muscle must be exported",
                 "+Exercise/fasting state (increased BCAA catabolism in muscle)"],
                _status(bcat_flux)),
        _enzyme("BCKDH", "Branched-Chain α-Ketoacid Dehydrogenase (BCKDH)",
                bckdh_flux, True,
                ["TPP (Thiamine/B1) + lipoate + CoA + FAD + NAD+ cofactors",
                 "Rate-limiting step of BCAA catabolism",
                 "BCKDH kinase (BDK): phosphorylates E1α → INACTIVE; inhibited by BCKAs",
                 "BCKDH phosphatase (PPM1K): reactivates; stimulated by exercise",
                 "MSUD (Maple Syrup Urine Disease): BCKDH deficiency → BCKAs accumulate → neurological crisis, maple syrup urine odour"],
                _status(bckdh_flux)),
        _enzyme("IVD", "Isovaleryl-CoA Dehydrogenase (IVD) — Leucine branch",
                ivd_flux, False,
                ["FAD-dependent (reduces FAD → FADH2 per Leu)",
                 "IVD deficiency → Isovaleric acidaemia: sweaty feet odour, encephalopathy",
                 "Treatment: glycine + carnitine supplementation to conjugate isovaleryl-CoA"],
                _status(ivd_flux)),
        _enzyme("MCC", "Methylcrotonyl-CoA Carboxylase (MCC) — Leucine branch",
                mcc_flux, False,
                ["Biotin-dependent (like PCC and PC)",
                 "MCC deficiency → 3-methylcrotonylglycinuria: generally benign variant",
                 "Often detected on newborn screening via MSM/MS"],
                _status(mcc_flux)),
        _enzyme("PCC_val", "Propionyl-CoA Carboxylase (PCC) — Val/Ile branch",
                pcc_val_flux, False,
                ["Biotin-dependent: propionyl-CoA + CO2 → methylmalonyl-CoA",
                 "PCC deficiency → Propionic acidaemia: metabolic acidosis, hyperammonaemia",
                 "Also processes odd-chain FA, Thr, Met side-chains"],
                _status(pcc_val_flux)),
        _enzyme("MUT", "Methylmalonyl-CoA Mutase (MUT)",
                mut_flux, False,
                ["Adenosylcobalamin (Vitamin B12) cofactor — ESSENTIAL",
                 "Converts (R)-methylmalonyl-CoA → succinyl-CoA (enters TCA cycle)",
                 "MUT deficiency or B12 deficiency → Methylmalonic acidaemia (MMA)",
                 "MMA: metabolic acidosis, encephalopathy, renal failure; MMA + propionate is biomarker"],
                _status(mut_flux)),
    ]

    metabolites = [
        {"metabolite_id": "bcaa_in",  "name": "BCAA (Val/Leu/Ile, input)", "concentration": round(bcaa_load, 3),          "trend": "falling"},
        {"metabolite_id": "bcka",     "name": "BCKAs (α-keto acids)",      "concentration": round(bcat_flux * 0.7, 3),     "trend": "stable" if bckdh_flux > 0.3 else "rising"},
        {"metabolite_id": "ivcd",     "name": "Isovaleryl-CoA (Leu)",      "concentration": round(ivd_flux * 0.4, 3),      "trend": "stable"},
        {"metabolite_id": "acetcoa_b","name": "Acetyl-CoA (→ TCA)",        "concentration": round(total_acetyl_coa * 0.5, 3),"trend": "stable"},
        {"metabolite_id": "succcoa_b","name": "Succinyl-CoA (→ TCA)",      "concentration": round(total_succinyl * 0.5, 3), "trend": "stable"},
        {"metabolite_id": "ketones_b","name": "Acetoacetate (Leu ketones)","concentration": round(leu_ketones * 0.4, 3),    "trend": "rising" if leu_ketones > 0.3 else "stable"},
        {"metabolite_id": "mma_b",    "name": "Methylmalonate",            "concentration": round((1.0 - mut_flux) * pcc_val_flux * 0.5, 3), "trend": "rising" if mut_flux < 0.5 else "stable"},
    ]

    notes = [
        "BCKAs catabolism is unusual — most organs (including liver) lack BCAT. BCKAs from Val/Leu/Ile transamination (in muscle) are exported as α-keto acids and decarboxylated by BCKDH in liver and other tissues.",
        "MSUD (Maple Syrup Urine Disease): BCKDH is deficient → BCKAs accumulate → toxic. Presents neonatally: poor feeding, encephalopathy, seizures, characteristic maple syrup odour (from sotolon, an BCKA oxidation product in urine). Emergency management: remove dietary BCAA, provide isoleucine to restore BCKDH activity. Long-term: low-BCAA diet or liver transplant.",
        "Leucine is uniquely ketogenic (no gluconeogenic contribution). HIGH leucine → activates mTORC1 → promotes protein synthesis. Also stimulates insulin secretion from β-cells (leucine activates GDH → leads to ATP → insulin release).",
        "Valine and isoleucine are partially glucogenic — they contribute succinyl-CoA → can support gluconeogenesis via succinate/fumarate/malate/OAA pathway. This is why BCAA catabolism increases during prolonged fasting.",
        "Methylmalonic acidaemia (MMA): MUT requires adenosylcobalamin (B12). Severe B12 deficiency or MUT mutations → methylmalonyl-CoA builds up → excreted as methylmalonate. MMA + elevated plasma homocysteine → combined methylmalonic and homocystinuria (cblC).",
    ]

    warnings = []
    if bckdh_flux < 0.2 and bcaa_load > 0.5:
        warnings.append("Very low BCKDH flux with high BCAA load — BCKAs accumulating. This mimics MSUD (Maple Syrup Urine Disease). Risk: neurotoxicity from BCKA accumulation, particularly α-ketoisocaproate (from Leu).")
    if mut_flux < 0.3 and pcc_val_flux > 0.2:
        warnings.append("Low MUT flux: Methylmalonyl-CoA accumulating → elevated methylmalonate in urine/plasma. Check B12 (adenosylcobalamin) status and MUT enzyme function.")

    return {
        "pathway": "branched_chain_aa",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "atp_invested": round(atp_invested, 2),
            "atp_substrate_produced": 0.0,
            "net_flux": round(bcat_flux, 3),
            "nadh_produced": round(total_nadh, 2),
            "fadh2_produced": round(total_fadh2, 2),
            "co2_released": round(bckdh_flux * 1.0, 2),   # 1 CO2 per BCKDH decarboxylation
            "acetyl_coa_produced": round(total_acetyl_coa, 2),
            "succinyl_coa_produced": round(total_succinyl, 2),
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": 0.0,
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
