"""
Testes automatizados com PyTest para o Sistema Especialista de Carreiras em TI.
Valida a base de conhecimento, o motor de inferência, a análise de lacunas,
o roadmap personalizado e as 10 Personas de Teste.
"""
import copy

import pytest

from engine.advisor import CareerAdvisor
from engine.inference import combine_certainty
from engine.knowledge_base import KnowledgeBase, KnowledgeBaseError, load_knowledge_base
from data.personas import TEST_PERSONAS
from data.career_tracks import CAREER_TRACKS

EXPECTED_CAREERS = {
    "backend", "frontend", "data_science", "data_engineering", "cybersecurity",
    "devops", "cloud", "mobile", "qa", "pm",
}


@pytest.fixture
def advisor():
    return CareerAdvisor()


def legacy_answers(persona_key):
    """Converte uma persona para o formato plano legado (apenas escolhas + matemática)."""
    answers = TEST_PERSONAS[persona_key]["answers"]
    flat = dict(answers["choices"])
    math = answers["affinities"].get("math")
    flat["math_affinity"] = {1: "Baixa", 2: "Baixa", 3: "Média", 4: "Alta", 5: "Alta"}[math]
    return flat


class TestKnowledgeBase:

    def test_loads_ten_careers_from_json(self):
        kb = load_knowledge_base()
        assert set(kb.careers) == EXPECTED_CAREERS
        assert set(CAREER_TRACKS) == EXPECTED_CAREERS
        assert kb.source.endswith("regras_carreiras.json")

    def test_every_career_has_profile_competencies_and_recommendations(self):
        kb = load_knowledge_base()
        for career in kb.careers.values():
            assert career["affinity_profile"]
            assert career["junior_competencies"]
            assert career["projects"]
            assert career["certifications"]

    def test_invalid_reference_is_rejected(self):
        data = copy.deepcopy(load_knowledge_base().data)
        data["rules"][0]["then"] = {"evidence": {"carreira_inexistente": 0.5}}
        with pytest.raises(KnowledgeBaseError):
            KnowledgeBase(data)


class TestInferenceEngine:

    @pytest.mark.parametrize("persona_key,persona_data", list(TEST_PERSONAS.items()))
    def test_all_personas_recommendations(self, advisor, persona_key, persona_data):
        """Cada persona de teste é diagnosticada na trilha esperada."""
        result = advisor.diagnose(persona_data["answers"])
        top_track = result["top_track"]
        assert top_track["track_id"] == persona_data["expected_track"], (
            f"Falha na persona {persona_data['name']}: esperado '{persona_data['expected_track']}', "
            f"obtido '{top_track['track_id']}' ({[(t['track_id'], t['percentage']) for t in result['top3']]})"
        )

    @pytest.mark.parametrize("persona_key", list(TEST_PERSONAS))
    def test_legacy_flat_answers_still_supported(self, advisor, persona_key):
        """O formato de respostas da versão anterior continua produzindo o mesmo diagnóstico."""
        result = advisor.diagnose(legacy_answers(persona_key))
        assert result["top_track"]["track_id"] == TEST_PERSONAS[persona_key]["expected_track"]

    def test_ranking_has_ten_normalized_careers_and_top3(self, advisor):
        result = advisor.diagnose(TEST_PERSONAS["ana_data_science"]["answers"])
        assert len(result["ranked_tracks"]) == 10
        assert len(result["top3"]) == 3
        percentages = [t["percentage"] for t in result["ranked_tracks"]]
        assert percentages == sorted(percentages, reverse=True)
        assert all(0.0 <= p <= 100.0 for p in percentages)

    def test_disambiguation_ds_vs_de(self, advisor):
        ds = advisor.diagnose(TEST_PERSONAS["ana_data_science"]["answers"])
        de = advisor.diagnose(TEST_PERSONAS["eduardo_data_eng"]["answers"])
        assert ds["top_track"]["track_id"] == "data_science"
        assert de["top_track"]["track_id"] == "data_engineering"

    def test_missing_answers_do_not_penalize(self, advisor):
        """Remover respostas reduz a confiança, mas não zera nem inverte o diagnóstico."""
        full = TEST_PERSONAS["mariana_devops"]["answers"]
        partial = copy.deepcopy(full)
        partial["affinities"] = {k: v for k, v in full["affinities"].items() if k in ("automation", "infrastructure")}
        partial["proficiencies"] = {}
        res_full = advisor.diagnose(full)
        res_partial = advisor.diagnose(partial)
        assert res_partial["top_track"]["track_id"] == "devops"
        assert res_partial["top_track"]["confidence"] < res_full["top_track"]["confidence"]

    def test_empty_answers_are_handled(self, advisor):
        result = advisor.diagnose({})
        assert len(result["ranked_tracks"]) == 10
        assert result["total_rules_fired"] == 0
        assert all(t["confidence_label"] == "Baixa" for t in result["ranked_tracks"])

    def test_invalid_values_are_ignored(self, advisor):
        result = advisor.diagnose({"affinities": {"math": 9, "design": "x", "inexistente": 3},
                                   "choices": {"work_preference": "valor inválido"}})
        assert result["input_answers"]["affinities"] == {}
        assert result["input_answers"]["choices"] == {}

    def test_forward_chaining_derives_traits(self, advisor):
        answers = {"affinities": {"math": 5, "data_analysis": 5}}
        result = advisor.diagnose(answers)
        assert result["derived_facts"].get("traits.analytical") is True
        fired = {f["rule_id"]: f for f in result["all_rule_firings"]}
        assert "T01" in fired and "R01" in fired
        assert fired["R01"]["cycle"] > fired["T01"]["cycle"]

    def test_unfavorable_evidence_lowers_compatibility(self, advisor):
        base = {"affinities": {"math": 3, "data_analysis": 4}}
        low_math = {"affinities": {"math": 1, "data_analysis": 4}}
        ds_base = next(t for t in advisor.diagnose(base)["ranked_tracks"] if t["track_id"] == "data_science")
        ds_low = next(t for t in advisor.diagnose(low_math)["ranked_tracks"] if t["track_id"] == "data_science")
        assert ds_low["certainty_factor"] < 0
        assert ds_low["percentage"] < ds_base["percentage"]

    def test_ambiguous_profile_is_flagged(self, advisor):
        answers = {"affinities": {k: 3 for k in advisor.kb.affinities}}
        result = advisor.diagnose(answers)
        assert result["ambiguity"]["is_ambiguous"]
        assert result["ambiguity"]["message"]

    def test_justification_transparency(self, advisor):
        result = advisor.diagnose(TEST_PERSONAS["ana_data_science"]["answers"])
        top = result["top_track"]
        assert top["justification"]["favorable"]
        assert result["top_track_rules"]
        for firing in result["top_track_rules"]:
            assert firing["points"] > 0
            assert firing["reason"] and firing["conditions"]

    def test_affinity_vs_proficiency_insights(self, advisor):
        answers = {"affinities": {"design": 5, "math": 1},
                   "proficiencies": {"ux_ui": 1, "html_css": 1, "estatistica": 5}}
        types = {i["type"] for i in advisor.diagnose(answers)["insights"]}
        assert types == {"latent_talent", "skill_without_interest"}

    def test_certainty_factor_combination_is_bounded(self):
        assert combine_certainty(0.6, 0.5) == pytest.approx(0.8)
        assert combine_certainty(-0.6, -0.5) == pytest.approx(-0.8)
        assert -1.0 <= combine_certainty(0.9, -0.4) <= 1.0


