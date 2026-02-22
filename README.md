# MetaboSim &nbsp; [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org) [![React 18](https://img.shields.io/badge/React-18-61dafb)](https://react.dev) [![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green)](https://fastapi.tiangolo.com)

> **An interactive biochemistry education platform (v2.0)** — simulate 23 metabolic pathways, explore 150+ enzyme entries with clinical details, work through patient cases with a full-screen modal experience, and test yourself with 24 quiz categories. New in v2.0: per-enzyme ATP↑↓ / NADH↑↓ / FADH₂↑ badges across all pathway maps.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Pathways Covered](#pathways-covered)
4. [Architecture](#architecture)
5. [Tech Stack](#tech-stack)
6. [Getting Started](#getting-started)
7. [Project Structure](#project-structure)
8. [API Reference](#api-reference)
9. [Enzyme Database](#enzyme-database)
10. [Quiz & Clinical Modules](#quiz--clinical-modules)
11. [Screenshots](#screenshots)
12. [Contributing](#contributing)
13. [Author](#author)
14. [License](#license)

---

## Overview

**MetaboSim** is a full-stack interactive biochemistry simulation application built for medical students, biochemistry educators, and anyone who wants to understand metabolic pathways at a mechanistic level.

Unlike static textbook diagrams, MetaboSim lets you:

- **Adjust physiological parameters** (glucose, insulin, glucagon, energy demand, nutritional state)
- **Watch enzyme activity change in real time** as a colour-coded pathway map
- **Click any enzyme** to see its EC number, cofactors, reaction, location, regulation, and a detailed clinical note
- **Run 23 distinct metabolic engines** — from glycolysis to nucleotide degradation
- **Prepare for exams** with 24 quiz categories and 50+ clinical case scenarios

---

## Features

| Feature                              | Details                                                                                                                                                                            |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **23 Simulation Engines**            | Each pathway has a dedicated Python simulation function returning enzyme flux, metabolite concentrations, ATP yield, educational notes, and scenario detection                     |
| **150+ Enzyme Entries**              | Full biochemical profiles: EC number, class, reaction, cofactors, subcellular location, allosteric regulation, PDB ID, and clinical note                                           |
| **ATP / NADH / FADH₂ Badges** ⭐ New | Every enzyme node shows colour-coded pills: `ATP↓` (red), `ATP↑` (cyan), `NADH↑` (yellow), `NADH↓` (grey), `FADH₂↑` (orange) — always visible, without needing to run a simulation |
| **Interactive Pathway Map**          | Real-time SVG pathway diagrams — enzyme nodes colour-coded by activity (active/allosteric/inhibited) and annotated with energy badges                                              |
| **Enzyme Detail Modal**              | Click any enzyme node in the map to open a rich detail popup with EC number, cofactors, regulation, and clinical pharmacology                                                      |
| **Clinical Case Modal** ⭐ New       | Clicking a clinical case card opens a full-screen modal with presentation, labs, pathophysiology, and simulation metrics. Dismiss via backdrop or ✕ button                         |
| **Enzyme Alias Resolution** ⭐ New   | `getEnzymeData` now resolves 20+ ID aliases (PFK1→PFK, ALD→ALDO, ACN→ACON, PGM2/3→PGM, G6P→G6PASE, etc.) ensuring every enzyme click shows full details                            |
| **Metabolic Scenarios**              | 8+ presets: Fed State, Fasted, Diabetic Hyperglycaemia, Intense Exercise, Liver Failure, Sepsis, Obesity, Starvation                                                               |
| **Clinical Cases Module**            | 50+ vignette-based patient cases linked to specific enzyme defects with diagnostic reasoning                                                                                       |
| **Quiz Module**                      | 24 pathway categories with exam-style MCQs (USMLE/PLAB style), instant feedback, and explanations                                                                                  |
| **Downloadable Reports**             | HTML Flux Reports (v2.0) generated per simulation — includes metrics, enzyme badge legend, metabolite table, and per-pathway biochemical breakdown                                 |
| **Dark / Light Mode**                | Full theme system with persisted user preference                                                                                                                                   |
| **Mobile Responsive**                | Responsive CSS with breakpoints at 768px and 480px                                                                                                                                 |
| **User Guide**                       | Built-in interactive guide (Help section) with step-by-step instructions, pathway table, badge legend, and FAQ                                                                     |

---

## Pathways Covered

### 🟦 Carbohydrate Metabolism (9 pathways)

| Pathway                       | Location             | Net ATP              |
| ----------------------------- | -------------------- | -------------------- |
| Glycolysis                    | Cytoplasm            | +2 net               |
| TCA (Citric Acid) Cycle       | Mitochondria         | +10 per acetyl-CoA   |
| Oxidative Phosphorylation     | Inner mito. membrane | ~28 ATP per glucose  |
| Gluconeogenesis               | Cyto + Mito          | −6 ATP per glucose   |
| HMP / Pentose Phosphate Shunt | Cytoplasm            | NADPH + ribose-5P    |
| Glycogenesis                  | Cytoplasm            | −2 ATP (UDP-glucose) |
| Glycogenolysis                | Cytoplasm            | +1                   |
| Fructose Metabolism           | Liver cytoplasm      | −1 ATP               |
| Galactose Metabolism          | Liver cytoplasm      | −1 UTP               |

### 🟣 Amino Acid Metabolism (5 pathways)

| Pathway                   | Location            | Key Feature                            |
| ------------------------- | ------------------- | -------------------------------------- |
| Amino Acid Catabolism     | Liver (mito + cyto) | ALT, AST, GDH; glucogenic vs ketogenic |
| Urea Cycle                | Liver (mito + cyto) | NH₄⁺ detox; −4 ATP                     |
| Phe / Tyr Metabolism      | Liver (mito + cyto) | PAH, TH, AADC, Tyrosinase              |
| Branched-Chain AAs (BCAA) | Muscle/Liver mito   | BCAT2, BCKDH, IVD, MCC, MUT            |
| Amino Acid Synthesis      | Cyto / Mito         | GS, PHGDH, SHMT, P5CS, ASN_SYN, GDH    |

### 🟡 Lipid Metabolism (5 pathways)

| Pathway                | Location           | Key Feature                    |
| ---------------------- | ------------------ | ------------------------------ |
| β-Oxidation (FAO)      | Mitochondria       | +106 ATP per palmitoyl-CoA     |
| Fatty Acid Synthesis   | Cytoplasm          | ACC1, FASN, ACLY; −14 NADPH    |
| Ketogenesis            | Liver mitochondria | HMGCS2, HMGCL, BDH1, SCOT      |
| Cholesterol Synthesis  | ER + Cytoplasm     | HMGCR (statin target); −18 ATP |
| Lipoprotein Metabolism | Plasma / Liver     | LPL, LDLR, PCSK9, LCAT, ABCA1  |

### 🟢 Nucleotide Metabolism (4 pathways)

| Pathway                    | Location          | Key Feature                             |
| -------------------------- | ----------------- | --------------------------------------- |
| Purine (De Novo) Synthesis | Cytoplasm         | −5 ATP per IMP; PPAT, GART, IMPDH       |
| Pyrimidine Synthesis       | Cyto + Mito       | CAD, DHODH (mito), UMPS, CTPS1          |
| Purine Salvage             | Cytoplasm         | HGPRT, APRT, ADA, AK, CD73              |
| Nucleotide Degradation     | Cytoplasm / Blood | XO (xanthine oxidase → uric acid), DPYD |

---

## Architecture

```
MetaboSim
├── backend/                   # FastAPI Python backend
│   ├── main.py                # API routes, CORS, 24-pathway registry
│   ├── models/
│   │   └── simulation.py      # Pydantic request/response models
│   └── engine/
│       ├── glycolysis.py      # Simulation engine (× 23)
│       ├── ... (22 more)
│       ├── quiz_data.py       # 24 quiz categories, 200+ questions
│       └── scenarios.py       # 8 scenario presets
│
└── frontend/                  # React 18 + Vite frontend
    ├── src/
    │   ├── App.jsx            # Root router — 5 pages
    │   ├── components/
    │   │   ├── Header.jsx     # Sticky nav + theme toggle
    │   │   ├── Dashboard.jsx  # Landing / stats / domain tiles
    │   │   ├── SimulationPanel.jsx  # Pathway selector + parameters
    │   │   ├── PathwayMap.jsx       # Interactive SVG enzyme map
    │   │   ├── MetricsPanel.jsx     # ATP, NADH, flux metrics
    │   │   ├── LearningPanel.jsx    # Educational notes per enzyme
    │   │   ├── EnzymeModal.jsx      # Clickable enzyme detail popup
    │   │   ├── ClinicalModule.jsx   # Clinical cases browser
    │   │   ├── QuizModule.jsx       # 24-category quiz
    │   │   └── GuideModule.jsx      # Built-in user guide
    │   ├── utils/
    │   │   ├── enzymeDatabase.js    # 150+ enzyme profiles
    │   │   ├── pathwayData.js       # SVG node/edge definitions for 23 pathways
    │   │   ├── api.js               # Fetch wrappers
    │   │   └── downloadReport.js    # PDF report generator
    │   ├── context/
    │   │   └── ThemeContext.jsx     # Dark/Light theme provider
    │   └── index.css                # Design tokens + responsive CSS
    └── index.html
```

---

## Tech Stack

| Layer                    | Technology                                             |
| ------------------------ | ------------------------------------------------------ |
| **Frontend Framework**   | React 18 with Vite 5                                   |
| **Styling**              | Vanilla CSS with CSS custom properties (design tokens) |
| **Backend**              | FastAPI (Python 3.10+)                                 |
| **ASGI Server**          | Uvicorn with hot-reload                                |
| **Data Validation**      | Pydantic v2                                            |
| **State Management**     | React `useState` / `useCallback` / `useContext`        |
| **No database required** | All data is in-memory Python / JS modules              |

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm 9+

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/praizekene1/MetaboSim.git
cd MetaboSim

# 2. Backend setup
cd backend
pip install -r requirements.txt
# or manually: pip install fastapi uvicorn pydantic

# 3. Frontend setup
cd ..\frontend
npm install
```

### Running the Application

Open **two terminals**:

**Terminal 1 — Backend:**

```bash
cd MetaboSim/backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**

```bash
cd MetaboSim/frontend
npm run dev
```

Open your browser at: **http://localhost:5173**

The API documentation (Swagger UI) is available at: **http://localhost:8000/docs**

---

## Project Structure

```
MetaboSim/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── models/
│   │   └── simulation.py
│   └── engine/
│       ├── __init__.py
│       ├── glycolysis.py
│       ├── tca_cycle.py
│       ├── oxphos.py
│       ├── gluconeogenesis.py
│       ├── hmp_shunt.py
│       ├── glycogenesis.py
│       ├── glycogenolysis.py
│       ├── fructose_metabolism.py
│       ├── galactose_metabolism.py
│       ├── amino_acid_catabolism.py
│       ├── urea_cycle.py
│       ├── phenylalanine_tyrosine.py
│       ├── branched_chain_aa.py
│       ├── amino_acid_synthesis.py
│       ├── fatty_acid_oxidation.py
│       ├── fatty_acid_synthesis.py
│       ├── ketogenesis.py
│       ├── cholesterol_synthesis.py
│       ├── lipoprotein_metabolism.py
│       ├── purine_synthesis.py
│       ├── pyrimidine_synthesis.py
│       ├── purine_salvage.py
│       ├── nucleotide_degradation.py
│       ├── quiz_data.py
│       └── scenarios.py
└── frontend/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── index.css
        ├── context/
        │   └── ThemeContext.jsx
        ├── components/
        │   ├── Header.jsx
        │   ├── Dashboard.jsx
        │   ├── SimulationPanel.jsx
        │   ├── PathwayMap.jsx
        │   ├── MetricsPanel.jsx
        │   ├── LearningPanel.jsx
        │   ├── EnzymeModal.jsx
        │   ├── ClinicalModule.jsx
        │   ├── QuizModule.jsx
        │   ├── GuideModule.jsx
        │   └── ErrorBoundary.jsx
        └── utils/
            ├── enzymeDatabase.js
            ├── pathwayData.js
            ├── api.js
            └── downloadReport.js
```

---

## API Reference

### Base URL

```
http://localhost:8000
```

### Endpoints

#### `GET /`

Health check.

```json
{ "status": "ok", "version": "2.0.0" }
```

#### `GET /api/pathways`

List all 23 available pathways with metadata.

```json
{
  "glycolysis": {
    "id": "glycolysis",
    "name": "Glycolysis",
    "description": "...",
    "steps": 10,
    "location": "Cytoplasm",
    "net_atp": "2 net"
  },
  ...
}
```

#### `GET /api/scenarios`

List all physiological scenario presets.

#### `POST /api/simulate`

Run a metabolic simulation.

**Request body:**

```json
{
  "pathway": "glycolysis",
  "params": {
    "glucose_mM": 5.0,
    "insulin_fold": 1.0,
    "glucagon_fold": 1.0,
    "energy_demand": 1.0,
    "nutritional_state": "fed"
  }
}
```

**Response:**

```json
{
  "pathway": "glycolysis",
  "scenario_detected": "basal_glycolysis",
  "enzymes": [
    {
      "enzyme_id": "HK",
      "enzyme_name": "Hexokinase (HK)",
      "flux": 0.72,
      "activity": 0.72,
      "is_regulated": true,
      "regulators": ["..."],
      "status": "active"
    }
  ],
  "metabolites": [...],
  "metrics": {
    "atp_yield": 2.0,
    "nadh_produced": 2.0,
    ...
  },
  "educational_notes": [...],
  "warnings": []
}
```

#### `GET /api/quiz/{pathway}`

Get quiz questions for a specific pathway category.

```json
[
  {
    "question": "Which enzyme is the rate-limiting step of glycolysis?",
    "options": ["Hexokinase", "PFK-1", "Pyruvate kinase", "Enolase"],
    "answer": 1,
    "explanation": "PFK-1 is allosterically regulated by AMP, ADP, fructose-2,6-BP (activators) and ATP, citrate (inhibitors)..."
  }
]
```

---

## Enzyme Database

The enzyme database (`frontend/src/utils/enzymeDatabase.js`) contains **150+ enzyme profiles** across all metabolic domains. Each entry includes:

```javascript
HMGCR: {
  id: 'HMGCR',
  name: 'HMG-CoA Reductase',
  fullName: 'HMG-CoA Reductase (HMGCR; 3-Hydroxy-3-Methylglutaryl-CoA Reductase)',
  ec: '1.1.1.34',
  class: 'Oxidoreductase',
  subclass: 'NADPH-dependent reductase',
  reaction: 'HMG-CoA + 2 NADPH → Mevalonate + 2 NADP⁺ + CoA',
  cofactors: 'NADPH (×2)',
  location: 'Endoplasmic reticulum membrane',
  regulation: 'Insulin → SREBP-2 → ↑HMGCR...',
  clinicalNote: 'Statins (atorvastatin, rosuvastatin, simvastatin) are competitive inhibitors...',
  pdbId: '1HWK',
  color: '#a78bfa',
}
```

### Coverage by Domain

| Domain       | Enzymes                                                                                                                                                           |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Carbohydrate | HK, GCK, PGI, PFK, ALDO, TPI, GAPDH, PGK, PGM, ENO, PK, PDH, CS, ACO, IDH, AKGDH, SCS, SDH, FH, MDH, PC, PEPCK, FBPase, G6Pase, GS, GP, G6PD, 6PGD, ATP_SYN, ...  |
| Amino Acid   | ALT, AST, GDH, GDH_REV, CPS1, OTC, ASS, ASL, ARG1, PAH, TH, AADC, DBH, TAT, TYR, BCAT2, BCKDH, IVD, MCC, MUT, GS_aa, PHGDH, SHMT, ASN_SYN, ALT_SYN, P5CS, ...     |
| Lipid        | CPT1, VLCAD, MCAD, LHAD, THIOLASE, ACC1, FASN, CLY, ME1, HMGCS2, HMGCL, BDH1, SCOT, ACAT1, HMGCR, MVK, SQLE, DHCR7, FPS, LPL, LDLR, PCSK9, LCAT, ABCA1, HTGL, ... |
| Nucleotide   | PPAT, GART, IMPDH, ADSS, ADSL, CAD, DHODH, UMPS, TYMS, DHFR, CTPS1, HGPRT, APRT, ADA, AK, CD73, XO, PNP, NT5E, DPYD, ...                                          |

---

## Quiz & Clinical Modules

### Quiz Categories (24 total)

**Carbohydrate** (5): Glycolysis · TCA Cycle · Gluconeogenesis · Glycogen Metabolism · HMP Shunt

**Amino Acid** (5): AA Catabolism · Urea Cycle · Phe/Tyr Metabolism · Branched-Chain AAs · AA Synthesis

**Lipid** (5): Fatty Acid Oxidation · Fatty Acid Synthesis · Ketone Bodies · Cholesterol Synthesis · Lipoprotein Metabolism

**Nucleotide** (4): Purine Synthesis · Pyrimidine Synthesis · Purine Salvage · Nucleotide Degradation

**Clinical & Integration** (5): Clinical Biochemistry · Integration · Vitamins & Cofactors · Enzymology · Metabolic Regulation

### Clinical Cases

Clinical cases cover:

- Inherited metabolic disorders (PKU, MSUD, Gaucher, Pompe, G6PD deficiency, MCADD, etc.)
- Acquired disorders (alcoholic liver disease, diabetic ketoacidosis, statin myopathy)
- Vitamin deficiency states (thiamine, B6, B12, folate)
- Pharmacological targets (statins, allopurinol, methotrexate, fibrates, insulin)
- Integration cases linking multiple pathways

---

## Simulation Parameters

| Parameter           | Range              | Default | Physiological Meaning                |
| ------------------- | ------------------ | ------- | ------------------------------------ |
| `glucose_mM`        | 1–20 mM            | 5.0     | Blood glucose concentration          |
| `insulin_fold`      | 0–10               | 1.0     | Insulin level × basal                |
| `glucagon_fold`     | 0–10               | 1.0     | Glucagon level × basal               |
| `energy_demand`     | 0–10               | 1.0     | ATP demand (exercise intensity)      |
| `nutritional_state` | fed/fasted/starved | fed     | Absorptive vs. post-absorptive state |

### Scenario Presets

| Scenario                     | Glucose | Insulin | Glucagon | State          |
| ---------------------------- | ------- | ------- | -------- | -------------- |
| Fed State                    | 7.5 mM  | 3.0×    | 0.5×     | fed            |
| Fasted (12 h)                | 4.0 mM  | 0.5×    | 2.0×     | fasted         |
| Diabetic Hyperglycaemia      | 18.0 mM | 0.2×    | 3.0×     | fed            |
| Intense Exercise             | 4.5 mM  | 0.8×    | 1.5×     | fed            |
| Starvation (72 h)            | 3.5 mM  | 0.1×    | 4.0×     | starved        |
| Liver Failure                | 5.0 mM  | 1.0×    | 1.0×     | fed (impaired) |
| Obesity / Insulin Resistance | 8.0 mM  | 5.0×    | 0.8×     | fed            |
| Sepsis                       | 9.0 mM  | 0.5×    | 2.5×     | fed            |

---

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository and create a feature branch
2. For new simulation engines: follow the `_enzyme()` helper pattern in existing engines
3. For new enzyme entries: add to `enzymeDatabase.js` with all required fields (ec, class, subclass, reaction, cofactors, location, regulation, clinicalNote, pdbId, color)
4. For new quiz questions: add to the relevant section in `quiz_data.py`
5. Open a pull request with a clear description of changes

### Running Tests

```bash
# Backend — verify all engines load and run successfully
cd backend
python -c "
from engine.glycolysis import simulate_glycolysis
# ... (see audit script in documentation)
"

# Frontend
cd frontend
npm run build   # confirms no JSX/TS compile errors
```

---

## Screenshots

> Start both servers and visit http://localhost:5173 to view the full application.

| Section         | Description                                                                    |
| --------------- | ------------------------------------------------------------------------------ |
| Dashboard       | Domain tiles + ATP/NADH badge feature highlight + pathway stats                |
| Simulation Page | Left: controls, Centre: Pathway Map with energy badges, Right: Metrics + Notes |
| Enzyme Modal    | Click any enzyme node → EC number, reaction, cofactors, clinical note          |
| Clinical Cases  | Patient vignettes with full-screen detail modal (v2.0 modal overlay)           |
| Quiz Module     | 24 pathway categories with MCQs and instant explanations                       |
| Guide           | Built-in user manual with pathway table, badge legend, and FAQ (v2.0 updated)  |

---

## Author

**Chibuike Praise Okechukwu**

- 📧 Email: [praizekene1@gmail.com](mailto:praizekene1@gmail.com)
- 🔬 Area: Biochemistry · Medical Education · Computational Biology

MetaboSim was developed as a comprehensive biochemistry learning tool, integrating rigorous metabolic pathway science with an accessible, interactive interface designed for medical and science students preparing for professional examinations.

---

## Disclaimer

> MetaboSim is intended **for educational purposes only**. All flux values, enzyme activities, and metabolite concentrations are relative units calibrated to reflect physiological trends — they are **not** quantitative clinical measurements and should **not** be used for clinical decision-making. For research-grade kinetic modelling, refer to tools such as COPASI, SBML/SBtab, or BRENDA.

---

## License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Chibuike Praise Okechukwu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<div align="center">
  <strong>MetaboSim v2.0</strong> · Built with FastAPI + React + ❤️ for Biochemistry Education
  <br/>
  <em>© 2026 Chibuike Praise Okechukwu · praizekene1@gmail.com</em>
</div>
