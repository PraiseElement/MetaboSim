"""Quick ATP audit verification script."""
from engine.glycolysis import simulate_glycolysis
from engine.tca_cycle import simulate_tca
from engine.fructose_metabolism import simulate_fructose_metabolism
from engine.galactose_metabolism import simulate_galactose_metabolism
from engine.glycogenolysis import simulate_glycogenolysis
from engine.glycogenesis import simulate_glycogenesis

FED  = {'glucose_mM': 7.0, 'oxygen_pct': 100, 'insulin_fold': 2.0, 'glucagon_fold': 1.0, 'energy_demand': 1.5, 'nutritional_state': 'fed'}
FAST = {'glucose_mM': 3.5, 'oxygen_pct': 100, 'insulin_fold': 0.5, 'glucagon_fold': 2.0, 'energy_demand': 1.0, 'nutritional_state': 'fasted'}

print("=== ATP AUDIT AFTER FIXES ===\n")

# Glycolysis
m = simulate_glycolysis(FED)['metrics']
print(f"Glycolysis (fed):     ATP={m['atp_yield']:.2f}  invested={m['atp_invested']:.2f}  produced={m['atp_substrate_produced']:.2f}  NADH={m['nadh_produced']:.2f}")
assert 1.5 <= m['atp_yield'] <= 2.5, f"Glycolysis ATP {m['atp_yield']} out of expected 2 ± 0.5"

# TCA
m = simulate_tca(FED)['metrics']
print(f"TCA Cycle (fed):      GTP={m['atp_yield']:.2f}  NADH={m['nadh_produced']:.2f}  FADH2={m['fadh2_produced']:.2f}")
assert m['atp_yield'] <= 1.1, f"TCA GTP {m['atp_yield']} should be ≤1"

# Fructose
m = simulate_fructose_metabolism(FED)['metrics']
print(f"Fructose (fed):       ATP={m['atp_yield']:.2f}  invested={m['atp_invested']:.2f}  produced={m['atp_substrate_produced']:.2f}")
assert -0.5 <= m['atp_yield'] <= 0.5, f"Fructose net ATP {m['atp_yield']} should be ~0"

# Galactose
m = simulate_galactose_metabolism(FED)['metrics']
print(f"Galactose (fed):      ATP={m['atp_yield']:.2f}  invested={m['atp_invested']:.2f}  produced={m['atp_substrate_produced']:.2f}")
assert 0.0 <= m['atp_yield'] <= 1.5, f"Galactose net ATP {m['atp_yield']} should be ~1"

# Glycogenolysis
m = simulate_glycogenolysis(FAST)['metrics']
print(f"Glycogenolysis (fast): ATP={m['atp_yield']:.2f}  (1 ATP saved advantage)  NADH={m['nadh_produced']}")
assert 0.0 <= m['atp_yield'] <= 1.0, f"Glycogenolysis ATP {m['atp_yield']} should be <=1"
assert m['nadh_produced'] == 0.0, "Glycogenolysis should produce no NADH itself"

# Glycogenesis
m = simulate_glycogenesis(FED)['metrics']
print(f"Glycogenesis (fed):   ATP={m['atp_yield']:.2f}  (negative = correct, consumes ATP)")
assert m['atp_yield'] < 0, f"Glycogenesis ATP {m['atp_yield']} should be negative"

print("\nALL ASSERTIONS PASSED")