class TestSkillGapAndRoadmap:

    def test_skill_gap_classification(self, advisor):
        answers = {"proficiencies": {"linux": 5, "docker": 2, "git": 3}}
        gap = advisor.analyze_skill_gap("devops", answers)
        assert "linux" in gap["dominated"]
        assert "git" in gap["dominated"]
        assert "docker" in gap["partial"]
        assert "kubernetes" in gap["missing"]
        assert 0 < gap["readiness_pct"] < 100

    def test_learning_order_respects_prerequisites(self, advisor):
        gap = advisor.analyze_skill_gap("data_science", {"proficiencies": {}})
        order = gap["learning_order"]
        items = {it["id"]: it for it in gap["items"]}
        for cid in order:
            for prereq in items[cid]["pending_prerequisites"]:
                assert order.index(prereq) < order.index(cid)

    def test_any_of_uses_best_known_alternative(self, advisor):
        gap = advisor.analyze_skill_gap("backend", {"proficiencies": {"javascript": 4, "python": 2}})
        ids = [it["id"] for it in gap["items"]]
        assert "javascript" in ids and "python" not in ids

    def test_roadmap_is_personalized(self, advisor):
        beginner = {"profile": {"weekly_hours": 5, "deadline_months": 3}, "proficiencies": {}}
        advanced = {"profile": {"weekly_hours": 20, "deadline_months": 6},
                    "proficiencies": {"linux": 4, "git": 4, "docker": 3, "bash": 3, "ci_cd": 3, "redes": 3}}
        plan_b = advisor.build_development_plan("devops", beginner)["roadmap"]
        plan_a = advisor.build_development_plan("devops", advanced)["roadmap"]
        assert plan_b["total_hours"] > plan_a["total_hours"]
        assert plan_b["level"]["id"] != plan_a["level"]["id"]
        assert not plan_b["fits_deadline"]
        steps_b = {s["competency_id"] for p in plan_b["phases"] for s in p["steps"]}
        steps_a = {s["competency_id"] for p in plan_a["phases"] for s in p["steps"]}
        assert "linux" in steps_b and "linux" not in steps_a

    def test_roadmap_contains_required_sections(self, advisor):
        plan = advisor.build_development_plan("frontend", TEST_PERSONAS["beatriz_frontend"]["answers"])
        roadmap = plan["roadmap"]
        assert roadmap["phases"]
        first_step = roadmap["phases"][0]["steps"][0]
        assert first_step["resources"] and first_step["exercises"]
        assert any(p["milestone_project"] for p in roadmap["phases"])
        assert roadmap["certifications"]
        assert roadmap["tips"]
        weeks = [s["start_week"] for p in roadmap["phases"] for s in p["steps"]]
        assert weeks == sorted(weeks)

    @pytest.mark.parametrize("persona_key", list(TEST_PERSONAS))
    def test_milestone_projects_only_use_studied_competencies(self, advisor, persona_key):
        answers = TEST_PERSONAS[persona_key]["answers"]
        for career_id in advisor.kb.careers:
            plan = advisor.build_development_plan(career_id, answers)
            pending = set(plan["skill_gap"]["learning_order"])
            studied = set()
            for phase in plan["roadmap"]["phases"]:
                studied |= {s["competency_id"] for s in phase["steps"]}
                project = phase["milestone_project"]
                if project:
                    title_to_comps = {p["title"]: p["competencies"] for p in advisor.kb.careers[career_id]["projects"]}
                    assert (set(title_to_comps[project["title"]]) & pending) <= studied

    def test_fully_qualified_user_gets_empty_plan(self, advisor):
        kb = advisor.kb
        profs = {cid: 5 for cid in kb.competencies}
        plan = advisor.build_development_plan("qa", {"proficiencies": profs})
        assert plan["skill_gap"]["readiness_pct"] == 100.0
        assert plan["roadmap"]["phases"] == []
        assert plan["roadmap"]["portfolio_projects"]
