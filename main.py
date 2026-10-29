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
    print(" Demonstração e Validação das Personas de Teste (Regras SE-ENTÃO + Fatores de Certeza)")
    print("=" * 78)

    failures = 0
    for pid, pdata in TEST_PERSONAS.items():
        print(f"\n>> Testando Persona: {pdata['name']} ({pdata['badge']})")
        print(f"   Descrição: {pdata['description']}")
        res = advisor.diagnose(pdata["answers"])
        top = res["top_track"]
        expected = pdata["expected_track"]
        ok = top["track_id"] == expected
        failures += 0 if ok else 1
        status = "[SUCESSO]" if ok else "[FALHA]"

        print(f"   Resultado: {top['icon']} {top['name']} ({top['percentage']}%) [Status: {status}]")
        print("   Top 3: " + " | ".join(f"{t['name']} {t['percentage']}%" for t in res["top3"]))
        if res["ambiguity"]["message"]:
            print(f"   Atenção: {res['ambiguity']['message']}")
        print(f"   Total de regras disparadas no ciclo: {res['total_rules_fired']}")
        print("   Principais regras que ativaram esta recomendação:")
        for rule in res["top_track_rules"][:3]:
            print(f"     - [{rule['rule_id']}] {rule['rule_name']} (FC {rule['points']:+.2f})")
            print(f"       Justificativa: {rule['reason']}")

        plan = advisor.build_development_plan(top["track_id"], pdata["answers"])
        gap, roadmap = plan["skill_gap"], plan["roadmap"]
        print(f"   Prontidão Júnior: {gap['readiness_pct']}% ({gap['level']['label']}) | "
              f"Plano: {roadmap['total_hours']} h em {roadmap['total_weeks']} semanas")

    print("\n" + "=" * 78)
    if failures:
        print(f" Validação concluída com {failures} persona(s) fora do esperado.")
    else:
        print(" Validação concluída com sucesso para todas as personas!")
    print("=" * 78)


def _ask_scale(prompt: str) -> int | None:
    raw = input(f"{prompt} (1-5, Enter para pular): ").strip()
    return int(raw) if raw in {"1", "2", "3", "4", "5"} else None


def run_cli_interview():
    """Executa uma entrevista interativa via console usando a base de conhecimento."""
    advisor = CareerAdvisor()
    kb = advisor.kb
    print("=" * 70)
    print(" ENTREVISTA VOCACIONAL EM TI (MODO TERMINAL)")
    print("=" * 70)

    answers = {"profile": {}, "affinities": {}, "proficiencies": {}, "choices": {}}
    print("\nAfinidades: quanto você GOSTA de cada tema?")
    for aff_id, aff in kb.affinities.items():
        value = _ask_scale(f"  {aff['label']}")
        if value:
            answers["affinities"][aff_id] = value

    print("\nPreferências de atuação:")
    for question in kb.choice_questions:
        print(f"\n{question['question']}")
        for i, option in enumerate(question["options"], start=1):
            print(f"   [{i}] {option['value']}")
        raw = input("Escolha (Enter para pular): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(question["options"]):
            answers["choices"][question["id"]] = question["options"][int(raw) - 1]["value"]

    res = advisor.diagnose(answers)
    print("\n" + "=" * 70)
    for pos, track in enumerate(res["top3"], start=1):
        print(f"{pos}º {track['icon']} {track['name']}: {track['percentage']}% (confiança {track['confidence_label']})")
    if res["ambiguity"]["message"]:
        print(res["ambiguity"]["message"])
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
