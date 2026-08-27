import sqlite3
import pandas as pd

# Conecta ao banco de dados

conexao = sqlite3.connect('banco_financeiro.db')

# Query SQL cruzando as duas tabelas com INNER JOIN e agregações

query_insights = """
SELECT 

f.ativo,
min(h.fechamento) AS min_fechamento,
max(h.fechamento) AS max_fechamento,
round(avg(h.fechamento),2) AS media_fechamento,
round(avg(h.volume),0) AS media_volume,
f.roe_pct AS ROE,
f.p_l AS Preco_Lucro,
f.dividend_yield_pct AS DY

FROM fundamentos_ativos f

INNER JOIN historico_ativos h ON f.ativo = h.ativo

GROUP BY f.ativo, f.p_l, f.dividend_yield_pct, f.roe_pct

ORDER BY f.roe_pct DESC
"""

# Executa a query e exibe o resultado no terminal

df_insights = pd.read_sql(query_insights, conexao)
print("Insights Cruzados: Fundamentos vs Performance 2026")
print("-" * 70)
print(df_insights.to_string(index=False))

conexao.close()