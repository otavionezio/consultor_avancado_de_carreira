"""
Consultor Inteligente de Carreiras em TI - Interface Web com Streamlit.
Sistema Especialista baseado em regras (Experta) com encadeamento para frente.
"""
import streamlit as st
import pandas as pd
import json

from engine.advisor import CareerAdvisor
from data.career_tracks import CAREER_TRACKS
from data.personas import TEST_PERSONAS


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
        margin-bottom: 2rem;
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
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .badge-primary {
        background-color: #DBEAFE;
        color: #1E40AF;
    }
    .card-recommendation {
        background: #F8FAFC;
        border: 2px solid #3B82F6;
        border-radius: 12px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
    }
    .rule-card {
        background: #FFFFFF;
        border-left: 4px solid #10B981;
        padding: 0.9rem 1.2rem;
        margin-bottom: 0.6rem;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .cross-rule-card {
        background: #FFFBEB;
        border-left: 4px solid #F59E0B;
        padding: 0.9rem 1.2rem;
        margin-bottom: 0.6rem;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)


# Inicializa estado da sessão para formulário
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "math_affinity": "Média",
        "work_preference": "Lógica de negócios, APIs e bancos de dados",
        "primary_tool": "Python",
        "value_delivery": "APIs robustas, regras de negócio e estabilidade de servidor",
        "daily_challenge": "Otimizar algoritmos e consultas SQL complexas",
        "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
        "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
    }

if "diagnosis_result" not in st.session_state:
    st.session_state.diagnosis_result = None


def load_persona(persona_key: str):
    """Carrega as respostas de uma persona pré-definida."""
    persona = TEST_PERSONAS[persona_key]
    st.session_state.form_data = dict(persona["answers"])
    advisor = CareerAdvisor()
    st.session_state.diagnosis_result = advisor.diagnose(persona["answers"])


# =============================================================================
# BARRA LATERAL (SIDEBAR)
# =============================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=70)
    st.title("Painel de Controle")
    st.caption("Motor de Inferência: **Experta (Forward Chaining)**")

    st.markdown("---")
    st.subheader("⚡ Personas de Validação")
    st.write("Selecione uma persona para carregar respostas e testar a inferência instantaneamente:")

    persona_options = {
        "Selecione uma persona...": None,
        "🧠 Ana Silva (Cientista de Dados)": "ana_data_science",
        "🛡️ Carlos Rocha (Cibersegurança)": "carlos_security",
        "🎨 Beatriz Lima (Front-end & UI/UX)": "beatriz_frontend",
        "🧭 Lucas Mendes (Product Manager)": "lucas_product",
        "🏗️ Eduardo Santos (Engenheiro de Dados)": "eduardo_data_eng",
        "♾️ Mariana Costa (DevOps & SRE)": "mariana_devops",
        "⚙️ Gabriel Alencar (Back-end)": "gabriel_backend",
        "📱 Rafael Nogueira (Mobile)": "rafael_mobile",
        "🔍 Camila Duarte (QA / Qualidade)": "camila_qa",
        "☁️ Rodrigo Fonseca (Cloud Architect)": "rodrigo_cloud"
    }

    selected_persona_label = st.selectbox(
        "Carregar Perfil de Teste:",
        list(persona_options.keys()),
        index=0
    )

    if selected_persona_label and persona_options[selected_persona_label]:
        persona_key = persona_options[selected_persona_label]
        if st.button("Carregar Dados da Persona", use_container_width=True, type="secondary"):
            load_persona(persona_key)
            st.rerun()

    st.markdown("---")
    st.markdown("""
    **ℹ️ Sobre o Sistema Especialista:**
    - **Base de Conhecimento:** 52 Regras Lógicas
    - **Motor:** Experta (Rete Algorithm)
    - **Estratégia:** Forward Chaining
    - **Escopo:** 10 Trilhas Especializadas
    - **Transparência:** Justificativa passo a passo
    """)


