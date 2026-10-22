"""
Personas de Teste e Validação para o Sistema Especialista.
Inclui as 4 personas principais exigidas formalmente e 6 personas complementares
cobrindo todas as 10 trilhas de carreira.
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
            "math_affinity": "Alta",
            "work_preference": "Modelagem estatística, machine learning e inteligência artificial",
            "primary_tool": "Python",
            "value_delivery": "Modelos preditivos acurados e inteligência artificial para decisão",
            "daily_challenge": "Calibrar hiperparâmetros e testar hipóteses estatísticas",
            "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
            "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
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
            "math_affinity": "Média",
            "work_preference": "Defesa cibernética, análise de vulnerabilidades e testes de invasão",
            "primary_tool": "Linux / Bash / Ferramentas de Redes e Segurança",
            "value_delivery": "Proteção contra invasões, dados seguros e sistemas blindados",
            "daily_challenge": "Simular ataques, encontrar brechas zero-day e auditar logs",
            "communication_vs_code": "Foco predominante em código e arquitetura técnica profunda",
            "device_focus": "Redes, roteadores, firewalls e servidores físicos"
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
            "math_affinity": "Baixa",
            "work_preference": "Interfaces visuais interativas, design e experiência do usuário",
            "primary_tool": "JavaScript / TypeScript",
            "value_delivery": "Telas encantadoras, responsivas e navegação agradável",
            "daily_challenge": "Ajustar CSS, microinterações e acessibilidade web",
            "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
            "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
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
            "math_affinity": "Média",
            "work_preference": "Gestão de produto, estratégia de negócio, priorização e comunicação",
            "primary_tool": "Ferramentas de Gestão e Ágil (Jira, Trello, Miro, Notion)",
            "value_delivery": "Produtos que resolvem dores de usuários e geram receita",
            "daily_challenge": "Negociar com stakeholders e definir o roadmap do produto",
            "communication_vs_code": "Foco predominante em pessoas, alinhamento de negócio e facilitação",
            "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
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
            "math_affinity": "Média",
            "work_preference": "Pipelines de dados, arquitetura ETL/ELT e Data Lakes",
            "primary_tool": "SQL / Ferramentas de Big Data (Spark, Airflow)",
            "value_delivery": "Fluxo de dados limpo, rápido e confiável para toda a empresa",
            "daily_challenge": "Escalar pipelines de processamento distribuído de terabytes",
            "communication_vs_code": "Foco predominante em código e arquitetura técnica profunda",
            "device_focus": "Serviços virtuais gerenciados e data centers na nuvem"
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
            "math_affinity": "Média",
            "work_preference": "Automação de CI/CD, esteiras de deploy, contêineres e alta disponibilidade",
            "primary_tool": "Docker / Kubernetes / Terraform / CI-CD",
            "value_delivery": "Deploys frequentes sem quedas e esteiras ágeis automatizadas",
            "daily_challenge": "Resolver gargalos em contêineres e orquestrar clusters K8s",
            "communication_vs_code": "Foco predominante em código e arquitetura técnica profunda",
            "device_focus": "Serviços virtuais gerenciados e data centers na nuvem"
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
            "math_affinity": "Média",
            "work_preference": "Lógica de negócios, APIs e bancos de dados",
            "primary_tool": "Java / C# / Go",
            "value_delivery": "APIs robustas, regras de negócio e estabilidade de servidor",
            "daily_challenge": "Otimizar algoritmos e consultas SQL complexas",
            "communication_vs_code": "Foco predominante em código e arquitetura técnica profunda",
            "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
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
            "math_affinity": "Baixa",
            "work_preference": "Aplicativos móveis nativos ou multiplataforma para smartphones",
            "primary_tool": "Swift / Kotlin / Flutter / React Native",
            "value_delivery": "Experiência móvel fluida e acessível na palma da mão",
            "daily_challenge": "Gerenciar ciclo de vida de apps e permissões de hardware móvel",
            "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
            "device_focus": "Dispositivos móveis, smartphones e tablets"
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
            "math_affinity": "Média",
            "work_preference": "Testes automatizados, caça a bugs e garantia de qualidade",
            "primary_tool": "Ferramentas de Teste (Cypress, Selenium, PyTest, JUnit)",
            "value_delivery": "Software sem bugs, estável e que cumpre todos os critérios",
            "daily_challenge": "Automatizar suítes de testes de regressão e carga",
            "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
            "device_focus": "Agnóstico a hardware, foco total em software/lógica/regras"
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
            "math_affinity": "Média",
            "work_preference": "Arquitetura de sistemas em nuvem, migração e infraestrutura escalável",
            "primary_tool": "Nuvem AWS / Azure / GCP",
            "value_delivery": "Estrutura de nuvem escalável, resiliente e com custos otimizados",
            "daily_challenge": "Desenhar diagramas de nuvem e arquitetar alta disponibilidade",
            "communication_vs_code": "Foco balanceado entre desenvolvimento técnico e colaboração",
            "device_focus": "Serviços virtuais gerenciados e data centers na nuvem"
        }
    }
}
