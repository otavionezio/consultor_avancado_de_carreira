"""
Testes automatizados com PyTest para o Sistema Especialista de Carreiras em TI.
Valida o comportamento do motor de inferência, o disparo de regras e as 10 Personas de Teste.
"""
import pytest
from engine.advisor import CareerAdvisor
from engine.facts import UserProfile
from data.personas import TEST_PERSONAS
from data.career_tracks import CAREER_TRACKS


@pytest.fixture
def advisor():
    return CareerAdvisor()


class TestCareerAdvisor:

    def test_engine_initialization(self, advisor):
        """Verifica se o motor inicializa com 10 trilhas zeradas."""
        assert len(advisor.engine.scores) == 10
        for score in advisor.engine.scores.values():
            assert score == 0.0

    @pytest.mark.parametrize("persona_key,persona_data", list(TEST_PERSONAS.items()))
    def test_all_personas_recommendations(self, advisor, persona_key, persona_data):
        """
        Valida que cada persona de teste é diagnosticada exatamente
        na trilha de carreira esperada.
        """
        result = advisor.diagnose(persona_data["answers"])
        top_track = result["top_track"]
        expected_track = persona_data["expected_track"]

        assert top_track is not None, f"Diagnóstico retornou vazio para {persona_key}"
        assert top_track["track_id"] == expected_track, (
            f"Falha na persona {persona_data['name']}: "
            f"Esperado '{expected_track}', mas obteve '{top_track['track_id']}' "
            f"(Score: {top_track['score']})"
        )

    def test_disambiguation_ds_vs_de(self, advisor):
        """
        Testa a diferenciação precisa entre Cientista de Dados e Engenheiro de Dados.
        Ambos trabalham com dados e Python/SQL, mas o Cientista foca em matemática/modelagem
        e o Engenheiro foca em pipelines/infraestrutura.
        """
        ds_profile = {
            "math_affinity": "Alta",
            "work_preference": "Modelagem estatística, machine learning e inteligência artificial",
            "primary_tool": "Python",
            "value_delivery": "Modelos preditivos acurados e inteligência artificial para decisão",
            "daily_challenge": "Calibrar hiperparâmetros e testar hipóteses estatísticas",
            "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
            "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
        }
        res_ds = advisor.diagnose(ds_profile)
        assert res_ds["top_track"]["track_id"] == "data_science"

        de_profile = {
            "math_affinity": "Média",
            "work_preference": "Pipelines de dados, arquitetura ETL/ELT e Data Lakes",
            "primary_tool": "SQL / Ferramentas de Big Data (Spark, Airflow)",
            "value_delivery": "Fluxo de dados limpo, rápido e confiável para toda a empresa",
            "daily_challenge": "Escalar pipelines de processamento distribuído de terabytes",
            "communication_vs_code": "Foco predominante em código e arquitetura técnica profunda",
            "device_focus": "Serviços virtuais gerenciados e data centers na nuvem"
        }
        res_de = advisor.diagnose(de_profile)
        assert res_de["top_track"]["track_id"] == "data_engineering"

    def test_disambiguation_front_vs_mobile(self, advisor):
        """
        Testa desambiguação entre Front-end Web e Mobile.
        Ambos lidam com UI, mas um é focado em navegadores/CSS e outro em smartphones/dispositivos.
        """
        web_profile = {
            "math_affinity": "Baixa",
            "work_preference": "Interfaces visuais interativas, design e experiência do usuário",
            "primary_tool": "JavaScript / TypeScript",
            "value_delivery": "Telas encantadoras, responsivas e navegação agradável",
            "daily_challenge": "Ajustar CSS, microinterações e acessibilidade web",
            "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
            "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
        }
        res_web = advisor.diagnose(web_profile)
        assert res_web["top_track"]["track_id"] == "frontend"

        mobile_profile = {
            "math_affinity": "Baixa",
            "work_preference": "Aplicativos móveis nativos ou multiplataforma para smartphones",
            "primary_tool": "Swift / Kotlin / Flutter / React Native",
            "value_delivery": "Experiência móvel fluida e acessível na palma da mão",
            "daily_challenge": "Gerenciar ciclo de vida de apps e permissões de hardware móvel",
            "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
            "device_focus": "Dispositivos móveis, smartphones e tablets"
        }
        res_mob = advisor.diagnose(mobile_profile)
        assert res_mob["top_track"]["track_id"] == "mobile"

    def test_disambiguation_devops_vs_cloud(self, advisor):
        """
        Testa desambiguação entre DevOps/SRE e Cloud Architecture.
        """
        devops_profile = {
            "math_affinity": "Média",
            "work_preference": "Automação de CI/CD, esteiras de deploy, contêineres e alta disponibilidade",
            "primary_tool": "Docker / Kubernetes / Terraform / CI-CD",
            "value_delivery": "Deploys frequentes sem quedas e esteiras ágeis automatizadas",
            "daily_challenge": "Resolver gargalos em contêineres e orquestrar clusters K8s",
            "communication_vs_code": "Foco predominante em código e arquitetura técnica profunda",
            "device_focus": "Serviços virtuais gerenciados e data centers na nuvem"
        }
        res_devops = advisor.diagnose(devops_profile)
        assert res_devops["top_track"]["track_id"] == "devops"

        cloud_profile = {
            "math_affinity": "Média",
            "work_preference": "Arquitetura de sistemas em nuvem, migração e infraestrutura escalável",
            "primary_tool": "Nuvem AWS / Azure / GCP",
            "value_delivery": "Estrutura de nuvem escalável, resiliente e com custos otimizados",
            "daily_challenge": "Desenhar diagramas de nuvem e arquitetar alta disponibilidade",
            "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
            "device_focus": "Serviços virtuais gerenciados e data centers na nuvem"
        }
        res_cloud = advisor.diagnose(cloud_profile)
        assert res_cloud["top_track"]["track_id"] == "cloud"

    def test_justification_transparency(self, advisor):
        """Verifica se o relatório fornece transparência nas regras disparadas."""
        sample_profile = TEST_PERSONAS["ana_data_science"]["answers"]
        result = advisor.diagnose(sample_profile)

        assert len(result["top_track_rules"]) > 0
        assert len(result["all_rule_firings"]) >= 4
        assert result["total_rules_fired"] > 0
        for firing in result["top_track_rules"]:
            assert "rule_id" in firing
            assert "reason" in firing
            assert "points" in firing
            assert firing["points"] > 0
