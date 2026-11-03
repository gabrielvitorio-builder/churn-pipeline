# Pipeline Preditivo de Churn com Scikit-Learn e FastAPI

Tech Challenge da pos-graduacao. O projeto cobre todo o caminho de um modelo de classificacao, da analise exploratoria ate a predicao servida por uma API REST, para uma operadora de telecomunicacoes que precisa identificar clientes com risco de cancelamento.

## Resultado em resumo

| Modelo | ROC-AUC (CV 5 folds) | ROC-AUC (teste) | F1 (teste) | Recall (teste) |
|---|---|---|---|---|
| Random Forest (campeao) | 0,8471 | 0,8425 | 0,6303 | 0,8021 |
| Regressao Logistica (baseline) | 0,8460 | 0,8414 | 0,6180 | 0,7246 |
| MLP | 0,8423 | 0,8369 | 0,6156 | 0,6979 |

O Random Forest foi escolhido pelo maior ROC-AUC medio na validacao cruzada. As diferencas entre os modelos ficam dentro do desvio entre folds (cerca de 0,01), e o Model Card discute isso com detalhe.

## Estrutura do repositorio

```
.
├── api/index.py                 ponto de entrada do deploy na Vercel
├── data/raw/                    dataset Telco Customer Churn (IBM)
├── docs/
│   ├── ml_canvas.md             ML Canvas (stakeholders, metricas, riscos)
│   ├── model_card.md            Model Card (desempenho, limitacoes, vieses)
│   ├── roteiro_video_star.md    roteiro do video de 5 minutos
│   ├── figures/                 graficos da EDA e da modelagem
│   └── results/                 tabela comparativa, importancias e metricas por subgrupo
├── models/                      modelo campeao (.joblib) e metadados
├── notebooks/
│   ├── 01_eda_baseline.ipynb    EDA, metricas e baseline
│   └── 02_modelagem_comparacao.ipynb   Random Forest, MLP e comparacao
├── src/
│   ├── churn/                   codigo produtivo (dados, pipeline, treino, predicao)
│   └── churn_api/               API FastAPI e contratos Pydantic
├── tests/                       testes pytest
├── pyproject.toml
├── requirements.txt             dependencias de execucao (API e modelo)
└── requirements-dev.txt         dependencias de desenvolvimento (testes e notebooks)
```

Os notebooks servem para experimentar e explicar. Toda a logica reutilizavel mora em `src/` e e importada pelos notebooks, pelos testes e pela API.

## Como instalar

Requer Python 3.11 ou superior. No terminal do VS Code, na raiz do projeto.

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux ou macOS
source .venv/bin/activate

pip install -r requirements-dev.txt
pip install -e . --no-deps
```

A versao do scikit-learn esta fixada em 1.9.1 porque o arquivo `.joblib` do modelo depende dela. Se o `pip` nao encontrar essa versao para a sua versao do Python, use Python 3.12 ou 3.13, ou apenas rode o treino novamente depois de instalar uma versao compativel.

## Como rodar

**Treinar e comparar os modelos.** Gera o modelo campeao, os metadados e a tabela comparativa.

```bash
python -m churn.train
```

**Rodar os testes.**

```bash
pytest
```

**Subir a API localmente.**

```bash
uvicorn churn_api.main:app --reload --app-dir src
```

A documentacao interativa fica em http://127.0.0.1:8000/docs.

**Checar a saude da API.**

```bash
curl http://127.0.0.1:8000/health
```

**Pedir uma predicao.**

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"gender":"Female","SeniorCitizen":0,"Partner":"Yes","Dependents":"No","tenure":2,"PhoneService":"Yes","MultipleLines":"No","InternetService":"Fiber optic","OnlineSecurity":"No","OnlineBackup":"No","DeviceProtection":"No","TechSupport":"No","StreamingTV":"Yes","StreamingMovies":"Yes","Contract":"Month-to-month","PaperlessBilling":"Yes","PaymentMethod":"Electronic check","MonthlyCharges":95.5,"TotalCharges":191.0}'
```

Resposta esperada.

```json
{"churn_probability": 0.8688, "churn_prediction": true, "risk_level": "alto", "threshold": 0.449}
```

**Reproduzir as metricas por subgrupo.**

```bash
python -m churn.subgroups
```

**Abrir os notebooks.** Rode `jupyter lab` na raiz e abra a pasta `notebooks/`.

## Endpoints

| Metodo | Rota | Descricao |
|---|---|---|
| GET | `/health` | Estado da API e se o modelo foi carregado |
| POST | `/predict` | Recebe os dados de um cliente e devolve probabilidade, classe e nivel de risco |

O nivel de risco e baixo abaixo do limiar do modelo (0,449), medio entre o limiar e 0,70, e alto a partir de 0,70. Entradas invalidas retornam 422, e a ausencia do arquivo do modelo retorna 503.

## Metricas

- **Tecnica principal** ROC-AUC, com F1, recall e precisao da classe churn como apoio.
- **Negocio** valor liquido da campanha de retencao, calculado com as premissas do ML Canvas e editaveis em `src/churn/config.py`.

## Reprodutibilidade

- Seed fixa em 42 para a divisao, os modelos e a validacao cruzada.
- Divisao estratificada de 80% treino e 20% teste.
- Pre-processamento dentro do `Pipeline`, entao imputacao, escala e one-hot sao ajustados apenas nos dados de treino de cada fold.
- O conjunto de teste e usado uma unica vez, na avaliacao final.

## Deploy na Vercel (opcional)

O repositorio ja inclui `api/index.py`, `vercel.json` e `.vercelignore`.

```bash
npm i -g vercel
vercel login
vercel --prod
```

Tambem e possivel importar o repositorio do GitHub pelo painel da Vercel, sem configurar nada alem do que ja esta no projeto. Depois do deploy, teste `https://SEU-PROJETO.vercel.app/health`.

Duas observacoes. A Vercel limita o tamanho da funcao serverless, e scikit-learn com pandas ficam perto desse limite, entao o `requirements.txt` foi mantido apenas com o necessario para inferencia. O Cloudflare Workers nao foi usado porque o suporte a scikit-learn no ambiente Python deles e limitado.

## Documentacao

- [ML Canvas](docs/ml_canvas.md)
- [Model Card](docs/model_card.md)
- [Roteiro do video STAR](docs/roteiro_video_star.md)

## Dados

Telco Customer Churn, publicado pela IBM. Copia em `data/raw/telco_customer_churn.csv`, originada de https://github.com/IBM/telco-customer-churn-on-icp4d.

## Autor

gabrielvitorio-builder (gabrielvitorioadms@gmail.com)
