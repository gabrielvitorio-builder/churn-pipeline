# Model Card - Previsao de Churn (Random Forest)

## Detalhes do modelo

| Item | Descricao |
|---|---|
| Nome | churn_model (Random Forest dentro de um Pipeline do Scikit-Learn) |
| Versao | 0.1.0 |
| Tarefa | Classificacao binaria, probabilidade de cancelamento do cliente |
| Biblioteca | scikit-learn 1.9.1 |
| Pre-processamento | Imputacao (mediana e moda), padronizacao das numericas e one-hot das categoricas, tudo dentro do pipeline |
| Hiperparametros principais | 300 arvores, profundidade maxima 10, minimo de 5 amostras por folha, `class_weight="balanced_subsample"` |
| Seed | 42 |
| Limiar de decisao | 0,449 (maximiza o F1 em previsoes out-of-fold do treino) |
| Arquivos | `models/churn_model.joblib` e `models/model_metadata.json` |

## Uso pretendido

O modelo apoia o time de retencao na priorizacao de clientes de telecomunicacoes com maior risco de cancelamento. A saida e uma probabilidade, uma classe e um nivel de risco (baixo, medio ou alto), e deve alimentar uma lista de abordagem revisada por pessoas.

Fora do escopo. O modelo nao deve ser usado para negar servico, alterar preco de forma individual sem revisao, nem em outra operadora ou pais sem nova validacao.

## Dados

Dataset publico Telco Customer Churn (IBM), com 7.043 clientes, 19 variaveis preditoras e 26,5% de churn. A divisao foi estratificada, com 5.634 clientes para treino e 1.409 para teste. A coluna `customerID` foi descartada e as 11 linhas com `TotalCharges` ausente (clientes com tenure 0) foram imputadas dentro do pipeline.

## Desempenho

Validacao cruzada estratificada de 5 folds no treino e avaliacao unica no teste.

| Modelo | ROC-AUC (CV) | ROC-AUC (teste) | F1 (teste) | Recall (teste) | Precisao (teste) |
|---|---|---|---|---|---|
| Random Forest (campeao) | 0,8471 | 0,8425 | 0,6303 | 0,8021 | 0,5190 |
| Regressao Logistica (baseline) | 0,8460 | 0,8414 | 0,6180 | 0,7246 | 0,5388 |
| MLP | 0,8423 | 0,8369 | 0,6156 | 0,6979 | 0,5506 |

Matriz de confusao do campeao no teste, com limiar 0,449.

| | Previsto permanece | Previsto cancela |
|---|---|---|
| Real permanece | 757 | 278 |
| Real cancela | 74 | 300 |

O modelo sinaliza 578 dos 1.409 clientes de teste (41%) e captura 300 dos 374 churners reais. Sob as premissas do ML Canvas, o valor liquido estimado no teste e de R$ 19.320.

A diferenca de AUC entre os tres modelos e menor que o desvio entre folds (cerca de 0,01), entao a escolha do Random Forest e sustentada por uma vantagem pequena. A Regressao Logistica e uma alternativa mais simples e interpretavel com desempenho muito proximo.

## Variaveis mais influentes

Importancia por permutacao no teste (queda de ROC-AUC). Tipo de contrato (0,058), tenure (0,024), tipo de internet (0,015) e cobrancas totais (0,013) lideram, o que coincide com os padroes vistos na EDA. A lista completa esta em `docs/results/feature_importance.csv`.

## Analise de vieses por subgrupo

Metricas no conjunto de teste, com o limiar de producao. O detalhe esta em `docs/results/subgroup_metrics.csv`.

| Atributo | Grupo | Clientes | Churn real | Sinalizados | Precisao | Recall |
|---|---|---|---|---|---|---|
| Genero | Feminino | 687 | 28,1% | 40,6% | 54,1% | 78,2% |
| Genero | Masculino | 722 | 25,1% | 41,4% | 49,8% | 82,3% |
| Idoso | Nao | 1.187 | 23,3% | 36,5% | 49,0% | 76,8% |
| Idoso | Sim | 222 | 44,1% | 65,3% | 60,7% | 89,8% |

Leitura.

- Por genero, as taxas de sinalizacao sao quase iguais, e a diferenca de recall (cerca de 4 pontos) e moderada.
- Clientes idosos sao sinalizados com muito mais frequencia (65% contra 36%). Parte disso reflete um churn real bem maior nesse grupo (44% contra 23%), mas o modelo tambem sinaliza mais idosos que nao cancelariam, o que pode gerar abordagens desnecessarias e tratamento diferente por idade.
- O modelo usa `gender` e `SeniorCitizen` como entradas. Recomenda-se avaliar o retreino sem esses atributos e monitorar as metricas por subgrupo antes de uso real.

## Limitacoes

- Dataset estatico e de uma unica operadora, sem dimensao temporal. O desempenho em outro periodo ou mercado pode ser pior.
- Nao ha custos reais. As premissas de R$ 600 por cliente retido, R$ 60 por abordagem e 30% de sucesso sao ilustrativas.
- O limiar maximiza o F1, e nao o valor de negocio. Com custos reais, o limiar ideal pode ser diferente.
- Precisao de cerca de 52%. Quase metade dos clientes sinalizados nao cancelaria, o que a campanha precisa absorver.
- As probabilidades nao foram calibradas e devem ser lidas como ranking de risco, e nao como chance exata.
- Nao houve busca de hiperparametros. Os valores foram fixados de forma conservadora.
- O modelo mostra associacao e nao causa. Contrato mensal e tenure baixo indicam risco, mas nao provam que mudar o contrato evitaria o cancelamento.
- O arquivo `.joblib` depende da versao do scikit-learn usada no treino (1.9.1). Em outra versao, rode `python -m churn.train` para regenerar.

## Monitoramento recomendado

Acompanhar a taxa de churn real contra a prevista, a distribuicao das probabilidades, o ROC-AUC em janelas recentes e as metricas por subgrupo, com reavaliacao a cada trimestre ou quando houver mudanca de planos e precos.

## Contato

Autor gabrielvitorio-builder (gabrielvitorioadms@gmail.com).
