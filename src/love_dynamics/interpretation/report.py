from pathlib import Path
from .comparison import DyadicComparisonMatrix
class ReportGenerator:
    @staticmethod
    def generate_markdown_report(output_path: str = "results/reports/interpretation_report.md") -> None:

        df_matrix = DyadicComparisonMatrix.generate_matrix()

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        report_content = [
            "# Informe Psicodinámico de Relaciones Diádicas",
            "> Análisis basado en el modelo lineal de J. C. Sprott (2004).",
            "",
            "## 1. Introducción",
            "Este documento sintetiza la clasificación de estabilidad topológica y comportamiento "
            "relacional a largo plazo para las 16 combinaciones posibles de estilos románticos.",
            "",
            "## 2. Matriz Comparativa de Arquetipos (4x4)",
            "",
            "| Romeo Style | Juliet Style | Topología Dinámica | Índice de Armonía | Diagnóstico Psicológico |",
            "| :--- | :--- | :--- | :---: | :--- |"
        ]

        for _, row in df_matrix.iterrows():
            line = (
                f"| {row['Romeo_Style']} | {row['Juliet_Style']} | "
                f"{row['Topology']} | {row['Harmony_Score']} | {row['Summary']} |"
            )
            report_content.append(line)

        report_content.extend([
            "",
            "## 3. Conclusiones Generales",
            "- Las parejas con perfiles de **Cautious Lover** tienden hacia equilibrios estables o amortiguados.",
            "- Las combinaciones de tipo Saddle Point exponen una alta dependencia de las primeras impresiones iniciales.",
            "- Los sistemas con traza positiva y determinante positivo conducen a una escalada explosiva o insostenible."
        ])

        path.write_text("\n".join(report_content), encoding="utf-8")

    @staticmethod
    def generate_latex_report(output_path: str = "results/reports/interpretation_report.tex") -> None:
        """Compila la matriz comparativa de arquetipos en un documento LaTeX profesional."""
        df_matrix = DyadicComparisonMatrix.generate_matrix()

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        latex_content = [
            r"\documentclass{article}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[spanish]{babel}",
            r"\usepackage{geometry}",
            r"\geometry{a4paper, margin=1in}",
            r"\usepackage{booktabs}",
            r"\usepackage{longtable}",
            r"",
            r"\title{Informe Psicodinámico de Relaciones Diádicas}",
            r"\author{Tarea 5 - Modelos Dinámicos de Amor (Sprott 2004)}",
            r"\date{\today}",
            r"",
            r"\begin{document}",
            r"\maketitle",
            r"",
            r"\section{Introducción}",
            r"Este documento sintetiza la clasificación de estabilidad topológica y comportamiento relacional a largo plazo para las 16 combinaciones posibles de estilos románticos analizados mediante el modelo lineal.",
            r"",
            r"\section{Matriz Comparativa de Arquetipos}",
            r"\begin{longtable}{p{2.5cm} p{2.5cm} p{3cm} c p{4cm}}",
            r"\toprule",
            r"\textbf{Romeo} & \textbf{Julieta} & \textbf{Topología} & \textbf{Armonía} & \textbf{Diagnóstico Psicológico} \\",
            r"\midrule",
            r"\endhead",
            r"\bottomrule",
            r"\endfoot"
        ]

        for _, row in df_matrix.iterrows():
            # Escapando caracteres especiales básicos para LaTeX si fuera necesario
            r_style = str(row['Romeo_Style']).replace("_", r"\_")
            j_style = str(row['Juliet_Style']).replace("_", r"\_")
            topo = str(row['Topology']).replace("_", r"\_")
            score = row['Harmony_Score']
            summary = str(row['Summary']).replace("_", r"\_")

            row_str = f"{r_style} & {j_style} & {topo} & {score} & {summary} \\\\"
            latex_content.append(row_str)

        latex_content.extend([
            r"\end{longtable}",
            r"",
            r"\section{Conclusiones}",
            r"\begin{itemize}",
            r"    \item Las parejas con perfiles de \textbf{Cautious Lover} tienden hacia equilibrios estables o amortiguados.",
            r"    \item Las combinaciones de tipo \textbf{Saddle Point} exponen una alta dependencia de las primeras impresiones iniciales.",
            r"    \item Los sistemas con traza positiva y determinante positivo conducen a una escalada explosiva o insostenible.",
            r"\end{itemize}",
            r"",
            r"\end{document}"
        ])

        path.write_text("\n".join(latex_content), encoding="utf-8")

    @classmethod
    def generate_all_reports(cls) -> None:
        cls.generate_markdown_report()
        cls.generate_latex_report()