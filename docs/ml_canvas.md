# ML Canvas - Predicao de Churn em Telecomunicacoes

## 1. Proposta de valor

Identificar com antecedencia os clientes com maior risco de cancelamento para que o time de retencao aborde primeiro quem tem mais chance de sair, reduzindo a perda de receita recorrente com um custo de acao controlado.

## 2. Stakeholders

| Papel | Interesse |
|---|---|
| Diretoria | Reduzir a taxa de cancelamento e proteger a receita recorrente |
| Time de retencao e CRM | Receber uma lista priorizada de clientes para abordar |
| Atendimento | Entender os fatores de risco para conduzir a conversa de retencao |
| Financeiro | Medir o retorno das campanhas de retencao |
| Time de dados | Manter, monitorar e reavaliar o modelo |

## 3. Decisao que o modelo apoia

Quais clientes receberao uma oferta ou contato de retencao no ciclo seguinte. A saida do modelo e uma probabilidade de churn por cliente, convertida em classe (risco alto ou baixo) por um limiar calibrado para o negocio.

## 4. Fonte de dados

Dataset publico Telco Customer Churn (IBM), com 7.043 clientes e 21 colunas, que cobrem demografia, servicos contratados, tipo de contrato, forma de pagamento, cobrancas mensais e totais, tempo de casa (tenure) e o rotulo de churn.

## 5. Tarefa de ML

Classificacao binaria supervisionada. O alvo `Churn` vale 1 quando o cliente cancelou e 0 quando permaneceu. A classe positiva representa cerca de 26,5% dos casos, portanto o problema e desbalanceado.

## 6. Metricas

**Metrica tecnica principal.** ROC-AUC, por medir a qualidade do ranqueamento independentemente do limiar e por lidar bem com o desbalanceamento. Como metrica de apoio usamos o F1 da classe churn, a revocacao (recall) e a precisao.

**Metrica de negocio.** Valor liquido esperado da campanha de retencao, calculado sobre o conjunto de teste. Para cada cliente sinalizado paga-se o custo de abordagem, e para cada churner real sinalizado ganha-se o valor do cliente multiplicado pela taxa de sucesso da retencao.

```
valor_liquido = (verdadeiros_positivos * taxa_sucesso * valor_cliente)
              - ((verdadeiros_positivos + falsos_positivos) * custo_abordagem)
```

Premissas iniciais, todas editaveis em `src/churn/config.py`.

| Parametro | Valor |
|---|---|
| Valor preservado por cliente retido | R$ 600 |
| Custo de abordagem por cliente | R$ 60 |
| Taxa de sucesso da retencao | 30% |

Essas premissas sao ilustrativas, ja que o dataset nao traz custos reais. Em producao devem ser substituidas pelos valores do financeiro.

## 7. Estrategia de avaliacao

Separacao estratificada de 80% treino e 20% teste com seed fixa. Validacao cruzada estratificada de 5 folds sobre o treino para comparar modelos e escolher o campeao. O conjunto de teste e usado uma unica vez, na avaliacao final do campeao.

## 8. Modelos considerados

1. Regressao Logistica (baseline linear)
2. Random Forest (ensemble de arvores)
3. MLPClassifier (rede neural simples)

## 9. Uso em producao

API REST com FastAPI. O endpoint `/predict` recebe os dados de um cliente e devolve a probabilidade de churn, a classe prevista e o nivel de risco. O endpoint `/health` informa se o servico e o modelo estao no ar.

## 10. Riscos e restricoes

- Dataset estatico de uma unica operadora, sem informacao temporal, o que limita a generalizacao.
- Sem custos reais, a metrica de negocio depende de premissas.
- Atributos demograficos (genero, idoso) exigem cuidado para nao gerar tratamento desigual. Detalhes no Model Card.
- O modelo indica associacao e nao causa. A decisao de oferta deve considerar o contexto do cliente.
