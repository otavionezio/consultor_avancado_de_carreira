"""
Definição dos Fatos (Facts) do Sistema Especialista utilizando Experta.
"""
from experta import Fact


class UserProfile(Fact):
    """
    Representa as características, afinidades e respostas fornecidas pelo usuário
    durante a entrevista interativa.
    Campos comuns:
      - math_affinity: 'Baixa', 'Média', 'Alta'
      - work_preference: atividade diária preferida
      - primary_tool: ferramenta ou linguagem com maior afinidade
      - value_delivery: tipo de entrega de valor preferida
      - daily_challenge: tipo de desafio diário que mais instiga
      - communication_vs_code: equilíbrio entre código técnico e pessoas/negócios
      - device_focus: foco de dispositivo ou infraestrutura
      - methodology_preference: preferência de processos (ex: ágil/produto vs técnico profundo)
    """
    pass


class IntermediateProfile(Fact):
    """
    Fato deduzido pelo motor em encadeamento para frente (forward chaining)
    para agrupar traços de perfil (ex: 'analitico', 'infraestrutura', 'visual', 'lideranca').
    """
    pass


class TrackScore(Fact):
    """
    Representa incremento ou ajuste de pontuação associado a uma trilha de carreira.
    Campos:
      - track: nome da trilha
      - points: pontuação adicionada
      - rule_id: identificador da regra disparada
      - rule_name: nome amigável da regra
      - reason: justificativa detalhada para transparência
    """
    pass


class TrackEvaluation(Fact):
    """
    Representa o estado de avaliação de uma trilha específica.
    """
    pass


class RuleFiring(Fact):
    """
    Registro histórico de cada regra disparada com seus motivos e impacto.
    """
    pass


class FinalRecommendation(Fact):
    """
    Diagnóstico final consolidado do Sistema Especialista.
    """
    pass
