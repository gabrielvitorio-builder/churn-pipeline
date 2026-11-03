# Roteiro e script do video (5 minutos, metodo STAR)

Este documento tem duas partes. A primeira e o roteiro, com o que aparece na tela em cada momento. A segunda e o script, com o texto sugerido para falar. O texto tem cerca de 590 palavras, que levam 4min30s de fala em ritmo de 130 palavras por minuto. Com os cliques da demonstracao, o video fica perto de 4min50s, entao o ensaio com cronometro e importante. Se passar de 4min55s, aplique os cortes indicados no plano B.

## Parte 1. Roteiro

### Visao geral

| Bloco | Tempo | Duracao | Palavras | Objetivo |
|---|---|---|---|---|
| Situation | 0:00 a 0:40 | 40s | 93 | Apresentar o problema de negocio e o dataset |
| Task | 0:40 a 1:15 | 35s | 78 | Dizer qual era a tarefa, os objetivos tecnicos e as metricas |
| Action | 1:15 a 3:05 | 110s | 233 | Mostrar as decisoes tecnicas (dados, modelos, engenharia, API) |
| Result | 3:05 a 4:30 | 85s | 184 | Demonstrar a API e os resultados, com limitacoes |

O ritmo considerado e de 130 palavras por minuto. Se a sua fala for mais rapida ou mais lenta, ajuste cortando ou acrescentando frases do bloco Action.

### Cena a cena

| Cena | Tempo | O que aparece na tela | O que fazer |
|---|---|---|---|
| 1 | 0:00 a 0:15 | README.md aberto no VS Code, no topo, com o titulo e a tabela de resultados | Aparecer na camera, se quiser, e cumprimentar. Depois deixar so a tela |
| 2 | 0:15 a 0:40 | `notebooks/01_eda_baseline.ipynb`, grafico de distribuicao do alvo (barras 73% e 26,5%) | Apontar o cursor para as duas barras |
| 3 | 0:40 a 1:15 | `docs/ml_canvas.md`, secao de metricas com a formula do valor liquido | Rolar devagar ate a formula e parar nela |
| 4 | 1:15 a 1:45 | Notebook 01, grafico "Taxa de churn por categoria" (contrato, internet, pagamento) | Passar o cursor sobre a barra de contrato mensal e a de cheque eletronico |
| 5 | 1:45 a 2:05 | Explorador de arquivos do VS Code com a pasta `src/churn`, depois `preprocessing.py` | Abrir `preprocessing.py` e mostrar as duas pipelines (numerica e categorica) |
| 6 | 2:05 a 2:35 | Notebook 02, tabela comparativa e grafico das curvas ROC | Mostrar a tabela, depois as curvas |
| 7 | 2:35 a 3:05 | Terminal com `python -m pytest` rodando, depois `src/churn_api/main.py` | Rodar o pytest ao vivo e deixar aparecer "13 passed" |
| 8 | 3:05 a 3:25 | Navegador em `http://127.0.0.1:8000/docs`, GET `/health` executado | Clicar em Try it out e Execute no `/health` |
| 9 | 3:25 a 3:50 | Swagger, POST `/predict` com o cliente de risco alto (JSON na secao "Cliente A") | Colar o JSON, executar e dar zoom na resposta |
| 10 | 3:50 a 4:05 | Mesmo POST com o cliente de risco baixo (JSON "Cliente B") | Trocar o corpo, executar e mostrar a resposta |
| 11 | 4:05 a 4:30 | `docs/model_card.md`, tabela de subgrupos, depois o historico de commits no terminal (`git log --oneline`) | Parar na linha dos idosos e encerrar no log |

### JSON para a demonstracao

**Cliente A (esperado, probabilidade 0,8688, risco alto)**

```json
{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 2,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "Fiber optic",
  "OnlineSecurity": "No",
  "OnlineBackup": "No",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "Yes",
  "StreamingMovies": "Yes",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 95.5,
  "TotalCharges": 191.0
}
```

**Cliente B (esperado, probabilidade 0,0622, risco baixo)**

```json
{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 60,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "DSL",
  "OnlineSecurity": "Yes",
  "OnlineBackup": "No",
  "DeviceProtection": "No",
  "TechSupport": "Yes",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Two year",
  "PaperlessBilling": "No",
  "PaymentMethod": "Bank transfer (automatic)",
  "MonthlyCharges": 40.0,
  "TotalCharges": 2400.0
}
```

### Preparacao antes de gravar

