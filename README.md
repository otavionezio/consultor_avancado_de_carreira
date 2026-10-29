#  Consultor Avançado de Carreiras em TI
### Sistema Especialista para Mapeamento, Compatibilidade e Trilha de Carreira (Python & Streamlit)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Knowledge Base: JSON](https://img.shields.io/badge/Base%20de%20Conhecimento-JSON-green.svg)](data/regras_carreiras.json)
[![UI: Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![Tests: Pytest](https://img.shields.io/badge/Tests-50%20Passed-brightgreen.svg)](https://pytest.org/)

---

##  Visão Geral do Projeto

O **Consultor Avançado de Carreiras em TI** é um **Sistema Especialista baseado em regras** do tipo *SE-ENTÃO* que:

1. **Mapeia o perfil** do usuário com um questionário em etapas, diferenciando **afinidade** (o que a pessoa gosta de fazer) de **proficiência** (o que ela realmente sabe fazer);
2. **Calcula a compatibilidade** (0% a 100%) com 10 carreiras de TI, apresentando ranking, Top 3, justificativas e tratamento de perfis ambíguos;
3. **Analisa lacunas de competências** (*Skill Gap Analysis*) em relação ao nível Júnior da carreira escolhida;
4. **Gera um roadmap personalizado** conforme as lacunas, o nível atual e o tempo disponível para estudar.

Toda a regra de negócio — perfis das carreiras, pesos, regras, competências e recomendações — fica na base de conhecimento externa [`data/regras_carreiras.json`](data/regras_carreiras.json), carregada dinamicamente. Nenhuma regra está fixa no código Python.

> Os percentuais representam **compatibilidade segundo as regras do sistema**, e não probabilidade de sucesso profissional.

---

##  Escopo: As 10 Trilhas de Carreira

1. **Back-end:** lógica de servidores, APIs REST/gRPC, regras de negócio e bancos de dados.
2. **Front-end & UI/UX:** interfaces web responsivas, frameworks reativos, design systems e acessibilidade.
3. **Ciência de Dados:** estatística, modelagem preditiva, Machine Learning e IA.
4. **Engenharia de Dados:** pipelines ETL/ELT, orquestração, Data Lakes e Data Warehouses.
5. **Cibersegurança:** defesa cibernética, análise de vulnerabilidades, redes seguras e pentest.
6. **DevOps & SRE:** CI/CD, contêineres, Kubernetes, IaC e observabilidade.
7. **Arquitetura de Cloud:** topologias em AWS/Azure/GCP, migração, alta disponibilidade e FinOps.
8. **Desenvolvimento Mobile:** apps nativos ou multiplataforma (Flutter/React Native/Kotlin/Swift).
9. **QA e Testes:** estratégia de testes, automação E2E, testes de API e de carga.
10. **Product Management:** discovery, priorização, métricas de produto e gestão de stakeholders.

---

##  Arquitetura

```
        [ Questionário em etapas / Persona / CLI ]
                          │
                          ▼
      Normalização das respostas (perfil, afinidades,
      proficiências, preferências; ausentes descartadas)
                          │
                          ▼
     ┌──────────── Base de Conhecimento (JSON) ────────────┐
     │ perfis das carreiras · pesos · regras SE-ENTÃO ·    │
     │ competências Júnior · pré-requisitos · projetos ·   │
     │ certificações · parâmetros do motor                 │
     └─────────────────────────────────────────────────────┘
                          │
                          ▼
   Motor de Inferência (engine/inference.py)
     1. Encadeamento para frente (ciclos reconhecer-agir,
        lógica de três valores para respostas ausentes)
     2. Pontuação ponderada: afinidades · preferências · proficiência
     3. Fatores de certeza (MYCIN) para evidências favoráveis/desfavoráveis
                          │
          ┌───────────────┼─────────────────┐
          ▼               ▼                 ▼
  Ranking + Top 3   Skill Gap Analysis   Roadmap personalizado
  justificativas    (engine/skill_gap)   (engine/roadmap)
  ambiguidade
                          │
                          ▼
           Interface Streamlit (app.py + ui/charts.py)
```

### Motor de inferência

- **Regras SE-ENTÃO (46):** regras de **derivação** (inferem traços como "perfil analítico" ou "perfil de infraestrutura"), de **evidência** (afinidades), de **desambiguação** (ex.: Ciência × Engenharia de Dados, Front-end × Mobile, DevOps × Cloud) e de **proficiência** (conhecimentos práticos). Os fatos derivados habilitam novas regras nos ciclos seguintes.
- **Respostas ausentes:** condições sobre fatos não informados ficam "desconhecidas" e a regra não dispara. Na pontuação, cada componente pesa conforme a evidência disponível, com um *prior* neutro; respostas ausentes reduzem a **confiança** da avaliação, mas não penalizam a compatibilidade.
- **Incerteza:** cada regra contribui com um fator de certeza entre -1 e +1. As contribuições são combinadas pelo modelo MYCIN e ajustam a pontuação base de forma limitada, mantendo o resultado entre 0% e 100% sem penalidades arbitrárias.
- **Perfis ambíguos:** quando carreiras ficam a menos de 5 pontos percentuais da primeira colocada, o sistema sinaliza a ambiguidade e aponta as afinidades que mais as diferenciam.
- **Afinidade × proficiência:** identifica talentos latentes (gosta, mas ainda não pratica) e competências sem interesse (domina, mas não gosta).

### Análise de lacunas e roadmap

- Cada competência exigida para o nível Júnior é classificada como **dominada**, **parcial** ou **ausente**, com prioridade calculada por peso, tamanho da lacuna e quantidade de competências que ela desbloqueia.
- A ordem de estudo é uma **ordenação topológica** dos pré-requisitos; pré-requisitos externos à carreira são incluídos automaticamente.
- O roadmap distribui as competências em **3 fases** (fundamentos, tecnologias prioritárias e diferenciais), calcula semanas conforme as horas semanais, verifica o prazo desejado e marca itens opcionais quando o plano não cabe no prazo.
- Cada etapa traz **recursos de aprendizagem e exercícios práticos**; cada fase termina com um **projeto de portfólio** que usa apenas competências já estudadas. **Certificações** são recomendadas conforme o nível atual.

---

##  Interface Streamlit

O questionário é apresentado em 5 etapas, com as respostas preservadas durante a navegação:

1. **Perfil pessoal:** objetivo, experiência, horas semanais, prazo e estilo de trabalho.
2. **Afinidades técnicas:** 14 afinidades em escala de 1 a 5 (com opção "Não informado") e preferências de atuação.
3. **Conhecimentos atuais:** proficiência de 1 a 5 em 54 competências, agrupadas por área.
4. **Resultados:** Top 3, ranking em barras, radar de afinidades, composição da pontuação, justificativas, regras disparadas e panorama de mercado.
5. **Plano de desenvolvimento:** análise de lacunas, roadmap por fases e semanas, projetos, certificações e recomendações.

A barra lateral permite carregar as personas de validação e exportar diagnóstico e plano em JSON.

---

##  Personas de Teste

| Persona | Perfil | Trilha Esperada | Compatibilidade | Status |
|---|---|---|---|:---:|
| **Ana Silva** | Analítico / Estatístico | Ciência de Dados | 85.3% | Aprovado |
| **Carlos Rocha** | Infraestrutura / Segurança | Cibersegurança | 87.7% | Aprovado |
| **Beatriz Lima** | Criativo / UI/UX | Front-end & UI/UX | 80.6% | Aprovado |
| **Lucas Mendes** | Negócios / Estratégia | Product Management | 89.4% | Aprovado |
| **Eduardo Santos** | Big Data / Pipelines | Engenharia de Dados | 85.7% | Aprovado |
| **Mariana Costa** | Automação / Contêineres | DevOps & SRE | 87.0% | Aprovado |
| **Gabriel Alencar** | APIs / Servidor | Back-end | 81.3% | Aprovado |
| **Rafael Nogueira** | Dispositivos Móveis | Mobile | 88.6% | Aprovado |
| **Camila Duarte** | Qualidade / Bugs | QA & Testes | 82.8% | Aprovado |
| **Rodrigo Fonseca** | Nuvem / FinOps | Cloud Architecture | 85.3% | Aprovado |

---

##  Como Instalar e Executar

### 1. Pré-requisitos
- Python **3.10 ou superior** e `pip`.

### 2. Clonar o repositório
```bash
git clone https://github.com/otavionezio/consultor_avancado_de_carreira.git
cd consultor_avancado_de_carreira
```

### 3. Criar e ativar o ambiente virtual (opcional, recomendado)
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 4. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 5. Executar a interface web
```bash
streamlit run app.py
```

### 6. Executar via linha de comando
```bash
# Validação das personas com diagnóstico e resumo do plano
python main.py --demo

# Entrevista interativa no terminal
python main.py --cli

# Iniciar o Streamlit pelo main.py
python main.py --web
```

### 7. Executar os testes
```bash
pytest -v
```
Os 50 testes cobrem a base de conhecimento, o motor de inferência, o tratamento de respostas ausentes, a ambiguidade, a análise de lacunas, o roadmap e as 10 personas.

---

##  Estrutura do Repositório

```
consultor_avancado_de_carreira/
├── app.py                      # Interface Streamlit em etapas
├── main.py                     # Demonstração das personas, CLI e inicialização web
├── requirements.txt
├── matriz_decisao.md           # Matriz de decisão da versão anterior (regras Experta)
├── data/
│   ├── regras_carreiras.json   # Base de conhecimento: carreiras, pesos, regras, competências
│   ├── career_tracks.py        # Catálogo das carreiras carregado do JSON
│   └── personas.py             # Personas de validação
├── engine/
│   ├── knowledge_base.py       # Carregamento e validação da base de conhecimento
│   ├── inference.py            # Motor de inferência (forward chaining + fatores de certeza)
│   ├── skill_gap.py            # Análise de lacunas de competências
│   ├── roadmap.py              # Gerador de roadmap personalizado
│   └── advisor.py              # Fachada usada pela interface e pela CLI
├── ui/
│   └── charts.py               # Gráficos Altair (ranking, radar, lacunas, composição)
└── tests/
    └── test_advisor.py         # Testes automatizados com PyTest
```

---

##  Como Evoluir a Base de Conhecimento

Alterações de regra de negócio são feitas apenas em `data/regras_carreiras.json`:

- **Nova regra:** adicione um item em `rules` com `if` (condições `all`/`any`/`not` sobre fatos como `affinities.math`, `proficiencies.sql`, `choices.work_preference` ou `traits.analytical`) e `then` (`infer` para derivar fatos ou `evidence` com fatores de certeza por carreira).
- **Pesos de uma carreira:** ajuste `affinity_profile` e `junior_competencies` em `careers`.
- **Competências e recursos:** edite `competencies` (pré-requisitos, horas, recursos e exercícios).
- **Parâmetros do motor:** pesos dos componentes, limiar de ambiguidade e limites de prioridade ficam em `parameters`.

A base é validada ao carregar: referências a carreiras, afinidades ou competências inexistentes geram erro descritivo.

---

## Evidências visuais 

<img width="1905" height="933" alt="image" src="https://github.com/user-attachments/assets/09d1d1b1-8924-4ea8-bb81-979a6395aa29" />

<img width="1908" height="932" alt="image" src="https://github.com/user-attachments/assets/17cacdc6-3649-4af1-928e-eeaf461e7258" />

<img width="1908" height="927" alt="image" src="https://github.com/user-attachments/assets/ff4d3551-a181-4498-aa0e-3d123fd572bd" />

<img width="1907" height="930" alt="image" src="https://github.com/user-attachments/assets/41ef9403-59af-45ea-8a3a-670d4f0ce565" />

<img width="1908" height="930" alt="image" src="https://github.com/user-attachments/assets/cf64b62b-e5e5-494d-b65e-c2b03f73f336" />

<img width="1910" height="934" alt="image" src="https://github.com/user-attachments/assets/74d90336-1a7b-405c-9bb8-710d5e45b5f4" />

<img width="1917" height="931" alt="image" src="https://github.com/user-attachments/assets/35df4c03-f654-4573-a6f6-caa1a0ee6626" />

<img width="1911" height="936" alt="image" src="https://github.com/user-attachments/assets/df200a40-c296-4f0c-b9a7-5b53164698b5" />







