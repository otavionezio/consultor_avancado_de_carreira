"""
Catálogo detalhado das 10 Trilhas de Carreira em TI do Sistema Especialista.
Cada trilha contém descrição técnica, competências-chave, tecnologias dominantes,
faixas salariais de mercado e roteiro de aprendizado (roadmap).
"""

CAREER_TRACKS = {
    "backend": {
        "id": "backend",
        "name": "Desenvolvimento Back-end",
        "icon": "⚙️",
        "summary": "Foco em lógica de servidores, construção de APIs, regras de negócio e bancos de dados.",
        "description": (
            "O Engenheiro Back-end é o arquiteto invisível dos sistemas digitais. "
            "Ele projeta a lógica central de negócio, modela e otimiza bancos de dados relacionais "
            "e não-relacionais, cria APIs RESTful e gRPC seguras, e garante que as requisições "
            "sejam processadas com alto desempenho, escalabilidade e integridade."
        ),
        "key_skills": [
            "Lógica de programação avançada e algoritmos",
            "Modelagem relacional e normalização de bancos de dados",
            "Arquitetura de microsserviços e padrões de projeto (Clean Architecture, DDD)",
            "Autenticação, autorização (OAuth2, JWT) e segurança de endpoints",
            "Gerenciamento de concorrência, filas assíncronas e mensageria"
        ],
        "technologies": [
            "Python (FastAPI, Django, Flask)",
            "Node.js / TypeScript (NestJS, Express)",
            "Java (Spring Boot) / C# (.NET Core) / Go",
            "PostgreSQL, MySQL, MongoDB, Redis",
            "RabbitMQ, Apache Kafka, Celery"
        ],
        "salary_range": {
            "junior": "R$ 4.000 - R$ 6.500",
            "pleno": "R$ 7.500 - R$ 12.000",
            "senior": "R$ 13.000 - R$ 22.000+"
        },
        "market_demand": "Muito Alta (Pilar fundamental de qualquer produto digital)",
        "roadmap": [
            "Fundamentos sólidos de algoritmos, estruturas de dados e POO",
            "Domínio de uma linguagem de back-end (Python, Java, Go ou C#)",
            "SQL avançado, indexação, transações ACID e ORMs",
            "Criação de APIs RESTful e integração com microsserviços",
            "Mensageria assíncrona (RabbitMQ/Kafka) e cache com Redis",
            "Testes automatizados (Unitários e Integração) e Clean Code"
        ]
    },

    "frontend": {
        "id": "frontend",
        "name": "Desenvolvimento Front-end & UI/UX",
        "icon": "🎨",
        "summary": "Foco em interfaces web responsivas, experiência do usuário e frameworks reativos.",
        "description": (
            "O Engenheiro Front-end & UI/UX dá vida à interação humana com a tecnologia. "
            "Ele transforma conceitos visuais e protótipos em interfaces web fluidas, acessíveis, "
            "reativas e esteticamente impecáveis, otimizando performance de renderização, "
            "acessibilidade (a11y) e usabilidade em múltiplos navegadores e resoluções."
        ),
        "key_skills": [
            "HTML5 semântico, CSS3 moderno (Flexbox, Grid, Animações) e Tailwind CSS",
            "JavaScript moderno (ES6+) e TypeScript profundo",
            "Gerenciamento de estado global e reatividade",
            "Princípios de UI/UX, Design Systems e heurísticas de usabilidade",
            "Otimização de Core Web Vitals, SSR e SEO técnico"
        ],
        "technologies": [
            "React.js, Next.js, Vue.js, Nuxt, Angular",
            "TypeScript, Tailwind CSS, SASS, Styled Components",
            "Figma, Adobe XD (integração design-to-code)",
            "Vite, Webpack, Vitest, Cypress para componentes"
        ],
        "salary_range": {
            "junior": "R$ 3.800 - R$ 6.000",
            "pleno": "R$ 7.000 - R$ 11.500",
            "senior": "R$ 12.500 - R$ 20.000+"
        },
        "market_demand": "Muito Alta (O visual e a experiência determinam a retenção do cliente)",
        "roadmap": [
            "HTML5 semântico, CSS avançado (Flexbox, Grid, Media Queries)",
            "JavaScript avançado: manipulação DOM, assincronismo, closures",
            "Framework reativo principal (React, Vue ou Angular)",
            "TypeScript aplicado ao desenvolvimento de componentes",
            "Next.js / SSR e gerenciamento de estado (Redux Toolkit, Zustand)",
            "Testes de interface com Jest/Vitest e React Testing Library"
        ]
    },

    "data_science": {
        "id": "data_science",
        "name": "Ciência de Dados e Machine Learning",
        "icon": "🧠",
        "summary": "Foco em estatística, modelagem preditiva, análise de grandes massas de dados e inteligência artificial.",
        "description": (
            "O Cientista de Dados é o estrategista analítico que transforma dados em previsões "
            "e inteligência de negócio. Utiliza rigor estatístico, álgebra linear, algoritmos de "
            "Machine Learning supervisionado e não-supervisionado, Processamento de Linguagem Natural "
            "e Deep Learning para resolver problemas preditivos complexos."
        ),
        "key_skills": [
            "Estatística inferencial, probabilidades e testes de hipóteses",
            "Modelagem preditiva (Regressão, Árvores, Boosting, Redes Neurais)",
            "Feature engineering e pré-processamento minucioso de dados",
            "Validação cruzada, métricas de avaliação (AUC-ROC, F1-Score, RMSE)",
            "Storytelling com dados e tradução de métricas técnicas para impacto de negócio"
        ],
        "technologies": [
            "Python (Pandas, NumPy, Scikit-Learn, SciPy)",
            "PyTorch, TensorFlow, Keras, Hugging Face Transformers",
            "Jupyter Notebooks, Google Colab, MLflow",
            "Matplotlib, Seaborn, Plotly, Streamlit",
            "SQL para consultas analíticas"
        ],
        "salary_range": {
            "junior": "R$ 4.500 - R$ 7.000",
            "pleno": "R$ 8.500 - R$ 13.500",
            "senior": "R$ 14.500 - R$ 25.000+"
        },
        "market_demand": "Alta e em forte expansão impulsionada por IA Generativa",
        "roadmap": [
            "Python intermediário/avançado para manipulação de dados",
            "Estatística descritiva, inferencial e cálculo vetorial",
            "Análise exploratória com Pandas, NumPy, Matplotlib e Seaborn",
            "Machine Learning clássico com Scikit-Learn (classificação, regressão, clustering)",
            "Deep Learning e NLP com PyTorch ou TensorFlow",
            "Práticas de MLOps: versionamento de modelos e deploy de APIs de IA"
        ]
    },

    "data_engineering": {
        "id": "data_engineering",
        "name": "Engenharia de Dados",
        "icon": "🏗️",
        "summary": "Foco em arquitetura de dados, construção de pipelines (ETL/ELT) e infraestrutura para Data Lakes.",
        "description": (
            "O Engenheiro de Dados constrói os dutos, reservatórios e rodovias por onde trafegam "
            "os dados da organização. Ele projeta pipelines escaláveis de ETL/ELT, gerencia "
            "Data Lakes e Data Warehouses distribuídos, garante governança, consistência, baixa "
            "latência e alta vazão para alimentar cientistas, analistas e aplicações em tempo real."
        ),
        "key_skills": [
            "Construção de pipelines de dados resilientes (ETL/ELT) em lote e streaming",
            "Modelagem dimensional de dados (Star Schema, Snowflake Schema)",
            "Computação distribuída e processamento massivo de dados",
            "Governança de dados, lineage, qualidade e segurança da informação",
            "Otimização de custos de armazenamento e consulta em larga escala"
        ],
        "technologies": [
            "Apache Spark (PySpark), Apache Airflow, dbt, Apache Kafka",
            "Data Warehouses: Snowflake, Google BigQuery, AWS Redshift",
            "Data Lakes: Delta Lake, Apache Iceberg, AWS S3",
            "SQL avançado para Big Data e Python para engenharia",
            "Docker, Kubernetes para orquestração de cargas de dados"
        ],
        "salary_range": {
            "junior": "R$ 4.500 - R$ 7.200",
            "pleno": "R$ 8.500 - R$ 14.000",
            "senior": "R$ 15.000 - R$ 26.000+"
        },
        "market_demand": "Altíssima (Escassez crônica de profissionais especializados em pipelines)",
        "roadmap": [
            "Lógica de programação com Python e domínio absoluto de SQL avançado",
            "Modelagem dimensional para Data Warehouses (Kimball)",
            "Orquestração de pipelines de dados com Apache Airflow e Prefect",
            "Processamento distribuído de grandes volumes com Apache Spark / PySpark",
            "Transformação moderna com dbt e plataformas de nuvem (BigQuery/Snowflake)",
            "Streaming de dados em tempo real com Apache Kafka e Flink"
        ]
    },

    "cybersecurity": {
        "id": "cybersecurity",
        "name": "Cibersegurança (Security / Pentesting)",
        "icon": "🛡️",
        "summary": "Foco em defesa cibernética, análise de vulnerabilidades, criptografia e redes seguras.",
        "description": (
            "O Especialista em Cibersegurança é o guardião dos ativos digitais contra ameaças "
            "e ataques cibernéticos. Atua na frente defensiva (Blue Team) monitorando SIEM e "
            "fortalecendo arquiteturas, ou na frente ofensiva (Red Team / Pentesting) simulando "
            "invasões éticas para identificar e corrigir brechas críticas antes de agentes maliciosos."
        ),
        "key_skills": [
            "Redes de computadores profundas (TCP/IP, roteamento, firewalls, DNS, VPNs)",
            "Análise e mitigação de vulnerabilidades (OWASP Top 10, CVEs)",
            "Criptografia simétrica, assimétrica, PKI e hashing seguro",
            "Auditoria de conformidade (LGPD, ISO 27001, SOC 2, NIST)",
            "Perícia digital (forensics), resposta a incidentes e testes de intrusão"
        ],
        "technologies": [
            "Kali Linux, Wireshark, Nmap, Burp Suite, Metasploit",
            "SIEM & EDR (Splunk, Elastic Security, CrowdStrike)",
            "Python e Bash scripting para automação de exploits e auditoria",
            "Ferramentas de SAST/DAST (SonarQube, Snyk, Zap)",
            "Sistemas operacionais Linux hardening e Active Directory"
        ],
        "salary_range": {
            "junior": "R$ 4.200 - R$ 6.800",
            "pleno": "R$ 8.000 - R$ 13.500",
            "senior": "R$ 14.000 - R$ 24.000+"
        },
        "market_demand": "Muito Alta e Estratégica (Segurança é prioridade regulatória e corporativa)",
        "roadmap": [
            "Fundamentos sólidos de Redes (TCP/IP, UDP, Subredes, Protocolos)",
            "Administração e segurança de sistemas Linux e Windows Server",
            "Segurança de aplicações web (OWASP Top 10, autenticação, injeção)",
            "Scripting defensivo e ofensivo em Python e Bash",
            "Uso de ferramentas essenciais: Nmap, Wireshark, Burp Suite",
            "Certificações recomendadas: CompTIA Security+, CEH, OSCP"
        ]
    },

    "devops": {
        "id": "devops",
        "name": "DevOps & SRE",
        "icon": "♾️",
        "summary": "Foco em automação de processos, integração e entrega contínua (CI/CD) e contêineres.",
        "description": (
            "O Engenheiro DevOps e SRE (Site Reliability Engineer) une as pontas de desenvolvimento "
            "e operações de infraestrutura. É responsável por criar esteiras automatizadas de "
            "integração e entrega contínua (CI/CD), orquestrar contêineres, garantir observabilidade "
            "(métricas, logs, traces) e manter a confiabilidade e disponibilidade máxima de serviços."
        ),
        "key_skills": [
            "Criação e manutenção de pipelines automatizados de CI/CD",
            "Conteinerização e orquestração de microsserviços em escala",
            "Infraestrutura como Código (IaC)",
            "Observabilidade proativa: monitoramento, alertas, tracing distribuído",
            "Gestão de incidentes, SLOs/SLIs, Error Budgets e engenharia de caos"
        ],
        "technologies": [
            "Docker, Podman, Kubernetes, Helm",
            "GitHub Actions, GitLab CI, Jenkins, ArgoCD",
            "Terraform, Ansible, Pulumi",
            "Prometheus, Grafana, Datadog, ELK Stack",
            "Linux avançado, Shell Scripting, Python/Go para automação"
        ],
        "salary_range": {
            "junior": "R$ 4.500 - R$ 7.200",
            "pleno": "R$ 8.500 - R$ 14.000",
            "senior": "R$ 15.000 - R$ 25.000+"
        },
        "market_demand": "Altíssima (Todas as empresas modernas de tecnologia exigem CI/CD e K8s)",
        "roadmap": [
            "Linux avançado, Bash scripting e redes para servidores",
            "Contêineres com Docker: criação de imagens otimizadas e volumes",
            "Automação de esteiras CI/CD com GitHub Actions ou GitLab CI",
            "Orquestração com Kubernetes (Pods, Deployments, Services, Ingress)",
            "Infraestrutura como Código com Terraform",
            "Observabilidade com Prometheus e Grafana, aplicando conceitos SRE"
        ]
    },

    "cloud": {
        "id": "cloud",
        "name": "Computação em Nuvem (Cloud Architecture)",
        "icon": "☁️",
        "summary": "Foco em planejamento, migração e gestão de infraestruturas escaláveis (AWS/Azure/GCP).",
        "description": (
            "O Arquiteto de Nuvem projeta a estrutura corporativa sobre os provedores globais "
            "como AWS, Azure e Google Cloud. É o responsável por desenhar topologias distribuídas, "
            "planejar migrações de sistemas legados para a nuvem, garantir redundância geográfica, "
            "governança de acessos e otimização financeira contínua de recursos (FinOps)."
        ),
        "key_skills": [
            "Desenho de soluções resilientes, tolerantes a falhas e altamente disponíveis",
            "Estratégias de migração para nuvem (Rehost, Replatform, Refactor)",
            "FinOps: governança de custos, dimensionamento e otimização de faturas de cloud",
            "Segurança em nuvem, IAM (Identity and Access Management) e redes VPC",
            "Serviços gerenciados, Serverless e arquiteturas híbridas/multicloud"
        ],
        "technologies": [
            "AWS (EC2, S3, RDS, Lambda, VPC, CloudFormation)",
            "Microsoft Azure (Virtual Machines, Blob, App Services, Entra ID)",
            "Google Cloud Platform (Compute Engine, BigQuery, GKE)",
            "Terraform, CloudFormation, Bicep para provisionamento",
            "Ferramentas de FinOps e Cloud Health Monitoring"
        ],
        "salary_range": {
            "junior": "R$ 4.800 - R$ 7.500",
            "pleno": "R$ 9.000 - R$ 15.000",
            "senior": "R$ 16.000 - R$ 28.000+"
        },
        "market_demand": "Muito Alta e com alta remuneração para arquitetos sêniores certificados",
        "roadmap": [
            "Fundamentos de redes (VPC, subredes, roteamento, peering, VPN)",
            "Serviços essenciais de um provedor líder (AWS, Azure ou GCP)",
            "Arquitetura de soluções: escalabilidade horizontal, balanceadores de carga, failover",
            "Infraestrutura como Código com Terraform para nuvem",
            "Segurança em Nuvem e governança com políticas IAM rigorosas",
            "Certificações estratégicas: AWS Solutions Architect, Azure Solutions Architect"
        ]
    },

    "mobile": {
        "id": "mobile",
        "name": "Desenvolvimento Mobile",
        "icon": "📱",
        "summary": "Foco no ecossistema de dispositivos móveis (nativo ou multiplataforma com Flutter/React Native).",
        "description": (
            "O Desenvolvedor Mobile cria aplicações que acompanham os usuários em seus bolsos 24 horas por dia. "
            "Ele lida com desafios específicos de consumo de bateria, gerenciamento de memória, conectividade "
            "intermitente (offline-first), integração com hardware (câmera, GPS, biometria) e publicações "
            "nas lojas App Store da Apple e Google Play Store."
        ),
        "key_skills": [
            "Desenvolvimento multiplataforma ou nativo para iOS e Android",
            "Ciclo de vida de aplicativos móveis e arquiteturas reativas (Bloc, Provider, MVVM)",
            "Gerenciamento de armazenamento local offline e sincronização em background",
            "Integração com sensores de hardware (GPS, câmera, Bluetooth, biometria)",
            "Publicação, assinatura digital e esteira de CI/CD para lojas de aplicativos"
        ],
        "technologies": [
            "Flutter / Dart",
            "React Native / TypeScript",
            "Kotlin / Jetpack Compose (Android Nativo)",
            "Swift / SwiftUI (iOS Nativo)",
            "Firebase, SQLite, Realm, Fastlane"
        ],
        "salary_range": {
            "junior": "R$ 3.800 - R$ 6.200",
            "pleno": "R$ 7.200 - R$ 12.000",
            "senior": "R$ 13.000 - R$ 21.000+"
        },
        "market_demand": "Alta (O consumo digital do consumidor final é majoritariamente mobile)",
        "roadmap": [
            "Fundamentos da linguagem base (Dart para Flutter, TypeScript para RN, ou Kotlin/Swift)",
            "Construção de layouts móveis responsivos e tratamento de gestos e animações",
            "Gerenciamento de estado na aplicação móvel (ex: BLoC, Riverpod, Redux)",
            "Consumo de APIs REST e persistência local (SQLite/Hive)",
            "Integração com recursos nativos do aparelho (sensores, câmera, push notifications)",
            "Automatização de builds e distribuição com Fastlane e Google Play / App Store"
        ]
    },

    "qa": {
        "id": "qa",
        "name": "Engenharia de Qualidade e Testes (QA)",
        "icon": "🔍",
        "summary": "Foco em testes automatizados, confiabilidade de software e processos de qualidade.",
        "description": (
            "O Engenheiro de Qualidade (QA / SDET) é o defensor incansável da confiabilidade do software. "
            "Ele projeta estratégias de testes contínuos, automação de ponta a ponta (E2E), testes de carga, "
            "desempenho e regressão. Atua preventivamente desde a definição de requisitos (Shift-Left Testing) "
            "para garantir que falhas e bugs sejam erradicados antes de chegarem aos usuários reais."
        ),
        "key_skills": [
            "Estratégia e pirâmide de testes (Unitários, Integração, Contrato, E2E)",
            "Desenvolvimento de frameworks de testes automatizados",
            "Testes de carga, estresse e desempenho (Performance Testing)",
            "Shift-Left Testing e garantia de critérios de aceitação em BDD/Gherkin",
            "Integração de baterias de testes em esteiras automatizadas de CI/CD"
        ],
        "technologies": [
            "Cypress, Playwright, Selenium WebDriver",
            "PyTest, JUnit, TestNG, Jest",
            "Postman, Newman, RestAssured (testes de API)",
            "JMeter, k6 (testes de carga e estresse)",
            "Cucumber / Gherkin (BDD), Jira / Xray"
        ],
        "salary_range": {
            "junior": "R$ 3.600 - R$ 5.800",
            "pleno": "R$ 6.800 - R$ 11.000",
            "senior": "R$ 12.000 - R$ 19.000+"
        },
        "market_demand": "Alta (A complexidade de microsserviços exige automação rigorosa de qualidade)",
        "roadmap": [
            "Fundamentos de testes de software, casos de teste e conceitos de qualidade (ISTQB)",
            "Lógica de programação aplicada à automação de scripts (Python ou JavaScript)",
            "Automação de testes de API RESTful com Postman e bibliotecas de código",
            "Automação de interfaces web e E2E com Playwright ou Cypress",
            "Testes de carga e estresse utilizando k6 ou JMeter",
            "Execução de baterias de testes integradas no pipeline de CI/CD"
        ]
    },

    "pm": {
        "id": "pm",
        "name": "Gestão de Produtos (Product Management)",
        "icon": "🧭",
        "summary": "Foco na ponte entre negócio, design e desenvolvimento, metodologias ágeis e priorização de produto.",
        "description": (
            "O Product Manager (Gerente de Produto) é o líder estratégico na interseção entre "
            "as necessidades dos clientes, a viabilidade técnica da engenharia e a rentabilidade do negócio. "
            "Ele define a visão do produto, conduz pesquisas de descoberta (Discovery), prioriza backlogs, "
            "estabelece métricas de sucesso (OKRs/KPIs) e alinha equipes multidisciplinares para gerar valor contínuo."
        ),
        "key_skills": [
            "Product Discovery e validação de hipóteses com usuários reais",
            "Priorização estratégica de backlog (RICE, MoSCoW, Value vs Effort)",
            "Análise de dados de produto e métricas de engajamento (Retention, Churn, LTV, CAC)",
            "Comunicação executiva, facilitação de ritos ágeis e gestão de stakeholders",
            "Visão de negócio, estratégia de monetização e roadmap evolutivo"
        ],
        "technologies": [
            "Jira, Confluence, Trello, Linear, Notion",
            "Miro, FigJam (dinâmicas e ideação colaborativa)",
            "Mixpanel, Amplitude, Google Analytics, Hotjar (Product Analytics)",
            "Figma (leitura e feedback de protótipos)",
            "SQL básico para extração independente de dados de produto"
        ],
        "salary_range": {
            "junior": "R$ 5.000 - R$ 8.000",
            "pleno": "R$ 9.500 - R$ 15.500",
            "senior": "R$ 16.000 - R$ 27.000+"
        },
        "market_demand": "Muito Alta (O alinhamento entre investimento em tech e retorno financeiro depende do PM)",
        "roadmap": [
            "Fundamentos de Gestão de Produto e Metodologias Ágeis (Scrum, Kanban)",
            "Técnicas de Product Discovery, entrevistas com usuários e testes de usabilidade",
            "Frameworks de priorização de demandas (RICE, Kano Model, Matriz de Esforço x Impacto)",
            "Definição de métricas de produto e acompanhamento de OKRs/KPIs",
            "Uso de ferramentas analíticas para entender o funil de retenção do usuário",
            "Liderança por influência, storytelling executivo e negociação com stakeholders"
        ]
    }
}
