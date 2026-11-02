"""
Task 4: Plotting helpers for numerical simulations.

Funciones reutilizables para generar las gráficas que corresponden
a Task 4 (simulación numérica). No toca qualitative/ ni interpretation/.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt

from love_dynamics.simulation import LoveSimulator, SimulationResult


class Task4Plotter:
    """Generador de gráficas para Task 4."""

    @staticmethod
    def plot_time_series(
        results: Dict[str, SimulationResult],
        title: str = "Series temporales R(t), J(t)",
        figsize: Tuple[float, float] = (12, 8),
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """Gráfica 1: Series temporales R(t), J(t) para distintos estilos.

        results: dict con clave = nombre del estilo, valor = SimulationResult
        """
        n_styles = len(results)
        fig, axes = plt.subplots(n_styles, 2, figsize=figsize, squeeze=False)
        fig.suptitle(title, fontsize=14, fontweight="bold")

        for idx, (style_name, res) in enumerate(results.items()):
            t = res.t
            R = res.y[0]
            J = res.y[1]

            # R(t)
            axes[idx, 0].plot(t, R, label="R(t)", color="blue", linewidth=1.5)
            axes[idx, 0].set_title(f"{style_name} - R(t)")
            axes[idx, 0].set_xlabel("t")
            axes[idx, 0].set_ylabel("R(t)")
            axes[idx, 0].grid(True, alpha=0.3)
            axes[idx, 0].legend()

            # J(t)
            axes[idx, 1].plot(t, J, label="J(t)", color="red", linewidth=1.5)
            axes[idx, 1].set_title(f"{style_name} - J(t)")
            axes[idx, 1].set_xlabel("t")
            axes[idx, 1].set_ylabel("J(t)")
            axes[idx, 1].grid(True, alpha=0.3)
            axes[idx, 1].legend()

        plt.tight_layout()
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"[Task4Plotter] Guardado: {save_path}")
        return fig

    @staticmethod
    def plot_phase_plane_nonlinear(
        results: Dict[str, SimulationResult],
        title: str = "Plano fase numérico R vs J - Modelo no lineal",
        figsize: Tuple[float, float] = (10, 8),
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """Gráfica 3: Plano fase numérico del modelo no lineal con solve_ivp."""
        fig, ax = plt.subplots(figsize=figsize)
        fig.suptitle(title, fontsize=14, fontweight="bold")

        colors = ["blue", "red", "green", "orange", "purple", "brown"]
        for idx, (name, res) in enumerate(results.items()):
            R = res.y[0]
            J = res.y[1]
            color = colors[idx % len(colors)]
            ax.plot(R, J, label=name, color=color, linewidth=1.5)
            # Marcar punto inicial
            ax.plot(R[0], J[0], "o", color=color, markersize=6)
            # Marcar punto final
            ax.plot(R[-1], J[-1], "s", color=color, markersize=6)

        ax.set_xlabel("R (Romeo)")
        ax.set_ylabel("J (Juliet)")
        ax.set_title("Trayectoria numérica R vs J")
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.axhline(y=0, color="k", linestyle="--", alpha=0.3)
        ax.axvline(x=0, color="k", linestyle="--", alpha=0.3)

        plt.tight_layout()
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"[Task4Plotter] Guardado: {save_path}")
        return fig

    @staticmethod
    def plot_time_series_nonlinear(
        results: Dict[str, SimulationResult],
        title: str = "Series temporales modelo no lineal",
        figsize: Tuple[float, float] = (12, 6),
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """Series temporales para el modelo no lineal."""
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        fig.suptitle(title, fontsize=14, fontweight="bold")

        colors = ["blue", "red", "green", "orange", "purple", "brown"]
        for idx, (name, res) in enumerate(results.items()):
            t = res.t
            R = res.y[0]
            J = res.y[1]
            color = colors[idx % len(colors)]
            axes[0].plot(t, R, label=f"R(t) - {name}", color=color, linewidth=1.5)
            axes[1].plot(t, J, label=f"J(t) - {name}", color=color, linewidth=1.5)

        axes[0].set_xlabel("t")
        axes[0].set_ylabel("R(t)")
        axes[0].set_title("Evolución temporal de R")
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()

        axes[1].set_xlabel("t")
        axes[1].set_ylabel("J(t)")
        axes[1].set_title("Evolución temporal de J")
        axes[1].grid(True, alpha=0.3)
        axes[1].legend()

        plt.tight_layout()
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"[Task4Plotter] Guardado: {save_path}")
        return fig


__all__ = ["Task4Plotter"]
