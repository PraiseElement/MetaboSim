"""
Pyrimidine De Novo Synthesis + Salvage
UMP synthesis: 6 steps from Gln + CO2 + Asp

De novo:
  CAD (trifunctional: CPS-II → ATCase → DHOase): Gln + CO2 + Asp → dihydroorotate (3 enzymes, 2 ATP)
  DHODH (mitochondria): DHO → Orotate (FAD-dependent)
  UMPS (trifunctional: OPRT + OMP decarboxylase): OMP → UMP
  UMP → UDP → UTP → CTP (CTP synthase, consumes ATP + Gln)

Thymidylate (dTMP) synthesis:
  dUMP + 5,10-methylene-THF → dTMP + DHF (TYMS / TS)
  DHFR: DHF → THF (regenerates cofactor) — TARGET OF METHOTREXATE

Key regulatory differences from purines:
  CAD (cytoplasmic CPS-II) vs CPS-I in urea cycle (mitochondrial): different genes, different requirements

Clinical:
  OTC deficiency → orotic aciduria (carbamoyl-P → pyrimidine synthesis)
  UMP hydrolase deficiency (hereditary orotic aciduria type I)
  DHODH inhibitors: leflunomide/teriflunomide (RA, MS) → blocks pyrimidine synthesis in lymphocytes
  5-FU (chemotherapy): inhibits TYMS → blocks dTMP synthesis → thymineless death
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


def simulate_pyrimidine_synthesis(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")

    # Pyrimidine synthesis in proliferating cells (DNA/RNA synthesis demand)
    growth_demand = min(energy_demand * 0.5, 1.0)
    prpp_avail    = min(glucose_mM / 5.0 * 0.6, 1.0)   # PRPP needed to add ribose to orotate

    if growth_demand > 0.7:
        scenario = "high_proliferation_pyrimidine_synthesis"
    elif nutr_state == "fasted":
        scenario = "fasted_low_pyrimidine_synthesis"
    else:
        scenario = "basal_pyrimidine_synthesis"

    # --- De novo pathway ---
    # CAD (CPS-II → ATCase → DHOase): first 3 reactions, cytoplasmic
    # CPS-II uses Gln to fix CO2 + Asp → carbamoyl aspartate
    # Activated by PRPP (unlike CPS-I which uses NH3 and NAG)
    cad_flux  = min(prpp_avail * growth_demand * 0.8, 1.0)
    cad_flux  = max(0.1, cad_flux)
    # DHODH (dihydroorotate dehydrogenase): DHO → Orotate; MITOCHONDRIAL INNER MEMBRANE
    # Uses oxidised ubiquinone (CoQ) as electron acceptor; couples pyrimidine synthesis to ETC
    dhodh_flux = cad_flux * 0.85
    # UMPS (OPRT + OMP decarboxylase): Orotate + PRPP → UMP (bifunctional)
    umps_flux  = dhodh_flux * 0.90
    ump_produced = umps_flux

    # UMP → UDP → UTP (nucleoside diphosphate kinase / UMP kinase)
    udp_flux  = ump_produced * 0.90
    utp_flux  = udp_flux * 0.88

    # CTP synthesis: UTP + Gln + ATP → CTP (CTP synthase, CTPS1)
    ctps_flux = utp_flux * 0.60    # not all UTP → CTP; some goes to RNA as UTP
    ctp_produced = ctps_flux

    # dTMP synthesis (thymidylate synthesis, for DNA):
    # dUDP → dUMP (dUTPase); then TYMS: dUMP + 5,10-meTHF → dTMP + DHF
    tyms_flux = ump_produced * 0.30   # fraction going to thymidylate
    # DHFR: DHF → THF (regeneration); target of methotrexate
    dhfr_flux = tyms_flux * 0.95

    # --- ATP accounting ---
    # CAD (CPS-II): 2 ATP per carbamoyl-P (Gln + CO2 + 2Pi)
    # UMPS (OPRT requires PRPP → involves ATP in PRPP synthesis)
    # CTPS: 1 ATP per CTP synthesised
    atp_invested  = cad_flux * 2.0 + ctps_flux * 1.0   # 2 from CAD + 1 from CTPS per CTP
    utp_atp_cost  = ump_produced * 2.0    # 2 ATP to phosphorylate UMP → UTP via kinases
    atp_invested += utp_atp_cost
    atp_yield     = -atp_invested

    # FADH2: DHODH reduces CoQ (like FADH2 equivalent to ETC)
    fadh2_equiv = dhodh_flux * 1.0   # 1 CoQH2 per DHODH cycle

    enzymes = [
        _enzyme("CAD", "CAD (CPS-II/ATCase/DHOase, trifunctional)",
                cad_flux, True,
                ["Cytoplasmic trifunctional enzyme — entry point of pyrimidine de novo synthesis",
                 "+PRPP (allosteric activator of CPS-II domain)",
                 "+UTP (allosteric inhibitor — prevents over-synthesis of uridine)",
                 "CPS-II uses Gln (not NH3 or NAG — unlike CPS-I in urea cycle)",
                 "S1778 phosphorylation by MAP kinase → activated during growth factor signalling"],
                _status(cad_flux)),
        _enzyme("DHODH", "Dihydroorotate Dehydrogenase (DHODH)",
                dhodh_flux, True,
                ["ONLY mitochondrial enzyme in de novo pyrimidine pathway",
                 "Oxidises DHO → Orotate using CoQ (ubiquinone) as electron acceptor",
                 "Directly couples pyrimidine synthesis to mitochondrial ETC",
                 "TARGET OF LEFLUNOMIDE/TERIFLUNOMIDE: selective DHODH inhibitors",
                 "  → blocks pyrimidine synthesis in rapidly dividing lymphocytes",
                 "  → used for RA (leflunomide), MS (teriflunomide, Aubagio)",
                 "DHODH used as marker of lymphocyte proliferation"],
                _status(dhodh_flux)),
        _enzyme("UMPS", "UMP Synthase (OPRT + OMP Decarboxylase)",
                umps_flux, False,
                ["Bifunctional enzyme: OPRT adds ribose-P (from PRPP) to orotate",
                 "OMP decarboxylase: 1 of fastest enzyme rate constants known (10^11 acceleration)",
                 "UMPS deficiency → Hereditary Orotic Aciduria: orotic acid in urine + megaloblastic anaemia",
                 "Treat with uridine supplementation (bypasses defect)"],
                _status(umps_flux)),
        _enzyme("TYMS", "Thymidylate Synthase (TYMS / TS)",
                tyms_flux, True,
                ["dUMP + 5,10-methylene-THF → dTMP + DHF",
                 "Only de novo source of dTMP (for DNA; not RNA)",
                 "TARGET OF 5-FLUOROURACIL (5-FU): 5-FdUMP irreversibly inhibits TYMS",
                 "  → no dTMP → cell cannot replicate DNA → thymineless death",
                 "Used in colorectal cancer, head and neck cancer, breast cancer",
                 "Also inhibited by pemetrexed (multikinase antifolate)"],
                _status(tyms_flux)),
        _enzyme("DHFR", "Dihydrofolate Reductase (DHFR)",
                dhfr_flux, True,
                ["DHF + NADPH → THF (regenerates folate cofactor for TYMS and SHMT)",
                 "CRITICAL REGENERATION STEP: without DHFR, THF is trapped as DHF → TYMS stalls",
                 "TARGET OF METHOTREXATE (MTX): tight competitive inhibitor (polyglutamated)",
                 "Also target of trimethoprim (bacterial DHFR), pyrimethamine (parasitic DHFR)",
                 "DHFR resistance mechanism: amplification of DHFR gene in cancer"],
                _status(dhfr_flux)),
        _enzyme("CTPS1", "CTP Synthase 1 (CTPS1)",
                ctps_flux, False,
                ["UTP + Gln + ATP → CTP + Glu + ADP + Pi",
                 "Provides CTP for RNA synthesis, phospholipid synthesis (CTP for CDP-DAG)",
                 "CTPS1 deficiency → combined immunodeficiency (rare, EBV susceptibility)"],
                _status(ctps_flux)),
    ]

    metabolites = [
        {"metabolite_id": "carbasp", "name": "Carbamoyl-Aspartate",      "concentration": round(cad_flux * 0.5, 3),      "trend": "stable"},
        {"metabolite_id": "dho",     "name": "Dihydroorotate (DHO)",     "concentration": round(cad_flux * 0.3, 3),      "trend": "stable"},
        {"metabolite_id": "orotate", "name": "Orotate",                  "concentration": round(dhodh_flux * 0.3, 3),    "trend": "stable"},
        {"metabolite_id": "ump",     "name": "UMP",                      "concentration": round(ump_produced, 3),        "trend": "rising" if cad_flux > 0.4 else "stable"},
        {"metabolite_id": "utp",     "name": "UTP",                      "concentration": round(utp_flux * 0.6, 3),      "trend": "stable"},
        {"metabolite_id": "ctp",     "name": "CTP",                      "concentration": round(ctp_produced, 3),        "trend": "stable"},
        {"metabolite_id": "dtmp",    "name": "dTMP (thymidylate)",        "concentration": round(tyms_flux * 0.5, 3),    "trend": "stable"},
        {"metabolite_id": "orotic_ac","name":"Orotic Acid (urine marker)","concentration": round(max(0, dhodh_flux - umps_flux) * 0.5, 3),"trend": "rising" if umps_flux < dhodh_flux * 0.5 else "stable"},
    ]

    notes = [
        "Key difference from purine synthesis: pyrimidine ring is completed FIRST, then ribose-phosphate is added (from PRPP via UMPS). For purines, PRPP is added first, and the ring is built ON the ribose (GAR→IMP pathway).",
        "DHODH is uniquely mitochondrial and couples pyrimidine synthesis directly to the ETC (uses CoQ as oxidant). This is why DHODH inhibitors (leflunomide, teriflunomide) block DNA replication in lymphocytes even without directly targeting DNA. Lymphocytes lack sufficient salvage capacity to compensate.",
        "Orotic Aciduria diagnosis: elevated orotate in urine. Two causes: (1) UMPS deficiency (cannot process orotate → UMP); treat with uridine. (2) OTC deficiency: carbamoyl-P cannot be used in urea cycle → spills into CPS-II territory → excess pyrimidine synthesis → orotate. In OTC def., this is accompanied by hyperammonaemia (absent in UMPS def.).",
        "5-FU pharmacology: 5-FU → 5-FdUMP (by thymidine kinase) → irreversible TYMS inhibitor (forms ternary complex with TYMS and 5,10-methylene-THF). No dTMP → cannot replicate DNA. Folinic acid (leucovorin) POTENTIATES 5-FU by stabilising the ternary complex (more TYMS inhibition). Paradoxically, folinic acid helps 5-FU work BETTER (used in FOLFOX).",
        "Methotrexate (DHFR inhibitor) blocks BOTH purine synthesis (at step 3/9, formyl-THF donor for GART/ATIC) AND thymidylate synthesis (TYMS stalls without THF). Cancer cells (high proliferative demand) cannot tolerate loss of either. Rescue: leucovorin given 24h after MTX to replete THF without competing with DHFR (leucovorin → not a DHFR substrate).",
    ]

    warnings = []
    if tyms_flux < 0.2 and growth_demand > 0.5:
        warnings.append("Severely suppressed TYMS: consistent with 5-FU therapy or MTX treatment. dTMP production near zero — rapidly proliferating cells will undergo thymineless death. Ensure rescue with leucovorin if MTX-related.")
    if dhodh_flux < 0.15:
        warnings.append("DHODH severely inhibited: leflunomide/teriflunomide effect or DHODH deficiency. Pyrimidine-depleted lymphocytes → profound immunosuppression. Monitor for opportunistic infections.")

    return {
        "pathway": "pyrimidine_synthesis",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "atp_invested": round(atp_invested, 2),
            "atp_substrate_produced": 0.0,
            "net_flux": round(cad_flux, 3),
            "nadh_produced": 0.0,
            "fadh2_produced": round(fadh2_equiv, 2),    # DHODH CoQ equivalent
            "co2_released": round(umps_flux * 1.0, 2),  # OMP decarboxylase releases 1 CO2
            "ump_produced": round(ump_produced, 2),
            "ctp_produced": round(ctp_produced, 2),
            "pyruvate_output": 0.0,
            "lactate_output": 0.0,
            "glucose_consumed": round(cad_flux * 0.3, 2),
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
