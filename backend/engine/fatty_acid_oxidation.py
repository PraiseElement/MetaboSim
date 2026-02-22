"""
Fatty Acid β-Oxidation (Palmitate, 16C example)
Palmitoyl-CoA (C16) → 8 Acetyl-CoA via 7 oxidation cycles

Per complete oxidation of palmitoyl-CoA:
  Activation:  −2 ATP (palmitoyl-AMP → palmitoyl-CoA: costs 2 ATP equivalents, i.e., ATP→AMP+PPi)
  7 cycles produce:  7 FADH2 + 7 NADH + 8 Acetyl-CoA
  Total (SUBSTRATE LEVEL FROM β-OXIDATION ITSELF): 0 ATP direct
  Total with TCA + OxPhos (educational note): ~106 ATP net

Key enzymes: VLCAD/LCAD/MCAD/SCAD (chain-length specific acyl-CoA dehydrogenases),
             Enoyl-CoA hydratase, LHAD/HAD, Thiolase (ACAA), CPT-I (regulatory)
Regulation: CPT-I inhibited by malonyl-CoA (from ACC, active with insulin — prevents futile cycle)
Clinical: MCAD (most common, neonatal screening), VLCAD, LCAD, LCHAD, CPT-I/II, Zellweger
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


def simulate_fatty_acid_oxidation(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")
    oxygen_pct    = params.get("oxygen_pct", 100)

    # FA mobilisation driven by glucagon, fasting, low glucose
    fa_load = min(glucagon_fold / 1.5 + (0.5 if nutr_state == "fasted" else 0.0)
                  + energy_demand * 0.2, 2.5)
    # Malonyl-CoA (from ACC) inhibits CPT-I — high insulin = high malonyl-CoA = low β-ox
    malonyl_coa = min(insulin_fold * 0.5 + (0.4 if glucose_mM > 6 else 0.0), 1.5)
    cpt1_inhibition = min(malonyl_coa / 2.0, 0.9)
    fa_load = max(0.05, min(fa_load, 2.0))

    # CPT-I flux (rate-limiting): transport of LCFA-CoA from cytoplasm into mitochondria
    cpt1_flux = max(0.05, min(fa_load * (1.0 - cpt1_inhibition), 1.0))

    if nutr_state == "fasted" and glucagon_fold > 1.5:
        scenario = "fasted_high_betaox"
    elif nutr_state == "fed" and insulin_fold > 2:
        scenario = "fed_low_betaox"
    elif energy_demand > 3:
        scenario = "exercise_betaox"
    else:
        scenario = "basal_betaox"

    # Number of oxidation cycles depends on chain length (palmitate = 7 cycles → 8 acetyl-CoA)
    cycles = 7    # for C16 palmitate
    n_acetyl_coa = cycles + 1   # = 8

    # Per-cycle enzyme fluxes (scale with CPT-I as bottleneck)
    vlcad_flux = cpt1_flux      # VLCAD handles C14-C20 chains
    lcad_flux  = cpt1_flux * 0.9
    mcad_flux  = cpt1_flux * 0.85   # MCAD handles C6-C12 — deficiency most common FAO disorder
    scad_flux  = cpt1_flux * 0.80   # SCAD handles C4-C6

    enoyl_flux  = cpt1_flux * 0.95   # Enoyl-CoA hydratase (all chain lengths)
    lhad_flux   = cpt1_flux * 0.90   # L-3-Hydroxyacyl-CoA dehydrogenase (long-chain)
    hacd_flux   = cpt1_flux * 0.88   # Short-chain HAD (equivalent for short chains)
    thiolase_flux = cpt1_flux * 0.85  # Thiolase releases acetyl-CoA per cycle

    # Products per palmitate at this flux level:
    fadh2_per_cycle = 1.0
    nadh_per_cycle  = 1.0
    total_fadh2 = cycles * fadh2_per_cycle * cpt1_flux
    total_nadh  = cycles * nadh_per_cycle  * cpt1_flux
    total_acetyl_coa = n_acetyl_coa * cpt1_flux

    # ATP accounting (β-OXIDATION ITSELF):
    # The oxidation steps produce NO direct ATP (no substrate-level phosphorylation)
    # The 2 ATP activation cost is real and important to account
    atp_invested = 2.0 * cpt1_flux    # Activation: fatty acid + CoA + ATP → acyl-CoA + AMP + PPi
    atp_yield    = -atp_invested        # Net: β-oxidation COSTS 2 ATP to initiate

    # Total ATP if downstream TCA + OxPhos activated (educational note only):
    # 7 FADH2 × 1.5 + 7 NADH × 2.5 + 8 × (1 GTP + 3 NADH × 2.5 + 1 FADH2 × 1.5) - 2 activation
    # = 10.5 + 17.5 + 8 × (1 + 7.5 + 1.5) - 2 = 28 + 80 - 2 = 106 ATP per palmitate
    total_atp_if_full = round(
        (total_fadh2 * 1.5 + total_nadh * 2.5 +
         total_acetyl_coa * (1.0 + 3.0 * 2.5 + 1.0 * 1.5)) - 2.0 * cpt1_flux, 1
    )

    enzymes = [
        _enzyme("CPT1", "Carnitine Palmitoyltransferase I (CPT-I)",
                cpt1_flux, True,
                ["Rate-limiting step for long-chain FA entry into mitochondria",
                 "−Malonyl-CoA (from ACC, active in fed/insulin state): prevents futile cycle",
                 "+Glucagon → reduces ACC → reduces malonyl-CoA → CPT-I activated",
                 "CPT-I deficiency → impaired LCFA oxidation; hypoglycaemia without ketonaemia",
                 "Two isoforms: CPT-IA (liver), CPT-IB (muscle/heart)"],
                _status(cpt1_flux)),
        _enzyme("VLCAD", "Very Long-Chain Acyl-CoA Dehydrogenase (VLCAD)",
                vlcad_flux, False,
                ["Handles C14-C20 acyl-CoA; FAD-dependent (produces FADH2)",
                 "VLCAD deficiency: cardiomyopathy, hypoglycaemia, rhabdomyolysis on fasting",
                 "Newborn screen: elevated C14 acylcarnitine"],
                _status(vlcad_flux)),
        _enzyme("MCAD", "Medium-Chain Acyl-CoA Dehydrogenase (MCAD)",
                mcad_flux, True,
                ["Handles C6-C12 acyl-CoA; FAD-dependent",
                 "MOST COMMON FATTY ACID OXIDATION DISORDER (1:10,000–15,000)",
                 "Presentss with hypoketotic hypoglycaemia, encephalopathy, 'Reye-like' syndrome during intercurrent illness / fasting",
                 "Newborn screen: elevated C8 (octanoylcarnitine) → high sensitivity",
                 "Treated by avoiding prolonged fasting; 95% c.985G>A founder mutation (Caucasian)"],
                _status(mcad_flux)),
        _enzyme("LHAD", "L-3-Hydroxyacyl-CoA Dehydrogenase (LHAD/HADHB)",
                lhad_flux, False,
                ["Part of Mitochondrial Trifunctional Protein (MTP)",
                 "LCHAD deficiency: maternal AFLP (acute fatty liver of pregnancy) in carrier mother",
                 "Produces NADH per cycle; NAD+ must be available (not hypoxic)"],
                _status(lhad_flux)),
        _enzyme("THIOLASE", "Acetyl-CoA Acetyltransferase (Thiolase / ACAA)",
                thiolase_flux, False,
                ["Thiolytic cleavage: 3-ketoacyl-CoA → acetyl-CoA + shortened acyl-CoA",
                 "Releases one acetyl-CoA per cycle → enters TCA or ketogenesis",
                 "Mitochondrial thiolase (T2) also catalyses ketolysis (last step of ketone utilisation)"],
                _status(thiolase_flux)),
    ]

    metabolites = [
        {"metabolite_id": "lcfa",     "name": "Long-Chain FA (in)",         "concentration": round(fa_load * 0.6, 3),       "trend": "falling" if cpt1_flux > 0.4 else "stable"},
        {"metabolite_id": "malonyl",  "name": "Malonyl-CoA (CPT-I inhibitor)","concentration": round(malonyl_coa * 0.5, 3),"trend": "rising" if insulin_fold > 1.5 else "falling"},
        {"metabolite_id": "acyl_coa", "name": "Acyl-CoA intermediates",     "concentration": round(cpt1_flux * 0.4, 3),     "trend": "stable"},
        {"metabolite_id": "acetcoa_f","name": "Acetyl-CoA (→ TCA)",         "concentration": round(total_acetyl_coa * 0.3, 3),"trend": "rising"},
        {"metabolite_id": "fadh2_f",  "name": "FADH₂ produced",             "concentration": round(total_fadh2 * 0.5, 3),   "trend": "rising"},
        {"metabolite_id": "nadh_f",   "name": "NADH produced",              "concentration": round(total_nadh * 0.5, 3),    "trend": "rising"},
        {"metabolite_id": "ketone_f", "name": "Ketone bodies (if excess acetyl-CoA)","concentration": round(total_acetyl_coa * 0.2 if nutr_state == "fasted" else 0.0, 3),"trend": "rising" if nutr_state == "fasted" else "stable"},
    ]

    notes = [
        f"β-Oxidation of palmitoyl-CoA (C16) yields 7 FADH₂ + 7 NADH + 8 acetyl-CoA per molecule. At {round(cpt1_flux*100)}% flux: ~{round(total_fadh2,1)} FADH₂, ~{round(total_nadh,1)} NADH, ~{round(total_acetyl_coa,1)} acetyl-CoA.",
        f"IMPORTANT — ATP accounting: β-oxidation itself produces ZERO substrate-level ATP. The activation step (palmitoyl + CoA + ATP → palmitoyl-CoA) costs 2 ATP equivalents (ATP→AMP+PPi = 2 phosphate bonds). Once activated, all energy is captured as reducing equivalents (FADH₂/NADH) and acetyl-CoA. Total ATP if all proceeds through TCA+OxPhos: ~{total_atp_if_full} ATP per C16 at current flux.",
        "CPT-I and malonyl-CoA: the critical crossroads. When insulin is high → ACC active → malonyl-CoA high → CPT-I inhibited → FA stays in cytoplasm (for synthesis, not oxidation). When glucagon/fasting → ACC inactive → malonyl-CoA low → CPT-I active → FA enters mitochondria for oxidation. This prevents simultaneous synthesis and breakdown of fatty acids (futile cycle).",
        "MCAD deficiency is the most important teaching point: presents in infants/toddlers during a viral illness (→ prolonged fasting). Classic triad: hypoketotic hypoglycaemia (no ketones because medium-chain oxidation blocked, and ketogenesis requires acetyl-CoA from FAO), encephalopathy, elevated C8 acylcarnitine. Treat: never fast > 6–8h; glucose emergency protocol.",
        "Odd-chain fatty acids (rare in diet): produce 1 propionyl-CoA at the end of the last cycle → PCC/MUT → succinyl-CoA → TCA. This provides a small gluconeogenic contribution from fat — the only fat-to-glucose route in mammals.",
    ]

    warnings = []
    if cpt1_flux < 0.2 and nutr_state == "fasted":
        warnings.append("Very low β-oxidation flux during fasting: cells cannot access fatty acid energy stores. Hypoglycaemia + hypoketonaemia pattern (as in MCAD deficiency or CPT-I deficiency). Emergency glucose needed.")
    if oxygen_pct < 40:
        warnings.append("Severe hypoxia: β-oxidation requires mitochondrial NAD+ to be regenerated via ETC/OxPhos. Under hypoxia, NAD+ becomes limiting → β-oxidation stalls even if CPT-I is active.")

    return {
        "pathway": "fatty_acid_oxidation",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),                   # Negative (-2 activation cost)
            "atp_invested": round(atp_invested, 2),             # 2 ATP activation per FA
            "atp_substrate_produced": 0.0,                       # No direct substrate-level ATP
            "net_flux": round(cpt1_flux, 3),
            "nadh_produced": round(total_nadh, 2),
            "fadh2_produced": round(total_fadh2, 2),
            "co2_released": 0.0,                                 # CO2 from downstream TCA
            "acetyl_coa_produced": round(total_acetyl_coa, 2),
            "total_atp_full_oxidation": total_atp_if_full,      # For educational note
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": 0.0,
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
