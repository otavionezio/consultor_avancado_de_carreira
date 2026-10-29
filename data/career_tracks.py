"""
Catálogo das 10 Trilhas de Carreira em TI do Sistema Especialista.
Os dados (descrição, competências, tecnologias, salários, projetos e certificações)
são carregados da base de conhecimento externa data/regras_carreiras.json.
"""
from engine.knowledge_base import load_knowledge_base

CAREER_TRACKS = {
    career_id: {**career, "id": career_id}
    for career_id, career in load_knowledge_base().careers.items()
}
