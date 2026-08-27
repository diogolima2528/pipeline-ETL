import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import os

print("Iniciando extração de dados...")
# Ativos atualizados com o sufixo da bolsa brasileira (.SA)
ativos = ['ITUB4.SA', 'TOTS3.SA', 'WEGE3.SA', 'B3SA3.SA']

dados_historico = []
lista_fundamentos = []

for ativo in ativos:
    acao = yf.Ticker(ativo)

    # EXTRAÇÃO 1: Histórico de Cotações
    
    df_temp = acao.history(start="2026-01-01")
    df_temp = df_temp.reset_index()
    df_temp['ticker'] = ativo
    dados_historico.append(df_temp)
    
    # EXTRAÇÃO 2: Dados Fundamentalistas

    info = acao.info
    
    pl = info.get('trailingPE', None)
    dy = info.get('dividendYield', None)
    roe = info.get('returnOnEquity', None)
    
    lista_fundamentos.append({
        'ativo': ativo,
        'p_l': round(pl, 2) if pl else None,
        'dividend_yield_pct': round(dy * 100, 2) if dy else None,
        'roe_pct': round(roe * 100, 2) if roe else None
    })
    
# TRANSFORMAÇÃO

print("Realizando tratamento e cálculos...")

df_bruto = pd.concat(dados_historico, ignore_index=True)
df_tratado = df_bruto.copy()

df_tratado.columns = [col.lower().replace(' ', '_') for col in df_tratado.columns]
df_tratado['date'] = pd.to_datetime(df_tratado['date'], utc=True).dt.strftime('%d/%m/%Y')

dicionario_nomes = {
    'date': 'data', 'ticker': 'ativo', 'open': 'abertura',
    'high': 'maximo', 'low': 'minimo', 'close': 'fechamento'
}
df_tratado = df_tratado.rename(columns=dicionario_nomes)

df_tratado['variacao_diaria_pct'] = df_tratado.groupby('ativo')['fechamento'].pct_change() * 100
df_tratado['media_movel_7d'] = df_tratado.groupby('ativo')['fechamento'].transform(lambda x: x.rolling(window=7, min_periods=1).mean())

df_tratado = df_tratado.dropna(subset=['variacao_diaria_pct'])

colunas_finais = ['data', 'ativo', 'abertura', 'maximo', 'minimo', 'fechamento', 'volume', 'variacao_diaria_pct', 'media_movel_7d']
df_tratado = df_tratado[colunas_finais]

colunas_arredondar = ['abertura', 'maximo', 'minimo', 'fechamento', 'variacao_diaria_pct', 'media_movel_7d']
df_tratado[colunas_arredondar] = df_tratado[colunas_arredondar].round(2)

df_fundamentos = pd.DataFrame(lista_fundamentos)

# CARGA (Load)

print("Carregando dados no PostgreSQL (Supabase)...")

# Substitua pelas suas credenciais fornecidas no painel do Supabase
# Formato: postgresql://usuario:senha@host:porta/nome_do_banco
DATABASE_URL = os.environ.get("DATABASE_URL")

# Cria o motor de conexão
engine = create_engine(DATABASE_URL)

# Salva as tabelas na nuvem
df_tratado.to_sql('historico_ativos', engine, if_exists='replace', index=False)
df_fundamentos.to_sql('fundamentos_ativos', engine, if_exists='replace', index=False)

print("Pipeline ETL finalizado com sucesso! Tabelas atualizadas na nuvem.")