1. Ativar o ambiente virtual e subir a API em um terminal separado com `uvicorn churn_api.main:app --app-dir src`.
2. Deixar abertas, nesta ordem, as abas do VS Code (README, notebook 01, `ml_canvas.md`, `preprocessing.py`, notebook 02, `main.py`, `model_card.md`) e a aba do navegador com `/docs`.
3. Conferir que os notebooks estao com as saidas visiveis. Se estiverem sem graficos, rode todas as celulas antes.
4. Fechar notificacoes, e-mail e mensageiros. Aumentar o zoom do editor para 125% ou 150%, para o texto ficar legivel em 1080p.
5. Fazer um ensaio completo com cronometro. O tempo final precisa ficar entre 4min20s e 4min55s.
6. Gravar em 1080p, com microfone proximo e sem eco. OBS Studio, Xbox Game Bar (Windows + G) ou a gravacao do proprio Teams funcionam.

### Plano B se algo falhar na gravacao

| Problema | O que fazer |
|---|---|
| A API nao sobe | Mostrar o teste de API no pytest (`test_predict_returns_probability`) e comentar que o servico foi validado por testes |
| O navegador nao abre `/docs` | Usar `curl` no terminal, com o comando do README |
| O tempo estourou | Cortar a cena 5 (estrutura de pastas) e encurtar a cena 4 |
| Errou uma frase | Continuar normalmente e corrigir na edicao. Pausas curtas sao melhores que recomecar |

### Publicacao

Exportar em MP4 e subir como nao listado no YouTube ou em uma pasta do Drive com acesso por link. Conferir o link em uma janela anonima antes de enviar.

---

## Parte 2. Script (texto sugerido)

Os trechos entre colchetes sao indicacoes de tela e nao entram na fala. Ajuste o nome e as expressoes para o seu jeito de falar.

### Situation (0:00 a 0:40)

[Cena 1. README aberto.]

> Oi, eu sou o Gabriel e este e o meu Tech Challenge da pos-graduacao. Uma operadora de telecomunicacoes esta perdendo clientes em ritmo acelerado e precisa saber, antes do cancelamento, quem esta em risco.

[Cena 2. Grafico de distribuicao do alvo.]

> Eu trabalhei com o dataset publico Telco Customer Churn, da IBM, com sete mil e quarenta e tres clientes. Cerca de vinte e seis e meio por cento cancelaram, o que deixa o problema desbalanceado, e por isso a acuracia sozinha engana, ja que um modelo que sempre diz que o cliente fica acertaria setenta e tres por cento.

### Task (0:40 a 1:15)

[Cena 3. ML Canvas, secao de metricas.]

> A minha tarefa foi construir um pipeline completo, da analise exploratoria ate uma API. Treinei um baseline de Regressao Logistica, comparei com Random Forest e MLP usando validacao cruzada, escolhi um campeao e servi o modelo com FastAPI e testes.
>
> Defini o ROC-AUC como metrica principal, com F1 e recall de apoio, e uma metrica de negocio, o valor liquido da campanha de retencao, que desconta o custo de cada abordagem do ganho de reter quem ia sair.

### Action (1:15 a 3:05)

[Cena 4. Grafico de churn por categoria.]

> Na exploracao, o que mais chamou atencao foi o contrato. Clientes com contrato mensal cancelam quarenta e dois virgula sete por cento, contra dois virgula oito por cento nos contratos de dois anos. Fibra otica e pagamento por cheque eletronico tambem ficam bem acima da media. Os unicos dados ausentes eram onze valores de cobranca total, de clientes novos, tratados dentro do pipeline para nao vazar informacao do teste.

[Cena 5. Pasta `src/churn` e `preprocessing.py`.]

> Separei o codigo produtivo em modulos na pasta src e deixei os notebooks para experimentar e explicar. O pre-processamento e um ColumnTransformer dentro de um Pipeline do Scikit-Learn, com seed fixada em quarenta e dois e divisao estratificada entre treino e teste.

[Cena 6. Tabela comparativa e curvas ROC.]

> Treinei os tres modelos com validacao cruzada de cinco folds. O Random Forest ficou com o maior AUC medio, zero virgula oitocentos e quarenta e sete, contra zero virgula oitocentos e quarenta e seis da Regressao Logistica e zero virgula oitocentos e quarenta e dois do MLP. Essa diferenca e menor que a variacao entre os folds, entao os modelos sao praticamente equivalentes. Escolhi o Random Forest pelo criterio definido antes do treino, e ele tambem teve o melhor F1 e o melhor valor de negocio no teste.

[Cena 7. Terminal com pytest e depois `main.py`.]

> Depois construi a API com FastAPI, com os endpoints health e predict e validacao de entrada com Pydantic. Escrevi treze testes com pytest, que cobrem pre-processamento, metricas, predicao e a API, e todos passam.

### Result (3:05 a 4:30)

[Cena 8. Swagger, GET `/health`.]

> Vou mostrar a API funcionando. O health responde que o servico esta no ar e que o modelo foi carregado.

