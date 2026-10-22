# Matriz de Decisão e Engenharia de Conhecimento

Este documento detalha a modelagem de conhecimento do **Consultor Inteligente de Carreiras em TI**, explicitando as dimensões de entrada, a matriz de correspondência lógica e o mapeamento formal de regras do motor de inferência **Experta**.

---

## 1. As 10 Trilhas de Carreira no Escopo

| ID Trilha | Nome da Trilha | Foco Central | Tecnologias Principais |
|---|---|---|---|
| `backend` | **Desenvolvimento Back-end** | Lógica de negócio, APIs REST/gRPC, servidores e bancos relacionais/não-relacionais | Java (Spring), C#, Python (FastAPI), Go, PostgreSQL, Redis |
| `frontend` | **Desenvolvimento Front-end & UI/UX** | Interfaces web responsivas, componentes reativos, design systems e acessibilidade | React, Next.js, Vue, TypeScript, Tailwind CSS, Figma |
| `data_science` | **Ciência de Dados e Machine Learning** | Estatística inferencial, modelos preditivos, NLP, visão computacional e IA | Python, Pandas, Scikit-Learn, PyTorch, TensorFlow |
| `data_engineering` | **Engenharia de Dados** | Pipelines escaláveis (ETL/ELT), Data Lakes, Data Warehouses e computação distribuída | Apache Spark, Airflow, dbt, Kafka, BigQuery, Snowflake, SQL |
| `cybersecurity` | **Cibersegurança (Security / Pentesting)** | Defesa cibernética, testes de intrusão, análise de vulnerabilidades e criptografia | Kali Linux, Wireshark, Burp Suite, Nmap, SIEM, Python/Bash |
| `devops` | **DevOps & SRE** | Automação de CI/CD, contêineres, observabilidade, confiabilidade e IaC | Docker, Kubernetes, Terraform, GitHub Actions, Prometheus |
| `cloud` | **Computação em Nuvem (Cloud Architecture)** | Arquiteturas distribuídas escaláveis, migração corporativa e governança FinOps | AWS, Azure, GCP, CloudFormation, Terraform, IAM |
| `mobile` | **Desenvolvimento Mobile** | Aplicativos móveis (iOS/Android), ciclo de vida móvel e hardware nativo | Flutter, React Native, Swift (iOS), Kotlin (Android) |
| `qa` | **Engenharia de Qualidade e Testes (QA)** | Testes automatizados (E2E, carga, estresse), shift-left e prevenção de bugs | Cypress, Playwright, Selenium, PyTest, k6, Postman |
| `pm` | **Gestão de Produtos (Product Management)** | Descoberta de produto, priorização de backlog, estratégia de negócio e ritos ágeis | Jira, Miro, Mixpanel, Discovery, Scrum, Kanban |

---

## 2. Dimensões de Avaliação da Entrevista Dinâmica

1. **Afinidade Matemática e Estatística:**
   - *Alta:* Essencial para modelos estatísticos, Machine Learning e algoritmos complexos.
   - *Média:* Suficiente para raciocínio lógico estruturado, engenharia e arquitetura.
   - *Baixa:* Favorece áreas focadas em experiência do usuário, design ou gestão humana.

2. **Preferência de Atuação Diária:**
   - O que o profissional mais tem prazer em executar rotineiramente (lógica pura, telas, dados brutos, segurança, esteiras, nuvem, mobile, testes, negócios).

3. **Linguagem / Ferramenta de Maior Afinidade:**
   - Ecossistema de linguagens e ferramentas dominado ou almejado pelo usuário.

4. **Tipo de Entrega de Valor Preferida:**
   - Como o usuário mede a satisfação do seu trabalho (sistemas estáveis, telas encantadoras, modelos preditivos, blindagem, etc.).

5. **Desafio Diário Estimulante:**
   - Resolução de gargalos específicos que geram engajamento intelectual.

6. **Equilíbrio entre Código e Pessoas/Negócio:**
   - Foco profundo em código técnico vs foco em colaboração e alinhamento executivo.

7. **Ambiente / Foco em Dispositivos:**
   - Dispositivos móveis, redes/servidores físicos, provedores gerenciados em nuvem ou agnosticismo de hardware.

---

## 3. Matriz de Correlação Lógica (Perguntas vs Trilhas)

A tabela abaixo sintetiza como cada resposta se correlaciona primariamente (★★★) e secundariamente (★) com as 10 carreiras:

