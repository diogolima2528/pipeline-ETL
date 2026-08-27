# 📈 Pipeline ETL Financeiro Automatizado (B3)

Um pipeline de dados de ponta a ponta que extrai, transforma e carrega (ETL) dados de mercado e fundamentos contábeis de ativos da bolsa brasileira (B3). O projeto utiliza Python e Pandas para o processamento e modelagem dos dados em um banco relacional SQLite, operando de forma 100% autônoma via GitHub Actions.

## 🛠️ Arquitetura e Tecnologias

- **Extração (Extract):** `yfinance` API (Python) para coleta de histórico de preços e indicadores fundamentalistas.
- **Transformação (Transform):** `Pandas` para higienização de dados, padronização de tipagem, renomeação de colunas e criação de métricas de negócio (Variação Percentual Diária e Média Móvel de 7 dias).
- **Carga (Load):** `SQLite3` para estruturação em banco de dados relacional.
- **Automação (Orquestração):** `GitHub Actions` rodando um gatilho CRON diário (pós-fechamento de mercado) para manter o banco de dados sempre atualizado.

## 🗄️ Modelagem de Dados

O banco de dados (`banco_financeiro.db`) foi modelado separando dados transacionais e dimensionais em duas tabelas, aplicando conceitos de Data Warehousing:

1. **`historico_ativos` (Tabela Fato):** Registra o comportamento diário das ações, empilhando o histórico de eventos no tempo.
   - Colunas: `data`, `ativo`, `abertura`, `maximo`, `minimo`, `fechamento`, `volume`, `variacao_diaria_pct`, `media_movel_7d`.
2. **`fundamentos_ativos` (Tabela Dimensão):** Armazena a "foto" fundamentalista e os indicadores de performance da empresa.
   - Colunas: `ativo`, `p_l` (Preço/Lucro), `dividend_yield_pct`, `roe_pct` (Retorno sobre Patrimônio Líquido).
   - **Arquitetura SCD Tipo 1:** Utiliza o conceito de *Slowly Changing Dimension Type 1*. Como os fundamentos (ex: P/L e DY) sofrem atualizações com base no preço diário ou novos balanços, a pipeline de carga atualiza e sobrescreve o dado anterior (`if_exists='replace'`), garantindo que a tabela reflita sempre o estado mais atual do ativo sem gerar redundância de histórico.

## 🚀 Como Executar Localmente

1. Clone este repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)