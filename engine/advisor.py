"""
Orquestrador do Sistema Especialista: CareerAdvisor.
Responsável por instanciar o motor de inferência, declarar os fatos,
executar o ciclo de encadeamento para frente, normalizar os resultados
e produzir o diagnóstico completo com justificativas transparentes.
"""
from typing import Dict, Any, List
from engine.rules import CareerKnowledgeEngine
from engine.facts import UserProfile
from data.career_tracks import CAREER_TRACKS


class CareerAdvisor:
    """
    Fachada inteligente que orquestra a entrevista e a inferência baseada em regras.
    """

    def __init__(self):
        self.engine = CareerKnowledgeEngine()

    def diagnose(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o processo de inferência com base nas respostas fornecidas.

        Args:
            answers: Dicionário contendo as respostas do usuário:
                - math_affinity
                - work_preference
                - primary_tool
                - value_delivery
                - daily_challenge
                - communication_vs_code
                - device_focus

        Returns:
            Dicionário com o diagnóstico completo, ranking de compatibilidade,
            regras disparadas e justificativas detalhadas.
        """
        # Cria uma instância limpa do motor para assegurar total isolamento de cada ciclo
        engine = CareerKnowledgeEngine()
        engine.reset()

        # Declaração do fato principal com as respostas do usuário
        user_fact = UserProfile(
            math_affinity=answers.get("math_affinity", "Média"),
            work_preference=answers.get("work_preference", ""),
            primary_tool=answers.get("primary_tool", ""),
            value_delivery=answers.get("value_delivery", ""),
            daily_challenge=answers.get("daily_challenge", ""),
            communication_vs_code=answers.get("communication_vs_code", ""),
            device_focus=answers.get("device_focus", "")
        )

        engine.declare(user_fact)
        engine.run()

        self.engine = engine
        raw_scores = dict(engine.scores)
        firings = list(engine.rule_firings)

        # Garantir que nenhum score seja negativo antes da normalização percentual
        sanitized_scores = {k: max(0.0, v) for k, v in raw_scores.items()}
        max_possible_score = 110.0  # Pontuação máxima teórica média com bônus cruzados

        # Normalização percentual proporcional (0% a 100%)
        ranked_tracks = []
        for track_id, raw_val in sanitized_scores.items():
            percent = min(100.0, round((raw_val / max_possible_score) * 100.0, 1))
            metadata = CAREER_TRACKS.get(track_id, {})
            ranked_tracks.append({
                "track_id": track_id,
                "name": metadata.get("name", track_id),
                "icon": metadata.get("icon", "💼"),
                "summary": metadata.get("summary", ""),
                "score": raw_val,
                "percentage": percent,
                "metadata": metadata
            })

        # Ordenar do mais compatível para o menos compatível
        ranked_tracks.sort(key=lambda x: x["score"], reverse=True)

        top_track = ranked_tracks[0] if ranked_tracks else None
        top_track_id = top_track["track_id"] if top_track else None

        # Filtrar regras que beneficiaram diretamente a trilha vencedora
        top_track_rules = [
            f for f in firings
            if f["track"] == top_track_id and f["points"] > 0
        ]

        # Filtrar regras de desambiguação cruzada disparadas na sessão
        cross_rules_fired = [
            f for f in firings
            if "CROSS" in f["rule_id"] or "PENALTY" in f["rule_id"]
        ]

        # Trilha secundária (vice-campeã) para análise comparativa
        runner_up = ranked_tracks[1] if len(ranked_tracks) > 1 else None

        return {
            "top_track": top_track,
            "runner_up": runner_up,
            "ranked_tracks": ranked_tracks,
            "all_rule_firings": firings,
            "top_track_rules": top_track_rules,
            "cross_rules_fired": cross_rules_fired,
            "total_rules_fired": len(firings),
            "input_answers": answers
        }
