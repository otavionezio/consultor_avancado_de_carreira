"""
Base de Conhecimento e Motor de Regras do Sistema Especialista em Carreiras de TI.
Implementado com a biblioteca Experta utilizando encadeamento para frente (forward chaining).
Contém mais de 50 regras lógicas (diretas, dimensionais e de desambiguação cruzada).
"""
import collections
import collections.abc

# Assegura patch de compatibilidade Python 3.10+
for attr in ['Mapping', 'MutableMapping', 'Sequence', 'MutableSequence', 'Iterable', 'Callable', 'Container', 'Hashable', 'Sized']:
    if not hasattr(collections, attr) and hasattr(collections.abc, attr):
        setattr(collections, attr, getattr(collections.abc, attr))

from experta import KnowledgeEngine, Rule, Fact, MATCH, AS, AND, OR, NOT, L
from engine.facts import UserProfile, IntermediateProfile, FinalRecommendation


class CareerKnowledgeEngine(KnowledgeEngine):
    """
    Motor de Inferência baseado em regras Experta para recomendação de carreiras em TI.
    Avalia fatos do usuário, calcula pontuação ponderada para cada uma das 10 trilhas
    e registra detalhadamente todas as regras disparadas e justificativas.
    """

    def __init__(self):
        super().__init__()
        self._init_state()

    def _init_state(self):
        """Reinicia o acumulador de pontuações e histórico de disparos."""
        self.scores = {
            "backend": 0.0,
            "frontend": 0.0,
            "data_science": 0.0,
            "data_engineering": 0.0,
            "cybersecurity": 0.0,
            "devops": 0.0,
            "cloud": 0.0,
            "mobile": 0.0,
            "qa": 0.0,
            "pm": 0.0,
        }
        self.rule_firings = []

    def reset(self):
        """Sobrescreve o reset do Experta para limpar o estado interno."""
        self._init_state()
        super().reset()

    def _add_score(self, track: str, points: float, rule_id: str, rule_name: str, reason: str):
        """Registra a pontuação e a justificativa da regra disparada."""
        if track in self.scores:
            self.scores[track] += points
        self.rule_firings.append({
            "rule_id": rule_id,
            "rule_name": rule_name,
            "track": track,
            "points": points,
            "reason": reason
        })

    # =========================================================================
    # GRUPO 1: REGRAS DIRETAS DE ATUAÇÃO DIÁRIA (R01 - R10)
    # =========================================================================

    @Rule(UserProfile(work_preference='Lógica de negócios, APIs e bancos de dados'))
    def r01_work_backend(self):
        self._add_score(
            'backend', 35.0, 'R01', 'Atuação em Lógica de Servidor & APIs',
            'Preferência central em criar regras de negócio, modelar bancos e construir APIs robustas.'
        )

    @Rule(UserProfile(work_preference='Interfaces visuais interativas, design e experiência do usuário'))
    def r02_work_frontend(self):
        self._add_score(
            'frontend', 35.0, 'R02', 'Atuação em Interfaces & UI/UX',
            'Foco central na criação de layouts responsivos, microinterações e experiência do usuário final.'
        )

    @Rule(UserProfile(work_preference='Modelagem estatística, machine learning e inteligência artificial'))
    def r03_work_data_science(self):
        self._add_score(
            'data_science', 35.0, 'R03', 'Atuação em Modelagem Preditiva & IA',
            'Forte direcionamento para aplicação de estatística, algoritmos de machine learning e inteligência artificial.'
        )

    @Rule(UserProfile(work_preference='Pipelines de dados, arquitetura ETL/ELT e Data Lakes'))
    def r04_work_data_engineering(self):
        self._add_score(
            'data_engineering', 35.0, 'R04', 'Atuação em Engenharia de Pipelines & Data Lakes',
            'Preferência fundamental por arquitetar dutos de dados escaláveis, ETL/ELT e repositórios de Big Data.'
        )

    @Rule(UserProfile(work_preference='Defesa cibernética, análise de vulnerabilidades e testes de invasão'))
    def r05_work_cybersecurity(self):
        self._add_score(
            'cybersecurity', 35.0, 'R05', 'Atuação em Cibersegurança & Pentest',
            'Direcionamento explícito para auditoria de segurança, detecção de vulnerabilidades e testes de invasão.'
        )

    @Rule(UserProfile(work_preference='Automação de CI/CD, esteiras de deploy, contêineres e alta disponibilidade'))
    def r06_work_devops(self):
        self._add_score(
            'devops', 35.0, 'R06', 'Atuação em Automação DevOps & SRE',
            'Foco no ciclo de integração e entrega contínua (CI/CD), orquestração de contêineres e alta confiabilidade.'
        )

    @Rule(UserProfile(work_preference='Arquitetura de sistemas em nuvem, migração e infraestrutura escalável'))
    def r07_work_cloud(self):
        self._add_score(
            'cloud', 35.0, 'R07', 'Atuação em Arquitetura Cloud Escalável',
            'Preferência por desenhar topologias distribuídas em nuvem (AWS/Azure/GCP) e coordenar migrações.'
        )

    @Rule(UserProfile(work_preference='Aplicativos móveis nativos ou multiplataforma para smartphones'))
    def r08_work_mobile(self):
        self._add_score(
            'mobile', 35.0, 'R08', 'Atuação em Aplicativos Mobile',
            'Interesse prioritário no ecossistema de smartphones e tablets (Android/iOS).'
        )

    @Rule(UserProfile(work_preference='Testes automatizados, caça a bugs e garantia de qualidade'))
    def r09_work_qa(self):
        self._add_score(
            'qa', 35.0, 'R09', 'Atuação em Engenharia de Qualidade (QA)',
            'Preferência dedicada a prevenir defeitos, caçar bugs e construir baterias de testes automatizados.'
        )

    @Rule(UserProfile(work_preference='Gestão de produto, estratégia de negócio, priorização e comunicação'))
    def r10_work_pm(self):
        self._add_score(
            'pm', 35.0, 'R10', 'Atuação em Gestão de Produtos (PM)',
            'Foco em conectar negócios, clientes e engenharia através de priorização estratégica e liderança por influência.'
        )

    # =========================================================================
    # GRUPO 2: REGRAS DE LINGUAGEM E FERRAMENTAS PRINCIPAIS (R11 - R20)
    # =========================================================================

    @Rule(UserProfile(primary_tool='Java / C# / Go'))
    def r11_tool_backend(self):
        self._add_score(
            'backend', 25.0, 'R11', 'Domínio de Linguagens de Alto Desempenho para Servidor',
            'Java, C# e Go são referências na construção de microsserviços corporativos e APIs escaláveis.'
        )
        self._add_score('cloud', 5.0, 'R11_B', 'Afinidade Secundária Cloud', 'Linguagens amplamente utilizadas em microsserviços na nuvem.')

    @Rule(UserProfile(primary_tool='JavaScript / TypeScript'))
    def r12_tool_javascript_ts(self):
        self._add_score(
            'frontend', 22.0, 'R12', 'Afinidade com Ecossistema Web Reativo (JS/TS)',
            'JavaScript e TypeScript são os pilares mandatórios para o desenvolvimento front-end moderno.'
        )
        self._add_score('mobile', 8.0, 'R12_MOB', 'Sinergia Mobile Híbrido', 'TypeScript é a base do React Native para apps móveis.')
        self._add_score('backend', 6.0, 'R12_BACK', 'Sinergia com Node.js', 'Permite construção de APIs com Node.js e NestJS.')

    @Rule(UserProfile(primary_tool='Python'))
    def r13_tool_python(self):
        self._add_score(
            'data_science', 18.0, 'R13_DS', 'Linguagem Padrão de IA e Ciência de Dados',
            'Python é o ecossistema líder absoluto em bibliotecas de Machine Learning, Deep Learning e estatística.'
        )
        self._add_score(
            'backend', 10.0, 'R13_BACK', 'Sinergia com Back-end Moderno',
            'Python destaca-se em APIs velozes com FastAPI e Django.'
        )
        self._add_score(
            'data_engineering', 10.0, 'R13_DE', 'Sinergia com Engenharia de Dados',
            'Python é amplamente utilizado em scripts ETL e PySpark.'
        )

    @Rule(UserProfile(primary_tool='SQL / Ferramentas de Big Data (Spark, Airflow)'))
    def r14_tool_big_data_sql(self):
        self._add_score(
            'data_engineering', 25.0, 'R14_DE', 'Domínio de SQL Avançado e Big Data',
            'SQL com ferramentas como Spark e Airflow compõe o núcleo tecnológico de Engenharia de Dados.'
        )
        self._add_score('data_science', 8.0, 'R14_DS', 'Sinergia com Consultas Analíticas', 'Cientistas de dados usam SQL para extração.')
        self._add_score('backend', 6.0, 'R14_BACK', 'Sinergia com Bancos Relacionais', 'Consultas relacionais essenciais no back-end.')

    @Rule(UserProfile(primary_tool='Linux / Bash / Ferramentas de Redes e Segurança'))
    def r15_tool_security_linux(self):
        self._add_score(
            'cybersecurity', 25.0, 'R15_SEC', 'Especialização em Linux Hardening & Redes',
            'Profundo conhecimento de Linux, scripts Bash e tráfego de redes é mandatório em Cibersegurança.'
        )
        self._add_score('devops', 10.0, 'R15_DEV', 'Sinergia com Infraestrutura DevOps', 'Linux e Bash são cruciais para esteiras e servidores.')

    @Rule(UserProfile(primary_tool='Docker / Kubernetes / Terraform / CI-CD'))
    def r16_tool_devops_containers(self):
        self._add_score(
            'devops', 25.0, 'R16_DEV', 'Domínio de Contêineres e Infraestrutura como Código',
            'Docker, Kubernetes e Terraform são os três pilares que definem a engenharia de DevOps contemporânea.'
        )
        self._add_score('cloud', 12.0, 'R16_CLOUD', 'Sinergia com Nuvem', 'Contêineres e Terraform são base do provisionamento em Cloud.')

    @Rule(UserProfile(primary_tool='Nuvem AWS / Azure / GCP'))
    def r17_tool_cloud_providers(self):
        self._add_score(
            'cloud', 25.0, 'R17_CLOUD', 'Especialização em Provedores Globais de Nuvem',
            'Conhecimento nativo das arquiteturas de hyperscalers (AWS, Azure, GCP).'
        )
        self._add_score('devops', 10.0, 'R17_DEV', 'Sinergia com Ambientes em Nuvem', 'DevOps utiliza intensamente provedores de nuvem.')

    @Rule(UserProfile(primary_tool='Swift / Kotlin / Flutter / React Native'))
    def r18_tool_mobile_frameworks(self):
        self._add_score(
            'mobile', 25.0, 'R18_MOB', 'Domínio de Stacks Nativas e Multiplataforma Mobile',
            'Fluência com Flutter, Swift, Kotlin ou React Native indica vocação direta para apps móveis.'
        )

    @Rule(UserProfile(primary_tool='Ferramentas de Teste (Cypress, Selenium, PyTest, JUnit)'))
    def r19_tool_qa_testing(self):
        self._add_score(
            'qa', 25.0, 'R19_QA', 'Domínio de Frameworks de Automação de Testes',
            'Uso ativo de Cypress, Playwright, PyTest ou JUnit é a assinatura técnica de Engenheiros de QA.'
        )

    @Rule(UserProfile(primary_tool='Ferramentas de Gestão e Ágil (Jira, Trello, Miro, Notion)'))
    def r20_tool_pm_agile(self):
        self._add_score(
            'pm', 25.0, 'R20_PM', 'Domínio de Ferramentas de Gestão, Produto e Facilitação',
            'Fluência com Jira, Miro e plataformas de Discovery compõe o arsenal diário de Product Managers.'
        )

    # =========================================================================
    # GRUPO 3: REGRAS DE ENTREGA DE VALOR PREFERIDA (R21 - R30)
    # =========================================================================

    @Rule(UserProfile(value_delivery='APIs robustas, regras de negócio e estabilidade de servidor'))
    def r21_val_backend(self):
        self._add_score(
            'backend', 18.0, 'R21', 'Entrega de Confiabilidade Estrutural e Lógica',
            'Prioriza que a fundação lógica do sistema opere sem falhas de negócio ou corrupção de dados.'
        )

    @Rule(UserProfile(value_delivery='Telas encantadoras, responsivas e navegação agradável'))
    def r22_val_frontend(self):
        self._add_score(
            'frontend', 18.0, 'R22', 'Entrega de Encantamento Visual e Experiência',
            'Valoriza o impacto perceptível direto na retenção e satisfação dos usuários através do design.'
        )

    @Rule(UserProfile(value_delivery='Modelos preditivos acurados e inteligência artificial para decisão'))
    def r23_val_data_science(self):
        self._add_score(
            'data_science', 18.0, 'R23', 'Entrega de Previsibilidade e Inteligência de Negócio',
            'Busca capacitar a organização com modelos que antecipam comportamentos futuros e otimizam decisões.'
        )

    @Rule(UserProfile(value_delivery='Fluxo de dados limpo, rápido e confiável para toda a empresa'))
    def r24_val_data_eng(self):
        self._add_score(
            'data_engineering', 18.0, 'R24', 'Entrega de Infraestrutura e Disponibilidade de Dados',
            'Almeja democratizar dados confiáveis e em tempo hábil para cientistas, analistas e aplicações.'
        )

    @Rule(UserProfile(value_delivery='Proteção contra invasões, dados seguros e sistemas blindados'))
    def r25_val_security(self):
        self._add_score(
            'cybersecurity', 18.0, 'R25', 'Entrega de Blindagem e Preservação de Ativos',
            'Reconhece o valor inestimável de evitar vazamentos, manter sigilo e repelir ciberataques.'
        )

    @Rule(UserProfile(value_delivery='Deploys frequentes sem quedas e esteiras ágeis automatizadas'))
    def r26_val_devops(self):
        self._add_score(
            'devops', 18.0, 'R26', 'Entrega de Eficiência Operacional e Zero Downtime',
            'Foca em reduzir o lead time de lançamento de código mantendo estabilidade ininterrupta.'
        )

    @Rule(UserProfile(value_delivery='Estrutura de nuvem escalável, resiliente e com custos otimizados'))
    def r27_val_cloud(self):
        self._add_score(
            'cloud', 18.0, 'R27', 'Entrega de Escalabilidade Global e FinOps',
            'Prioriza a elasticidade arquitetural, tolerância a desastres e governança financeira de nuvem.'
        )

    @Rule(UserProfile(value_delivery='Experiência móvel fluida e acessível na palma da mão'))
    def r28_val_mobile(self):
        self._add_score(
            'mobile', 18.0, 'R28', 'Entrega de Portabilidade e Conveniência Móvel',
            'Prioriza colocar a solução tecnológica diretamente na mão do cliente onde quer que ele esteja.'
        )

    @Rule(UserProfile(value_delivery='Software sem bugs, estável e que cumpre todos os critérios'))
    def r29_val_qa(self):
        self._add_score(
            'qa', 18.0, 'R29', 'Entrega de Confiança Absoluta e Zero Defeitos',
            'Compromisso com o mais alto padrão de conformidade e integridade da experiência do produto.'
        )

    @Rule(UserProfile(value_delivery='Produtos que resolvem dores de usuários e geram receita'))
    def r30_val_pm(self):
        self._add_score(
            'pm', 18.0, 'R30', 'Entrega de Retorno Financeiro e Resolução de Dores Reais',
            'Prioriza a viabilidade de mercado do produto e o encaixe perfeito com as dores dos clientes.'
        )

    # =========================================================================
    # GRUPO 4: REGRAS DE DESAFIOS DIÁRIOS E RESOLUÇÃO DE PROBLEMAS (R31 - R40)
    # =========================================================================

    @Rule(UserProfile(daily_challenge='Otimizar algoritmos e consultas SQL complexas'))
    def r31_challenge_backend(self):
        self._add_score(
            'backend', 14.0, 'R31', 'Gosto por Algoritmos e Otimização de Consultas',
            'Prazer em reduzir milissegundos de latência em APIs e desvendar planos de execução de banco.'
        )
        self._add_score('data_engineering', 6.0, 'R31_DE', 'Sinergia de Otimização SQL', 'Otimização de consultas é vital em Big Data.')

    @Rule(UserProfile(daily_challenge='Ajustar CSS, microinterações e acessibilidade web'))
    def r32_challenge_frontend(self):
        self._add_score(
            'frontend', 16.0, 'R32', 'Atenção aos Detalhes de Interface e Acessibilidade',
            'Prazer em refinar o posicionamento pixel-perfect, estados de hover e conformidade WCAG.'
        )

    @Rule(UserProfile(daily_challenge='Calibrar hiperparâmetros e testar hipóteses estatísticas'))
    def r33_challenge_data_science(self):
        self._add_score(
            'data_science', 16.0, 'R33', 'Rigor em Experimentação e Ajuste Fino de Modelos',
            'Prazer pelo método científico: formular hipóteses, rodar A/B tests e elevar o F1-Score.'
        )

    @Rule(UserProfile(daily_challenge='Escalar pipelines de processamento distribuído de terabytes'))
    def r34_challenge_data_engineering(self):
        self._add_score(
            'data_engineering', 16.0, 'R34', 'Paixão por Desafios de Alta Vazão e Big Data',
            'Prazer em gerenciar particionamento distribuído, shuffle e vazão contínua em larga escala.'
        )

    @Rule(UserProfile(daily_challenge='Simular ataques, encontrar brechas zero-day e auditar logs'))
    def r35_challenge_cybersecurity(self):
        self._add_score(
            'cybersecurity', 16.0, 'R35', 'Mindset de Pensamento Adversarial e Pentesting',
            'Prazer em pensar como o atacante para antecipar pontos fracos e blindar sistemas.'
        )

    @Rule(UserProfile(daily_challenge='Resolver gargalos em contêineres e orquestrar clusters K8s'))
    def r36_challenge_devops(self):
        self._add_score(
            'devops', 16.0, 'R36', 'Dedicação à Orquestração e Resolução de Gargalos em Produção',
            'Prazer em debugar loops de pods, configurar autoescalonamento e manter sistemas no ar.'
        )

    @Rule(UserProfile(daily_challenge='Desenhar diagramas de nuvem e arquitetar alta disponibilidade'))
    def r37_challenge_cloud(self):
        self._add_score(
            'cloud', 16.0, 'R37', 'Visão Sistêmica de Topologia e Disponibilidade Multi-Região',
            'Prazer em projetar sistemas distribuídos com redundância geográfica e failover automático.'
        )

    @Rule(UserProfile(daily_challenge='Gerenciar ciclo de vida de apps e permissões de hardware móvel'))
    def r38_challenge_mobile(self):
        self._add_score(
            'mobile', 16.0, 'R38', 'Domínio dos Recursos e Restrições de Dispositivos Móveis',
            'Prazer em lidar com ciclo de vida de telas, permissões de câmera/GPS e otimização de bateria.'
        )

    @Rule(UserProfile(daily_challenge='Automatizar suítes de testes de regressão e carga'))
    def r39_challenge_qa(self):
        self._add_score(
            'qa', 16.0, 'R39', 'Meticulosidade em Automação de Casos de Borda',
            'Prazer em antecipar comportamentos atípicos e garantir estabilidade antes do lançamento.'
        )

    @Rule(UserProfile(daily_challenge='Negociar com stakeholders e definir o roadmap do produto'))
    def r40_challenge_pm(self):
        self._add_score(
            'pm', 16.0, 'R40', 'Habilidade em Alinhamento Estratégico e Priorização',
            'Prazer em conduzir negociações complexas, dizer "não" com elegância e guiar a visão do produto.'
        )

    # =========================================================================
    # GRUPO 5: REGRAS CRUZADAS DE DESAMBIGUAÇÃO CRÍTICA (R41 - R52)
    # =========================================================================

    @Rule(
        UserProfile(math_affinity='Alta'),
        OR(
            UserProfile(work_preference='Modelagem estatística, machine learning e inteligência artificial'),
            UserProfile(daily_challenge='Calibrar hiperparâmetros e testar hipóteses estatísticas'),
            UserProfile(value_delivery='Modelos preditivos acurados e inteligência artificial para decisão')
        )
    )
    def r41_cross_ds_vs_de_analytics(self):
        self._add_score(
            'data_science', 18.0, 'R41_CROSS', 'Desambiguação: Perfil Analítico vs Engenharia de Dados',
            'A afinidade matemática alta somada ao interesse em modelos preditivos diferencia decisivamente o Cientista de Dados do Engenheiro de Dados.'
        )

    @Rule(
        OR(
            UserProfile(work_preference='Pipelines de dados, arquitetura ETL/ELT e Data Lakes'),
            UserProfile(daily_challenge='Escalar pipelines de processamento distribuído de terabytes'),
            UserProfile(primary_tool='SQL / Ferramentas de Big Data (Spark, Airflow)')
        ),
        OR(
            UserProfile(value_delivery='Fluxo de dados limpo, rápido e confiável para toda a empresa'),
            UserProfile(communication_vs_code='Foco predominante em código e arquitetura técnica profunda')
        )
    )
    def r42_cross_ds_vs_de_engineering(self):
        self._add_score(
            'data_engineering', 18.0, 'R42_CROSS', 'Desambiguação: Engenharia de Dados vs Ciência de Dados',
            'Foco em dutos de dados escaláveis, arquitetura de Data Lakes e computação distribuída consolida a vocação em Engenharia de Dados.'
        )

    @Rule(
        OR(
            UserProfile(work_preference='Interfaces visuais interativas, design e experiência do usuário'),
            UserProfile(daily_challenge='Ajustar CSS, microinterações e acessibilidade web')
        ),
        UserProfile(device_focus='Agnóstico a hardware, foco total em software/lógica/regras')
    )
    def r43_cross_front_vs_mobile_web(self):
        self._add_score(
            'frontend', 16.0, 'R43_CROSS', 'Desambiguação: Front-end Web vs Mobile',
            'O foco em interfaces sem amarração exclusiva a hardware móvel aponta para o desenvolvimento Front-end Web responsivo.'
        )

    @Rule(
        OR(
            UserProfile(work_preference='Aplicativos móveis nativos ou multiplataforma para smartphones'),
            UserProfile(primary_tool='Swift / Kotlin / Flutter / React Native'),
            UserProfile(daily_challenge='Gerenciar ciclo de vida de apps e permissões de hardware móvel')
        ),
        UserProfile(device_focus='Dispositivos móveis, smartphones e tablets')
    )
    def r44_cross_front_vs_mobile_app(self):
        self._add_score(
            'mobile', 18.0, 'R44_CROSS', 'Desambiguação: Especialização Mobile Nativo/Híbrido',
            'A preferência explícita por dispositivos móveis e frameworks como Flutter/Swift desempata totalmente para a trilha Mobile.'
        )

    @Rule(
        OR(
            UserProfile(work_preference='Automação de CI/CD, esteiras de deploy, contêineres e alta disponibilidade'),
            UserProfile(primary_tool='Docker / Kubernetes / Terraform / CI-CD'),
            UserProfile(daily_challenge='Resolver gargalos em contêineres e orquestrar clusters K8s')
        )
    )
    def r45_cross_devops_vs_cloud_k8s(self):
        self._add_score(
            'devops', 16.0, 'R45_CROSS', 'Desambiguação: Foco Operacional DevOps & SRE',
            'O direcionamento para esteiras de deploy contínuo, clusters Kubernetes e resiliência diária define a disciplina de DevOps & SRE.'
        )

    @Rule(
        OR(
            UserProfile(work_preference='Arquitetura de sistemas em nuvem, migração e infraestrutura escalável'),
            UserProfile(primary_tool='Nuvem AWS / Azure / GCP'),
            UserProfile(daily_challenge='Desenhar diagramas de nuvem e arquitetar alta disponibilidade')
        )
    )
    def r46_cross_devops_vs_cloud_arch(self):
        self._add_score(
            'cloud', 16.0, 'R46_CROSS', 'Desambiguação: Foco em Arquitetura e Estratégia Cloud',
            'O planejamento abrangente de migração corporativa e desenho de soluções para hyperscalers consolida a trilha de Cloud Architecture.'
        )

    @Rule(
        UserProfile(device_focus='Redes, roteadores, firewalls e servidores físicos'),
        OR(
            UserProfile(work_preference='Defesa cibernética, análise de vulnerabilidades e testes de invasão'),
            UserProfile(primary_tool='Linux / Bash / Ferramentas de Redes e Segurança')
        )
    )
    def r47_cross_sec_vs_infra_offensive(self):
        self._add_score(
            'cybersecurity', 18.0, 'R47_CROSS', 'Desambiguação: Foco Ofensivo/Defensivo em Segurança',
            'A união entre conhecimento de infraestrutura física/redes e postura investigativa de brechas direciona para Cibersegurança.'
        )

    @Rule(
        OR(
            UserProfile(work_preference='Testes automatizados, caça a bugs e garantia de qualidade'),
            UserProfile(daily_challenge='Automatizar suítes de testes de regressão e carga')
        ),
        UserProfile(value_delivery='Software sem bugs, estável e que cumpre todos os critérios')
    )
    def r48_cross_qa_vs_dev_quality(self):
        self._add_score(
            'qa', 18.0, 'R48_CROSS', 'Desambiguação: Foco Sistemático em Qualidade vs Codificação Pura',
            'A dedicação integral à garantia de critérios de aceitação e prevenção de regressões prioriza a Engenharia de QA.'
        )

    @Rule(
        UserProfile(communication_vs_code='Foco predominante em pessoas, alinhamento de negócio e facilitação'),
        OR(
            UserProfile(work_preference='Gestão de produto, estratégia de negócio, priorização e comunicação'),
            UserProfile(primary_tool='Ferramentas de Gestão e Ágil (Jira, Trello, Miro, Notion)')
        )
    )
    def r49_cross_pm_vs_tech_lead(self):
        self._add_score(
            'pm', 22.0, 'R49_CROSS', 'Desambiguação: Gestão de Negócios e Produto vs Engenharia Técnica',
            'A escolha primária por comunicação executiva, resolução de dores do usuário e ritos ágeis define o perfil do Product Manager.'
        )

    @Rule(
        UserProfile(math_affinity='Alta'),
        NOT(UserProfile(work_preference='Modelagem estatística, machine learning e inteligência artificial'))
    )
    def r50_cross_math_high_general(self):
        self._add_score(
            'backend', 5.0, 'R50_MATH', 'Bônus de Raciocínio Lógico Matemático',
            'Alta capacidade analítica favorece o desenvolvimento de algoritmos complexos no Back-end.'
        )
        self._add_score(
            'data_engineering', 5.0, 'R50_MATH_DE', 'Bônus Matemático para Dados',
            'Bases matemáticas aceleram o domínio de particionamento e computação distribuída.'
        )

    @Rule(UserProfile(math_affinity='Baixa'))
    def r51_cross_math_low_penalty_ds(self):
        self._add_score(
            'data_science', -20.0, 'R51_PENALTY', 'Penalidade: Ciência de Dados Exige Rigor Matemático',
            'Ciência de Dados demanda álgebra linear, cálculo e probabilidade frequentes; afinidade baixa gera forte atrito na curva de aprendizado.'
        )
        self._add_score(
            'frontend', 5.0, 'R51_FRONT', 'Afinidade com Lógica Visual',
            'O Front-end concentra desafios em estruturação visual, UI/UX e reatividade onde matemática pura é raramente exigida.'
        )

    @Rule(
        UserProfile(device_focus='Redes, roteadores, firewalls e servidores físicos'),
        NOT(UserProfile(work_preference='Defesa cibernética, análise de vulnerabilidades e testes de invasão'))
    )
    def r52_cross_network_infra_boost(self):
        self._add_score(
            'devops', 8.0, 'R52_INFRA', 'Bônus de Redes para Infraestrutura',
            'Domínio de roteamento e servidores físicos apoia a gestão de infraestruturas locais e híbridas em DevOps.'
        )
        self._add_score(
            'cloud', 8.0, 'R52_CLOUD', 'Bônus de Redes para Cloud',
            'Topologias de nuvem corporativa dependem de subredes, peering e VPNs sólidas.'
        )