# =============================================================================
# CABEÇALHO PRINCIPAL
# =============================================================================
st.markdown("""
<div class="main-header">
    <h1>🎓 Consultor Inteligente de Carreiras em TI</h1>
    <p>Sistema Especialista baseado em Regras para orientação vocacional de alta precisão em Tecnologia da Informação.</p>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# FORMULÁRIO DE ENTREVISTA DINÂMICA
# =============================================================================
st.markdown("### 📋 Entrevista de Afinidades e Preferências Profissionais")
st.write("Responda às questões abaixo de acordo com seu perfil para receber um diagnóstico fundamentado:")

# Listas de opções
math_options = ["Baixa", "Média", "Alta"]

work_options = [
    "Lógica de negócios, APIs e bancos de dados",
    "Interfaces visuais interativas, design e experiência do usuário",
    "Modelagem estatística, machine learning e inteligência artificial",
    "Pipelines de dados, arquitetura ETL/ELT e Data Lakes",
    "Defesa cibernética, análise de vulnerabilidades e testes de invasão",
    "Automação de CI/CD, esteiras de deploy, contêineres e alta disponibilidade",
    "Arquitetura de sistemas em nuvem, migração e infraestrutura escalável",
    "Aplicativos móveis nativos ou multiplataforma para smartphones",
    "Testes automatizados, caça a bugs e garantia de qualidade",
    "Gestão de produto, estratégia de negócio, priorização e comunicação"
]

tool_options = [
    "Python",
    "JavaScript / TypeScript",
    "Java / C# / Go",
    "SQL / Ferramentas de Big Data (Spark, Airflow)",
    "Swift / Kotlin / Flutter / React Native",
    "Linux / Bash / Ferramentas de Redes e Segurança",
    "Docker / Kubernetes / Terraform / CI-CD",
    "Nuvem AWS / Azure / GCP",
    "Ferramentas de Teste (Cypress, Selenium, PyTest, JUnit)",
    "Ferramentas de Gestão e Ágil (Jira, Trello, Miro, Notion)",
    "Nenhuma / Iniciante"
]

val_options = [
    "APIs robustas, regras de negócio e estabilidade de servidor",
    "Telas encantadoras, responsivas e navegação agradável",
    "Modelos preditivos acurados e inteligência artificial para decisão",
    "Fluxo de dados limpo, rápido e confiável para toda a empresa",
    "Proteção contra invasões, dados seguros e sistemas blindados",
    "Deploys frequentes sem quedas e esteiras ágeis automatizadas",
    "Estrutura de nuvem escalável, resiliente e com custos otimizados",
    "Experiência móvel fluida e acessível na palma da mão",
    "Software sem bugs, estável e que cumpre todos os critérios",
    "Produtos que resolvem dores de usuários e geram receita"
]

challenge_options = [
    "Otimizar algoritmos e consultas SQL complexas",
    "Ajustar CSS, microinterações e acessibilidade web",
    "Calibrar hiperparâmetros e testar hipóteses estatísticas",
    "Escalar pipelines de processamento distribuído de terabytes",
    "Simular ataques, encontrar brechas zero-day e auditar logs",
    "Resolver gargalos em contêineres e orquestrar clusters K8s",
    "Desenhar diagramas de nuvem e arquitetar alta disponibilidade",
    "Gerenciar ciclo de vida de apps e permissões de hardware móvel",
    "Automatizar suítes de testes de regressão e carga",
    "Negociar com stakeholders e definir o roadmap do produto"
]

comm_options = [
    "Foco predominante em código e arquitetura técnica profunda",
    "Foco balanceado entre desenvolvimento técnico e colaboração",
    "Foco predominante em pessoas, alinhamento de negócio e facilitação"
]

device_options = [
    "Agnóstico a hardware, foco total em software/lógica/regras",
    "Dispositivos móveis, smartphones e tablets",
    "Redes, roteadores, firewalls e servidores físicos",
    "Serviços virtuais gerenciados e data centers na nuvem"
]

with st.form("career_quiz_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 1. Afinidade Matemática e Estatística")
        st.caption("Quanto você gosta e se sente confortável com álgebra, cálculo e probabilidade?")
        cur_math = st.session_state.form_data.get("math_affinity", "Média")
        math_affinity = st.radio(
            "Selecione sua afinidade matemática:",
            math_options,
            index=math_options.index(cur_math) if cur_math in math_options else 1,
            horizontal=True
        )

        st.markdown("##### 2. Atuação Diária Preferida")
        st.caption("Qual dessas atividades práticas mais te motiva no dia a dia?")
        cur_work = st.session_state.form_data.get("work_preference", work_options[0])
        work_preference = st.selectbox(
            "Sua atuação dos sonhos:",
            work_options,
            index=work_options.index(cur_work) if cur_work in work_options else 0
        )

        st.markdown("##### 3. Ferramenta ou Linguagem de Maior Afinidade")
        st.caption("Qual ecossistema ou conjunto de ferramentas você mais domina ou prefere aprender?")
        cur_tool = st.session_state.form_data.get("primary_tool", tool_options[0])
        primary_tool = st.selectbox(
            "Ecossistema / Ferramenta favorita:",
            tool_options,
            index=tool_options.index(cur_tool) if cur_tool in tool_options else 0
        )

    with col2:
        st.markdown("##### 4. Tipo de Entrega de Valor Preferida")
        st.caption("Ao término de uma sprint, o que te dá mais orgulho de ter entregue?")
        cur_val = st.session_state.form_data.get("value_delivery", val_options[0])
        value_delivery = st.selectbox(
            "Entrega de valor mais satisfatória:",
            val_options,
            index=val_options.index(cur_val) if cur_val in val_options else 0
        )

        st.markdown("##### 5. Desafio que Mais te Instiga")
        st.caption("Que tipo de problema complexo te mantém engajado?")
        cur_chal = st.session_state.form_data.get("daily_challenge", challenge_options[0])
        daily_challenge = st.selectbox(
            "Desafio técnico estimulante:",
            challenge_options,
            index=challenge_options.index(cur_chal) if cur_chal in challenge_options else 0
        )

        st.markdown("##### 6. Equilíbrio: Código vs Negócio/Pessoas")
        cur_comm = st.session_state.form_data.get("communication_vs_code", comm_options[1])
        communication_vs_code = st.selectbox(
            "Estilo de trabalho predominante:",
            comm_options,
            index=comm_options.index(cur_comm) if cur_comm in comm_options else 1
        )

        st.markdown("##### 7. Foco em Dispositivos ou Infraestrutura")
        cur_dev = st.session_state.form_data.get("device_focus", device_options[0])
        device_focus = st.selectbox(
            "Ambiente de execução de maior interesse:",
            device_options,
            index=device_options.index(cur_dev) if cur_dev in device_options else 0
        )

    submit_button = st.form_submit_width = st.form_submit_button(
        "🚀 Diagnosticar Minha Carreira Ideal",
        type="primary",
        use_container_width=True
    )

if submit_button:
    user_inputs = {
        "math_affinity": math_affinity,
        "work_preference": work_preference,
        "primary_tool": primary_tool,
        "value_delivery": value_delivery,
        "daily_challenge": daily_challenge,
        "communication_vs_code": communication_vs_code,
        "device_focus": device_focus
    }
    st.session_state.form_data = user_inputs
    advisor = CareerAdvisor()
    st.session_state.diagnosis_result = advisor.diagnose(user_inputs)


# =============================================================================
# EXIBIÇÃO DOS RESULTADOS DO SISTEMA ESPECIALISTA
# =============================================================================
res = st.session_state.diagnosis_result

if res:
    top = res["top_track"]
    metadata = top["metadata"]

    st.markdown("---")
    st.markdown("## 🎯 Diagnóstico do Sistema Especialista")

    # Card Principal da Recomendação
    col_icon, col_desc = st.columns([1, 4])
    with col_icon:
        st.markdown(f"<div style='font-size: 5rem; text-align: center;'>{top['icon']}</div>", unsafe_allow_html=True)
    with col_desc:
        st.markdown(f"### {top['name']}")
        st.markdown(f"**Compatibilidade diagnosticada:** `{top['percentage']}%` (Pontuação: {top['score']:.1f} pts)")
        st.markdown(f"_{top['summary']}_")
        st.write(metadata.get("description", ""))

    # Métricas de Mercado
    st.markdown("#### 💼 Panorama de Mercado & Remuneração")
    m1, m2, m3, m4 = st.columns(4)
    sal = metadata.get("salary_range", {})
    with m1:
        st.metric(label="Salário Júnior", value=sal.get("junior", "N/A"))
    with m2:
        st.metric(label="Salário Pleno", value=sal.get("pleno", "N/A"))
    with m3:
        st.metric(label="Salário Sênior", value=sal.get("senior", "N/A"))
    with m4:
        st.metric(label="Demanda de Mercado", value="Altíssima")

    # Justificativas Transparentes (Regras Disparadas)
    st.markdown("---")
    st.markdown("### 🔎 Justificativa Transparente (Regras Disparadas)")
    st.write(
        "Diferente de modelos 'caixa-preta', o Sistema Especialista explica "
        "cada regra lógica do motor Experta que contribuiu para essa recomendação:"
    )

    col_rules1, col_rules2 = st.columns(2)

    with col_rules1:
        st.markdown("##### 📌 Regras Específicas de Ativação")
        for firing in res["top_track_rules"]:
            st.markdown(f"""
            <div class="rule-card">
                <b>[{firing['rule_id']}] {firing['rule_name']}</b> (+{firing['points']:.0f} pts)<br/>
                <span style="color: #4B5563; font-size: 0.95rem;">{firing['reason']}</span>
            </div>
            """, unsafe_allow_html=True)

    with col_rules2:
        st.markdown("##### ⚖️ Regras Cruzadas & Desambiguação")
        if res["cross_rules_fired"]:
            for firing in res["cross_rules_fired"]:
                st.markdown(f"""
                <div class="cross-rule-card">
                    <b>[{firing['rule_id']}] {firing['rule_name']}</b> ({firing['points']:+.0f} pts)<br/>
                    <span style="color: #4B5563; font-size: 0.95rem;">{firing['reason']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhuma regra de desempate cruzado ou penalidade precisou ser acionada.")

    # Gráfico Comparativo das 10 Carreiras
    st.markdown("---")
    st.markdown("### 📊 Ranking Comparativo de Compatibilidade (10 Carreiras)")
    st.write("Abaixo está o índice de compatibilidade calculado pelo motor para cada uma das opções avaliadas:")

    df_ranked = pd.DataFrame([
        {
            "Carreira": f"{t['icon']} {t['name']}",
            "Compatibilidade (%)": t["percentage"],
            "Pontos": t["score"]
        }
        for t in res["ranked_tracks"]
    ])

    st.bar_chart(
        df_ranked.set_index("Carreira")["Compatibilidade (%)"],
        color="#3B82F6",
        horizontal=True
    )

    # Detalhes da Trilha Secundária (Vice-campeã)
    runner_up = res.get("runner_up")
    if runner_up and runner_up["percentage"] > 20:
        st.markdown("---")
        st.markdown("### 🥈 Segunda Opção Mais Próxima")
        st.write(
            f"Se você deseja uma alternativa correlata, sua segunda maior afinidade foi com "
            f"**{runner_up['icon']} {runner_up['name']}** com **{runner_up['percentage']}%** de compatibilidade. "
            f"Ela compartilha algumas das suas preferências de ferramentas e valor entregue."
        )

    # Roadmap e Próximos Passos
    st.markdown("---")
    st.markdown(f"### 🗺️ Roteiro de Aprendizado Recomendado para {top['name']}")

    col_skills, col_roadmap = st.columns(2)

    with col_skills:
        st.markdown("##### 🛠️ Competências & Tecnologias Essenciais")
        st.markdown("**Habilidades Técnicas:**")
        for skill in metadata.get("key_skills", []):
            st.markdown(f"- {skill}")

        st.markdown("**Tecnologias Mais Utilizadas:**")
        for tech in metadata.get("technologies", []):
            st.markdown(f"- `{tech}`")

    with col_roadmap:
        st.markdown("##### 🚀 Passo a Passo para Evolução")
        for idx, step in enumerate(metadata.get("roadmap", []), start=1):
            st.markdown(f"**Passo {idx}:** {step}")

    # Exportar Diagnóstico
    st.markdown("---")
    st.markdown("### 💾 Exportar Relatório de Diagnóstico")
    export_payload = {
        "recommended_track": top["name"],
        "compatibility_percent": top["percentage"],
        "score": top["score"],
        "summary": top["summary"],
        "user_answers": res["input_answers"],
        "rules_fired_count": res["total_rules_fired"],
        "top_rules": res["top_track_rules"],
        "all_ranked_tracks": [
            {"track": t["name"], "score": t["score"], "percent": t["percentage"]}
            for t in res["ranked_tracks"]
        ]
    }
    st.download_button(
        label="📥 Baixar Relatório em JSON",
        data=json.dumps(export_payload, ensure_ascii=False, indent=2),
        file_name=f"diagnostico_carreira_{top['track_id']}.json",
        mime="application/json",
        use_container_width=True
    )
