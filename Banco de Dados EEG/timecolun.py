
import csv
import pandas as pd
import numpy as np

x = 1

while x <= 24:
    numero_formatado = '{:02d}'.format(x)  # Formata o número com dois dígitos, adicionando zeros à esquerda se necessário
    nome_arquivo = 'Amanda{}.csv'.format(numero_formatado)
    print(nome_arquivo)
    x += 1
    with open(nome_arquivo, 'r') as arquivo_csv:
        leitor_csv = pd.read_csv(arquivo_csv)

    #Concatenando coluna de tempo com a base de dados!
    passo = np.arange(0, 53, 1)
    t = np.arange(0, 53, 53/len(leitor_csv))
    df2=pd.DataFrame({'Tempo' :t})
    df_concat = pd.concat([leitor_csv, df2], axis=1)
    df_concat.to_csv(nome_arquivo, index=False)

    #print(df_concat.head())
