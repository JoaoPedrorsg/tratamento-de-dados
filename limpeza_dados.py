import pandas as pd
from datetime import datetime
import os

# === LER O ARQUIVO CSV ===
df = pd.read_csv(r'clientes_para_limpeza.csv')

# Exibe colunas e primeiras linhas
pd.set_option('display.width', None)
print("Colunas disponíveis:", df.columns.tolist())
print("Dados iniciais:\n", df.head())

# === AJUSTA NOMES DAS COLUNAS PARA PADRÃO (sem espaços, minúsculas) ===
df.columns = df.columns.str.strip().str.lower()

# === REMOVE DADOS ===
df.drop('pais', axis=1, inplace=True, errors='ignore')     # Remove coluna "pais" se existir
df.drop(2, axis=0, inplace=True, errors='ignore')           # Remove linha de índice 2

# === NORMALIZA CAMPOS DE TEXTO ===
df['nome'] = df['nome'].astype(str).str.title()
df['endereco'] = df['endereco'].astype(str).str.lower()
df['estado'] = df['estado'].astype(str).str.strip().str.upper()

print('Normalização de texto concluída:\n', df.head())

# === VALORES NULOS ===
df_fillna = df.fillna(0)
df_dropna = df.dropna()
df_dropna4 = df.dropna(thresh=4)
df = df.dropna(subset=['cpf'])  # Remove registros com CPF nulo

print('Valores nulos por coluna:\n', df.isnull().sum())
print('Qtd nulos com fillna:', df_fillna.isnull().sum().sum())
print('Qtd nulos com dropna:', df_dropna.isnull().sum().sum())
print('Qtd nulos com dropna4:', df_dropna4.isnull().sum().sum())
print('Qtd de registros com CPF nulo (após limpeza):', df.isnull().sum().sum())

# Preenche campos específicos com valores padrão
df['estado'] = df['estado'].fillna('DESCONHECIDO')
df['endereco'] = df['endereco'].fillna('Endereço não informado')

# === TRATAMENTO DE DATA E CÁLCULO DE IDADE ===

# Função para tentar vários formatos de data
def parse_datas(data):
    for fmt in ('%d/%m/%Y', '%Y/%m/%d', '%m/%d/%Y'):
        try:
            return pd.to_datetime(data, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT

# Aplica a conversão
df['data_nascimento'] = df['data_nascimento'].apply(parse_datas)

# Função para calcular idade
def calcular_idade(data_nasc):
    if pd.isnull(data_nasc):
        return None
    hoje = datetime.today()
    return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

# Aplica cálculo de idade
df['idade'] = df['data_nascimento'].apply(calcular_idade)

# Corrige idades inválidas (ex: negativas ou > 120)
df['idade_corrigida'] = df['idade'].apply(lambda x: x if pd.notnull(x) and 0 <= x <= 120 else None)

# === CORRIGE O AVISO DE FUTUREWARNING ===
df['idade_corrigida'] = pd.to_numeric(df['idade_corrigida'], errors='coerce')
df['idade_corrigida'] = df['idade_corrigida'].fillna(df['idade_corrigida'].mean()).round()

# Cria nova coluna com data formatada
df['data_corrigida'] = df['data_nascimento'].dt.strftime('%d/%m/%Y')

# === REMOVE DUPLICATAS ===
print('Qtd de registros antes:', df.shape[0])
df.drop_duplicates(inplace=True)
df.drop_duplicates(subset='cpf', inplace=True)
print('Qtd de registros após remover duplicatas:', len(df))

# === PREPARA ARQUIVO FINAL ===
df['data'] = df['data_corrigida']
df['idade'] = df['idade_corrigida']

df_salvar = df[['nome', 'cpf', 'idade', 'data', 'endereco', 'estado']]
df_salvar.to_csv('Clientes_limpeza.csv', index=False)

# Exibe o novo DataFrame salvo
print('Novo DataFrame salvo:\n', pd.read_csv('Clientes_limpeza.csv'))

# Mostra diretório atual
print('Diretório atual:', os.getcwd())
