"""
Consultor Inteligente de Carreiras em TI - Interface Web com Streamlit.
Questionário em etapas, ranking de compatibilidade, análise de lacunas e roadmap.
Toda a lógica de inferência fica em engine/; esta camada apenas coleta e apresenta dados.
"""
import copy
import json

import pandas as pd
import streamlit as st

from engine.advisor import CareerAdvisor
from data.personas import TEST_PERSONAS
from ui import charts


# Configuração da página Streamlit
st.set_page_config(
    page_title="Consultor Inteligente de Carreiras em TI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada para dar acabamento profissional
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: #FFFFFF !important;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }
    .main-header p {
        color: #E0E7FF;
        font-size: 1.05rem;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    .card-recommendation {
        background: #F8FAFC;
        border: 2px solid #3B82F6;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
        min-height: 230px;
        color: #0F172A;
    }
    .card-recommendation .pct {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    .rule-card {
        background: #FFFFFF;
        border-left: 4px solid #10B981;
        padding: 0.7rem 1.1rem;
        margin-bottom: 0.5rem;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        color: #0F172A;
    }
    .cross-rule-card {
        background: #FFFBEB;
        border-left: 4px solid #F59E0B;
        padding: 0.7rem 1.1rem;
        margin-bottom: 0.5rem;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        color: #0F172A;
    }
    .negative-rule-card {
        background: #FEF2F2;
        border-left: 4px solid #EF4444;
        padding: 0.7rem 1.1rem;
        margin-bottom: 0.5rem;
        border-radius: 0 8px 8px 0;
        color: #0F172A;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_advisor() -> CareerAdvisor:
    """Carrega a base de conhecimento JSON uma única vez por sessão do servidor."""
    return CareerAdvisor()


advisor = get_advisor()
kb = advisor.kb
scale = kb.scale

STEPS = [
    "👤 Perfil pessoal",
    "💡 Afinidades técnicas",
    "🧰 Conhecimentos atuais",
    "🎯 Resultados",
    "🗺️ Plano de desenvolvimento",
]
STEP_RESULTS = 3
STEP_PLAN = 4

# Perguntas de escolha exibidas na etapa de perfil; as demais aparecem em afinidades técnicas
PROFILE_CHOICE_QUESTIONS = ("communication_vs_code", "device_focus")
WIDGET_PREFIX = "w__"
COMPONENT_LABELS = {"affinity": "Afinidades", "preference": "Preferências", "proficiency": "Proficiência"}
STATUS_LABELS = {"dominada": "✅ Dominada", "parcial": "🟡 Parcial", "ausente": "🔴 Ausente"}


# =============================================================================
# ESTADO DA SESSÃO (respostas preservadas durante a navegação)
# =============================================================================
def empty_answers() -> dict:
    return {"profile": {}, "affinities": {}, "proficiencies": {}, "choices": {}}


if "answers" not in st.session_state:
    st.session_state.answers = empty_answers()
if "step" not in st.session_state:
    st.session_state.step = 0
if "selected_career" not in st.session_state:
    st.session_state.selected_career = None


def reset_widgets():
    """Remove o estado dos widgets para que sejam recriados a partir das respostas salvas."""
    for key in [k for k in st.session_state.keys() if str(k).startswith(WIDGET_PREFIX)]:
        del st.session_state[key]


def go_to(step: int):
    st.session_state.step = max(0, min(step, len(STEPS) - 1))


def store(section: str, key: str, value):
    if value is None or value == "":
        st.session_state.answers[section].pop(key, None)
    else:
        st.session_state.answers[section][key] = value


def widget_key(section: str, key: str) -> str:
    return f"{WIDGET_PREFIX}{section}__{key}"


def scale_input(section: str, key: str, label: str, labels: dict, help_text: str = None):
    """Escala gradual de 1 a 5 com opção explícita de não responder."""
    options = [None] + list(range(scale["min"], scale["max"] + 1))
    current = st.session_state.answers[section].get(key)
    value = st.select_slider(
        label,
        options=options,
        value=current if current in options else None,
        format_func=lambda v: scale["unanswered_label"] if v is None else labels[str(v)],
        key=widget_key(section, key),
        help=help_text,
    )
    store(section, key, value)


def choice_input(question: dict):
    options = [None] + [o["value"] for o in question["options"]]
    current = st.session_state.answers["choices"].get(question["id"])
    value = st.selectbox(
        question["question"],
        options,
        index=options.index(current) if current in options else 0,
        format_func=lambda v: "Prefiro não responder" if v is None else v,
        key=widget_key("choices", question["id"]),
    )
    store("choices", question["id"], value)


def load_persona(persona_key: str):
    """Carrega as respostas de uma persona pré-definida e vai direto aos resultados."""
    persona = TEST_PERSONAS[persona_key]
    st.session_state.answers = copy.deepcopy(persona["answers"])
    st.session_state.selected_career = None
    reset_widgets()
    go_to(STEP_RESULTS)


def answered_count() -> dict:
    answers = st.session_state.answers
    return {
        "afinidades": (len(answers["affinities"]), len(kb.affinities)),
        "conhecimentos": (len(answers["proficiencies"]), len(kb.competencies)),
        "preferências": (len(answers["choices"]), len(kb.choice_questions)),
    }


# =============================================================================
# BARRA LATERAL (SIDEBAR)
# =============================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=70)
    st.title("Painel de Controle")
    st.caption("Motor: **Regras SE-ENTÃO + Fatores de Certeza (Forward Chaining)**")

    st.markdown("---")
    st.subheader("🧭 Etapas")
    for idx, label in enumerate(STEPS):
        st.button(
            label,
            key=f"nav_{idx}",
            use_container_width=True,
            type="primary" if idx == st.session_state.step else "secondary",
            on_click=go_to,
            args=(idx,),
        )

    st.markdown("---")
    st.subheader("📈 Progresso das respostas")
    for name, (done, total) in answered_count().items():
        st.caption(f"{name.capitalize()}: {done}/{total}")
        st.progress(done / total if total else 0.0)

    st.markdown("---")
    st.subheader("⚡ Personas de Validação")
    persona_options = {"Selecione uma persona...": None}
    persona_options.update({
        f"{p['avatar']} {p['name']} ({p['badge']})": key for key, p in TEST_PERSONAS.items()
    })
    selected_persona_label = st.selectbox("Carregar Perfil de Teste:", list(persona_options.keys()), index=0)
    if persona_options[selected_persona_label]:
        st.button("Carregar Dados da Persona", use_container_width=True, type="secondary",
                  on_click=load_persona, args=(persona_options[selected_persona_label],))

    if st.button("🔄 Reiniciar questionário", use_container_width=True):
        st.session_state.answers = empty_answers()
        st.session_state.selected_career = None
        reset_widgets()
        go_to(0)
        st.rerun()

    st.markdown("---")
    st.markdown(f"""
    **ℹ️ Base de Conhecimento** (`{kb.meta.get('version', '')}`):
    - **Regras SE-ENTÃO:** {len(kb.rules)}
    - **Carreiras:** {len(kb.careers)}
    - **Afinidades avaliadas:** {len(kb.affinities)}
    - **Competências mapeadas:** {len(kb.competencies)}
    - **Fonte:** `regras_carreiras.json`
    """)


# =============================================================================
# CABEÇALHO PRINCIPAL
# =============================================================================
st.markdown("""
<div class="main-header">
    <h1>🎓 Consultor Inteligente de Carreiras em TI</h1>
    <p>Sistema Especialista para mapeamento de perfil, compatibilidade com 10 carreiras, análise de lacunas e trilha de desenvolvimento.</p>
</div>
""", unsafe_allow_html=True)

step = st.session_state.step
st.progress((step + 1) / len(STEPS), text=f"Etapa {step + 1} de {len(STEPS)} · {STEPS[step]}")


def navigation_buttons(next_label: str = "Avançar →"):
    st.markdown("---")
    col_back, _, col_next = st.columns([1, 2, 1])
    with col_back:
        if step > 0:
            st.button("← Voltar", use_container_width=True, on_click=go_to, args=(step - 1,))
    with col_next:
        if step < len(STEPS) - 1:
            st.button(next_label, type="primary", use_container_width=True, on_click=go_to, args=(step + 1,))


# =============================================================================
# ETAPA 1 · PERFIL PESSOAL
# =============================================================================
def render_profile_step():
    st.markdown("### 👤 Perfil pessoal e objetivos")
    st.write("Essas informações personalizam o plano de estudos: objetivo, experiência e tempo disponível.")
    personal = kb.personal_profile
    profile = st.session_state.answers["profile"]
    road_cfg = kb.parameters["roadmap"]

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Como podemos te chamar?", value=profile.get("name", ""),
                             key=widget_key("profile", "name"))
        store("profile", "name", name.strip())

        objectives = {o["id"]: o["label"] for o in personal.get("objectives", [])}
        obj_options = [None] + list(objectives)
        objective = st.selectbox(
            "Qual é o seu principal objetivo profissional?", obj_options,
            index=obj_options.index(profile.get("objective")) if profile.get("objective") in obj_options else 0,
            format_func=lambda v: "Prefiro não responder" if v is None else objectives[v],
            key=widget_key("profile", "objective"))
        store("profile", "objective", objective)

        levels = {e["id"]: e["label"] for e in personal.get("experience_levels", [])}
        exp_options = [None] + list(levels)
        experience = st.selectbox(
            "Qual é a sua experiência atual em TI?", exp_options,
            index=exp_options.index(profile.get("experience")) if profile.get("experience") in exp_options else 0,
            format_func=lambda v: "Prefiro não responder" if v is None else levels[v],
            key=widget_key("profile", "experience"))
        store("profile", "experience", experience)

    with col2:
        weekly = st.slider("Quantas horas por semana você pode estudar?", 2, 40,
                           value=int(profile.get("weekly_hours", road_cfg["default_weekly_hours"])),
                           key=widget_key("profile", "weekly_hours"))
        store("profile", "weekly_hours", weekly)
        deadline = st.slider("Em quantos meses deseja estar pronto para vagas Júnior?", 1, 24,
                             value=int(profile.get("deadline_months", road_cfg["default_deadline_months"])),
                             key=widget_key("profile", "deadline_months"))
        store("profile", "deadline_months", deadline)

    st.markdown("#### Estilo de trabalho")
    cols = st.columns(len(PROFILE_CHOICE_QUESTIONS))
    for col, qid in zip(cols, PROFILE_CHOICE_QUESTIONS):
        question = kb.choice_question(qid)
        if question:
            with col:
                st.markdown(f"**{question['label']}**")
                choice_input(question)

    navigation_buttons()


# =============================================================================
# ETAPA 2 · AFINIDADES TÉCNICAS
# =============================================================================
def render_affinity_step():
    st.markdown("### 💡 Afinidades técnicas (o que você **gosta** de fazer)")
    st.info("Avalie seu **interesse** por cada tema, independentemente de já saber ou não. "
            "Seus conhecimentos serão avaliados na próxima etapa. Deixe em “Não informado” se não tiver certeza.")
    labels = scale["affinity_labels"]
    items = list(kb.affinities.items())
    col1, col2 = st.columns(2)
    for idx, (aff_id, aff) in enumerate(items):
        with (col1 if idx % 2 == 0 else col2):
            scale_input("affinities", aff_id, f"**{aff['label']}** — {aff['question']}", labels)

    st.markdown("#### Preferências de atuação")
    other_questions = [q for q in kb.choice_questions if q["id"] not in PROFILE_CHOICE_QUESTIONS]
    col1, col2 = st.columns(2)
    for idx, question in enumerate(other_questions):
        with (col1 if idx % 2 == 0 else col2):
            st.markdown(f"**{question['label']}**")
            choice_input(question)

    navigation_buttons()


# =============================================================================
# ETAPA 3 · CONHECIMENTOS ATUAIS
# =============================================================================
def render_knowledge_step():
    st.markdown("### 🧰 Conhecimentos atuais (o que você **sabe** fazer)")
    st.info("Indique seu nível real de proficiência. Competências não informadas são tratadas como "
            "ausentes de evidência: não reduzem sua compatibilidade, mas entram no plano como não estudadas.")
    labels = scale["proficiency_labels"]
    answers = st.session_state.answers["proficiencies"]
    for idx, area in enumerate(kb.competency_areas):
        comps = [(cid, c) for cid, c in kb.competencies.items() if c.get("area") == area]
        if not comps:
            continue
        done = sum(1 for cid, _ in comps if cid in answers)
        with st.expander(f"{area} ({done}/{len(comps)} respondidas)", expanded=(idx == 0)):
            col1, col2 = st.columns(2)
            for j, (cid, comp) in enumerate(comps):
                with (col1 if j % 2 == 0 else col2):
                    scale_input("proficiencies", cid, comp["name"], labels)

    navigation_buttons("Ver resultados →")


# =============================================================================
# ETAPA 4 · RESULTADOS
# =============================================================================
def has_any_answer() -> bool:
    answers = st.session_state.answers
    return bool(answers["affinities"] or answers["choices"] or answers["proficiencies"])


def render_rule(firing: dict):
    css = "rule-card" if firing["points"] > 0 else "negative-rule-card"
    if firing.get("category") == "desambiguacao" and firing["points"] > 0:
        css = "cross-rule-card"
    st.markdown(f"""
    <div class="{css}">
        <b>[{firing['rule_id']}] {firing['rule_name']}</b> (FC {firing['points']:+.2f})<br/>
        <span style="color: #4B5563; font-size: 0.9rem;"><b>SE</b> {firing['conditions']}</span><br/>
        <span style="color: #4B5563; font-size: 0.9rem;"><b>ENTÃO</b> {firing['reason']}</span>
    </div>
    """, unsafe_allow_html=True)


def render_results_step():
    if not has_any_answer():
        st.warning("Responda ao menos algumas perguntas das etapas anteriores para gerar o diagnóstico.")
        navigation_buttons()
        return

    res = advisor.diagnose(st.session_state.answers)
    ranked = res["ranked_tracks"]
    top3 = res["top3"]
    name = st.session_state.answers["profile"].get("name")

    st.markdown(f"## 🎯 Diagnóstico do Sistema Especialista{', ' + name if name else ''}")
    st.caption("Os percentuais indicam a **compatibilidade do seu perfil com cada carreira segundo as regras "
               "da base de conhecimento**, e não a probabilidade de sucesso profissional.")

    ambiguity = res["ambiguity"]
    if ambiguity["message"]:
        st.warning("⚖️ " + ambiguity["message"])

    # Top 3
    st.markdown("### 🏆 Top 3 carreiras mais compatíveis")
    cols = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]
    for col, medal, track in zip(cols, medals, top3):
        with col:
            st.markdown(f"""
            <div class="card-recommendation">
                <div style="font-size:2rem">{medal} {track['icon']}</div>
                <b>{track['name']}</b>
                <div class="pct">{track['percentage']:.1f}%</div>
                <div style="font-size:0.85rem;color:#475569">Confiança da avaliação: <b>{track['confidence_label']}</b>
                · Fator de certeza das regras: {track['certainty_factor']:+.2f}</div>
                <p style="font-size:0.9rem;margin-top:0.6rem">{track['summary']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Ver plano de desenvolvimento", key=f"plan_{track['track_id']}", use_container_width=True):
                st.session_state.selected_career = track["track_id"]
                go_to(STEP_PLAN)
                st.rerun()

    # Gráficos
    st.markdown("### 📊 Compatibilidade com as 10 carreiras")
    tab_rank, tab_radar, tab_comp = st.tabs(["Ranking", "Radar de afinidades", "Composição da pontuação"])
    with tab_rank:
        st.altair_chart(charts.ranking_chart(ranked), use_container_width=True)
    with tab_radar:
        radar_options = {t["track_id"]: f"{t['icon']} {t['name']} ({t['percentage']:.1f}%)" for t in ranked}
        radar_career = st.selectbox("Comparar suas afinidades com o perfil de:", list(radar_options),
                                    format_func=radar_options.get, key="radar_career")
        career = kb.careers[radar_career]
        st.altair_chart(charts.radar_chart(
            {k: a["label"] for k, a in kb.affinities.items()},
            res["input_answers"]["affinities"],
            career.get("affinity_profile", {}),
            career["name"],
        ))
        st.caption("Perfil da carreira = importância relativa de cada afinidade na base de conhecimento. "
                   "Afinidades não informadas aparecem no centro.")
    with tab_comp:
        st.altair_chart(charts.components_chart(top3, COMPONENT_LABELS))
        st.dataframe(pd.DataFrame([
            {
                "Carreira": f"{t['icon']} {t['name']}",
                "Compatibilidade (%)": t["percentage"],
                "Base ponderada (%)": t["base_percentage"],
                "Fator de certeza": t["certainty_factor"],
                **{f"{COMPONENT_LABELS[k]} (%)": round(c["score"] * 100, 1) for k, c in t["components"].items()},
                "Confiança": t["confidence_label"],
            }
            for t in ranked
        ]), hide_index=True, use_container_width=True)

    # Justificativas
    st.markdown("### 🔎 Por que essas carreiras? (justificativas)")
    for medal, track in zip(medals, top3):
        with st.expander(f"{medal} {track['icon']} {track['name']} — {track['percentage']:.1f}%", expanded=(track is top3[0])):
            col_fav, col_unf = st.columns(2)
            with col_fav:
                st.markdown("**Evidências favoráveis**")
                for text in track["justification"]["favorable"] or ["Nenhuma evidência forte registrada."]:
                    st.markdown(f"- {text}")
            with col_unf:
                st.markdown("**Evidências desfavoráveis**")
                for text in track["justification"]["unfavorable"] or ["Nenhuma evidência desfavorável."]:
                    st.markdown(f"- {text}")
            if track["rules"]:
                st.markdown("**Regras SE-ENTÃO que afetaram esta carreira**")
                for firing in track["rules"]:
                    render_rule(firing)

    if ambiguity["is_ambiguous"] and ambiguity["discriminating_affinities"]:
        st.markdown("#### 🧩 O que diferencia as carreiras empatadas")
        for d in ambiguity["discriminating_affinities"]:
            answered = f"sua resposta: {d['user_value']}/5" if d["user_value"] else "ainda não respondida"
            st.markdown(f"- **{d['label']}** pesa mais em **{d['favors_name']}** ({answered}).")

    if res["insights"]:
        st.markdown("### 💬 Afinidade × Proficiência")
        for insight in res["insights"]:
            icon = "🌱" if insight["type"] == "latent_talent" else "🔁"
            st.info(f"{icon} {insight['text']}")

    with st.expander(f"⚙️ Rastro do motor de inferência ({res['total_rules_fired']} regras disparadas)"):
        if res["derived_facts"]:
            st.markdown("**Fatos derivados por encadeamento para frente:** " + ", ".join(
                kb.trait_label(k.split(".", 1)[1]) for k in res["derived_facts"]))
        st.dataframe(pd.DataFrame([
            {
                "Ciclo": f["cycle"],
                "Regra": f["rule_id"],
                "Categoria": f["category"],
                "Nome": f["rule_name"],
                "SE": f["conditions"],
                "ENTÃO": ", ".join(f"{k} {v:+.2f}" for k, v in f["evidence"].items())
                         or ", ".join(f"{k} = {v}" for k, v in f["inferred"].items()),
            }
            for f in res["all_rule_firings"]
        ]), hide_index=True, use_container_width=True)

    # Panorama de mercado da carreira líder (funcionalidade original)
    top = res["top_track"]
    metadata = top["metadata"]
    st.markdown(f"### 💼 Panorama de mercado · {top['icon']} {top['name']}")
    st.write(metadata.get("description", ""))
    sal = metadata.get("salary_range", {})
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Salário Júnior", sal.get("junior", "N/A"))
    m2.metric("Salário Pleno", sal.get("pleno", "N/A"))
    m3.metric("Salário Sênior", sal.get("senior", "N/A"))
    m4.metric("Demanda de Mercado", metadata.get("market_demand", "N/A"))
    st.markdown("**Tecnologias mais utilizadas:** " + " · ".join(f"`{t}`" for t in metadata.get("technologies", [])))

    export_payload = {
        "top3": [{"track": t["name"], "percent": t["percentage"], "confidence": t["confidence_label"]} for t in top3],
        "ambiguity": {k: v for k, v in ambiguity.items() if k != "discriminating_affinities"},
        "user_answers": res["input_answers"],
        "derived_facts": res["derived_facts"],
        "rules_fired": [{k: f[k] for k in ("rule_id", "rule_name", "conditions", "evidence")} for f in res["all_rule_firings"]],
        "all_ranked_tracks": [
            {"track": t["name"], "percent": t["percentage"], "certainty_factor": t["certainty_factor"],
             "justification": t["justification"]}
            for t in ranked
        ],
    }
    st.download_button(
        label="📥 Baixar diagnóstico em JSON",
        data=json.dumps(export_payload, ensure_ascii=False, indent=2),
        file_name=f"diagnostico_carreira_{top['track_id']}.json",
        mime="application/json",
        use_container_width=True,
    )

    navigation_buttons("Montar plano de desenvolvimento →")


# =============================================================================
# ETAPA 5 · PLANO DE DESENVOLVIMENTO
# =============================================================================
def render_plan_step():
    if not has_any_answer():
        st.warning("Responda ao questionário para gerar um plano personalizado.")
        navigation_buttons()
        return

    res = advisor.diagnose(st.session_state.answers)
    ranked = res["ranked_tracks"]
    options = {t["track_id"]: f"{t['icon']} {t['name']} ({t['percentage']:.1f}%)" for t in ranked}
    default = st.session_state.selected_career or ranked[0]["track_id"]
    if st.session_state.get("plan_career") not in options:
        st.session_state.plan_career = default
    career_id = st.selectbox("Carreira para o plano de desenvolvimento:", list(options),
                             format_func=options.get, key="plan_career")
    st.session_state.selected_career = career_id

    plan = advisor.build_development_plan(career_id, st.session_state.answers)
    gap, roadmap = plan["skill_gap"], plan["roadmap"]

    st.markdown(f"## 🗺️ Plano para {roadmap['career_name']}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Prontidão para Júnior", f"{gap['readiness_pct']:.0f}%")
    c2.metric("Nível atual", gap["level"]["label"])
    c3.metric("Carga estimada", f"{roadmap['total_hours']} h")
    c4.metric("Duração estimada", f"{roadmap['total_weeks']} semanas",
              delta=f"prazo: {roadmap['deadline_weeks']} semanas",
              delta_color="normal" if roadmap["fits_deadline"] else "inverse")
    if not roadmap["fits_deadline"]:
        st.warning(f"Com {roadmap['weekly_hours']:.0f} h/semana o plano completo não cabe no prazo de "
                   f"{roadmap['deadline_months']:.0f} meses. Seriam necessárias cerca de "
                   f"{roadmap['required_weekly_hours']} h/semana — itens não essenciais foram marcados como opcionais.")

    # Análise de lacunas
    st.markdown("### 📐 Análise de lacunas de competências (nível Júnior)")
    s1, s2, s3 = st.columns(3)
    s1.metric("Dominadas", len(gap["dominated"]))
    s2.metric("Parcialmente desenvolvidas", len(gap["partial"]))
    s3.metric("Ausentes", len(gap["missing"]))
    st.altair_chart(charts.skill_gap_chart(gap["items"]), use_container_width=True)
    st.dataframe(pd.DataFrame([
        {
            "Competência": it["label"] + (" (pré-requisito)" if it["external"] else ""),
            "Situação": STATUS_LABELS[it["status"]],
            "Atual": it["current"] if it["informed"] else "Não informado",
            "Exigido": it["required"],
            "Prioridade": it["priority_label"] or "—",
            "Essencial": "Sim" if it["essential"] else "Não",
            "Pré-requisitos pendentes": ", ".join(kb.competency_name(p) for p in it["pending_prerequisites"]) or "—",
        }
        for it in gap["items"]
    ]), hide_index=True, use_container_width=True)
    if gap["uninformed"]:
        st.caption(f"{len(gap['uninformed'])} competência(s) sem nível informado foram consideradas como não estudadas.")
        st.button("Informar meus conhecimentos", on_click=go_to, args=(2,))

    # Roadmap
    st.markdown("### 🚀 Roadmap personalizado")
    st.caption(f"Sequência respeitando pré-requisitos, com {roadmap['weekly_hours']:.0f} h de estudo por semana.")
    if not roadmap["phases"]:
        st.success("Você já atende a todas as competências Júnior mapeadas para esta carreira!")
    for phase in roadmap["phases"]:
        st.markdown(f"#### {phase['name']} · {phase['hours']} h")
        st.caption(phase["description"])
        for s in phase["steps"]:
            tags = []
            if s["essential"]:
                tags.append("essencial")
            if s["external"]:
                tags.append("pré-requisito")
            if s.get("optional"):
                tags.append("opcional")
            tag_text = f" · {', '.join(tags)}" if tags else ""
            title = (f"Semanas {s['start_week']}–{s['end_week']} · {s['name']} "
                     f"({s['hours']} h · prioridade {s['priority']}{tag_text})")
            with st.expander(title):
                current = s["current"] if s["current"] is not None else "não informado"
                st.markdown(f"**Nível:** {current} → {s['required']} · **Situação:** {STATUS_LABELS[s['status']]}")
                if s["prerequisites"]:
                    st.markdown("**Pré-requisitos:** " + ", ".join(s["prerequisites"]))
                col_r, col_e = st.columns(2)
                with col_r:
                    st.markdown("**Recursos de aprendizagem**")
                    for r in s["resources"]:
                        st.markdown(f"- {r}")
                with col_e:
                    st.markdown("**Exercícios e atividades práticas**")
                    for e in s["exercises"]:
                        st.markdown(f"- {e}")
        project = phase["milestone_project"]
        if project:
            st.success(f"🧪 **Projeto marco (semanas {project['start_week']}–{project['end_week']}):** "
                       f"{project['title']} — {project['description']}  \n"
                       f"Pratica: {', '.join(project['practices'])} · {project.get('hours', 0)} h · "
                       f"publique no GitHub com README, prints e instruções de execução.")

    col_proj, col_cert = st.columns(2)
    with col_proj:
        st.markdown("### 📂 Projetos adicionais para o portfólio")
        if not roadmap["portfolio_projects"]:
            st.caption("Os projetos recomendados já foram incluídos como marcos das fases.")
        for p in roadmap["portfolio_projects"]:
            st.markdown(f"**{p['title']}** ({p['level']}, ~{p.get('hours', 0)} h)  \n{p['description']}  \n"
                        f"_Pratica:_ {', '.join(p['practices'])}")
    with col_cert:
        st.markdown("### 🎖️ Certificações")
        for c in roadmap["certifications"]:
            st.markdown(f"**{c['name']}** — {c['provider']}  \n{c['timing']} · {c['note']}")

    if roadmap["tips"]:
        st.markdown("### 💡 Recomendações personalizadas")
        for tip in roadmap["tips"]:
            st.markdown(f"- {tip}")

    st.download_button(
        label="📥 Baixar plano de desenvolvimento em JSON",
        data=json.dumps(plan, ensure_ascii=False, indent=2),
        file_name=f"plano_desenvolvimento_{career_id}.json",
        mime="application/json",
        use_container_width=True,
    )
    navigation_buttons()


RENDERERS = [render_profile_step, render_affinity_step, render_knowledge_step, render_results_step, render_plan_step]
RENDERERS[step]()
