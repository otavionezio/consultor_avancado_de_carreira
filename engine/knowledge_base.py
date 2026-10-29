"""
Carregamento e validação da Base de Conhecimento externa (regras_carreiras.json).
Toda regra de negócio do Sistema Especialista (perfis, pesos, regras SE-ENTÃO,
competências e recomendações) vive no arquivo JSON e é lida dinamicamente aqui.
"""
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

DEFAULT_KB_PATH = Path(__file__).resolve().parent.parent / "data" / "regras_carreiras.json"

REQUIRED_SECTIONS = (
    "parameters", "affinities", "competencies", "choice_questions", "rules", "careers"
)


class KnowledgeBaseError(ValueError):
    """Erro de estrutura ou de referência inválida na base de conhecimento."""


class KnowledgeBase:
    """
    Acesso somente leitura à base de conhecimento carregada do JSON.
    """

    def __init__(self, data: Dict[str, Any], source: str = "<memória>"):
        self.data = data
        self.source = source
        self.validate()

    # ------------------------------------------------------------------
    # Seções
    # ------------------------------------------------------------------
    @property
    def meta(self) -> Dict[str, Any]:
        return self.data.get("meta", {})

    @property
    def parameters(self) -> Dict[str, Any]:
        return self.data["parameters"]

    @property
    def affinities(self) -> Dict[str, Dict[str, Any]]:
        return self.data["affinities"]

    @property
    def competencies(self) -> Dict[str, Dict[str, Any]]:
        return self.data["competencies"]

    @property
    def competency_areas(self) -> List[str]:
        areas = self.data.get("competency_areas")
        if areas:
            return areas
        return sorted({c["area"] for c in self.competencies.values()})

    @property
    def choice_questions(self) -> List[Dict[str, Any]]:
        return self.data["choice_questions"]

    @property
    def rules(self) -> List[Dict[str, Any]]:
        return self.data["rules"]

    @property
    def careers(self) -> Dict[str, Dict[str, Any]]:
        return self.data["careers"]

    @property
    def legacy_mappings(self) -> Dict[str, Any]:
        return self.data.get("legacy_mappings", {})

    @property
    def personal_profile(self) -> Dict[str, Any]:
        return self.data.get("personal_profile", {})

    @property
    def scale(self) -> Dict[str, Any]:
        return self.parameters["scale"]

    # ------------------------------------------------------------------
    # Consultas auxiliares
    # ------------------------------------------------------------------
    def competency_name(self, competency_id: str) -> str:
        return self.competencies.get(competency_id, {}).get("name", competency_id)

    def affinity_label(self, affinity_id: str) -> str:
        return self.affinities.get(affinity_id, {}).get("label", affinity_id)

    def choice_question(self, question_id: str) -> Optional[Dict[str, Any]]:
        return next((q for q in self.choice_questions if q["id"] == question_id), None)

    def choice_option(self, question_id: str, value: Any) -> Optional[Dict[str, Any]]:
        question = self.choice_question(question_id)
        if not question:
            return None
        return next((o for o in question["options"] if o["value"] == value), None)

    def trait_label(self, trait_id: str) -> str:
        """Nome amigável de um traço derivado, obtido da regra que o infere."""
        key = f"traits.{trait_id}"
        for rule in self.rules:
            if key in rule.get("then", {}).get("infer", {}):
                return rule["name"].replace("Traço: ", "")
        return trait_id

    def fact_label(self, fact: str) -> str:
        """Descrição legível de um fato referenciado nas regras."""
        namespace, _, key = fact.partition(".")
        if namespace == "affinities":
            return f"Afinidade com {self.affinity_label(key)}"
        if namespace == "proficiencies":
            return f"Conhecimento em {self.competency_name(key)}"
        if namespace == "choices":
            question = self.choice_question(key)
            return question["label"] if question else key
        if namespace == "traits":
            return f"Traço '{self.trait_label(key)}'"
        if namespace == "profile":
            return f"Perfil: {key}"
        return fact

    # ------------------------------------------------------------------
    # Validação
    # ------------------------------------------------------------------
    def validate(self) -> None:
        missing = [s for s in REQUIRED_SECTIONS if s not in self.data]
        if missing:
            raise KnowledgeBaseError(f"Seções ausentes na base de conhecimento: {', '.join(missing)}")

        errors: List[str] = []
        competency_ids = set(self.competencies)
        career_ids = set(self.careers)

        def check_competency(ref: Union[str, List[str]], where: str):
            for cid in ([ref] if isinstance(ref, str) else ref):
                if cid not in competency_ids:
                    errors.append(f"Competência '{cid}' inexistente referenciada em {where}")

        for cid, comp in self.competencies.items():
            for prereq in comp.get("prerequisites", []):
                check_competency(prereq, f"pré-requisitos de '{cid}'")

        for aid, aff in self.affinities.items():
            for cid in aff.get("related_competencies", []):
                check_competency(cid, f"afinidade '{aid}'")

        for career_id, career in self.careers.items():
            for dim in career.get("affinity_profile", {}):
                if dim not in self.affinities:
                    errors.append(f"Afinidade '{dim}' inexistente no perfil de '{career_id}'")
            for entry in career.get("junior_competencies", []):
                check_competency(entry.get("any_of") or entry.get("id"), f"competências de '{career_id}'")
            for project in career.get("projects", []):
                for cid in project.get("competencies", []):
                    check_competency(cid, f"projeto '{project.get('title')}' de '{career_id}'")

        for question in self.choice_questions:
            for option in question["options"]:
                for target in option.get("weights", {}):
                    if target not in career_ids:
                        errors.append(f"Carreira '{target}' inexistente na pergunta '{question['id']}'")

        for rule in self.rules:
            for target in rule.get("then", {}).get("evidence", {}):
                if target not in career_ids:
                    errors.append(f"Carreira '{target}' inexistente na regra '{rule['id']}'")

        if errors:
            raise KnowledgeBaseError("Base de conhecimento inválida:\n- " + "\n- ".join(errors))


@lru_cache(maxsize=None)
def load_knowledge_base(path: Optional[str] = None) -> KnowledgeBase:
    """Carrega (com cache) a base de conhecimento a partir do arquivo JSON."""
    kb_path = Path(path) if path else DEFAULT_KB_PATH
    try:
        with open(kb_path, encoding="utf-8") as fp:
            data = json.load(fp)
    except FileNotFoundError as exc:
        raise KnowledgeBaseError(f"Arquivo da base de conhecimento não encontrado: {kb_path}") from exc
    except json.JSONDecodeError as exc:
        raise KnowledgeBaseError(f"JSON inválido em {kb_path}: {exc}") from exc
    return KnowledgeBase(data, source=str(kb_path))
