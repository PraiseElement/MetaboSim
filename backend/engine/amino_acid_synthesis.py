"""
Non-Essential Amino Acid Synthesis
Biosynthesis of non-essential amino acids from TCA intermediates and glycolysis.

Key pathways:
- Glu family (Glu, Gln, Pro, Arg): α-ketoglutarate input
- Asp family (Asp, Asn, Thr, Met, Lys): OAA input
- Ala/Ser/Gly: pyruvate/3-PG input
- Tyr: from Phe (PAH)

Key enzymes: GS (Gln synthetase), PSPH, PSAT, SHMT, ALT, AST, SPS,
             Asparagine synthetase, Ornithine synthetase
Clinical: Demand > synthesis → conditionally essential; sepsis, prematurity, PKU
ATP cost: Gln synthesis (GS) = 1 ATP; Asn synthesis (AS) = 1 ATP; Ser/Gly = free
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


def simulate_amino_acid_synthesis(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # Anabolic drive from insulin
    anabolic_drive = min(insulin_fold * 0.6 + (0.20 if nutr_state == "fed" else 0.0), 2.0)
    # Fasting reduces synthesis
    anabolic_drive *= max(0.3, 1.0 - (glucagon_fold - 1.0) * 0.2)
    anabolic_drive = max(0.15, min(anabolic_drive, 1.0))

    # Substrate availability: TCA intermediates driven by glucose supply
    substrate_avail = min(glucose_mM / 5.0, 1.5) * 0.8
    substrate_avail = max(0.2, min(substrate_avail, 1.0))

    if nutr_state == "fed" and insulin_fold > 2:
        scenario = "fed_anabolic_synthesis"
    elif nutr_state == "fasted":
        scenario = "fasted_reduced_synthesis"
    elif energy_demand > 3:
        scenario = "high_demand_synthesis"
    else:
        scenario = "basal_aa_synthesis"

    # --- Glutamate family (from α-KG) ---
    # GDH reverse: αKG + NH4+ + NADH → Glu (reductive amination)
    gdh_rev_flux = anabolic_drive * substrate_avail * 0.7
    # Glutamine synthetase (GS): Glu + NH3 + ATP → Gln (ATP-consuming)
    gs_flux = gdh_rev_flux * 0.85      # 1 ATP per Gln

    # Proline synthesis from Glu (Glu-5-kinase P5CS → P5CR, no direct ATP net)
    pro_synth = gdh_rev_flux * 0.3

    # --- Aspartate family (from OAA via AST reversal) ---
    ast_synth_flux = anabolic_drive * substrate_avail * 0.65
    # Asparagine: Asp + Gln + ATP → Asn + Glu  [Asparagine Synthetase]
    asn_synth_flux = ast_synth_flux * 0.4   # 1 ATP per Asn

    # --- Serine-Glycine family (from 3-phosphoglycerate) ---
    # PHGDH: 3-PG → 3-PHP (NAD+) → PSAT → PSP → d-Ser → SHMT → Gly
    phgdh_flux = substrate_avail * 0.5
    psph_flux  = phgdh_flux * 0.90    # PSPH: phosphoserine phosphatase
    shmt_flux  = psph_flux * 0.60     # SHMT: Ser ↔ Gly (+ THF shuttle, one-carbon metabolism)

    # --- Alanine from pyruvate (ALT reversal) ---
    alt_synth_flux = anabolic_drive * 0.5   # Pyruvate + Glu → Ala + αKG

    # --- ATP cost of synthesis ---
    atp_invested = gs_flux * 1.0 + asn_synth_flux * 1.0   # GS + AS use 1 ATP each
    # No direct ATP gain from transamination-based pathways
    atp_yield = -atp_invested   # Net negative (synthesis costs energy)

    # NADH consumed in some steps (reversal of catabolic reactions)
    nadh_consumed = gdh_rev_flux * 1.0    # GDH reverse uses NADH

    enzymes = [
        _enzyme("GS", "Glutamine Synthetase (GS)",
                gs_flux, True,
                ["+Glu + NH4+ availability",
                 "−Gln (product inhibition — 9 allosteric sites!)",
                 "Consumes 1 ATP per Gln; critical for nitrogen assimilation",
                 "L-Methionine sulfoximine (MSO): classic GS inhibitor"],
                _status(gs_flux)),
        # GDH exposed with both IDs so viz node (GDH) and report (GDH_REV) both resolve
        _enzyme("GDH", "Glutamate Dehydrogenase (reductive amination)",
                gdh_rev_flux, True,
                ["αKG + NH4+ + NADH → Glutamate (reductive amination; synthesis direction)",
                 "+ADP, leucine (low-energy activators)",
                 "−GTP, ATP, NADH (energy-surplus inhibitors)",
                 "Mitochondrial; links TCA intermediate αKG to amino acid pool"],
                _status(gdh_rev_flux)),
        _enzyme("AST", "Aspartate Aminotransferase (synthetic direction)",
                ast_synth_flux, True,
                ["OAA + Glutamate → Aspartate + α-KG (reverse of catabolic direction)",
                 "PLP (Vit B6) cofactor required",
                 "Feeds aspartate into: protein synthesis, urea cycle (ASS step), nucleotide synthesis",
                 "Serum AST elevation: hepatocellular damage + MI marker"],
                _status(ast_synth_flux)),
        _enzyme("P5CS", "Pyrroline-5-Carboxylate Synthase (P5CS)",
                pro_synth, False,
                ["Glutamate → P5C semialdehyde → Proline (via P5CR)",
                 "Bifunctional: γ-glutamyl kinase + glutamate-5-semialdehyde dehydrogenase",
                 "Requires ATP + NADPH; located in mitochondrial inner membrane",
                 "P5CS deficiency → cutis laxa, joint laxity, cataracts (De Barsy syndrome)"],
                _status(pro_synth)),
        _enzyme("PHGDH", "Phosphoglycerate Dehydrogenase (PHGDH)",
                phgdh_flux, True,
                ["Entry point of Ser biosynthesis from 3-phosphoglycerate",
                 "PHGDH amplification seen in some cancers (Warburg-like Ser demand)",
                 "Serine is required for one-carbon metabolism, phospholipid synthesis, GSH"],
                _status(phgdh_flux)),
        _enzyme("SHMT", "Serine Hydroxymethyltransferase (SHMT)",
                shmt_flux, True,
                ["PLP (Vit B6) and THF cofactors",
                 "Interconverts Ser ↔ Gly + methylene-THF",
                 "Provides one-carbon units for purine synthesis, dTMP synthesis (methylation)",
                 "Two isoforms: SHMT1 (cytoplasm), SHMT2 (mitochondria)"],
                _status(shmt_flux)),
        _enzyme("ASN_SYN", "Asparagine Synthetase (AS)",
                asn_synth_flux, False,
                ["Gln-dependent: uses Gln as N-donor (releases Glu)",
                 "Consumes 1 ATP → AMP + PPi (like ASS in urea cycle)",
                 "Over-expressed in some leukaemias to survive asparaginase treatment",
                 "L-Asparaginase is chemotherapy agent in ALL: degrades Asn → leukaemic cells die"],
                _status(asn_synth_flux)),
        _enzyme("ALT_SYN", "Alanine Aminotransferase (ALT, synthetic direction)",
                alt_synth_flux, True,
                ["Reversible: Pyr + Glu ⇌ Ala + αKG",
                 "Fed state: high glucose → Pyr → Ala (protein synthesis)",
                 "PLP cofactor",
                 "Alanine-glucose cycle (reverse): liver makes Ala from Pyr + Glu at high insulin"],
                _status(alt_synth_flux)),
    ]

    metabolites = [
        {"metabolite_id": "glu_s",  "name": "Glutamate (synthesised)",  "concentration": round(gdh_rev_flux * 0.7, 3), "trend": "rising"},
        {"metabolite_id": "gln_s",  "name": "Glutamine",                "concentration": round(gs_flux * 0.7, 3),      "trend": "rising" if gs_flux > 0.4 else "stable"},
        {"metabolite_id": "asn_s",  "name": "Asparagine",               "concentration": round(asn_synth_flux * 0.6, 3),"trend": "stable"},
        {"metabolite_id": "ser_s",  "name": "Serine",                   "concentration": round(psph_flux * 0.6, 3),    "trend": "stable"},
        {"metabolite_id": "gly_s",  "name": "Glycine",                  "concentration": round(shmt_flux * 0.5, 3),    "trend": "stable"},
        {"metabolite_id": "ala_s",  "name": "Alanine",                  "concentration": round(alt_synth_flux * 0.6, 3),"trend": "stable"},
        {"metabolite_id": "pro_s",  "name": "Proline",                  "concentration": round(pro_synth * 0.5, 3),    "trend": "stable"},
    ]

    notes = [
        "Non-essential amino acids are those whose carbon skeletons can be synthesised from central metabolic intermediates (glycolysis or TCA cycle) with the addition of a nitrogen group via transamination or GDH. They are still 'necessary' — just not 'dietary-essential' under normal conditions.",
        "Glutamine is the most abundant free amino acid in plasma. Synthesised by GS (1 ATP), it serves as: (1) nitrogen carrier between organs, (2) fuel for enterocytes and lymphocytes, (3) N-donor for purine/pyrimidine synthesis, (4) substrate for GDH → glutamate. GS inhibition (by glutamine > 9 different sites) is a masterpiece of allosteric regulation.",
        "Serine-one-carbon metabolism axis: PHGDH → PSAT → PSPH → Serine → SHMT → Gly + 5,10-methylene-THF. This one-carbon unit feeds: dTMP synthesis (thymidylate synthase), purine ring at steps 3 and 9, and methylation via SAM cycle (Met→SAH→Homocysteine→Met with B12+B9).",
        "L-Asparaginase therapy (in ALL): cancer cells over-express asparagine synthetase (AS) to survive. By depleting plasma asparagine (Asn), tumour cells die. However, AS over-expression is the major mechanism of resistance. Pegylated asparaginase is preferred to reduce immunogenicity.",
        "Conditionally essential amino acids: under stress/disease, some AAs become essential even though they can normally be synthesised. E.g., Tyr (needs PAH/Phe → deficient in PKU), Arg (urea cycle disorders), Glu/Gln (in hypermetabolic states like sepsis, burns, major surgery).",
    ]

    warnings = []
    if anabolic_drive < 0.3 and nutr_state == "fasted":
        warnings.append("Low anabolic drive in fasted state: non-essential AA synthesis is suppressed. Protein breakdown predominates — muscle wasting risk in prolonged fasting or illness.")

    return {
        "pathway": "amino_acid_synthesis",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "atp_invested": round(atp_invested, 2),
            "atp_substrate_produced": 0.0,
            "net_flux": round(anabolic_drive, 3),
            "nadh_produced": 0.0,
            "fadh2_produced": 0.0,
            "co2_released": 0.0,
            "nitrogen_load": round(gdh_rev_flux * 0.8, 2),   # nitrogen assimilated
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": round(phgdh_flux * 0.3, 2),   # 3-PG diverted from glycolysis
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