| Dimensão / Resposta | Back | Front | Data Sci | Data Eng | Cyber | DevOps | Cloud | Mobile | QA | PM |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Matemática: Alta** | ★ | - | ★★★ | ★ | - | - | - | - | - | - |
| **Matemática: Baixa** | - | ★★★ | Penal | - | - | - | - | ★★ | - | - |
| **Atuação: Lógica & APIs** | ★★★ | - | - | ★ | - | - | - | - | - | - |
| **Atuação: Interfaces & UI/UX** | - | ★★★ | - | - | - | - | - | ★ | - | - |
| **Atuação: Modelagem & IA** | - | - | ★★★ | - | - | - | - | - | - | - |
| **Atuação: Pipelines & Data Lakes** | - | - | ★ | ★★★ | - | - | - | - | - | - |
| **Atuação: Defesa & Pentest** | - | - | - | - | ★★★ | - | - | - | - | - |
| **Atuação: CI/CD & Contêineres** | - | - | - | - | - | ★★★ | ★ | - | - | - |
| **Atuação: Arquitetura Nuvem** | - | - | - | - | - | ★ | ★★★ | - | - | - |
| **Atuação: Apps Mobile** | - | - | - | - | - | - | - | ★★★ | - | - |
| **Atuação: Testes & Qualidade** | - | - | - | - | - | - | - | - | ★★★ | - |
| **Atuação: Gestão de Produto** | - | - | - | - | - | - | - | - | - | ★★★ |
| **Ferramenta: Python** | ★ | - | ★★★ | ★ | - | - | - | - | - | - |
| **Ferramenta: JS/TS** | ★ | ★★★ | - | - | - | - | - | ★ | - | - |
| **Ferramenta: Java/C#/Go** | ★★★ | - | - | - | - | - | ★ | - | - | - |
| **Ferramenta: SQL/Spark/Airflow** | ★ | - | ★ | ★★★ | - | - | - | - | - | - |
| **Ferramenta: Linux/Bash/Redes** | - | - | - | - | ★★★ | ★ | - | - | - | - |
| **Ferramenta: Docker/K8s/Terraform** | - | - | - | - | - | ★★★ | ★ | - | - | - |
| **Ferramenta: AWS/Azure/GCP** | - | - | - | - | - | ★ | ★★★ | - | - | - |
| **Ferramenta: Flutter/Swift/Kotlin** | - | - | - | - | - | - | - | ★★★ | - | - |
| **Ferramenta: Cypress/PyTest/JUnit** | - | - | - | - | - | - | - | - | ★★★ | - |
| **Ferramenta: Jira/Miro/Ágil** | - | - | - | - | - | - | - | - | - | ★★★ |

---

## 4. Catálogo das Regras Lógicas do Experta

### 4.1 Regras de Atuação Diária (R01 a R10)
- **R01 (`backend`):** `SE work_preference = 'Lógica de negócios, APIs e bancos de dados' ENTÃO backend +35 pts`
- **R02 (`frontend`):** `SE work_preference = 'Interfaces visuais interativas, design e experiência do usuário' ENTÃO frontend +35 pts`
- **R03 (`data_science`):** `SE work_preference = 'Modelagem estatística, machine learning e inteligência artificial' ENTÃO data_science +35 pts`
- **R04 (`data_engineering`):** `SE work_preference = 'Pipelines de dados, arquitetura ETL/ELT e Data Lakes' ENTÃO data_engineering +35 pts`
- **R05 (`cybersecurity`):** `SE work_preference = 'Defesa cibernética, análise de vulnerabilidades e testes de invasão' ENTÃO cybersecurity +35 pts`
- **R06 (`devops`):** `SE work_preference = 'Automação de CI/CD, esteiras de deploy, contêineres e alta disponibilidade' ENTÃO devops +35 pts`
- **R07 (`cloud`):** `SE work_preference = 'Arquitetura de sistemas em nuvem, migração e infraestrutura escalável' ENTÃO cloud +35 pts`
- **R08 (`mobile`):** `SE work_preference = 'Aplicativos móveis nativos ou multiplataforma para smartphones' ENTÃO mobile +35 pts`
- **R09 (`qa`):** `SE work_preference = 'Testes automatizados, caça a bugs e garantia de qualidade' ENTÃO qa +35 pts`
- **R10 (`pm`):** `SE work_preference = 'Gestão de produto, estratégia de negócio, priorização e comunicação' ENTÃO pm +35 pts`

