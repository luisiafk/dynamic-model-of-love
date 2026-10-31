# Dynamical Models of Love

>An academic software project in dynamical systems and ordinary differential equations (ODEs), based on the research paper "Dynamical Models of Love" by J. C. Sprott (2004).

---
Project Overview
This project provides an analytical, numerical, and computational framework to study dynamic romantic relationships using systems of ODEs. It models dyadic interactions (Romeo & Juliet 2D system), non-linear emotional saturation, and multi-actor romantic triangles (4D system).

The repository is built using a clean, modular architecture that decouples mathematical model definitions, symbolic derivations, numerical simulations, qualitative analysis, and psychological interpretation into independent task modules.

---

## Collaborative Work Distribution

The project is structured into 5 independent tasks designed for multi-developer collaboration:

- **Task 1: Mathematical Derivation (`task_1_derivation`)**
    Symbolic formulation and derivation of ODE systems (2D linear/nonlinear and 4D love triangles) using SymPy.
- **Task 2: Analytical Analysis (`task_2_analytical`)**
    Matrix analysis (A), characteristic polynomials, eigenvalues, eigenvectors, and closed-form exponential solutions (x(t) = e^{At}x_0).
- **Task 3: Qualitative & Phase Analysis (`task_3_qualitative`)**
   Nullcline computation, vector field generation, phase portraits, and topological stability analysis.
- **Task 4: Numerical Simulation (`task_4_simulation`)**
  Numerical integration using SciPy (solve_ivp), time-series trajectories, phase-space plots, and parameter sweeps.
- **Task 5: Dynamic & Psychological Interpretation (`task_5_interpretation`)**
  Sprott's romantic style taxonomy classification (Eager Lover, Cautious Lover, Hermit, Narcissist), 4x4 dyad archetype matrices, initial condition sensitivity, and report generation.

---

## Technology Stack

- **Language:** Python >= 3.11
- **Package Management:** uv (Fast Python package installer & resolver)
- **Numerical & Scientific Computation:** NumPy, SciPy
- **Symbolic Mathematics:** SymPy
- **Data Structuring & Analysis:** Pandas
- **Scientific Visualization:** Matplotlib
- **Interactive UI:** Streamlit
- **Unit Testing:** Pytest

---

## Environment Setup & Installation

This project uses uv for dependency management and environment isolation.

### 1. Prerequisites

Ensure you have uv installed:

```bash
pip install uv
# Or via curl: curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2.Envirenment Synchronization

```bash
uv sync
```

### 3.Activating the Virtual Environment

- Linux/macOS:

```bash
source .ven/bin/activate
```

- Windows:

```cmd
.venv\Scripts\activate
```

---

## Running the interactive Application

To launch the Streamlit dashboard and explore the dynamical models visually:

```bash
streamlit run app/main.py
```

## Running Tests

To verify package integrity and unit test execution across all modules:

```bash
pytest
```

---

Made with love <3.