[Cena 9. POST `/predict` com o Cliente A.]

> Agora envio um cliente com contrato mensal, fibra otica, dois meses de casa e pagamento por cheque eletronico. A resposta traz probabilidade de churn de oitenta e sete por cento e risco alto.

[Cena 10. POST `/predict` com o Cliente B.]

> Se eu troco por um cliente com contrato de dois anos, DSL, cinco anos de casa e suporte tecnico, a probabilidade cai para seis por cento, risco baixo. O modelo se comporta do jeito que a exploracao previa.

[Cena 11. Model Card, tabela de subgrupos, e depois `git log`.]

> No teste, o campeao chegou a AUC de zero virgula oitenta e quatro e recall de oitenta por cento, ou seja, encontra oito de cada dez clientes que cancelariam. A precisao e de cinquenta e dois por cento, entao metade dos abordados nao sairia, e a campanha precisa comportar isso. No Model Card documentei as limitacoes, como o dataset estatico e as premissas de custo ilustrativas, e um alerta de vies, porque clientes idosos sao sinalizados com muito mais frequencia.
>
> O repositorio tem README, dependencias, testes e commits por etapa. Obrigado por assistir.

---

## Parte 3. Material de apoio

### Numeros citados e onde conferir

| Informacao | Valor | Fonte |
|---|---|---|
| Clientes e taxa de churn | 7.043 e 26,5% | Notebook 01 |
| Divisao treino e teste | 5.634 e 1.409 | `docs/model_card.md` |
| Churn por contrato (mensal, um ano, dois anos) | 42,7%, 11,3% e 2,8% | Notebook 01 |
| Churn por internet (fibra, DSL, sem internet) | 41,9%, 19,0% e 7,4% | Notebook 01 |
| Churn com cheque eletronico | 45,3% | Notebook 01 |
| Tenure mediano de quem cancela e de quem fica | 10 e 38 meses | Notebook 01 |
| Valores ausentes em TotalCharges | 11 | Notebook 01 |
| AUC na validacao cruzada (RF, LR, MLP) | 0,8471, 0,8460 e 0,8423 | `docs/results/model_comparison.csv` |
| AUC no teste do campeao | 0,8425 | `docs/results/model_comparison.csv` |
| Recall e precisao do campeao no teste | 80,2% e 51,9% | `docs/results/model_comparison.csv` |
| Limiar de decisao | 0,449 | `models/model_metadata.json` |
| Valor liquido no teste (RF, LR, MLP) | R$ 19.320, R$ 18.600 e R$ 18.540 | `docs/results/model_comparison.csv` |
| Testes automatizados | 13 | `pytest` |
| Idosos e nao idosos sinalizados | 65,3% e 36,5% | `docs/results/subgroup_metrics.csv` |

### Perguntas que podem aparecer e respostas sugeridas

**Por que ROC-AUC e nao acuracia?**
Porque 73% dos clientes nao cancelam. Um modelo que sempre diz "fica" teria 73% de acuracia sem identificar nenhum churner. O ROC-AUC mede a capacidade de ranquear quem tem mais risco, independentemente do limiar.

**Por que o Random Forest e o campeao se a Regressao Logistica e quase igual?**
Pelo criterio definido antes do treino, que era o maior ROC-AUC medio na validacao cruzada. A diferenca e pequena e esta dentro da variacao entre folds, e isso esta dito no Model Card. Se a interpretabilidade pesar mais, a Regressao Logistica e uma escolha valida.

**Como voce evitou vazamento de dados?**
Imputacao, escala e one-hot estao dentro do Pipeline. A cada fold da validacao cruzada eles sao ajustados so com os dados de treino daquele fold. O conjunto de teste foi usado uma unica vez, no final, e o limiar foi escolhido com previsoes out-of-fold do treino.

**Como o limiar de 0,449 foi escolhido?**
Maximizando o F1 sobre previsoes out-of-fold do treino, sem olhar o teste. Com custos reais, o ideal seria escolher o limiar que maximiza o valor de negocio.

**A precisao de 52% nao e baixa?**
E um custo assumido. O recall de 80% mostra que o modelo captura a maior parte dos churners, e, com as premissas do ML Canvas, a campanha ainda tem valor liquido positivo. Para uma operacao real, o limiar e ajustado ao custo da abordagem.

**O que voce faria com mais tempo?**
Busca de hiperparametros, calibracao das probabilidades, teste sem os atributos genero e idoso para reduzir risco de vies, custos reais de retencao e monitoramento do modelo em producao.

**Por que Vercel?**
Roda FastAPI com scikit-learn sem adaptacao e tem deploy direto a partir do GitHub. O Cloudflare Workers tem suporte limitado a scikit-learn no ambiente Python.