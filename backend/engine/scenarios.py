"""
Preset physiological scenarios for the MetaboSim simulation.
Each scenario maps to a SimulationRequest parameter set.
"""

SCENARIOS = {
    "normal_fed": {
        "label": "Normal Fed State",
        "description": "Post-meal: high insulin, normal glucose, aerobic conditions. Glycolysis and TCA cycle fully active.",
        "color": "#00ff88",
        "icon": "🍽️",
        "params": {
            "glucose_mM": 7.0,
            "oxygen_pct": 100.0,
            "insulin_fold": 2.5,
            "glucagon_fold": 0.5,
            "energy_demand": 1.0,
            "nutritional_state": "fed",
        },
    },
    "fasting": {
        "label": "Fasting (12–24h)",
        "description": "Low glucose, high glucagon, gluconeogenesis active. Fatty acids being oxidised.",
        "color": "#ffaa00",
        "icon": "⏰",
        "params": {
            "glucose_mM": 3.5,
            "oxygen_pct": 100.0,
            "insulin_fold": 0.3,
            "glucagon_fold": 3.0,
            "energy_demand": 1.0,
            "nutritional_state": "fasted",
        },
    },
    "exercise": {
        "label": "Intense Exercise",
        "description": "Extreme energy demand. AMP rises → PFK-1 activated. TCA accelerated by Ca²⁺.",
        "color": "#00d4ff",
        "icon": "🏃",
        "params": {
            "glucose_mM": 5.0,
            "oxygen_pct": 90.0,
            "insulin_fold": 0.8,
            "glucagon_fold": 1.5,
            "energy_demand": 4.5,
            "nutritional_state": "fed",
        },
    },
    "type2_diabetes": {
        "label": "Type 2 Diabetes",
        "description": "Hyperglycaemia with insulin resistance. PFK-1 less responsive. GNG remains active.",
        "color": "#ff6b6b",
        "icon": "🩺",
        "params": {
            "glucose_mM": 15.0,
            "oxygen_pct": 100.0,
            "insulin_fold": 3.0,   # high insulin, but resistance modelled via glucose
            "glucagon_fold": 2.0,  # inappropriately elevated glucagon
            "energy_demand": 1.2,
            "nutritional_state": "fed",
        },
    },
    "hypoxia": {
        "label": "Hypoxia",
        "description": "O₂ depleted. ETC blocked → NADH accumulates → TCA slows → glycolysis shifts anaerobic → lactate rises.",
        "color": "#b388ff",
        "icon": "🫁",
        "params": {
            "glucose_mM": 5.0,
            "oxygen_pct": 15.0,
            "insulin_fold": 1.0,
            "glucagon_fold": 1.0,
            "energy_demand": 2.0,
            "nutritional_state": "fed",
        },
    },
    "lactic_acidosis": {
        "label": "Lactic Acidosis",
        "description": "Severe hypoxia + high demand. Lactate overwhelms buffering capacity → pH falls → clinical emergency.",
        "color": "#ff4444",
        "icon": "⚠️",
        "params": {
            "glucose_mM": 5.0,
            "oxygen_pct": 5.0,
            "insulin_fold": 1.0,
            "glucagon_fold": 1.2,
            "energy_demand": 3.5,
            "nutritional_state": "fed",
        },
    },
    "starvation": {
        "label": "Starvation (> 48h)",
        "description": "Glycogen depleted. Brain switches to ketones. Muscle proteins catabolised. Extreme GNG.",
        "color": "#ffd700",
        "icon": "🌵",
        "params": {
            "glucose_mM": 2.5,
            "oxygen_pct": 100.0,
            "insulin_fold": 0.1,
            "glucagon_fold": 4.0,
            "energy_demand": 0.8,
            "nutritional_state": "starved",
        },
    },
}
