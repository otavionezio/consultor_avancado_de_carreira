"""
Motor de Inferência do Sistema Especialista de Carreiras em TI.

Combina três mecanismos, todos parametrizados pela base de conhecimento JSON:
  1. Encadeamento para frente (forward chaining) sobre regras SE-ENTÃO, com
     lógica de três valores (verdadeiro / falso / desconhecido) para respostas ausentes.
  2. Pontuação ponderada entre o perfil do usuário e o perfil de cada carreira
     (afinidades, preferências de atuação e proficiência técnica).
  3. Tratamento de incerteza com Fatores de Certeza (modelo MYCIN) para combinar
     evidências favoráveis e desfavoráveis sem penalidades arbitrárias.

Os percentuais resultantes representam compatibilidade segundo as regras do
sistema, e não probabilidade de sucesso profissional.
"""
from typing import Any, Dict, List, Optional, Tuple

from engine.knowledge_base import KnowledgeBase

ANSWER_SECTIONS = ("profile", "affinities", "proficiencies", "choices")

_OPERATORS = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
    "in": lambda a, b: a in b,
}


def combine_certainty(cf_a: float, cf_b: float) -> float:
    """Combinação de dois fatores de certeza segundo o modelo MYCIN."""
    if cf_a >= 0 and cf_b >= 0:
        return cf_a + cf_b * (1 - cf_a)
    if cf_a < 0 and cf_b < 0:
        return cf_a + cf_b * (1 + cf_a)
    denominator = 1 - min(abs(cf_a), abs(cf_b))
    return (cf_a + cf_b) / denominator if denominator else 0.0


