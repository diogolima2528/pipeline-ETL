import sqlite3
import pandas as pd

# Conecta ao banco de dados

conexao = sqlite3.connect('banco_financeiro.db')

# Consulta simples

query = "SELECT * FROM historico_ativos LIMIT 10;"

# Leitura no terminal

df_resultado = pd.read_sql(query, conexao)

print(df_resultado)

conexao.close()