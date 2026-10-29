"""
Módulo do Motor Especialista de Carreiras em TI.
Motor de inferência guiado pela base de conhecimento externa (data/regras_carreiras.json).
"""
from engine.knowledge_base import KnowledgeBase, KnowledgeBaseError, load_knowledge_base
from engine.inference import InferenceEngine, combine_certainty
from engine.skill_gap import SkillGapAnalyzer, analyze_skill_gap
from engine.roadmap import RoadmapGenerator, generate_roadmap
from engine.advisor import CareerAdvisor

__all__ = [
    'KnowledgeBase',
    'KnowledgeBaseError',
    'load_knowledge_base',
    'InferenceEngine',
    'combine_certainty',
    'SkillGapAnalyzer',
    'analyze_skill_gap',
    'RoadmapGenerator',
    'generate_roadmap',
    'CareerAdvisor'
]
