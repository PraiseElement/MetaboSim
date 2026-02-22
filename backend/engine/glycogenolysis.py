"""
Glycogenolysis — Glycogen Breakdown Pathway
Glycogen -> G1P -> G6P -> (Free glucose in liver / Glycolysis in muscle)

Key enzymes: Glycogen Phosphorylase (GP-a active, GP-b inactive),
             Debranching Enzyme, Phosphoglucomutase, Glucose-6-Phosphatase (liver only)
Regulated by: Glucagon/Epinephrine activate (PKA -> phosphorylase kinase -> GP-b->GP-a),
              Insulin inhibits, AMP activates allosterically (muscle)
"""


def _enzyme(eid, name, flux, activity, is_reg, regs, status):
    return {
        "enzyme_id": eid, "enzyme_name": name,
        "flux": round(flux, 4), "activity": round(activity, 4),
        "is_regulated": is_reg, "regulators": regs, "status": status,
    }


def _status(x):
    if x >= 0.65: return "active"
    if x >= 0.30: return "allosteric"
    return "inhibited"


def simulate_glycogenolysis(params: dict) -> dict:
    glucose_mM    = params.get("glucose_mM", 5.0)
    insulin_fold  = params.get("insulin_fold", 1.0)
    glucagon_fold = params.get("glucagon_fold", 1.0)
    energy_demand = params.get("energy_demand", 1.0)
    nutr_state    = params.get("nutritional_state", "fed")
    oxygen_pct    = params.get("oxygen_pct", 100)

    # ── Scenario ───────────────────────────────────────────────────
    if glucagon_fold > 2.5 or nutr_state == "fasted":
        scenario = "fasting_glycogenolysis"
    elif glucagon_fold > 1.5 and glucose_mM < 4:
        scenario = "hypoglycemia_response"
    elif energy_demand > 3.0:
        scenario = "exercise_glycogenolysis"
    elif insulin_fold > 2.0 and glucose_mM > 7:
        scenario = "postprandial_suppressed"
    else:
        scenario = "basal_glycogenolysis"

    # ── Glycogen phosphorylase activation ──────────────────────────
    pka_activation  = min((glucagon_fold - 1.0) * 0.4, 1.0) if glucagon_fold > 1 else 0.0
    amp_activation  = min((energy_demand - 1.0) * 0.35, 0.6) if energy_demand > 1 else 0.0
    insulin_inh     = max(0.0, 1.0 - 0.45 * (insulin_fold - 1.0)) if insulin_fold > 1 else 1.0
    glucose_inh     = max(0.1, 1.0 - 0.08 * glucose_mM)

    gp_flux = (0.30 + pka_activation + amp_activation) * insulin_inh * glucose_inh
    gp_flux = max(0.05, min(gp_flux, 1.0))

    debranch_flux  = gp_flux * 0.15
    pgm_flux       = gp_flux * 0.95
    g6pase_flux    = gp_flux * 0.80

    # ATP accounting:
    #   Glycogenolysis itself produces ZERO ATP directly.
    #   Phosphorolysis (GP) uses inorganic Pi, not ATP → G1P is "pre-phosphorylated".
    #   The ONE ATP advantage over free glucose: G1P → G6P bypasses hexokinase,
    #   saving 1 ATP that glycolysis of free glucose would have consumed.
    #   Downstream glycolysis ATP belongs to the glycolysis pathway, NOT here.
    atp_saved    = gp_flux * 1.0    # 1 ATP saved per glycosyl unit (no HK step)
    atp_invested = 0.0               # no ATP consumed in glycogenolysis itself
    atp_yield    = atp_saved         # net = 1 ATP advantage per glycosyl unit

    enzymes = [
        _enzyme("GPB",   "Glycogen Phosphorylase b (inactive)", max(0.0, 0.2 - pka_activation * 0.2),
                max(0.0, 0.2 - pka_activation * 0.2), True,
                ["+AMP (muscle allosteric)", "converted to GP-a by phosphorylase kinase"], "inhibited"),
        _enzyme("GPA",   "Glycogen Phosphorylase a (active)", gp_flux, gp_flux, True,
                ["+glucagon/Epi via PKA", "-insulin (PP1)", "-glucose (liver)", "-G6P (muscle)", "+AMP (muscle)"],
                _status(gp_flux)),
        _enzyme("PHKN",  "Phosphorylase Kinase", min(pka_activation + amp_activation * 0.5, 1.0),
                min(pka_activation + amp_activation * 0.5, 1.0), True,
                ["+cAMP-PKA", "+Ca2+ (muscle contraction)"],
                _status(pka_activation + amp_activation * 0.5)),
        _enzyme("DBE",   "Debranching Enzyme (AGL)", debranch_flux, debranch_flux, False,
                ["bifunctional: glucantransferase + alpha-1,6-glucosidase",
                 "deficiency = GSD III (Cori disease)"],
                "active" if debranch_flux > 0.1 else "allosteric"),
        _enzyme("PGM2",  "Phosphoglucomutase", pgm_flux, pgm_flux, False,
                ["near-equilibrium"], _status(pgm_flux)),
        _enzyme("G6PASE","Glucose-6-Phosphatase (liver/kidney)", g6pase_flux, g6pase_flux, True,
                ["absent in muscle", "deficiency = GSD Ia (Von Gierke)"], _status(g6pase_flux)),
    ]

    metabolites = [
        {"metabolite_id": "glycogen_n",  "name": "Glycogen (n residues)",    "concentration": round(max(0, 1.0 - gp_flux * 0.5), 3), "trend": "falling" if gp_flux > 0.4 else "stable"},
        {"metabolite_id": "g1p_gl",      "name": "Glucose-1-Phosphate",      "concentration": round(gp_flux * 0.85, 3),              "trend": "rising" if gp_flux > 0.5 else "stable"},
        {"metabolite_id": "g6p_gl",      "name": "Glucose-6-Phosphate",      "concentration": round(pgm_flux * 0.80, 3),             "trend": "stable"},
        {"metabolite_id": "pi_gl",       "name": "Inorganic Phosphate (Pi)", "concentration": round(gp_flux * 0.90, 3),              "trend": "stable"},
        {"metabolite_id": "glucose_out", "name": "Free Glucose (hepatic)",   "concentration": round(g6pase_flux * 0.75, 3),          "trend": "rising" if g6pase_flux > 0.5 else "stable"},
        {"metabolite_id": "amp_gl",      "name": "AMP (muscle signal)",      "concentration": round(min(amp_activation * 1.2, 1.0), 3), "trend": "stable"},
        {"metabolite_id": "camp_gl",     "name": "cAMP (glucagon signal)",   "concentration": round(min(pka_activation * 1.3, 1.0), 3), "trend": "stable"},
    ]

    notes = []
    warnings = []

    if scenario == "exercise_glycogenolysis":
        notes.append("Exercise: rising AMP allosterically activates GP-b without PKA signalling — immediate energy mobilisation independent of hormones.")
    if scenario == "fasting_glycogenolysis":
        notes.append("Fasting: glucagon -> adenylate cyclase -> cAMP -> PKA -> phosphorylase kinase -> GP-b phosphorylated -> GP-a (active).")
    if scenario == "postprandial_suppressed":
        notes.append("Post-prandial: insulin activates PP1 -> dephosphorylates GP-a -> inactive GP-b. Glycogenolysis halted.")
    notes.append("Liver glycogenolysis releases free glucose (via G6Pase) to blood — primary glucose source in early fasting (0-6 hours).")
    notes.append("Muscle glycogenolysis cannot release free glucose (no G6Pase) — G6P enters local glycolysis only.")

    if gp_flux < 0.15 and scenario in ("fasting_glycogenolysis", "hypoglycemia_response"):
        warnings.append("Glycogen phosphorylase highly suppressed despite fasting — consider GSD V (McArdle) or GSD VI (Hers) enzyme deficiency.")

    return {
        "pathway": "glycogenolysis",
        "scenario_detected": scenario,
        "enzymes": enzymes,
        "metabolites": metabolites,
        "metrics": {
            "atp_yield": round(atp_yield, 2),
            "atp_invested": round(atp_invested, 2),      # 0 — glycogenolysis consumes no ATP
            "atp_substrate_produced": round(atp_saved, 2), # 1 ATP saved vs free glucose
            "net_flux": round(gp_flux, 3),
            "nadh_produced": 0.0,    # glycogenolysis itself produces no NADH
            "fadh2_produced": 0.0,
            "co2_released": 0.0,
            "pyruvate_output": 0.0,
            "lactate_output": 0.0 if oxygen_pct > 50 else round(gp_flux * 0.5, 3),
            "glucose_consumed": 0.0,
        },
        "educational_notes": notes,
        "warnings": warnings,
    }
