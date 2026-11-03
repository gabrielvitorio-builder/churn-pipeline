# Roteiro do video (5 minutos, metodo STAR)

Duracao estimada de 4min30s, com cerca de 580 palavras faladas (ritmo de 130 palavras por minuto). As indicacoes de tela ficam entre colchetes e nao sao lidas.

## Situation (0:00 a 0:50)

[Tela. Slide ou README aberto, com o titulo do projeto.]

Oi, eu sou o Gabriel e vou apresentar o meu Tech Challenge. O cenario e o de uma operadora de telecomunicacoes que esta perdendo clientes e precisa saber, antes do cancelamento acontecer, quem esta em risco.

[Tela. Notebook 01, grafico de distribuicao do alvo.]

Eu usei o dataset publico Telco Customer Churn, da IBM, com 7.043 clientes e dados de contrato, servicos, cobranca e tempo de casa. Cerca de 26,5% desses clientes cancelaram, entao o problema e desbalanceado, e isso muda a forma de medir o modelo, porque um modelo que sempre diz que o cliente fica acertaria 73% e nao serviria para nada.

## Task (0:50 a 1:30)

[Tela. docs/ml_canvas.md.]

A minha tarefa foi construir um pipeline completo, da analise exploratoria ate um modelo servido por API. Os objetivos tecnicos foram treinar um baseline de Regressao Logistica, comparar com Random Forest e com uma rede neural MLP usando validacao cruzada, escolher um campeao e entregar o modelo numa API FastAPI com testes.

Defini o ROC-AUC como metrica principal, com F1 e recall da classe churn de apoio, e uma metrica de negocio, que e o valor liquido de uma campanha de retencao, considerando o custo de abordar cada cliente e o ganho de reter quem ia sair.

## Action (1:30 a 3:40)

[Tela. Notebook 01, graficos de churn por contrato e por pagamento.]

Na exploracao, o que mais chamou atencao foi o contrato. Clientes com contrato mensal cancelam 42,7%, contra 2,8% nos de dois anos. Fibra otica e pagamento por cheque eletronico tambem aparecem com churn muito acima da media. Os unicos dados ausentes eram 11 valores de TotalCharges, de clientes novos, que eu tratei dentro do pipeline para nao vazar informacao do teste.

[Tela. src/churn, mostrando preprocessing.py e models.py.]

Para a engenharia, separei o codigo em modulos na pasta src. O pre-processamento e um ColumnTransformer dentro de um Pipeline do Scikit-Learn, com seed fixa em 42 e divisao estratificada. Os notebooks ficam so para experimentar e explicar.

[Tela. Notebook 02, tabela comparativa e curvas ROC.]

Treinei os tres modelos com validacao cruzada de cinco folds. O Random Forest ficou com o maior AUC medio, 0,847, seguido pela Regressao Logistica, com 0,846, e pelo MLP, com 0,842. Sendo bem honesto, a diferenca e menor que o desvio entre folds, entao os modelos sao praticamente equivalentes. Escolhi o Random Forest pelo criterio definido de antemao, e ele tambem teve o melhor F1 e o melhor valor de negocio no teste.

[Tela. Terminal com pytest passando e depois src/churn_api/main.py.]

Depois, construi a API com FastAPI e dois endpoints, health e predict, com validacao de entrada via Pydantic. Escrevi 13 testes com pytest, cobrindo o pre-processamento, as metricas, a predicao e a API, e todos passam.

## Result (3:40 a 4:45)

[Tela. Terminal com uvicorn rodando e a pagina /docs aberta.]

Vou mostrar a API funcionando. O health responde que o modelo esta carregado. Agora envio um cliente com contrato mensal, fibra otica, dois meses de casa e pagamento por cheque eletronico.

[Tela. Executar o POST /predict no Swagger e mostrar a resposta.]

A resposta traz probabilidade de churn de 87%, risco alto. Se eu troco para um cliente com contrato de dois anos, DSL e cinco anos de casa, a probabilidade cai para cerca de 6%, risco baixo. O modelo se comporta de forma coerente com o que a exploracao mostrou.

[Tela. docs/model_card.md, tabela de subgrupos.]

No teste, o campeao chegou a AUC de 0,84, com recall de 80%, ou seja, encontra 8 de cada 10 clientes que cancelariam. A precisao e de 52%, entao metade dos abordados nao sairia, e isso precisa caber no custo da campanha. No Model Card eu documentei essa e outras limitacoes, como o dataset estatico, as premissas de custo ilustrativas e um ponto de atencao com vies, porque clientes idosos sao sinalizados com muito mais frequencia que os demais.

[Tela. README e historico de commits.]

O repositorio tem README com instalacao e execucao, dependencias, testes e o deploy na Vercel. Obrigado por assistir.

---

## Checklist de gravacao

1. Deixar a API rodando antes de comecar a gravar (`uvicorn churn_api.main:app --app-dir src`).
2. Abrir antes as abas do README, do notebook 01 (graficos), do notebook 02 (tabela e ROC), do Model Card e do `/docs`.
3. Testar o tempo com um cronometro. Se passar de 5 minutos, corte a parte sobre estrutura de pastas.
4. Falar com calma nos numeros, mostrar o cursor em cada metrica citada.
5. Exportar em MP4 e conferir que o audio esta claro.

## Numeros citados (conferir antes de gravar)

| Informacao | Valor | Fonte |
|---|---|---|
| Clientes e taxa de churn | 7.043 e 26,5% | notebook 01 |
| Churn contrato mensal e dois anos | 42,7% e 2,8% | notebook 01 |
| AUC CV dos modelos | 0,8471, 0,8460 e 0,8423 | `docs/results/model_comparison.csv` |
| Recall e precisao do campeao no teste | 80,2% e 51,9% | `docs/results/model_comparison.csv` |
| Testes automatizados | 13 | `pytest` |
| Churn flagged idosos e nao idosos | 65,3% e 36,5% | `docs/results/subgroup_metrics.csv` |
