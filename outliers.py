from operator import index

import pandas as pd
from scipy import stats

pd.set_option('display.width', None)

df = pd.read_csv('Clientes_limpeza.csv')

df_filtro_basico = df[df['idade'] > 85]

print('Filtro basico:\n', df_filtro_basico[['nome', 'idade']])

# Identificar outliers co z-score
z_score = stats.zscore(df['idade'])
outliers_z = df[z_score >= 1]
print("Outlier pelo z-score:\n", outliers_z)

df_zscore = df[(stats.zscore(df['idade']) < 3)]

# identificar outliers com iqr
Q1 = df['idade'].quantile(0.25)
Q3 = df['idade'].quantile(0.75)
IQR = Q3 - Q1

limite_baixo = Q1 - 1.5 * IQR
limite_alto = Q3 + 1.5 * IQR

print('Limite IQR: ', limite_baixo, limite_alto)

outliers_iqr = df[(df['idade'] < limite_baixo) | (df['idade'] > limite_alto)]
print('Outliers pelo IQR:\n ', outliers_iqr)

limite_baixo = 15
limite_alto = 110
df = df[(df['idade'] >= limite_baixo) & (df['idade']<= limite_alto)]

print('Qnt endereços invalidos: ', (df['endereco'] == 'Endereco inválido').sum())

df['nome'] = df['nome'].apply(lambda x: 'Nome inválido' if isinstance(x, str) and len(x) > 40 else x)
print('Qtd de registros com nome grande: ', (df['nome'] == 'Nome inválido').sum())

print('Dado com outliers tratados:\n', df)

df.to_csv('Clientes_remove_outliers.csv', index=False)