### 4.2 Regras de Linguagem e Ferramentas (R11 a R20)
- **R11 (`backend`):** `SE primary_tool = 'Java / C# / Go' ENTÃO backend +25 pts, cloud +5 pts`
- **R12 (`frontend`):** `SE primary_tool = 'JavaScript / TypeScript' ENTÃO frontend +22 pts, mobile +8 pts, backend +6 pts`
- **R13 (`data_science`):** `SE primary_tool = 'Python' ENTÃO data_science +18 pts, backend +10 pts, data_engineering +10 pts`
- **R14 (`data_engineering`):** `SE primary_tool = 'SQL / Ferramentas de Big Data (Spark, Airflow)' ENTÃO data_engineering +25 pts, data_science +8 pts, backend +6 pts`
- **R15 (`cybersecurity`):** `SE primary_tool = 'Linux / Bash / Ferramentas de Redes e Segurança' ENTÃO cybersecurity +25 pts, devops +10 pts`
- **R16 (`devops`):** `SE primary_tool = 'Docker / Kubernetes / Terraform / CI-CD' ENTÃO devops +25 pts, cloud +12 pts`
- **R17 (`cloud`):** `SE primary_tool = 'Nuvem AWS / Azure / GCP' ENTÃO cloud +25 pts, devops +10 pts`
- **R18 (`mobile`):** `SE primary_tool = 'Swift / Kotlin / Flutter / React Native' ENTÃO mobile +25 pts`
- **R19 (`qa`):** `SE primary_tool = 'Ferramentas de Teste (Cypress, Selenium, PyTest, JUnit)' ENTÃO qa +25 pts`
- **R20 (`pm`):** `SE primary_tool = 'Ferramentas de Gestão e Ágil (Jira, Trello, Miro, Notion)' ENTÃO pm +25 pts`

### 4.3 Regras de Entrega de Valor (R21 a R30)
- **R21 a R30:** Bonificam com +18 pts a trilha correspondente à entrega de valor almejada pelo usuário.

### 4.4 Regras de Desafios Diários (R31 a R40)
- **R31 a R40:** Bonificam com +14 a +16 pts a respectiva carreira alinhada à motivação de resolução de problemas específicos.

### 4.5 Regras Cruzadas de Desambiguação (R41 a R52)
As regras cruzadas garantem que perfis com gostos compartilhados não fiquem ambíguos:
- **R41_CROSS (Ciência de Dados vs Engenharia de Dados):**
  - `SE math_affinity = 'Alta' E (trabalho analítico OU hipóteses estatísticas OU modelos preditivos) ENTÃO data_science +18 pts`
- **R42_CROSS (Engenharia de Dados vs Ciência de Dados):**
  - `SE (pipelines ETL OU Spark/Airflow OU terabytes distribuídos) E (fluxo confiável de dados OU código profundo) ENTÃO data_engineering +18 pts`
- **R43_CROSS (Front-end Web vs Mobile):**
  - `SE gosto por interfaces E foco agnóstico a hardware ENTÃO frontend +16 pts`
- **R44_CROSS (Mobile vs Front-end):**
  - `SE gosto por interfaces/Flutter E foco em smartphones/tablets ENTÃO mobile +18 pts`
- **R45_CROSS (DevOps vs Cloud):**
  - `SE foco em CI/CD, esteiras e contêineres K8s ENTÃO devops +16 pts`
- **R46_CROSS (Cloud vs DevOps):**
  - `SE foco em arquitetura global de nuvem, migração e provedores hyperscalers ENTÃO cloud +16 pts`
- **R47_CROSS (Cibersegurança vs Infra):**
  - `SE redes/firewalls E postura adversarial/pentest ENTÃO cybersecurity +18 pts`
- **R48_CROSS (QA vs Dev Convencional):**
  - `SE foco em critérios de aceitação e software sem bugs ENTÃO qa +18 pts`
- **R49_CROSS (Product Management vs Engenharia Técnica):**
  - `SE foco predominante em pessoas, facilitação e receita ENTÃO pm +22 pts`
- **R50_MATH (Bônus Lógico Geral):**
  - `SE math_affinity = 'Alta' E NÃO Ciência de Dados ENTÃO backend +5 pts, data_engineering +5 pts`
- **R51_PENALTY (Penalidade por Baixa Matemática em IA):**
  - `SE math_affinity = 'Baixa' ENTÃO data_science -20 pts, frontend +5 pts`
- **R52_INFRA (Bônus Redes Corporativas):**
  - `SE foco em redes e servidores físicos E NÃO Cibersegurança ENTÃO devops +8 pts, cloud +8 pts`
