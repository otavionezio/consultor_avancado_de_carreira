"""
Gráficos Altair usados pela interface Streamlit.
Recebem apenas estruturas já calculadas pelo motor (sem regra de negócio).
"""
import math
from typing import Any, Dict, List, Optional

import altair as alt
import pandas as pd

PRIMARY = "#3B82F6"
HIGHLIGHT = "#1E3A8A"
MUTED = "#CBD5E1"
STATUS_COLORS = {"dominada": "#10B981", "parcial": "#F59E0B", "ausente": "#EF4444"}


def ranking_chart(ranked: List[Dict[str, Any]]) -> alt.Chart:
    """Barras horizontais com a compatibilidade das dez carreiras, destacando o Top 3."""
    df = pd.DataFrame([
        {
            "Carreira": f"{t['icon']} {t['name']}",
            "Compatibilidade (%)": t["percentage"],
            "Confiança": t["confidence_label"],
            "Posição": "Top 3" if i < 3 else "Demais",
        }
        for i, t in enumerate(ranked)
    ])
    order = df["Carreira"].tolist()
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X("Compatibilidade (%):Q", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Carreira:N", sort=order, title=None, axis=alt.Axis(labelLimit=320)),
        color=alt.Color("Posição:N", scale=alt.Scale(domain=["Top 3", "Demais"], range=[HIGHLIGHT, MUTED]),
                        legend=alt.Legend(orient="bottom", title=None)),
        tooltip=["Carreira", "Compatibilidade (%)", "Confiança"],
    )
    labels = bars.mark_text(align="left", dx=4, color="#334155").encode(
        text=alt.Text("Compatibilidade (%):Q", format=".1f"), color=alt.value("#334155"))
    return (bars + labels).properties(height=34 * len(df))


def radar_chart(affinity_labels: Dict[str, str], user_values: Dict[str, Optional[int]],
                career_profile: Dict[str, float], career_name: str, max_weight: float = 3.0) -> alt.Chart:
    """Radar comparando as afinidades do usuário (0-1) com o perfil ideal da carreira."""
    dims = list(affinity_labels)
    n = len(dims)

    def point(i: int, r: float):
        angle = 2 * math.pi * i / n
        return r * math.sin(angle), r * math.cos(angle)

    rows = []
    for serie, values in (("Você", {d: ((user_values.get(d) or 1) - 1) / 4 for d in dims}),
                          (career_name, {d: career_profile.get(d, 0) / max_weight for d in dims})):
        for i, d in enumerate(dims + dims[:1]):
            x, y = point(i % n, values[d])
            rows.append({"x": x, "y": y, "Série": serie, "ordem": i, "Dimensão": affinity_labels[d],
                         "Valor": round(values[d], 2)})
    data = pd.DataFrame(rows)

    grid_rows = []
    for level in (0.25, 0.5, 0.75, 1.0):
        for i in range(n + 1):
            x, y = point(i % n, level)
            grid_rows.append({"x": x, "y": y, "nível": level, "ordem": i})
    axis_rows = []
    for i, d in enumerate(dims):
        x, y = point(i, 1.0)
        axis_rows += [{"x": 0, "y": 0, "eixo": d, "ordem": 0}, {"x": x, "y": y, "eixo": d, "ordem": 1}]
    label_rows = [{"x": point(i, 1.18)[0], "y": point(i, 1.18)[1], "rótulo": affinity_labels[d]}
                  for i, d in enumerate(dims)]

    scale = alt.Scale(domain=[-1.45, 1.45])
    x_enc = alt.X("x:Q", scale=scale, axis=None)
    y_enc = alt.Y("y:Q", scale=scale, axis=None)

    grid = alt.Chart(pd.DataFrame(grid_rows)).mark_line(color="#E2E8F0").encode(
        x=x_enc, y=y_enc, detail="nível:N", order="ordem:Q")
    axes = alt.Chart(pd.DataFrame(axis_rows)).mark_line(color="#E2E8F0").encode(
        x=x_enc, y=y_enc, detail="eixo:N", order="ordem:Q")
    labels = alt.Chart(pd.DataFrame(label_rows)).mark_text(fontSize=11, color="#475569").encode(
        x=x_enc, y=y_enc, text="rótulo:N")
    color = alt.Color("Série:N", scale=alt.Scale(domain=["Você", career_name], range=[PRIMARY, "#F59E0B"]),
                      legend=alt.Legend(orient="bottom", title=None))
    shapes = alt.Chart(data).mark_line(strokeWidth=2.5, point=True).encode(
        x=x_enc, y=y_enc, color=color, order="ordem:Q",
        tooltip=["Série", "Dimensão", "Valor"])
    return (grid + axes + shapes + labels).properties(width=460, height=460)


def skill_gap_chart(items: List[Dict[str, Any]]) -> alt.Chart:
    """Nível atual vs nível exigido para Júnior em cada competência."""
    df = pd.DataFrame([
        {
            "Competência": it["label"],
            "Atual": it["current"] if it["current"] is not None else 1,
            "Exigido": it["required"],
            "Situação": it["status"],
        }
        for it in items
    ])
    order = df["Competência"].tolist()
    base = alt.Chart(df).encode(y=alt.Y("Competência:N", sort=order, title=None, axis=alt.Axis(labelLimit=360)))
    current = base.mark_bar(cornerRadiusEnd=3, size=14).encode(
        x=alt.X("Atual:Q", scale=alt.Scale(domain=[0, 5]), title="Nível (1 a 5)",
                axis=alt.Axis(values=[1, 2, 3, 4, 5], format="d")),
        color=alt.Color("Situação:N", scale=alt.Scale(domain=list(STATUS_COLORS), range=list(STATUS_COLORS.values())),
                        legend=alt.Legend(orient="bottom", title=None)),
        tooltip=["Competência", "Atual", "Exigido", "Situação"],
    )
    required = base.mark_tick(color="#1E293B", thickness=3, size=20).encode(x="Exigido:Q")
    return (current + required).properties(height=28 * len(df))


def components_chart(top: List[Dict[str, Any]], labels: Dict[str, str]) -> alt.Chart:
    """Pontuação de cada componente (afinidade, preferência, proficiência) por carreira."""
    rows = []
    for t in top:
        for key, comp in t["components"].items():
            rows.append({"Carreira": f"{t['icon']} {t['name']}", "Componente": labels.get(key, key),
                         "Pontuação (%)": round(comp["score"] * 100, 1),
                         "Evidência (%)": round(comp["coverage"] * 100, 1)})
    df = pd.DataFrame(rows)
    component_order = [labels.get(k, k) for k in top[0]["components"]] if top else None
    return alt.Chart(df).mark_bar().encode(
        x=alt.X("Componente:N", title=None, sort=component_order, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Pontuação (%):Q", scale=alt.Scale(domain=[0, 100])),
        color=alt.Color("Componente:N", legend=None, sort=component_order),
        column=alt.Column("Carreira:N", title=None, sort=[f"{t['icon']} {t['name']}" for t in top]),
        tooltip=["Carreira", "Componente", "Pontuação (%)", "Evidência (%)"],
    ).properties(width=170, height=220)
