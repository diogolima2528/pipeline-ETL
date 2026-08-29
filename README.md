# 📈 Pipeline ETL Financeiro End-to-End & Dashboard BI (B3)

Um projeto de dados que extrai, transforma, armazena na nuvem e visualiza dados de mercado e fundamentos contábeis de ativos da bolsa brasileira (B3). O projeto utiliza Python e Pandas para o processamento, carrega os dados em um banco PostgreSQL no Supabase, e consome essas informações em um Dashboard profissional no Power BI, operando de forma 100% autônoma via GitHub Actions.

## 🛠️ Arquitetura e Tecnologias

- **Extração (Extract):** `yfinance` API (Python) para coleta de histórico de preços diários e indicadores fundamentalistas.
- **Transformação (Transform):** `Pandas` para higienização de dados, padronização de tipagem, limpeza de nomenclaturas (remoção do sufixo `.SA`) e criação de métricas de negócio (Variação Percentual Diária e Média Móvel de 7 dias).
- **Carga (Load):** `Supabase (PostgreSQL)` para armazenamento em nuvem seguro e escalável.
- **Automação (Orquestração):** `GitHub Actions` rodando um gatilho CRON diário após o fechamento do pregão da B3 para atualizar o banco de dados.
- **Visualização (Data Viz):** `Power BI` conectado diretamente ao banco em nuvem, com atualização automática agendada.

## 🗄️ Modelagem de Dados

O banco de dados foi modelado separando dados transacionais e dimensionais em duas tabelas, aplicando conceitos de Data Warehousing:

1. **`historico_ativos` (Tabela Fato):** Registra o comportamento diário das ações, empilhando o histórico de eventos no tempo (base histórica a partir de Jan/2024).
   - Colunas: `data`, `ativo`, `abertura`, `maximo`, `minimo`, `fechamento`, `volume`, `variacao_diaria_pct`, `media_movel_7d`.
2. **`fundamentos_ativos` (Tabela Dimensão):** Armazena a "foto" fundamentalista e os indicadores de performance da empresa.
   - Colunas: `ativo`, `p_l` (Preço/Lucro), `dividend_yield_pct`, `roe_pct` (Retorno sobre Patrimônio Líquido).
   - **Arquitetura SCD Tipo 1:** Utiliza o conceito de *Slowly Changing Dimension Type 1*. Como os fundamentos (ex: P/L e DY) sofrem atualizações, a pipeline sobrescreve o dado anterior, garantindo que a tabela reflita sempre o estado mais atual do ativo sem gerar redundância.

## 🖥️ Dashboard Analítico (Power BI)

O relatório foi desenvolvido com foco em UI/UX para simular um ambiente de *Home Broker* profissional:
* **Dark Mode:** Identidade visual escura para redução de fadiga visual e destaque dos dados.
* **Formatação Condicional:** Gráficos de variação diária utilizando verde (ganhos) e vermelho (perdas) com linha de base (zero).
* **Interatividade Avançada:** Dicas de ferramentas (tooltips) customizadas exibindo métricas cruzadas ao passar o mouse, e filtros de Data/Ativo totalmente responsivos.
