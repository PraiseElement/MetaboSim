"""
Fatty Acid Synthesis (De Novo Lipogenesis, DNL)
Acetyl-CoA → Malonyl-CoA → Palmitate (C16) via FAS complex

Stoichiometry per palmitate:
  8 acetyl-CoA + 7 ATP (ACC) + 14 NADPH → palmitate + 8 CoA + 7 ADP + 14 NADP+
  (Or more precisely: 7 malonyl-CoA + 1 acetyl-CoA → palmitate, with 7 ATP for ACC)

Key enzymes: Citrate shuttle (OAA + acetyl-CoA → citrate → exported → cytoplasm)
             ACC (acetyl-CoA carboxylase, biotin) → malonyl-CoA
             FAS (fatty acid synthase, multifunctional complex)
Regulation:  Activated by insulin/citrate; inhibited by AMPK (energy depletion), fatty acids
Clinical: Obesity, NAFLD, Type 2 diabetes; target for drugs (FASN inhibitors, ACC inhibitors)
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


def simulate_fatty_acid_synthesis(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # DNL is strongly activated by insulin and high glucose (especially in liver)
    dnl_drive = min(insulin_fold * 0.6 + (glucose_mM / 10.0) * 0.4, 2.0)
    # AMPK activation (energy depletion) inhibits ACC → shuts down DNL
    ampk_inhibition = max(0.0, (energy_demand - 2.0) * 0.3)
    # Glucagon/fasting inhibit DNL (via AMPK and reduced SREBP-1c expression)
    dnl_drive *= max(0.1, 1.0 - (glucagon_fold - 1.0) * 0.3 - ampk_inhibition)
    dnl_drive = max(0.05, min(dnl_drive, 1.0))

    # Citrate availability (export from mito for acetyl-CoA supply in cytoplasm)
    citrate_avail = min(glucose_mM / 5.0 * insulin_fold * 0.4, 1.0)

    if nutr_state == "fed" and insulin_fold > 2 and glucose_mM > 6:
        scenario = "fed_high_dnl"
    elif nutr_state == "fasted" or glucagon_fold > 1.5:
        scenario = "fasted_suppressed_dnl"
    elif energy_demand > 3:
        scenario = "high_demand_suppressed_dnl"
    else:
        scenario = "basal_dnl"

    # ACC (Acetyl-CoA Carboxylase): rate-limiting; biotin-dependent
    # Converts acetyl-CoA → malonyl-CoA; 1 ATP per reaction
    acc_flux = dnl_drive * 0.90
    malonyl_coa_out = acc_flux   # malonyl-CoA produced (also inhibits CPT-I in β-oxidation!)

    # FAS (Fatty Acid Synthase) complex:
    # 7 condensation cycles: malonyl-CoA + acetyl-CoA → extends chain by 2C
    # Each cycle: 1 NADPH (ketoreduction) + 1 NADPH (enoylreduction) = 2 NADPH per cycle
    # 7 cycles for palmitate = 14 NADPH total + 7 ATP (from ACC step)
    fas_flux = acc_flux * 0.85
    palmitate_produced = fas_flux   # 1 unit palmitate per FAS cycle completion

    # ATP costs (per palmitate molecule):
    atp_per_palmitate = 7.0   # 7 ATP from 7 ACC steps
    atp_invested      = atp_per_palmitate * fas_flux
    atp_yield         = -atp_invested    # Strongly negative — synthesis is energy-costly

    # NADPH consumed (from HMP shunt primarily)
    nadph_consumed = 14.0 * fas_flux   # 14 NADPH per palmitate

    # FASN post-transcriptional regulation
    malic_enzyme_flux = citrate_avail * 0.4   # ME1: malate → pyruvate + NADPH (extra NADPH for FAS)

    enzymes = [
        _enzyme("ACC1", "Acetyl-CoA Carboxylase 1 (ACC1, cytoplasmic)",
                acc_flux, True,
                ["+Citrate (allosteric activator — signals metabolic surplus)",
                 "+Insulin (SREBP-1c → ACC1 transcription; also dephosphorylates ACC1 → active)",
                 "−AMPK (phosphorylates ACC1 → INACTIVE during energy depletion/exercise)",
                 "−Fatty acids (product feedback)",
                 "Biotin cofactor: ACC1 is a biotin-dependent carboxylase",
                 "Malonyl-CoA product inhibits CPT-I → prevents futile cycle with β-oxidation"],
                _status(acc_flux)),
        _enzyme("FASN", "Fatty Acid Synthase (FAS/FASN, multifunctional)",
                fas_flux, True,
                ["+Malonyl-CoA supply (from ACC1)",
                 "+NADPH availability (from HMP shunt, malic enzyme)",
                 "−ACP-SA saturation (product inhibition when palmitate accumulates)",
                 "Overexpressed in cancer (tumor cells need lipids for membrane synthesis)",
                 "FASN inhibitors: orlistat (anti-obesity), TVB-2640 (clinical trials)"],
                _status(fas_flux)),
        _enzyme("CLY", "ATP-Citrate Lyase (ACLY)",
                citrate_avail, True,
                ["Citrate (exported from mito) → acetyl-CoA + OAA in cytoplasm",
                 "+Citrate availability (depends on mitochondrial TCA flux)",
                 "+Insulin (activates ACLY via PI3K pathway)",
                 "ACLY inhibitors: bempedoic acid (LDL-lowering drug, FDA approved 2020)"],
                _status(citrate_avail)),
        _enzyme("ME1", "Malic Enzyme 1 (ME1, cytoplasmic NADP+-dependent)",
                malic_enzyme_flux, False,
                ["Malate → Pyruvate + CO2 + NADPH",
                 "Provides NADPH for fatty acid synthesis alongside HMP shunt",
                 "Effectively recycles TCA-derived carbons into NADPH"],
                _status(malic_enzyme_flux)),
    ]

    metabolites = [
        {"metabolite_id": "acetcoa_s", "name": "Acetyl-CoA (cytoplasmic, input)","concentration": round(citrate_avail * 0.7, 3),"trend": "falling"},
        {"metabolite_id": "malonyl_s", "name": "Malonyl-CoA",                    "concentration": round(malonyl_coa_out * 0.6, 3),"trend": "rising" if acc_flux > 0.4 else "stable"},
        {"metabolite_id": "nadph_s",   "name": "NADPH consumed",                 "concentration": round(nadph_consumed * 0.3, 3), "trend": "falling"},
        {"metabolite_id": "palm_s",    "name": "Palmitate (C16) produced",       "concentration": round(palmitate_produced, 3),   "trend": "rising" if fas_flux > 0.3 else "stable"},
        {"metabolite_id": "tg_s",      "name": "Triglycerides (→ VLDL/lipid droplet)","concentration": round(palmitate_produced * 0.4, 3),"trend": "rising" if fas_flux > 0.3 else "stable"},
    ]

    notes = [
        f"De novo lipogenesis (DNL) current flux: {round(dnl_drive*100)}%. Estimated NADPH consumed: ~{round(nadph_consumed, 1)} units. ATP cost: ~{round(atp_invested, 1)} ATP. Palmitate produced: ~{round(palmitate_produced, 2)} units. This is an extremely energy-costly process — justified only when carbohydrate supply exceeds immediate energy needs.",
        "The citrate shuttle is essential: acetyl-CoA cannot cross the inner mitochondrial membrane. Instead, it condenses with OAA → citrate, which IS exported via the citrate/malate antiporter. Cytoplasmic ACLY then regenerates acetyl-CoA + OAA. The OAA is reduced (using NADH → NAD+) to malate, which re-enters mitochondria, completing the shuttle.",
        "NADPH supply for DNL: primarily from HMP shunt (G6PD reaction, 2 NADPH per G6P). Also from malic enzyme (ME1). This connects DNL tightly to HMP shunt activity — a reason why red blood cells (rich in G6PD) are protected from lipid peroxidation (NADPH → glutathione).",
        "Malonyl-CoA is the master switch between synthesis and oxidation: it both directs acetyl-CoA towards elongation AND simultaneously inhibits CPT-I (preventing FA entry into mitochondria). This elegant coordinate regulation ensures FA are never being synthesised and broken down simultaneously.",
        "Clinical relevance: excess hepatic DNL drives NAFLD/NASH. Fructose strongly activates DNL (bypasses PFK-1 regulation → delivers abundant acetyl-CoA without feedback). High-fructose diet → elevated palmitate → TG → hepatic steatosis → insulin resistance cycle.",
    ]

    warnings = []
    if dnl_drive > 0.7 and nutr_state == "fed" and glucose_mM > 7:
        warnings.append(f"High DNL activity ({round(dnl_drive*100)}%): excessive fatty acid synthesis. ATP cost ~{round(atp_invested, 1)}, NADPH consumed ~{round(nadph_consumed,1)}. Sustained high DNL → hepatic steatosis, dyslipidaemia (high TG, low HDL).")
    if nutr_state == "fed" and insulin_fold < 0.5:
        warnings.append("Insulin deficiency despite fed state: ACC1 is phosphorylated (AMPK/glucagon) → DNL severely suppressed. This pattern is seen in Type 1 Diabetes — adipose tissue cannot store fat efficiently; leads to DKA.")

    return {
        "pathway": "fatty_acid_synthesis",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "atp_invested": round(atp_invested, 2),
            "atp_substrate_produced": 0.0,
            "net_flux": round(fas_flux, 3),
            "nadh_produced": 0.0,
            "fadh2_produced": 0.0,
            "nadph_consumed": round(nadph_consumed, 2),
            "co2_released": 0.0,
            "palmitate_produced": round(palmitate_produced, 2),
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": round(citrate_avail * 0.8, 2),
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
