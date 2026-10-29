"""
Personas de Teste e Validação para o Sistema Especialista.
Inclui as 4 personas principais exigidas formalmente e 6 personas complementares
cobrindo todas as 10 trilhas de carreira. Cada persona informa perfil pessoal,
afinidades (o que gosta), proficiências (o que sabe) e preferências de atuação.
"""

TEST_PERSONAS = {
    "ana_data_science": {
        "id": "ana_data_science",
        "name": "Ana Silva",
        "badge": "Perfil Analítico",
        "expected_track": "data_science",
        "avatar": "🧠",
        "description": "Formada em Exatas, é apaixonada por descobrir padrões em números, formular hipóteses estatísticas e construir modelos de Machine Learning.",
        "answers": {
            "profile": {"name": "Ana Silva", "objective": "first_job", "experience": "student", "weekly_hours": 15, "deadline_months": 8},
            "affinities": {"programming": 4, "logic": 4, "math": 5, "design": 2, "data_analysis": 5, "infrastructure": 2, "security": 2,
                           "automation": 3, "testing": 3, "management": 2, "communication": 3, "business": 3, "mobile_devices": 1, "cloud_systems": 2},
            "proficiencies": {"logica_programacao": 4, "python": 3, "estatistica": 4, "algebra_calculo": 3, "pandas_numpy": 2, "sql": 2, "git": 2},
            "choices": {
                "work_preference": "Modelagem estatística, machine learning e inteligência artificial",
                "primary_tool": "Python",
                "value_delivery": "Modelos preditivos acurados e inteligência artificial para decisão",
                "daily_challenge": "Calibrar hiperparâmetros e testar hipóteses estatísticas",
                "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
                "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
            }
        }
    },

    "carlos_security": {
        "id": "carlos_security",
        "name": "Carlos Rocha",
        "badge": "Perfil Infra / Segurança",
        "expected_track": "cybersecurity",
        "avatar": "🛡️",
        "description": "Entusiasta de redes, sistemas operacionais e segurança defensiva/ofensiva. Adora analisar brechas, tráfego de pacotes e realizar testes de intrusão.",
        "answers": {
            "profile": {"name": "Carlos Rocha", "objective": "switch_track", "experience": "junior", "weekly_hours": 10, "deadline_months": 6},
            "affinities": {"programming": 3, "logic": 4, "math": 3, "design": 1, "data_analysis": 2, "infrastructure": 5, "security": 5,
                           "automation": 4, "testing": 3, "management": 2, "communication": 2, "business": 2, "mobile_devices": 1, "cloud_systems": 3},
            "proficiencies": {"linux": 4, "redes": 3, "bash": 3, "python": 2, "fundamentos_seguranca": 2, "git": 3},
            "choices": {
                "work_preference": "Defesa cibernética, análise de vulnerabilidades e testes de invasão",
                "primary_tool": "Linux / Bash / Ferramentas de Redes e Segurança",
                "value_delivery": "Proteção contra invasões, dados seguros e sistemas blindados",
                "daily_challenge": "Simular ataques, encontrar brechas zero-day e auditar logs",
                "communication_vs_code": "Foco predominante em código e arquitetura técnica profunda",
                "device_focus": "Redes, roteadores, firewalls e servidores físicos"
            }
        }
    },

    "beatriz_frontend": {
        "id": "beatriz_frontend",
        "name": "Beatriz Lima",
        "badge": "Perfil Visual / Frontend",
        "expected_track": "frontend",
        "avatar": "🎨",
        "description": "Criativa e com senso estético apurado. Encanta-se com interfaces fluidas, acessibilidade, microanimações e a experiência do usuário final no navegador.",
        "answers": {
            "profile": {"name": "Beatriz Lima", "objective": "career_change", "experience": "none", "weekly_hours": 8, "deadline_months": 9},
            "affinities": {"programming": 4, "logic": 3, "math": 1, "design": 5, "data_analysis": 2, "infrastructure": 1, "security": 1,
                           "automation": 2, "testing": 3, "management": 3, "communication": 4, "business": 2, "mobile_devices": 3, "cloud_systems": 1},
            "proficiencies": {"html_css": 3, "javascript": 2, "ux_ui": 3, "logica_programacao": 2},
            "choices": {
                "work_preference": "Interfaces visuais interativas, design e experiência do usuário",
                "primary_tool": "JavaScript / TypeScript",
                "value_delivery": "Telas encantadoras, responsivas e navegação agradável",
                "daily_challenge": "Ajustar CSS, microinterações e acessibilidade web",
                "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
                "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
            }
        }
    },

    "lucas_product": {
        "id": "lucas_product",
        "name": "Lucas Mendes",
        "badge": "Perfil Negócios / Produto",
        "expected_track": "pm",
        "avatar": "🧭",
        "description": "Excelente comunicador e estrategista. Prefere gerenciar roadmaps, alinhar expectativas com clientes e stakeholders e liderar ritos ágeis a programar o dia inteiro.",
        "answers": {
            "profile": {"name": "Lucas Mendes", "objective": "career_change", "experience": "none", "weekly_hours": 6, "deadline_months": 6},
            "affinities": {"programming": 2, "logic": 3, "math": 3, "design": 3, "data_analysis": 4, "infrastructure": 1, "security": 1,
                           "automation": 2, "testing": 2, "management": 5, "communication": 5, "business": 5, "mobile_devices": 2, "cloud_systems": 1},
            "proficiencies": {"agil": 3, "comunicacao_stakeholders": 4, "metricas_produto": 2, "sql": 1},
            "choices": {
                "work_preference": "Gestão de produto, estratégia de negócio, priorização e comunicação",
                "primary_tool": "Ferramentas de Gestão e Ágil (Jira, Trello, Miro, Notion)",
                "value_delivery": "Produtos que resolvem dores de usuários e geram receita",
                "daily_challenge": "Negociar com stakeholders e definir o roadmap do produto",
                "communication_vs_code": "Foco predominante em pessoas, alinhamento de negócio e facilitação",
                "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
            }
        }
    },

    "eduardo_data_eng": {
        "id": "eduardo_data_eng",
        "name": "Eduardo Santos",
        "badge": "Perfil Engenharia de Dados",
        "expected_track": "data_engineering",
        "avatar": "🏗️",
        "description": "Focado em infraestrutura de dados. Prefere construir pipelines robustos de ETL, orquestrar fluxos com Airflow/Spark e otimizar queries em Data Lakes.",
        "answers": {
            "profile": {"name": "Eduardo Santos", "objective": "switch_track", "experience": "junior", "weekly_hours": 12, "deadline_months": 6},
            "affinities": {"programming": 5, "logic": 4, "math": 3, "design": 1, "data_analysis": 4, "infrastructure": 4, "security": 2,
                           "automation": 4, "testing": 3, "management": 2, "communication": 2, "business": 2, "mobile_devices": 1, "cloud_systems": 4},
            "proficiencies": {"python": 4, "sql": 4, "logica_programacao": 4, "git": 3, "linux": 3, "etl_pipelines": 2},
            "choices": {
                "work_preference": "Pipelines de dados, arquitetura ETL/ELT e Data Lakes",
                "primary_tool": "SQL / Ferramentas de Big Data (Spark, Airflow)",
                "value_delivery": "Fluxo de dados limpo, rápido e confiável para toda a empresa",
                "daily_challenge": "Escalar pipelines de processamento distribuído de terabytes",
                "communication_vs_code": "Foco predominante em código e arquitetura técnica profunda",
                "device_focus": "Serviços virtuais gerenciados e data centers na nuvem"
            }
        }
    },

    "mariana_devops": {
        "id": "mariana_devops",
        "name": "Mariana Costa",
        "badge": "Perfil DevOps & SRE",
        "expected_track": "devops",
        "avatar": "♾️",
        "description": "Entusiasta de automação e confiabilidade. Gosta de criar pipelines de CI/CD, orquestrar contêineres Docker e Kubernetes e monitorar métricas com Prometheus.",
        "answers": {
            "profile": {"name": "Mariana Costa", "objective": "level_up", "experience": "junior", "weekly_hours": 10, "deadline_months": 6},
            "affinities": {"programming": 4, "logic": 4, "math": 3, "design": 1, "data_analysis": 2, "infrastructure": 5, "security": 3,
                           "automation": 5, "testing": 3, "management": 2, "communication": 3, "business": 2, "mobile_devices": 1, "cloud_systems": 4},
            "proficiencies": {"linux": 4, "git": 4, "docker": 3, "bash": 3, "ci_cd": 2, "redes": 2},
            "choices": {
                "work_preference": "Automação de CI/CD, esteiras de deploy, contêineres e alta disponibilidade",
                "primary_tool": "Docker / Kubernetes / Terraform / CI-CD",
                "value_delivery": "Deploys frequentes sem quedas e esteiras ágeis automatizadas",
                "daily_challenge": "Resolver gargalos em contêineres e orquestrar clusters K8s",
                "communication_vs_code": "Foco predominante em código e arquitetura técnica profunda",
                "device_focus": "Serviços virtuais gerenciados e data centers na nuvem"
            }
        }
    },

    "gabriel_backend": {
        "id": "gabriel_backend",
        "name": "Gabriel Alencar",
        "badge": "Perfil Back-end",
        "expected_track": "backend",
        "avatar": "⚙️",
        "description": "Focado na lógica de servidor, regras de negócio complexas, modelagem de banco relacional e criação de endpoints REST e gRPC performáticos.",
        "answers": {
            "profile": {"name": "Gabriel Alencar", "objective": "first_job", "experience": "student", "weekly_hours": 20, "deadline_months": 4},
            "affinities": {"programming": 5, "logic": 5, "math": 3, "design": 2, "data_analysis": 3, "infrastructure": 3, "security": 3,
                           "automation": 3, "testing": 3, "management": 2, "communication": 2, "business": 2, "mobile_devices": 2, "cloud_systems": 3},
            "proficiencies": {"logica_programacao": 4, "backend_typed": 3, "poo": 3, "sql": 3, "git": 3, "estruturas_dados": 2, "apis_rest": 2},
            "choices": {
                "work_preference": "Lógica de negócios, APIs e bancos de dados",
                "primary_tool": "Java / C# / Go",
                "value_delivery": "APIs robustas, regras de negócio e estabilidade de servidor",
                "daily_challenge": "Otimizar algoritmos e consultas SQL complexas",
                "communication_vs_code": "Foco predominante em código e arquitetura técnica profunda",
                "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
            }
        }
    },

    "rafael_mobile": {
        "id": "rafael_mobile",
        "name": "Rafael Nogueira",
        "badge": "Perfil Mobile",
        "expected_track": "mobile",
        "avatar": "📱",
        "description": "Fascinado pelo mundo móvel. Adora criar aplicativos com Flutter e React Native, consumir recursos nativos (câmera, biometria) e publicar nas lojas.",
        "answers": {
            "profile": {"name": "Rafael Nogueira", "objective": "first_job", "experience": "student", "weekly_hours": 12, "deadline_months": 6},
            "affinities": {"programming": 5, "logic": 4, "math": 2, "design": 4, "data_analysis": 2, "infrastructure": 2, "security": 2,
                           "automation": 3, "testing": 3, "management": 2, "communication": 3, "business": 2, "mobile_devices": 5, "cloud_systems": 2},
            "proficiencies": {"logica_programacao": 3, "dart_kotlin_swift": 3, "dev_mobile": 2, "git": 2, "poo": 2},
            "choices": {
                "work_preference": "Aplicativos móveis nativos ou multiplataforma para smartphones",
                "primary_tool": "Swift / Kotlin / Flutter / React Native",
                "value_delivery": "Experiência móvel fluida e acessível na palma da mão",
                "daily_challenge": "Gerenciar ciclo de vida de apps e permissões de hardware móvel",
                "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
                "device_focus": "Dispositivos móveis, smartphones e tablets"
            }
        }
    },

    "camila_qa": {
        "id": "camila_qa",
        "name": "Camila Duarte",
        "badge": "Perfil QA & Qualidade",
        "expected_track": "qa",
        "avatar": "🔍",
        "description": "Meticulosa e detalhista. Enxerga cenários de exceção que outros desenvolvedores esquecem, adora automatizar suítes de testes e caçar bugs antes da produção.",
        "answers": {
            "profile": {"name": "Camila Duarte", "objective": "career_change", "experience": "none", "weekly_hours": 10, "deadline_months": 6},
            "affinities": {"programming": 3, "logic": 5, "math": 3, "design": 2, "data_analysis": 3, "infrastructure": 2, "security": 2,
                           "automation": 4, "testing": 5, "management": 3, "communication": 3, "business": 2, "mobile_devices": 2, "cloud_systems": 2},
            "proficiencies": {"fundamentos_testes": 3, "logica_programacao": 3, "python": 2, "agil": 2},
            "choices": {
                "work_preference": "Testes automatizados, caça a bugs e garantia de qualidade",
                "primary_tool": "Ferramentas de Teste (Cypress, Selenium, PyTest, JUnit)",
                "value_delivery": "Software sem bugs, estável e que cumpre todos os critérios",
                "daily_challenge": "Automatizar suítes de testes de regressão e carga",
                "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
                "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
            }
        }
    },

    "rodrigo_cloud": {
        "id": "rodrigo_cloud",
        "name": "Rodrigo Fonseca",
        "badge": "Perfil Cloud Architecture",
        "expected_track": "cloud",
        "avatar": "☁️",
        "description": "Visionário em infraestrutura na nuvem. Projeta topologias escaláveis na AWS e Azure, desenha estratégias de migração corporativa e otimiza custos com FinOps.",
        "answers": {
            "profile": {"name": "Rodrigo Fonseca", "objective": "level_up", "experience": "experienced", "weekly_hours": 8, "deadline_months": 6},
            "affinities": {"programming": 2, "logic": 4, "math": 3, "design": 2, "data_analysis": 2, "infrastructure": 5, "security": 4,
                           "automation": 3, "testing": 2, "management": 3, "communication": 3, "business": 4, "mobile_devices": 1, "cloud_systems": 5},
            "proficiencies": {"redes": 4, "linux": 3, "cloud_fundamentos": 3, "fundamentos_seguranca": 3, "docker": 2},
            "choices": {
                "work_preference": "Arquitetura de sistemas em nuvem, migração e infraestrutura escalável",
                "primary_tool": "Nuvem AWS / Azure / GCP",
                "value_delivery": "Estrutura de nuvem escalável, resiliente e com custos otimizados",
                "daily_challenge": "Desenhar diagramas de nuvem e arquitetar alta disponibilidade",
                "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
                "device_focus": "Serviços virtuais gerenciados e data centers na nuvem"
            }
        }
    }
}
