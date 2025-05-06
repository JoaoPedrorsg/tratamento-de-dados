import pandas as pd

df = pd.read_csv(r'Clientes_tratados.csv')

# Verificar os primeiros registros
print(df.head().to_string())

# Verificar qtd  de linhas e colunas
print('Qtd: ', df.shape)

# Verificar tipos de dados
print('Tipagem:\n', df.dtypes)

# Checar valores nulos
print('Valores nulos:\n', df.isnull().sum())
