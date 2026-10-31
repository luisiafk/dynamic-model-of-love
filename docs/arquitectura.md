# System Architecture — Love Dynamics

## 1. Architectural Design Principles

The codebase strictly adheres to software engineering principles tailored for scientific computing and academic software development:

- **Separation of Concerns (SoC):** Every task outlined in the project specification resides in its own isolated sub-package inside src/love_dynamics/.
- **Object-Oriented & Extensible Models:** Differential equation systems inherit from an abstract base class (BaseLoveModel), allowing seamless integration of new linear, non-linear, or chaotic systems.
- **Type Safety & Documentation:** All functions and methods strictly enforce Python type hinting (typing) and comprehensive docstrings.
- **Reproducibility & Package Resolution:** Project builds and dependencies are managed through pyproject.toml and pinned via uv.lock.

---

## 2. Directory Tree Structure

```text
dynamical-models-of-love/
├── pyproject.toml               # Project specifications & metadata
├── uv.lock                      # Fixed dependency lockfile
├── README.md                    # Project landing page & user manual
├── .gitignore                   # Git exclusion rules
├── docs/                        # Project & mathematical documentation
│   ├── enunciado.md             # Project requirements & task statements
│   ├── modelo_matematico.md     # Differential equations & model specs
│   ├── arquitectura.md          # Architectural blueprints & design docs
│   └── convenciones.md          # Coding standard guidelines
│
├── src/
│   └── love_dynamics/           # Core library package
│       ├── __init__.py
│       │
│       ├── models/              # Mathematical ODE System Definitions
│       │   ├── __init__.py
│       │   ├── base.py          # Abstract base class for ODE models
│       │   ├── linear_model.py  # System 1: Romeo & Juliet (2D Linear)
│       │   ├── love_triangle.py # System 3: Romeo, Juliet & Guinevere (4D)
│       │   └── nonlinear_model.py # System 2: Non-linear Saturation Model
│       │
│       ├── task_1_derivation/   # Task 1: Symbolic Derivations (SymPy)
│       │   ├── __init__.py
│       │   └── derivation.py
│       │
│       ├── task_2_analytical/   # Task 2: Eigenvalues & Exact Solutions
│       │   ├── __init__.py
│       │   └── analytical.py
│       │
│       ├── task_3_qualitative/  # Task 3: Nullclines & Phase Portraits
│       │   ├── __init__.py
│       │   └── phase_portraits.py
│       │
│       ├── task_4_simulation/   # Task 4: Numerical Integration (SciPy)
│       │   ├── __init__.py
│       │   └── simulation.py
│       │
│       └── task_5_interpretation/ # Task 5: Dynamic & Psychological Analysis
│           ├── __init__.py
│           ├── romantic_styles.py       # Taxonomy classification
│           ├── dynamical_interpretation.py # Trace/Det mapping to psychology
│           ├── initial_conditions.py    # Sensitivity & short/long term trends
│           ├── comparison.py            # Dyadic archetype matrices
│           └── report.py                # Markdown report generation
│
├── tests/                        # Pytest suite
│   ├── test_models.py
│   └── test_interpretation.py
│
├── notebooks/                    # Jupyter exploratory notebooks (Task 1 to 5)
│   ├── task_1.ipynb
│   ├── task_2.ipynb
│   ├── task_3.ipynb
│   ├── task_4.ipynb
│   └── task_5.ipynb
│
├── results/                      # Output directory for generated assets
│   ├── figures/                 # Exported plots & phase diagrams
│   ├── simulations/             # Numerical simulation data exports
│   └── reports/                 # Auto-generated Markdown summaries
│
└── app/                         # Frontend application
    └── main.py                  # Streamlit dashboard entrypoint

```

---

## 3.Data Flow & Integration Pipeline

```text
[ User Inputs / Parameters ]
           │
           ▼
┌──────────────────────────┐
│   src/love_dynamics/     │
│   models/                │ ──► Defines ODE Vector Fields: dy/dt = f(y, t)
└──────────┬───────────────┘
           │
           ├───────────────────────────┬───────────────────────────┐
           ▼                           ▼                           ▼
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│  Task 1: Derivation  │    │  Task 2: Analytical  │    │ Task 3: Qualitative  │
│  (Symbolic SymPy)    │    │  (Eigenvalues/det/tr)│    │ (Phase portraits)    │
└──────────────────────┘    └──────────────────────┘    └──────────────────────┘
           │                           │                           │
           ├───────────────────────────┴───────────────────────────┘
           ▼
┌──────────────────────┐
│  Task 4: Simulation  │ ──► Solves IVP via scipy.integrate.solve_ivp
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│Task 5: Interpretation│ ──► Maps Trace & Determinant invariants to Sprott's
└──────────┬───────────┘     romantic style taxonomy & psychological outcomes
           │
           ▼
┌──────────────────────┐
│ app/main.py (UI)     │ ──► Displays visual dashboards & exports results
└──────────────────────┘
```
