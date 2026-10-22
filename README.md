# 🎓 Consultor Inteligente de Carreiras em TI
### Sistema Especialista Baseado em Regras em Python (Experta & Streamlit)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Rule Engine: Experta](https://img.shields.io/badge/Engine-Experta%201.9.4-green.svg)](https://github.com/nilp0inter/experta)
[![UI: Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![Tests: Pytest](https://img.shields.io/badge/Tests-15%20Passed-brightgreen.svg)](https://pytest.org/)

---

## 📌 Visão Geral do Projeto

O **Consultor Inteligente de Carreiras em TI** é um **Sistema Especialista baseado em regras lógicas** do tipo *SE-ENTÃO* que atua como orientador vocacional avançado em Tecnologia da Informação. 

O sistema entrevista o usuário por meio de perguntas objetivas sobre suas preferências de trabalho, conhecimentos técnicos prévios, afinidade matemática e estilo de atuação diária. Utilizando um **motor de inferência baseado no algoritmo Rete com encadeamento para frente (*forward chaining*)**, o consultor diagnostica a trilha de carreira ideal dentre 10 opções possíveis e **justifica transparentemente** todas as regras disparadas que fundamentaram a decisão.

---

## 🎯 Escopo: As 10 Trilhas de Carreira

O sistema é calibrado para diferenciar com precisão 10 áreas da tecnologia:

1. **⚙️ Desenvolvimento Back-end:** Foco em lógica de servidores, construção de APIs REST/gRPC, regras de negócio e modelagem de bancos de dados relacionais e NoSQL.
2. **🎨 Desenvolvimento Front-end & UI/UX:** Foco em interfaces web responsivas, componentes reativos, design systems, acessibilidade e experiência do usuário final.
3. **🧠 Ciência de Dados e Machine Learning:** Foco em métodos estatísticos, modelagem preditiva supervisionada/não-supervisionada, Processamento de Linguagem Natural e Inteligência Artificial.
4. **🏗️ Engenharia de Dados:** Foco em arquitetura e escalabilidade de pipelines de dados (ETL/ELT), orquestração de fluxos massivos e infraestrutura para Data Lakes e Data Warehouses.
5. **🛡️ Cibersegurança (Security / Pentesting):** Foco em defesa cibernética, análise de vulnerabilidades, perícia digital, criptografia, redes seguras e testes de invasão éticos.
6. **♾️ DevOps & SRE:** Foco em automação de esteiras de integração e entrega contínua (CI/CD), orquestração de contêineres em escala (Kubernetes) e confiabilidade operacional (Site Reliability Engineering).
7. **☁️ Computação em Nuvem (Cloud Architecture):** Foco em desenho de topologias distribuídas, migração corporativa para nuvem (AWS/Azure/GCP), alta disponibilidade e otimização financeira (FinOps).
8. **📱 Desenvolvimento Mobile:** Foco no ecossistema de dispositivos móveis (smartphones e tablets), abrangendo desenvolvimento multiplataforma (Flutter/React Native) ou nativo (Swift/Kotlin).
9. **🔍 Engenharia de Qualidade e Testes (QA):** Foco em automação de baterias de testes (unitários, integração, E2E, carga), prevenção de falhas em esteiras de software e processos de qualidade.
10. **🧭 Gestão de Produtos (Product Management):** Foco na interseção entre estratégia de negócio, priorização de backlogs, liderança de ritos ágeis (Scrum/Kanban) e alinhamento de stakeholders.

---

## 🧠 Arquitetura do Sistema e Encadeamento para Frente

```
               [ Respostas do Usuário / Persona ]
                               │
                               ▼
                    [ Fato: UserProfile ]
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
 [ Regras Diretas (R01-R10) ]          [ Regras de Ferramentas (R11-R20) ]
 [ Regras de Valor (R21-R30) ]         [ Regras de Desafios (R31-R40) ]
            │                                     │
            └──────────────────┬──────────────────┘
                               ▼
               [ Regras Cruzadas de Desambiguação ]
                   (Ex: Data Science vs Data Eng)
                   (Ex: Front-end Web vs Mobile)
                   (Ex: DevOps vs Cloud Arch)
                               │
                               ▼
        [ Diagnóstico Consolidado & Justificativa Aberta ]
               ├── Trilha Recomendada (com %)
               ├── Regras Lógicas Disparadas
               ├── Ranking das 10 Carreiras
               └── Roteiro de Aprendizado (Roadmap)
```

O sistema utiliza a biblioteca **Experta** (implementação em Python do algoritmo Rete de Sistemas Especialistas do padrão CLIPS).

### Destaque da Engenharia de Regras (52 Regras Implementadas):
- **10 Regras de Atuação Direta:** Identificam o núcleo de tarefas do dia a dia.
- **10 Regras de Ferramentas & Linguagens:** Pontuam o domínio de stacks específicas.
- **10 Regras de Entrega de Valor:** Capturam o propósito profissional almejado.
- **10 Regras de Desafios Técnicos:** Avaliam o tipo de problema que mais motiva o usuário.
- **12 Regras Cruzadas e Penalidades:** Eliminam ambiguidades em perfis com interesses sobrepostos (por exemplo, diferenciando rigor estatístico em Ciência de Dados de arquitetura de dados distribuída em Engenharia de Dados).

---

## ⚡ Personas de Teste (Validação com 100% de Acerto)

O sistema possui personas pré-configuradas para demonstração e validação automatizada:

| Persona | Perfil | Trilha Esperada | Diagnóstico Obtido | Status |
|---|---|---|---|:---:|
| **Ana Silva** | Perfil Analítico / Estatístico | Ciência de Dados | `data_science` (100.0%) | ✅ **Aprovado** |
| **Carlos Rocha** | Perfil Infraestrutura / Redes | Cibersegurança | `cybersecurity` (100.0%) | ✅ **Aprovado** |
| **Beatriz Lima** | Perfil Criativo / UI/UX | Front-end & UI/UX | `frontend` (100.0%) | ✅ **Aprovado** |
| **Lucas Mendes** | Perfil Negócios / Estratégia | Product Management | `pm` (100.0%) | ✅ **Aprovado** |
| **Eduardo Santos** | Perfil Big Data / Pipelines | Engenharia de Dados | `data_engineering` (100.0%) | ✅ **Aprovado** |
| **Mariana Costa** | Perfil Automação / Contêineres | DevOps & SRE | `devops` (100.0%) | ✅ **Aprovado** |
| **Gabriel Alencar**| Perfil APIs / Servidor | Back-end | `backend` (83.6%) | ✅ **Aprovado** |
| **Rafael Nogueira**| Perfil Dispositivos Móveis | Mobile | `mobile` (100.0%) | ✅ **Aprovado** |
| **Camila Duarte** | Perfil Qualidade / Bugs | QA & Testes | `qa` (100.0%) | ✅ **Aprovado** |
| **Rodrigo Fonseca**| Perfil Nuvem / FinOps | Cloud Architecture | `cloud` (100.0%) | ✅ **Aprovado** |

---

## 🚀 Como Instalar e Executar

### 1. Pré-requisitos
- Python versão **3.10 ou superior** instalado.
- Gerenciador de pacotes `pip`.

### 2. Clonar o Repositório ou Abrir a Pasta
```bash
cd C:\Users\Pichau\PycharmProjects\PythonProject
```

### 3. Criar e Ativar o Ambiente Virtual (Opcional, mas Recomendado)
```bash
# Windows PowerShell / CMD
python -m venv .venv
.venv\Scripts\activate
```

### 4. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 5. Executar a Interface Web (Streamlit)
```bash
streamlit run app.py
```
> O Streamlit abrirá automaticamente no seu navegador em `http://localhost:8501`. Na barra lateral, você pode selecionar e testar qualquer uma das Personas instantaneamente ou preencher o formulário manualmente!

### 6. Executar via Linha de Comando (Modos CLI e Demonstração)
```bash
# Modo Demonstração e Validação das Personas no Console:
python main.py --demo

# Modo Entrevista Interativa no Terminal:
python main.py --cli

# Iniciar o Streamlit pelo main.py:
python main.py --web
```

### 7. Executar a Suíte de Testes Automatizados
```bash
pytest -v
```
Todos os 15 testes unitários de integração, desambiguação e regras de justificativa serão executados.

---

## 📂 Estrutura do Repositório

```
PythonProject/
├── app.py                      # Interface Web Interativa desenvolvida com Streamlit
├── main.py                     # Inicializador CLI e executor de validação
├── requirements.txt            # Dependências do projeto
├── README.md                   # Documentação oficial do projeto
├── matriz_decisao.md           # Matriz de Decisão e mapeamento formal das 52 regras
├── engine/                     # Núcleo do Sistema Especialista (Experta)
│   ├── __init__.py             # Compatibilidade Python 3.10+ e exportação de classes
│   ├── facts.py                # Fatos do motor (UserProfile, etc.)
│   ├── rules.py                # Base de Conhecimento formal com 52 regras Experta
│   └── advisor.py              # Fachada orquestradora e normalizadora do diagnóstico
├── data/                       # Catálogos de dados e personas
│   ├── __init__.py
│   ├── career_tracks.py        # Metadados das 10 carreiras (salários, roadmaps, etc.)
│   └── personas.py             # Definição das Personas de Teste validadas
└── tests/                      # Testes automatizados
    ├── __init__.py
    └── test_advisor.py         # Testes com PyTest das personas e regras cruzadas
```

---

## ⚖️ Transparência e Explicabilidade

Diferente de sistemas baseados em caixas-pretas estatísticas, o Consultor Inteligente de Carreiras em TI detalha:
1. **Regras de Ativação:** Qual regra foi disparada pelo fato declarado e a pontuação somada.
2. **Regras Cruzadas:** A justificativa técnica que desempatou a carreira recomendada de outras trilhas similares.
3. **Ranking Comparativo:** Índice percentual de compatibilidade com cada uma das 10 trilhas.
4. **Roadmap de Estudos:** Próximos passos e tecnologias mandatórias para ingressar na carreira indicada.
5. <img width="571" height="227" alt="image" src="https://github.com/user-attachments/assets/c4b6524a-174b-483d-91d8-f06c11caf75d" />

