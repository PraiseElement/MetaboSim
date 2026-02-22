"""Smoke test all 14 new pathway engines."""
from engine.amino_acid_catabolism import simulate_amino_acid_catabolism
from engine.urea_cycle import simulate_urea_cycle
from engine.phenylalanine_tyrosine import simulate_phenylalanine_tyrosine
from engine.branched_chain_aa import simulate_branched_chain_aa
from engine.amino_acid_synthesis import simulate_amino_acid_synthesis
from engine.fatty_acid_oxidation import simulate_fatty_acid_oxidation
from engine.fatty_acid_synthesis import simulate_fatty_acid_synthesis
from engine.ketogenesis import simulate_ketogenesis
from engine.cholesterol_synthesis import simulate_cholesterol_synthesis
from engine.lipoprotein_metabolism import simulate_lipoprotein_metabolism
from engine.purine_synthesis import simulate_purine_synthesis
from engine.pyrimidine_synthesis import simulate_pyrimidine_synthesis
from engine.purine_salvage import simulate_purine_salvage
from engine.nucleotide_degradation import simulate_nucleotide_degradation

print("All 14 imports OK")

params = {
    "glucose_mM": 5.0,
    "insulin_fold": 1.0,
    "glucagon_fold": 1.0,
    "energy_demand": 1.0,
    "nutritional_state": "fed",
    "oxygen_pct": 100,
    "protein_load": 1.0,
    "bh4_availability": 1.0,
    "nad_ratio": 1.0,
}

engines = [
    ("amino_acid_catabolism",  simulate_amino_acid_catabolism),
    ("urea_cycle",             simulate_urea_cycle),
    ("phenylalanine_tyrosine", simulate_phenylalanine_tyrosine),
    ("branched_chain_aa",      simulate_branched_chain_aa),
    ("amino_acid_synthesis",   simulate_amino_acid_synthesis),
    ("fatty_acid_oxidation",   simulate_fatty_acid_oxidation),
    ("fatty_acid_synthesis",   simulate_fatty_acid_synthesis),
    ("ketogenesis",            simulate_ketogenesis),
    ("cholesterol_synthesis",  simulate_cholesterol_synthesis),
    ("lipoprotein_metabolism", simulate_lipoprotein_metabolism),
    ("purine_synthesis",       simulate_purine_synthesis),
    ("pyrimidine_synthesis",   simulate_pyrimidine_synthesis),
    ("purine_salvage",         simulate_purine_salvage),
    ("nucleotide_degradation", simulate_nucleotide_degradation),
]

all_ok = True
for name, fn in engines:
    try:
        r = fn(params)
        m = r["metrics"]
        print(f"  OK  {name}: flux={m['net_flux']}, atp={m['atp_yield']}, "
              f"enzymes={len(r['enzymes'])}, metabolites={len(r['metabolites'])}")
    except Exception as e:
        print(f"  FAIL {name}: {e}")
        all_ok = False

if all_ok:
    print("\nAll 14 engines ran successfully!")
else:
    print("\nSome engines FAILED — see above.")