class InferenceEngine:
    """
    Motor de inferência guiado por dados: nenhuma regra de negócio está no código.
    """

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.params = kb.parameters
        scale = self.params["scale"]
        self.scale_min = scale["min"]
        self.scale_max = scale["max"]

    # ==================================================================
    # Normalização das respostas
    # ==================================================================
    def normalize_answers(self, answers: Optional[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Converte as respostas para o formato estruturado
        {profile, affinities, proficiencies, choices}, descartando valores
        ausentes ou inválidos. Aceita também o formato plano legado
        (math_affinity, work_preference, ...).
        """
        answers = answers or {}
        normalized: Dict[str, Dict[str, Any]] = {section: {} for section in ANSWER_SECTIONS}

        structured = any(isinstance(answers.get(s), dict) for s in ANSWER_SECTIONS)
        if structured:
            for section in ANSWER_SECTIONS:
                normalized[section].update(answers.get(section) or {})
        else:
            question_ids = {q["id"] for q in self.kb.choice_questions}
            for key, value in answers.items():
                if key in question_ids:
                    normalized["choices"][key] = value

        # Mapeamentos legados (ex.: math_affinity 'Alta' -> afinidade matemática 5)
        for legacy_key, mapping in self.kb.legacy_mappings.items():
            value = answers.get(legacy_key)
            if value in mapping["values"]:
                section, _, target = mapping["target"].partition(".")
                normalized[section].setdefault(target, mapping["values"][value])

        normalized["affinities"] = {
            k: int(v) for k, v in normalized["affinities"].items()
            if k in self.kb.affinities and self._valid_scale(v)
        }
        normalized["proficiencies"] = {
            k: int(v) for k, v in normalized["proficiencies"].items()
            if k in self.kb.competencies and self._valid_scale(v)
        }
        normalized["choices"] = {
            k: v for k, v in normalized["choices"].items()
            if self.kb.choice_option(k, v) is not None
        }
        normalized["profile"] = {k: v for k, v in normalized["profile"].items() if v not in (None, "")}
        return normalized

    def _valid_scale(self, value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool) \
            and self.scale_min <= value <= self.scale_max

    def _norm(self, value: float) -> float:
        return (value - self.scale_min) / (self.scale_max - self.scale_min)

    # ==================================================================
    # Base de fatos e encadeamento para frente
    # ==================================================================
    @staticmethod
    def build_facts(normalized: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        facts: Dict[str, Any] = {}
        for section, values in normalized.items():
            for key, value in values.items():
                facts[f"{section}.{key}"] = value
        return facts

    def evaluate(self, condition: Dict[str, Any], facts: Dict[str, Any]) -> Optional[bool]:
        """
        Avalia uma condição com lógica de três valores:
        True (satisfeita), False (não satisfeita) ou None (desconhecida por falta de resposta).
        """
        if "all" in condition:
            results = [self.evaluate(c, facts) for c in condition["all"]]
            if any(r is False for r in results):
                return False
            return None if any(r is None for r in results) else True
        if "any" in condition:
            results = [self.evaluate(c, facts) for c in condition["any"]]
            if any(r is True for r in results):
                return True
            return None if any(r is None for r in results) else False
        if "not" in condition:
            result = self.evaluate(condition["not"], facts)
            return None if result is None else not result

        value = facts.get(condition["fact"])
        if value is None:
            return None
        operator = _OPERATORS.get(condition.get("op", "=="))
        if operator is None:
            raise ValueError(f"Operador desconhecido: {condition.get('op')}")
        try:
            return bool(operator(value, condition["value"]))
        except TypeError:
            return False

    def describe_condition(self, condition: Dict[str, Any]) -> str:
        """Texto legível de uma condição, usado nas justificativas."""
        if "all" in condition:
            return " E ".join(self._wrap(c) for c in condition["all"])
        if "any" in condition:
            return " OU ".join(self._wrap(c) for c in condition["any"])
        if "not" in condition:
            return f"NÃO ({self.describe_condition(condition['not'])})"
        label = self.kb.fact_label(condition["fact"])
        value = condition["value"]
        if value is True and condition.get("op", "==") == "==":
            return label
        if isinstance(value, str):
            value = f"“{value}”"
        return f"{label} {condition.get('op', '==')} {value}"

    def _wrap(self, condition: Dict[str, Any]) -> str:
        text = self.describe_condition(condition)
        return f"({text})" if ("all" in condition or "any" in condition) else text

    def forward_chain(self, facts: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Executa o ciclo reconhecer-agir do encadeamento para frente até um ponto fixo.
        Em cada ciclo, o conjunto de conflito (regras satisfeitas pelos fatos atuais)
        é disparado; fatos inferidos habilitam novas regras no ciclo seguinte.
        Cada regra dispara no máximo uma vez (refração).
        """
        facts = dict(facts)
        fired: List[Dict[str, Any]] = []
        pending = list(self.kb.rules)
        cycle = 0
        while pending:
            conflict_set = [r for r in pending if self.evaluate(r["if"], facts) is True]
            if not conflict_set:
                break
            cycle += 1
            for rule in conflict_set:
                pending.remove(rule)
                consequence = rule.get("then", {})
                inferred = consequence.get("infer", {})
                facts.update(inferred)
                fired.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "category": rule.get("category", "evidencia"),
                    "reason": rule.get("explanation", ""),
                    "conditions": self.describe_condition(rule["if"]),
                    "evidence": dict(consequence.get("evidence", {})),
                    "inferred": dict(inferred),
                    "cycle": cycle,
                })
        return facts, fired

    # ==================================================================
    # Pontuação ponderada por componente
    # ==================================================================
    def _shrunk(self, total: float, weight: float, component: str) -> float:
        """Média ponderada com prior neutro (suaviza conclusões com pouca evidência)."""
        prior = self.params["prior"]
        strength = prior["strength"]
        return (total + strength * prior[component]) / (weight + strength)

    def _affinity_component(self, career: Dict[str, Any], affinities: Dict[str, int]) -> Dict[str, Any]:
        profile = career.get("affinity_profile", {})
        total_weight = sum(profile.values())
        answered_weight = total = 0.0
        for dim, weight in profile.items():
            if dim in affinities:
                answered_weight += weight
                total += weight * self._norm(affinities[dim])
        return {
            "score": self._shrunk(total, answered_weight, "affinity"),
            "coverage": answered_weight / total_weight if total_weight else 0.0,
        }

    def _preference_component(self, career_id: str, choices: Dict[str, Any]) -> Dict[str, Any]:
        questions = self.kb.choice_questions
        answered = 0
        total = 0.0
        for question in questions:
            option = self.kb.choice_option(question["id"], choices.get(question["id"]))
            if option is None or option.get("neutral"):
                continue
            answered += 1
            total += option.get("weights", {}).get(career_id, 0.0)
        return {
            "score": self._shrunk(total, answered, "preference"),
            "coverage": answered / len(questions) if questions else 0.0,
        }

    def resolve_proficiency(self, entry: Dict[str, Any], proficiencies: Dict[str, int]) -> Tuple[str, Optional[int]]:
        """
        Resolve uma competência exigida (simples ou com alternativas 'any_of')
        para a opção em que o usuário tem maior proficiência informada.
        """
        options = entry.get("any_of") or [entry["id"]]
        informed = [(proficiencies[c], c) for c in options if c in proficiencies]
        if not informed:
            return options[0], None
        best_level = max(level for level, _ in informed)
        best_id = next(c for level, c in informed if level == best_level)
        return best_id, best_level

    def _proficiency_component(self, career: Dict[str, Any], proficiencies: Dict[str, int]) -> Dict[str, Any]:
        entries = career.get("junior_competencies", [])
        total_weight = sum(e["weight"] for e in entries)
        answered_weight = total = 0.0
        for entry in entries:
            _, level = self.resolve_proficiency(entry, proficiencies)
            if level is None:
                continue
            required = max(entry["level"], self.scale_min + 1)
            ratio = (level - self.scale_min) / (required - self.scale_min)
            answered_weight += entry["weight"]
            total += entry["weight"] * min(1.0, max(0.0, ratio))
        return {
            "score": self._shrunk(total, answered_weight, "proficiency"),
            "coverage": answered_weight / total_weight if total_weight else 0.0,
        }

    # ==================================================================
    # Justificativas
    # ==================================================================
    def _justify(self, career_id: str, career: Dict[str, Any], normalized: Dict[str, Dict[str, Any]],
                 track_rules: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        cfg = self.params["justification"]
        favorable: List[str] = []
        unfavorable: List[str] = []
        affinities = normalized["affinities"]

        profile = sorted(career.get("affinity_profile", {}).items(), key=lambda kv: -kv[1])
        for dim, weight in profile:
            if dim not in affinities or weight < cfg["relevant_weight_min"]:
                continue
            value = affinities[dim]
            label = self.kb.affinity_label(dim)
            if value >= cfg["high_affinity_min"]:
                favorable.append(f"Alta afinidade com {label} ({value}/5), característica central desta carreira.")
            elif value <= cfg["low_affinity_max"]:
                unfavorable.append(f"Baixa afinidade com {label} ({value}/5), que é central nesta carreira.")

        for question in self.kb.choice_questions:
            option = self.kb.choice_option(question["id"], normalized["choices"].get(question["id"]))
            if option and option.get("weights", {}).get(career_id, 0.0) >= cfg["strong_preference_min"]:
                favorable.append(f"{question['label']}: “{option['value']}” é típica desta carreira.")

        for firing in track_rules:
            text = f"[{firing['rule_id']}] {firing['rule_name']}: {firing['reason']}"
            (favorable if firing["points"] > 0 else unfavorable).append(text)

        limit = cfg["max_items"]
        favorable = favorable[:limit]
        mastered = []
        for entry in career.get("junior_competencies", []):
            comp_id, level = self.resolve_proficiency(entry, normalized["proficiencies"])
            if level is not None and level >= entry["level"]:
                mastered.append(self.kb.competency_name(comp_id))
        if mastered:
            favorable.append("Você já atende ao nível Júnior em: " + ", ".join(mastered) + ".")
        return {"favorable": favorable, "unfavorable": unfavorable[:limit]}

    # ==================================================================
    # Análise de ambiguidade e insights
    # ==================================================================
    def _ambiguity(self, ranked: List[Dict[str, Any]], affinities: Dict[str, int]) -> Dict[str, Any]:
        cfg = self.params["ambiguity"]
        if len(ranked) < 2:
            return {"is_ambiguous": False, "is_undefined": False, "gap": None, "tied_tracks": [], "discriminating_affinities": [], "message": ""}

        first, second = ranked[0], ranked[1]
        gap = round(first["percentage"] - second["percentage"], 1)
        tied = [t["track_id"] for t in ranked[1:] if first["percentage"] - t["percentage"] < cfg["gap_threshold"]]
        is_ambiguous = bool(tied)
        is_undefined = first["percentage"] < cfg["low_compatibility_threshold"]

        profile_a = first["metadata"].get("affinity_profile", {})
        profile_b = second["metadata"].get("affinity_profile", {})
        differences = []
        for dim in set(profile_a) | set(profile_b):
            delta = profile_a.get(dim, 0) - profile_b.get(dim, 0)
            if delta:
                differences.append({
                    "affinity": dim,
                    "label": self.kb.affinity_label(dim),
                    "favors": first["track_id"] if delta > 0 else second["track_id"],
                    "favors_name": first["name"] if delta > 0 else second["name"],
                    "weight_difference": abs(delta),
                    "user_value": affinities.get(dim),
                })
        differences.sort(key=lambda d: (d["user_value"] is not None, -d["weight_difference"]))
        discriminating = differences[:cfg["max_discriminating_affinities"]]

        messages = []
        if is_ambiguous:
            names = [first["name"]] + [t["name"] for t in ranked if t["track_id"] in tied]
            messages.append(
                f"Perfil ambíguo: a diferença entre {', '.join(names)} é menor que "
                f"{cfg['gap_threshold']:.0f} pontos percentuais. As carreiras são igualmente compatíveis "
                "segundo as regras; explore ambas antes de decidir."
            )
        if is_undefined:
            messages.append(
                f"Nenhuma carreira atingiu {cfg['low_compatibility_threshold']:.0f}% de compatibilidade. "
                "Responder mais perguntas ou experimentar projetos introdutórios ajudará a definir o perfil."
            )
        return {
            "is_ambiguous": is_ambiguous,
            "is_undefined": is_undefined,
            "gap": gap,
            "tied_tracks": tied,
            "discriminating_affinities": discriminating,
            "message": " ".join(messages),
        }

    def insights(self, normalized: Dict[str, Dict[str, Any]]) -> List[Dict[str, str]]:
        """Contrasta afinidade (o que gosta) com proficiência (o que sabe)."""
        cfg = self.params["justification"]
        templates = self.params.get("insights", {})
        affinities, proficiencies = normalized["affinities"], normalized["proficiencies"]
        insights: List[Dict[str, str]] = []
        for aff_id, aff in self.kb.affinities.items():
            value = affinities.get(aff_id)
            if value is None:
                continue
            related = [c for c in aff.get("related_competencies", []) if c in proficiencies]
            if not related:
                continue
            avg = sum(proficiencies[c] for c in related) / len(related)
            if value >= cfg["high_affinity_min"] and avg <= cfg["low_affinity_max"] and "latent_talent" in templates:
                insights.append({"type": "latent_talent", "text": templates["latent_talent"].format(
                    affinity=aff["label"], value=value,
                    skills=", ".join(self.kb.competency_name(c) for c in related))})
            if value <= cfg["low_affinity_max"] and "skill_without_interest" in templates:
                for comp_id in related:
                    if proficiencies[comp_id] >= cfg["high_affinity_min"]:
                        insights.append({"type": "skill_without_interest", "text": templates["skill_without_interest"].format(
                            skill=self.kb.competency_name(comp_id), value=proficiencies[comp_id], affinity=aff["label"])})
        return insights

    # ==================================================================
    # Inferência completa
    # ==================================================================
    def infer(self, answers: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        normalized = self.normalize_answers(answers)
        facts, firings = self.forward_chain(self.build_facts(normalized))

        weights = self.params["component_weights"]
        alpha = self.params["certainty_factor_influence"]
        levels = self.params["confidence_levels"]

        ranked = []
        for career_id, career in self.kb.careers.items():
            components = {
                "affinity": self._affinity_component(career, normalized["affinities"]),
                "preference": self._preference_component(career_id, normalized["choices"]),
                "proficiency": self._proficiency_component(career, normalized["proficiencies"]),
            }
            # Cada componente pesa proporcionalmente à evidência disponível para a carreira:
            # respostas ausentes reduzem a confiança, mas não penalizam a pontuação.
            effective = {k: weights[k] * c["coverage"] for k, c in components.items()}
            evidence_weight = sum(effective.values())
            base = (sum(effective[k] * components[k]["score"] for k in components) / evidence_weight
                    if evidence_weight else 0.0)

            track_rules = []
            certainty = 0.0
            for firing in firings:
                cf = firing["evidence"].get(career_id)
                if cf is None:
                    continue
                certainty = combine_certainty(certainty, cf)
                track_rules.append({
                    "rule_id": firing["rule_id"],
                    "rule_name": firing["rule_name"],
                    "category": firing["category"],
                    "track": career_id,
                    "points": cf,
                    "reason": firing["reason"],
                    "conditions": firing["conditions"],
                })

            if certainty >= 0:
                final = base + (1 - base) * certainty * alpha
            else:
                final = base * (1 + certainty * alpha)
            final = min(1.0, max(0.0, final))

            confidence = evidence_weight / sum(weights.values())
            confidence_label = next(l["label"] for l in levels if confidence >= l["min"])

            ranked.append({
                "track_id": career_id,
                "name": career["name"],
                "icon": career.get("icon", "💼"),
                "summary": career.get("summary", ""),
                "score": round(final, 4),
                "percentage": round(final * 100, 1),
                "base_percentage": round(base * 100, 1),
                "certainty_factor": round(certainty, 3),
                "confidence": round(confidence, 3),
                "confidence_label": confidence_label,
                "components": {k: {"score": round(c["score"], 3), "coverage": round(c["coverage"], 3)}
                               for k, c in components.items()},
                "rules": track_rules,
                "justification": self._justify(career_id, career, normalized, track_rules),
                "metadata": {**career, "id": career_id},
            })

        ranked.sort(key=lambda t: (t["score"], t["confidence"]), reverse=True)
        top = ranked[0] if ranked else None

        return {
            "top_track": top,
            "runner_up": ranked[1] if len(ranked) > 1 else None,
            "top3": ranked[:3],
            "ranked_tracks": ranked,
            "ambiguity": self._ambiguity(ranked, normalized["affinities"]),
            "insights": self.insights(normalized),
            "all_rule_firings": firings,
            "top_track_rules": [r for r in (top["rules"] if top else []) if r["points"] > 0],
            "cross_rules_fired": [f for f in firings if f["category"] == "desambiguacao"],
            "derived_facts": {k: v for k, v in facts.items() if k.startswith("traits.")},
            "total_rules_fired": len(firings),
            "input_answers": normalized,
        }
