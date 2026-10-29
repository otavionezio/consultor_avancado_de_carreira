"""
Gerador de Roadmap Personalizado.

Transforma o resultado da análise de lacunas em um plano de estudos sequencial,
distribuído em fases e semanas conforme o tempo disponível do usuário, com
exercícios, projetos de portfólio e certificações compatíveis com o seu nível.
"""
import math
from typing import Any, Dict, List, Optional

from engine.knowledge_base import KnowledgeBase

LEVEL_ORDER = ["iniciante", "intermediario", "avancado"]


class RoadmapGenerator:
    """Gera planos de desenvolvimento individualizados a partir da base de conhecimento."""

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.params = kb.parameters["roadmap"]

    # ------------------------------------------------------------------
    def _item_hours(self, item: Dict[str, Any]) -> int:
        base = self.kb.competencies[item["id"]].get("hours", 20)
        hours = base * item["gap_levels"] * self.params["hours_per_level"]
        return int(max(self.params["min_item_hours"], round(hours)))

    def _assign_phases(self, gap: Dict[str, Any]) -> Dict[str, int]:
        """A fase de uma competência nunca é anterior à fase dos seus pré-requisitos."""
        items = {it["id"]: it for it in gap["items"]}
        stages = sorted(p["stage"] for p in self.params["phases"])
        phase: Dict[str, int] = {}
        for cid in gap["learning_order"]:
            item = items[cid]
            stage = min(max(item["stage"], stages[0]), stages[-1])
            for pid in item["pending_prerequisites"]:
                stage = max(stage, phase.get(pid, stages[0]))
            phase[cid] = stage
        return phase

    def _select_projects(self, career: Dict[str, Any], level_index: int,
                         gap_ids: List[str]) -> List[Dict[str, Any]]:
        candidates = []
        for project in career.get("projects", []):
            p_index = LEVEL_ORDER.index(project.get("level", "iniciante"))
            if p_index > level_index + 1:
                continue
            overlap = [c for c in project.get("competencies", []) if c in gap_ids]
            candidates.append({
                **project,
                "practices": [self.kb.competency_name(c) for c in project.get("competencies", [])],
                "covers_gaps": [self.kb.competency_name(c) for c in overlap],
                "_overlap": set(overlap),
                "_fit": len(overlap) - 0.5 * abs(p_index - level_index),
            })
        candidates.sort(key=lambda p: -p["_fit"])
        return candidates

    def _certifications(self, career: Dict[str, Any], level_index: int) -> List[Dict[str, Any]]:
        result = []
        for cert in career.get("certifications", []):
            c_index = LEVEL_ORDER.index(cert.get("level", "iniciante"))
            if c_index <= level_index:
                timing = "Recomendada agora"
            elif c_index == level_index + 1:
                timing = "Recomendada ao concluir o plano"
            else:
                timing = "Objetivo de médio prazo"
            result.append({**cert, "timing": timing, "_order": c_index - level_index})
        result.sort(key=lambda c: (c["_order"] > 0, abs(c["_order"])))
        for cert in result:
            cert.pop("_order")
        return result

    # ------------------------------------------------------------------
    def generate(self, career_id: str, gap: Dict[str, Any],
                 profile: Optional[Dict[str, Any]] = None,
                 insights: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        profile = profile or {}
        career = self.kb.careers[career_id]
        weekly_hours = float(profile.get("weekly_hours") or self.params["default_weekly_hours"])
        deadline_months = float(profile.get("deadline_months") or self.params["default_deadline_months"])
        deadline_weeks = max(1, round(deadline_months * self.params["weeks_per_month"]))

        level = gap["level"]
        level_index = LEVEL_ORDER.index(level["id"]) if level["id"] in LEVEL_ORDER else 0
        items = {it["id"]: it for it in gap["items"]}
        phase_of = self._assign_phases(gap)
        projects = self._select_projects(career, level_index, gap["learning_order"])
        used_projects: set = set()
        gap_set = set(gap["learning_order"])
        scheduled: set = set()

        phases = []
        cumulative = 0.0
        for phase_cfg in sorted(self.params["phases"], key=lambda p: p["stage"]):
            phase_ids = [cid for cid in gap["learning_order"] if phase_of[cid] == phase_cfg["stage"]]
            if not phase_ids:
                continue
            steps = []
            for cid in phase_ids:
                item = items[cid]
                comp = self.kb.competencies[cid]
                hours = self._item_hours(item)
                start = cumulative
                cumulative += hours
                steps.append({
                    "competency_id": cid,
                    "name": item["label"],
                    "status": item["status"],
                    "current": item["current"],
                    "required": item["required"],
                    "priority": item["priority_label"],
                    "essential": item["essential"],
                    "external": item["external"],
                    "hours": hours,
                    "start_week": int(start // weekly_hours) + 1,
                    "end_week": max(int(start // weekly_hours) + 1, math.ceil(cumulative / weekly_hours)),
                    "prerequisites": [self.kb.competency_name(p) for p in item["prerequisites"]],
                    "resources": comp.get("resources", []),
                    "exercises": comp.get("exercises", []),
                })

            # Projeto marco: pratica a fase atual e só usa competências já estudadas até aqui
            milestone = None
            phase_set = set(phase_ids)
            scheduled |= phase_set
            for project in projects:
                not_ready = (project["_overlap"] & gap_set) - scheduled
                if project["title"] not in used_projects and project["_overlap"] & phase_set and not not_ready:
                    milestone = project
                    used_projects.add(project["title"])
                    break
            if milestone:
                start = cumulative
                cumulative += milestone.get("hours", 0)
                milestone = self._public_project(milestone)
                milestone["start_week"] = int(start // weekly_hours) + 1
                milestone["end_week"] = max(milestone["start_week"], math.ceil(cumulative / weekly_hours))

            phases.append({
                "stage": phase_cfg["stage"],
                "name": phase_cfg["name"],
                "description": phase_cfg["description"],
                "steps": steps,
                "milestone_project": milestone,
                "hours": sum(s["hours"] for s in steps) + (milestone.get("hours", 0) if milestone else 0),
            })

        total_hours = int(round(cumulative))
        total_weeks = math.ceil(total_hours / weekly_hours) if total_hours else 0
        fits_deadline = total_weeks <= deadline_weeks
        essential_hours = sum(s["hours"] for p in phases for s in p["steps"] if s["essential"] or s["external"])

        if not fits_deadline:
            for phase in phases:
                for step in phase["steps"]:
                    step["optional"] = not (step["essential"] or step["external"]) and phase["stage"] == phases[-1]["stage"]

        extra_projects = [self._public_project(p) for p in projects if p["title"] not in used_projects][:3]
        if not phases:
            # Todas as competências já atendidas: foco em portfólio avançado
            extra_projects = [self._public_project(p) for p in projects][:3]

        return {
            "career_id": career_id,
            "career_name": career["name"],
            "level": level,
            "readiness_pct": gap["readiness_pct"],
            "weekly_hours": weekly_hours,
            "deadline_months": deadline_months,
            "deadline_weeks": deadline_weeks,
            "total_hours": total_hours,
            "total_weeks": total_weeks,
            "estimated_months": round(total_weeks / self.params["weeks_per_month"], 1),
            "fits_deadline": fits_deadline,
            "essential_hours": essential_hours,
            "required_weekly_hours": math.ceil(total_hours / deadline_weeks) if total_hours else 0,
            "phases": phases,
            "portfolio_projects": extra_projects,
            "certifications": self._certifications(career, level_index),
            "tips": self._tips(profile, gap, phases, fits_deadline, deadline_weeks, total_hours,
                               essential_hours, weekly_hours, insights or []),
        }

    @staticmethod
    def _public_project(project: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in project.items() if not k.startswith("_")}

    def _tips(self, profile: Dict[str, Any], gap: Dict[str, Any], phases: List[Dict[str, Any]],
              fits_deadline: bool, deadline_weeks: int, total_hours: int, essential_hours: int,
              weekly_hours: float, insights: List[Dict[str, str]]) -> List[str]:
        personal = self.kb.personal_profile
        tips: List[str] = []

        objective = next((o for o in personal.get("objectives", []) if o["id"] == profile.get("objective")), None)
        if objective:
            tips.append(objective["tip"])
        experience_tip = personal.get("experience_tips", {}).get(profile.get("experience"))
        if experience_tip:
            tips.append(experience_tip)

        if not phases:
            tips.append("Você já atende a todas as competências Júnior mapeadas: concentre-se em projetos "
                        "avançados, certificações e candidaturas.")
        elif not fits_deadline:
            needed = math.ceil(total_hours / deadline_weeks)
            essential_weeks = math.ceil(essential_hours / weekly_hours) if essential_hours else 0
            tips.append(
                f"O plano completo exige cerca de {needed} h/semana para caber no seu prazo. "
                f"Com {weekly_hours:.0f} h/semana, priorize as competências essenciais "
                f"(≈ {essential_weeks} semanas) e trate os itens marcados como opcionais depois."
            )

        if gap["uninformed"]:
            tips.append(f"{len(gap['uninformed'])} competência(s) não tiveram nível informado e foram consideradas "
                        "como não estudadas; informe seu nível para um plano mais preciso.")
        if gap["dominated"]:
            tips.append(f"Você já domina {len(gap['dominated'])} competência(s) exigida(s): elas foram retiradas "
                        "do plano para concentrar seu tempo nas lacunas.")
        tips.extend(i["text"] for i in insights if i["type"] == "latent_talent")
        return tips


def generate_roadmap(kb: KnowledgeBase, career_id: str, gap: Dict[str, Any],
                     profile: Optional[Dict[str, Any]] = None,
                     insights: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """Atalho funcional para RoadmapGenerator(kb).generate(...)."""
    return RoadmapGenerator(kb).generate(career_id, gap, profile, insights)
