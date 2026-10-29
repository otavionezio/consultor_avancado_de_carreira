"""
Análise de Lacunas de Competências (Skill Gap Analysis).

Compara a proficiência atual do usuário com as competências exigidas para o
nível Júnior da carreira selecionada, classificando cada uma como dominada,
parcialmente desenvolvida ou ausente, e calcula prioridades e uma ordem de
aprendizagem que respeita os pré-requisitos definidos na base de conhecimento.
"""
import heapq
from typing import Any, Dict, List, Optional, Union

from engine.knowledge_base import KnowledgeBase

STATUS_DOMINATED = "dominada"
STATUS_PARTIAL = "parcial"
STATUS_MISSING = "ausente"


def _readiness_level(kb: KnowledgeBase, readiness: float) -> Dict[str, str]:
    for level in kb.parameters["roadmap"]["level_thresholds"]:
        if readiness >= level["min"]:
            return {"id": level["id"], "label": level["label"]}
    last = kb.parameters["roadmap"]["level_thresholds"][-1]
    return {"id": last["id"], "label": last["label"]}


class SkillGapAnalyzer:
    """Executa a análise de lacunas para uma carreira com base na base de conhecimento."""

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.params = kb.parameters["skill_gap"]
        self.scale_min = kb.scale["min"]

    # ------------------------------------------------------------------
    def _status(self, current: int, required: int) -> str:
        if current >= required:
            return STATUS_DOMINATED
        ratio = (current - self.scale_min) / max(1, required - self.scale_min)
        if current > self.scale_min and ratio >= self.params["partial_min_ratio"]:
            return STATUS_PARTIAL
        return STATUS_MISSING

    def _make_item(self, comp_id: str, label: str, required: int, weight: float,
                   current: Optional[int], external: bool = False) -> Dict[str, Any]:
        comp = self.kb.competencies[comp_id]
        effective = current if current is not None else self.scale_min
        ratio = (effective - self.scale_min) / max(1, required - self.scale_min)
        return {
            "id": comp_id,
            "name": comp["name"],
            "label": label,
            "area": comp.get("area", ""),
            "stage": comp.get("stage", 2),
            "required": required,
            "current": current,
            "informed": current is not None,
            "status": self._status(effective, required),
            "gap_levels": max(0, required - effective),
            "progress": round(min(1.0, max(0.0, ratio)), 3),
            "weight": weight,
            "essential": weight >= self.params["essential_weight"],
            "external": external,
            "prerequisites": [],
            "pending_prerequisites": [],
            "dependents": 0,
            "priority": 0.0,
            "priority_label": "",
        }

    def _resolve_prerequisite(self, prereq: Union[str, List[str]], items: Dict[str, Any],
                              proficiencies: Dict[str, int]) -> str:
        """Um pré-requisito pode ser uma lista de alternativas; escolhe a mais adequada."""
        if isinstance(prereq, str):
            return prereq
        for option in prereq:
            if option in items:
                return option
        informed = [o for o in prereq if o in proficiencies]
        if informed:
            return max(informed, key=lambda o: proficiencies[o])
        return prereq[0]

    # ------------------------------------------------------------------
    def analyze(self, career_id: str, proficiencies: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        if career_id not in self.kb.careers:
            raise KeyError(f"Carreira desconhecida: {career_id}")
        proficiencies = proficiencies or {}
        career = self.kb.careers[career_id]

        items: Dict[str, Dict[str, Any]] = {}
        for entry in career.get("junior_competencies", []):
            options = entry.get("any_of") or [entry["id"]]
            informed = [c for c in options if c in proficiencies]
            comp_id = max(informed, key=lambda c: proficiencies[c]) if informed else options[0]
            name = self.kb.competency_name(comp_id)
            label = f"{entry['label']}: {name}" if entry.get("any_of") else name
            items[comp_id] = self._make_item(comp_id, label, entry["level"], entry["weight"],
                                             proficiencies.get(comp_id))

        # Inclui pré-requisitos externos à carreira que ainda não foram atendidos
        external_level = self.params["external_prerequisite_level"]
        external_weight = self.params["external_prerequisite_weight"]
        queue = list(items)
        while queue:
            comp_id = queue.pop(0)
            resolved = []
            for prereq in self.kb.competencies[comp_id].get("prerequisites", []):
                pid = self._resolve_prerequisite(prereq, items, proficiencies)
                resolved.append(pid)
                if pid in items:
                    continue
                current = proficiencies.get(pid)
                if items[comp_id]["status"] != STATUS_DOMINATED and (current or self.scale_min) < external_level:
                    items[pid] = self._make_item(pid, self.kb.competency_name(pid), external_level,
                                                 external_weight, current, external=True)
                    queue.append(pid)
            items[comp_id]["prerequisites"] = [p for p in resolved if p in items]

        for item in items.values():
            item["pending_prerequisites"] = [
                p for p in item["prerequisites"] if items[p]["status"] != STATUS_DOMINATED
            ]

        gaps = {cid: it for cid, it in items.items() if it["status"] != STATUS_DOMINATED}
        self._compute_priorities(gaps)
        order = self._learning_order(gaps)

        career_items = [it for it in items.values() if not it["external"]]
        total_weight = sum(it["weight"] for it in career_items)
        readiness = (sum(it["weight"] * it["progress"] for it in career_items) / total_weight
                     if total_weight else 0.0)

        ordered = [items[cid] for cid in order] + \
                  [it for it in items.values() if it["status"] == STATUS_DOMINATED]

        def ids(status: str) -> List[str]:
            return [it["id"] for it in ordered if it["status"] == status]

        return {
            "career_id": career_id,
            "career_name": career["name"],
            "items": ordered,
            "dominated": ids(STATUS_DOMINATED),
            "partial": ids(STATUS_PARTIAL),
            "missing": ids(STATUS_MISSING),
            "uninformed": [it["id"] for it in ordered if not it["informed"]],
            "learning_order": order,
            "readiness": round(readiness, 3),
            "readiness_pct": round(readiness * 100, 1),
            "level": _readiness_level(self.kb, readiness),
        }

    # ------------------------------------------------------------------
    def _compute_priorities(self, gaps: Dict[str, Dict[str, Any]]) -> None:
        """Prioridade = peso x tamanho da lacuna + bônus por desbloquear outras competências."""
        dependents: Dict[str, set] = {cid: set() for cid in gaps}

        def collect(cid: str, origin: str, seen: set):
            for pid in gaps[cid]["prerequisites"]:
                if pid in gaps and pid not in seen:
                    seen.add(pid)
                    dependents[pid].add(origin)
                    collect(pid, origin, seen)

        for cid in gaps:
            collect(cid, cid, set())

        thresholds = self.params["priority_thresholds"]
        for cid, item in gaps.items():
            gap_ratio = item["gap_levels"] / max(1, item["required"] - self.scale_min)
            item["dependents"] = len(dependents[cid])
            item["priority"] = round(
                item["weight"] * gap_ratio
                + self.params["dependent_bonus"] * item["dependents"]
                + (self.params["essential_bonus"] if item["essential"] else 0.0), 2)
            if item["priority"] >= thresholds["high"]:
                item["priority_label"] = "Alta"
            elif item["priority"] >= thresholds["medium"]:
                item["priority_label"] = "Média"
            else:
                item["priority_label"] = "Baixa"

    @staticmethod
    def _learning_order(gaps: Dict[str, Dict[str, Any]]) -> List[str]:
        """Ordenação topológica (Kahn) priorizando fundamentos e maior prioridade."""
        indegree = {cid: 0 for cid in gaps}
        children: Dict[str, List[str]] = {cid: [] for cid in gaps}
        for cid, item in gaps.items():
            for pid in item["pending_prerequisites"]:
                if pid in gaps:
                    indegree[cid] += 1
                    children[pid].append(cid)

        def key(cid: str):
            return (gaps[cid]["stage"], -gaps[cid]["priority"], cid)

        heap = [key(cid) for cid, deg in indegree.items() if deg == 0]
        heapq.heapify(heap)
        order: List[str] = []
        while heap:
            _, _, cid = heapq.heappop(heap)
            order.append(cid)
            for child in children[cid]:
                indegree[child] -= 1
                if indegree[child] == 0:
                    heapq.heappush(heap, key(child))

        # Proteção contra ciclos acidentais na base: adiciona o restante por prioridade
        remaining = sorted((cid for cid in gaps if cid not in order), key=key)
        return order + remaining


def analyze_skill_gap(kb: KnowledgeBase, career_id: str,
                      proficiencies: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
    """Atalho funcional para SkillGapAnalyzer(kb).analyze(...)."""
    return SkillGapAnalyzer(kb).analyze(career_id, proficiencies)
