"""
Ketogenesis and Ketolysis (Ketone Body Metabolism)
Hepatic production of ketone bodies; extrahepatic utilisation

Ketogenesis (liver only — mitochondria):
  2 Acetyl-CoA → Acetoacetyl-CoA (thiolase, ACAT)
  AcAcCoA + Acetyl-CoA → HMG-CoA (HMGCS2 — liver-specific mitochondrial isoform)
  HMG-CoA → Acetoacetate + Acetyl-CoA (HMGCL)
  Acetoacetate → β-Hydroxybutyrate (BDH1, NADH-dependent, reversible)
  Acetoacetate → Acetone + CO2 (spontaneous decarboxylation in severe ketosis)

Livers CANNOT USE ketone bodies (no SCOT; no CoA activation)

Ketolysis (extrahepatic: brain, heart, muscle, kidney — not liver):
  β-OHB → Acetoacetate (BDH1, reverse, in periphery)
  Acetoacetate + Succinyl-CoA → AcAcCoA + Succinate (SCOT — succinyl-CoA oxoacid transferase)
  AcAcCoA → 2 Acetyl-CoA (thiolase) → TCA cycle

Regulation:
  Malonyl-CoA (FA synthesis active state) inhibits CPT-I → reduces Acetyl-CoA delivery to mito
  Low insulin/glucagon ratio, fasting, exercise → HMGCS2 de-repressed
  HMGCS2 activated by succinylation/NAD+ (SIRT3)

Clinical:
  DKA: type 1 DM, glucagon >> insulin → uncontrolled ketogenesis → pH < 7.3, bicarb < 18
  Alcoholic ketoacidosis: NADH excess (ethanol oxidation) → pyruvate → lactate, OAA depleted,
    Acetyl-CoA → ketones; gluconeogenesis inhibited; glucose low/normal
  Physiological ketosis (dietary): BHB < 7 mmol/L, no acidosis
  HMGCL deficiency: rare AR disorder — no ketogenesis; hypoglycaemic crisis, hyperammonaemia
  SCOT deficiency: rare — cannot utilise ketones; persistent ketoacidosis
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


def simulate_ketogenesis(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")
    nad_ratio     = params.get("nad_ratio", 1.0)   # NADH/NAD+ ratio (elevated in alcoholism)

    # Ketogenesis requires: high glucagon, low glucose, low insulin, fasted state
    low_glucose_factor = max(0.1, 1.0 - glucose_mM / 10.0)
    hormonal_drive     = min(glucagon_fold / max(insulin_fold, 0.5), 4.0) / 4.0  # normalise to 0-1
    fasting_factor     = 1.2 if nutr_state in ("fasted", "starved") else (0.7 if nutr_state == "fed" else 1.0)
    malonyl_coa_inhib  = max(0.05, 0.5 - insulin_fold * 0.2)   # low insulin → low ACC → less malonyl-CoA inhibition

    # Overall ketogenesis drive
    keto_drive = min(low_glucose_factor * hormonal_drive * fasting_factor, 1.0)
    keto_drive = max(0.05, keto_drive)

    if glucose_mM > 11 and insulin_fold > 2:
        scenario = "fed_low_ketogenesis"
    elif glucose_mM < 3.5 and glucagon_fold > 2:
        scenario = "hypoglycaemia_high_ketogenesis"
    elif nutr_state in ("fasted", "starved") and insulin_fold < 0.5:
        scenario = "prolonged_fast_ketosis"
    elif nad_ratio > 2.0:
        scenario = "alcoholic_ketoacidosis"
    elif insulin_fold < 0.2 and glucagon_fold > 3:
        scenario = "dka_or_t1dm"
    else:
        scenario = "basal_ketogenesis"

    # Enzyme fluxes
    acat_flux  = keto_drive * 0.90    # thiolase: 2 AcCoA → AcAcCoA
    hmgcs2_flux = acat_flux * 0.80   # HMGCS2 (rate-limiting; liver-specific)
    hmgcl_flux  = hmgcs2_flux * 0.92  # HMGCL: HMG-CoA → Acetoacetate
    acat_produced = hmgcl_flux        # acetoacetate production

    # BDH1 direction depends on NADH/NAD+ ratio (liver)
    # High NAD ratio (ethanol) → favours β-OHB production
    bhb_ratio = min(nad_ratio * 0.5, 0.9)   # fraction of AcAc converted to β-OHB
    bdh1_flux = acat_produced * bhb_ratio
    bhb_produced  = bdh1_flux
    acac_remaining = acat_produced * (1.0 - bhb_ratio)   # stays as AcAc (or → acetone)
    acetone_prod  = acac_remaining * 0.15   # small spontaneous decarboxylation

    # Ketolysis in periphery (brain, heart): SCOT activity
    scot_flux  = acat_produced * 0.6    # extrahepatic; cannot be modelled in liver
    thiolase_kl = scot_flux * 0.90      # AcAcCoA → 2 AcCoA → TCA

    # ATP: ketogenesis itself produces 0 substrate-level ATP in the liver
    # Each AcCoA that enters TCA → 10 ATP, but that's the TCA/OxPhos pathway
    atp_yield   = 0.0
    atp_invested = 0.0   # no direct investment cost (uses CoA from pool)

    # NADH for BDH1 (liver, ketogenesis direction): uses NADH
    nadh_consumed = bdh1_flux * 1.0   # BDH1 uses 1 NADH per β-OHB

    enzymes = [
        _enzyme("HMGCS2", "HMG-CoA Synthase 2 (mitochondrial, HMGCS2)",
                hmgcs2_flux, True,
                ["Rate-limiting step of hepatic ketogenesis",
                 "LIVER-SPECIFIC mitochondrial isoform (HMGCS1 is cytoplasmic, cholesterol synthesis)",
                 "+Acetyl-CoA + Acetoacetyl-CoA → HMG-CoA",
                 "−Succinylation (SIRT3 removes succinyl group to activate in fasting)",
                 "+Glucagon/cAMP signalling de-represses HMGCS2 gene transcription",
                 "HMGCS2 deficiency (AR) → no ketogenesis → hypoglycaemic crisis, hyperammonia",
                 "Succinyl-CoA inhibits HMGCS2 (when TCA runs well, ketogenesis suppressed)"],
                _status(hmgcs2_flux)),
        _enzyme("HMGCL", "HMG-CoA Lyase (HMGCL)",
                hmgcl_flux, False,
                ["HMG-CoA → Acetoacetate + Acetyl-CoA",
                 "HMGCL deficiency → AR disorder: presentations in neonates with hypoglycaemia",
                 "  + organic acids in urine (3-methylglutarate, 3-methylglutaconate, 3-OH-3-methylglutarate)",
                 "  Also blocks Leu catabolism (shares intermediate HMG-CoA)"],
                _status(hmgcl_flux)),
        _enzyme("BDH1", "β-Hydroxybutyrate Dehydrogenase (BDH1)",
                bdh1_flux, True,
                ["Reversible: Acetoacetate + NADH ⇌ β-Hydroxybutyrate + NAD+",
                 "Direction depends on NADH/NAD+ ratio:",
                 "  LIVER (high NADH: fasting, ethanol) → favours β-OHB PRODUCTION",
                 "  PERIPHERY (lower NADH) → favours AcAc production for SCOT",
                 "ALCOHOLIC KETOACIDOSIS: ethanol → high NADH → BDH1 pushed to β-OHB side",
                 "  β-OHB >> AcAc → blood ketones HIGH but urine ketostix negative (measures AcAc!)",
                 "  Risk: normalise ethanol, NADH drops → AcAc rises transiently (ketonuria appears)"],
                _status(bdh1_flux)),
        _enzyme("SCOT", "Succinyl-CoA Oxoacid Transferase (SCOT / OXCT1)",
                scot_flux, True,
                ["ONLY in extrahepatic tissues (NOT liver — explains why liver can't use KB)",
                 "AcAc + Succinyl-CoA → AcAcCoA + Succinate",
                 "Rate limited by succinyl-CoA availability (depletes TCA intermediate)",
                 "In DKA: full SCOT activity but overwhelmed by massive AcAc/β-OHB delivery",
                 "SCOT deficiency (AR): persistent severe ketoacidosis from birth; cannot utilise ketones"],
                _status(scot_flux)),
        _enzyme("ACAT1", "Thiolase (ACAT1/T2) — ketogenesis + ketolysis",
                acat_flux, False,
                ["Ketogenesis: 2 AcCoA → AcAcCoA (condensation)",
                 "Ketolysis: AcAcCoA → 2 AcCoA (thiolysis)",
                 "ACAT1 deficiency → β-ketothiolase deficiency: Ile catabolism defect",
                 "  Episodic ketoacidosis precipitated by fasting/illness; urinary 2-methylaceto-AcAc"],
                _status(acat_flux)),
    ]

    metabolites = [
        {"metabolite_id": "acac",   "name": "Acetoacetate",            "concentration": round(acac_remaining, 3), "trend": "rising" if keto_drive > 0.5 else "stable"},
        {"metabolite_id": "bhb",    "name": "β-Hydroxybutyrate (β-OHB)","concentration": round(bhb_produced, 3),   "trend": "rising" if keto_drive > 0.4 else "stable"},
        {"metabolite_id": "acetone","name": "Acetone (in breath)",     "concentration": round(acetone_prod, 3),    "trend": "rising" if acac_remaining > 0.3 else "stable"},
        {"metabolite_id": "hmgcoa", "name": "HMG-CoA (intermediate)",  "concentration": round(hmgcs2_flux * 0.3, 3),"trend": "stable"},
        {"metabolite_id": "acac_coa","name":"AcAcCoA (intermediate)",  "concentration": round(acat_flux * 0.2, 3), "trend": "stable"},
    ]

    notes = [
        "Ketogenesis is an exclusively HEPATIC process (liver mitochondria). The liver contains HMGCS2 (mitochondrial) and HMGCL but NOT SCOT — so it produces ketone bodies but CANNOT consume them. Extrahepatic tissues (brain, heart, kidney, muscle) express SCOT and actively use ketones, especially when glucose is low.",
        "β-Hydroxybutyrate is not technically a 'ketone' (it's a hydroxy acid — the keto group has been reduced). This matters clinically: standard urine/blood ketostix only measure acetoacetate. In alcoholic ketoacidosis or early DKA, the NADH/NAD+ ratio is very high → BDH1 almost completely converts AcAc → β-OHB → urine ketostix can be FALSELY NEGATIVE despite severe ketoacidosis. Always measure β-OHB directly (serum).",
        "DKA management: insulin targets the root cause (restores glucose disposal + suppresses lipolysis and ketogenesis). IV bicarbonate is controversial — only if pH < 6.9 (dangerous H+ levels impair cardiac contractility). As insulin works, acidosis corrects but plasma glucose may normalise first; DKA is treated when the anion gap normalises, not just when glucose < 11 mmol/L.",
        "Ketogenic diet (dietary ketosis): blood β-OHB 1–7 mmol/L; brain can derive ~60% of its energy from ketones after 3–4 weeks adaptation. Used in drug-resistant epilepsy (reduces seizures by ~50% in 50% of patients — mechanism uncertain: may modulate GABA/glutamate balance, reduce reactive oxygen species, or have direct anti-seizure effect through ATP-sensitive K+ channels).",
    ]

    warnings = []
    if bhb_produced + acac_remaining > 0.8:
        warnings.append(f"High ketone production ({round(bhb_produced + acac_remaining, 2)} units). At physiological levels (< 7 mmol/L): normal dietary ketosis. Above this threshold (DKA: usually > 5 mM total ketones) → metabolic acidosis. Check blood gas and pH.")
    if nad_ratio > 2.0 and glucose_mM < 4.0:
        warnings.append("High NADH/NAD+ ratio with low glucose: alcoholic ketoacidosis pattern. β-OHB will dominate over acetoacetate; urine ketostix unreliable. Gluconeogenesis inhibited (low OAA due to high NADH). Treat with glucose + thiamine before insulin.")

    return {
        "pathway": "ketogenesis",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": 0.0,
            "atp_invested": 0.0,
            "atp_substrate_produced": 0.0,
            "net_flux": round(hmgcs2_flux, 3),
            "nadh_produced": 0.0,
            "fadh2_produced": 0.0,
            "nadh_consumed": round(nadh_consumed, 2),   # BDH1 uses NADH
            "co2_released": round(acetone_prod, 2),     # AcAc → Acetone + CO2
            "bhb_produced": round(bhb_produced, 2),
            "acac_produced": round(acac_remaining, 2),
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": 0.0,
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
