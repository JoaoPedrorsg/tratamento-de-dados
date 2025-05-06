import pandas as pd
import numpy as np
from scipy.sparse.csgraph import depth_first_tree

from limpeza_dados import df_salvar

pd.set_option('display.width', None)


df = pd.read_csv('Clientes_remove_outliers.csv')

print(df.head())
#Mascarar dadpos pessoais
df['cpf_mascara'] = df['cpf'].astype(str).apply(lambda cpf: f'{cpf[:3]}.***.***-{cpf[-2:]}')

#corrigir datas
df['data'] = pd.to_datetime(df['data'], format='%y-%m-%d', errors='coerce')

data_atual = pd.to_datetime('today')
df['data_atualizada'] = df['data'].where(df['data'] <= data_atual, pd.to_datetime('1900-01-01'))
df['idade_ajustada'] = data_atual.year - df['data_atualizada'].dt.year
df['idade_ajustada'] -= ((data_atual.month <= df['data_atualizada'].dt.month) & (data_atual.day < df['data_atualizada'].dt.day)).astype(int)
df.loc[df['idade_ajustada'] > 100, 'idade_ajustada'] = np.nan

#corrigir campos com múltiplas informações
df['endereco_curto'] = df['endereco'].astype(str)
df['endereco_curto'] = df['endereco_curto'].apply(lambda x: 'Endereco invalido' if len(x) > 60 or len(x) < 5 else x)

df['cpf'] = df['cpf'].astype(str)
df['cpf'] = df['cpf'].apply(lambda x: x if len(x) == 14 else "CPF inválido")

df['estado_sigla'] = df['estado'].astype(str)
estados_br = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
df['estado_sigla'] = df['estado_sigla'].str.upper().apply(lambda x: x if x in estados_br else 'Desconhecido')

print('Dados tratados:\n', df.head())

df['cpf'] = df['cpf_mascara']
df['idade'] = df['idade_ajustada']
df['endereco'] = df['endereco_curto']
df['estado'] = df['estado_sigla']
df_salvar = df[['nome', 'cpf', 'idade', 'data', 'endereco', 'estado']]
df_salvar.to_csv('Clientes_tratados.csv', index=False)

print('Novo DataFrame: \n', pd.read_csv('Clientes_tratados.csv'))
