"""
Consultor Inteligente de Carreiras em TI.
Ponto de entrada principal do projeto.
Permite executar demonstração das Personas de Teste, rodar via linha de comando (CLI)
ou iniciar o servidor web interativo Streamlit.
"""
import sys
import subprocess
import os

# Configura encoding UTF-8 no console Windows para suportar emojis e caracteres acentuados
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from engine.advisor import CareerAdvisor
from data.personas import TEST_PERSONAS


def run_personas_demo():
    """Executa a validação e demonstração automática com as Personas de Teste."""
    advisor = CareerAdvisor()
    print("=" * 78)
    print(" CONSULTOR INTELIGENTE DE CARREIRAS EM TI - SISTEMA ESPECIALISTA")
    print(" Demonstração e Validação das Personas de Teste (Experta / Forward Chaining)")
    print("=" * 78)

    for pid, pdata in TEST_PERSONAS.items():
        print(f"\n>> Testando Persona: {pdata['name']} ({pdata['badge']})")
        print(f"   Descrição: {pdata['description']}")
        res = advisor.diagnose(pdata["answers"])
        top = res["top_track"]
        expected = pdata["expected_track"]
        status = "[SUCESSO]" if top["track_id"] == expected else "[FALHA]"

        print(f"   Resultado: {top['icon']} {top['name']} ({top['percentage']}%) [Status: {status}]")
        print(f"   Total de regras disparadas no ciclo: {res['total_rules_fired']}")
        print("   Principais regras que ativaram esta recomendação:")
        for rule in res["top_track_rules"][:3]:
            print(f"     - [{rule['rule_id']}] {rule['rule_name']} (+{rule['points']:.0f} pts)")
            print(f"       Justificativa: {rule['reason']}")

    print("\n" + "=" * 78)
    print(" Validação concluída com sucesso para todas as personas!")
    print("=" * 78)


def run_cli_interview():
    """Executa uma entrevista interativa via console."""
    print("=" * 70)
    print(" ENTREVISTA VOCACIONAL EM TI (MODO TERMINAL)")
    print("=" * 70)

    print("\n1. Afinidade Matemática e Estatística:")
    print("   [1] Baixa  [2] Média  [3] Alta")
    math_choice = input("Escolha (1-3): ").strip()
    math_map = {"1": "Baixa", "2": "Média", "3": "Alta"}
    math_affinity = math_map.get(math_choice, "Média")

    print("\n2. Preferência de Atuação Diária:")
    work_list = [
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
    for i, w in enumerate(work_list, start=1):
        print(f"   [{i}] {w}")
    w_idx = int(input("Escolha (1-10): ").strip() or "1") - 1
    work_preference = work_list[max(0, min(w_idx, len(work_list) - 1))]

    # Executa diagnóstico preliminar com o motor
    advisor = CareerAdvisor()
    res = advisor.diagnose({
        "math_affinity": math_affinity,
        "work_preference": work_preference,
        "primary_tool": "Python",
        "value_delivery": "APIs robustas, regras de negócio e estabilidade de servidor",
        "daily_challenge": "Otimizar algoritmos e consultas SQL complexas",
        "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
        "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
    })

    top = res["top_track"]
    print("\n" + "=" * 70)
    print(f"TRILHA RECOMENDADA: {top['icon']} {top['name']}")
    print(f"Compatibilidade: {top['percentage']}%")
    print(f"{top['summary']}")
    print("=" * 70)


def start_streamlit_app():
    """Inicia a interface Streamlit no navegador padrão."""
    print("Iniciando interface Web do Streamlit...")
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])


if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli_interview()
    elif "--demo" in sys.argv:
        run_personas_demo()
    elif "--web" in sys.argv:
        start_streamlit_app()
    else:
        # Modo padrão: executa a validação e orienta sobre o Streamlit
        run_personas_demo()
        print("\nPara iniciar a interface web interativa do Streamlit, execute:")
        print("    streamlit run app.py")
        print("Ou execute: python main.py --web\n")
