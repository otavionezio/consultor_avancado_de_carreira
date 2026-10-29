"""
Orquestrador do Sistema Especialista: CareerAdvisor.
Fachada única usada pela interface (Streamlit/CLI) para executar a inferência
de compatibilidade, a análise de lacunas de competências e a geração do roadmap,
mantendo a apresentação separada da lógica do motor.
"""
from typing import Any, Dict, Optional

from engine.inference import InferenceEngine
from engine.knowledge_base import KnowledgeBase, load_knowledge_base
from engine.roadmap import RoadmapGenerator
from engine.skill_gap import SkillGapAnalyzer


class CareerAdvisor:
    """
    Fachada inteligente que orquestra a entrevista e a inferência baseada em regras.
    """

    def __init__(self, knowledge_base: Optional[KnowledgeBase] = None):
        self.kb = knowledge_base or load_knowledge_base()
        self.engine = InferenceEngine(self.kb)
        self.gap_analyzer = SkillGapAnalyzer(self.kb)
        self.roadmap_generator = RoadmapGenerator(self.kb)

    def diagnose(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a inferência de compatibilidade com as dez carreiras.

        Args:
            answers: Respostas estruturadas {profile, affinities, proficiencies, choices}
                ou no formato plano legado (math_affinity, work_preference, ...).

        Returns:
            Diagnóstico com ranking normalizado (0-100%), Top 3, regras disparadas,
            justificativas, análise de ambiguidade e insights do perfil.
        """
        return self.engine.infer(answers)

    def analyze_skill_gap(self, career_id: str, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Compara a proficiência do usuário com as competências Júnior da carreira."""
        normalized = self.engine.normalize_answers(answers)
        return self.gap_analyzer.analyze(career_id, normalized["proficiencies"])

    def build_development_plan(self, career_id: str, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Gera a análise de lacunas e o roadmap personalizado para a carreira escolhida."""
        normalized = self.engine.normalize_answers(answers)
        gap = self.gap_analyzer.analyze(career_id, normalized["proficiencies"])
        insights = self.engine.insights(normalized)
        roadmap = self.roadmap_generator.generate(career_id, gap, normalized["profile"], insights)
        return {"skill_gap": gap, "roadmap": roadmap}
