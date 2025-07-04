# ds_real_state_analysis

Projeto de Data Science voltado à análise de dados do mercado imobiliário, utilizando webscraping dinâmico (Playwright, Scrapy) e técnicas avançadas de Machine Learning/Deep Learning.

---

## Instalação e execução rápida

### 1. Clone este repositório

```bash
git clone https://github.com/seuusuario/ds_real_state_analysis.git
cd ds_real_state_analysis
```

### 2. Crie e ative um ambiente virtual

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

> **Obs.:** Para rodar o Playwright, é necessário instalar os browsers uma única vez:

```bash
playwright install
```

### 4. Execute os scripts principais

```bash
python src/collect.py
python src/normalize.py
jupyter notebook notebooks/exploracao_inicial.ipynb
```

---

## Organização

- `src/` — Scripts de coleta (Scrapy/Playwright), normalização, banco de dados e utilidades.
- `data/` — Dados brutos e processados (não são versionados).
- `notebooks/` — Análises, explorações e modelos de ML/DL.
- `docs/` — Documentos e imagens.

---

## Observações

- O projeto no momento não tem fins financeiros

---

## OBJETIVO:

- Aplicar todos os conceitos apresentados na ISTQB CT-AI

┌── src/
│
├── coleta/ # Crawlers e coletores (Scrapy, Playwright)
├── processamento/ # Normalização, ETL, transformação de dados
├── banco_dados/ # Scripts de integração com bancos/armazenamento
├── analises/
│ ├── qualidade_dados.py # Checagens: nulos, duplicados, outliers
│ ├── envenenamento_dados.py # Detecção de data poisoning, drift intencional
│ ├── ataque_contraditorio.py # Geração/avaliação de adversarial attacks
│ ├── viés_fairness.py # Métricas e relatórios de viés, paridade, equidade
│ ├── explicabilidade.py # SHAP, LIME, saliency maps, etc.
│ ├── robustez_modelo.py # Testes de stress, mutações, perturbações controladas
│ └── integridade_notebooks.py # Checagem automática de execução e outputs
│
├── notebooks/
│ ├── exploracao_dados.ipynb
│ ├── treinamento_modelo.ipynb
│ ├── avaliacao_robustez.ipynb # Ataques, perturbações, adversarial
│ ├── explicabilidade_e_etica.ipynb # Foco em transparência e justificativa
│ └── template_analise_validacao.ipynb # Estrutura sugerida para novas análises
│
├── docs/
│ ├── criterios_aceitacao.md # O que é considerado “ok” para cada aspecto
│ └── guia_analises.md # Breve explicação dos scripts e métricas
│
├── data/
│ ├── raw/
│ └── processed/
└── requirements.txt
