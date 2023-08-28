
import os
import csv
import pandas as pd
import numpy as np

mav = []  # mean absolute value
rms = []  # root mean square
directory_name = 'features'
times = [8, 23, 39, 52]

lista_arquivos = [i for i in os.listdir('./filtrados') if i.find('.csv') != -1]

for nome_arquivo in lista_arquivos:
    with open(f'./filtrados/{nome_arquivo}', 'r') as arquivo_csv:
        leitor_csv = pd.read_csv(arquivo_csv)

    channels = list(leitor_csv.head())[:-1]

    for canal in channels:
        for i in range(3):
            dados = leitor_csv[(leitor_csv['Tempo'] >= times[i]) & (leitor_csv['Tempo'] <= times[i+1])][canal]

            mav.append(np.mean(np.abs(dados)))
            rms.append(np.sqrt(np.mean(dados ** 2)))

            # Escrever características no arquivo CSV
            nome_saida = f'./{directory_name}/{nome_arquivo}_features.csv'
            with open(nome_saida, mode='w', newline='') as arquivo_csv:
                escritor = csv.writer(arquivo_csv)
                escritor.writerow(["mav"])  # Cabeçalho
                escritor.writerows(zip(mav, channels, times))

            print(f"Características foram escritas em {nome_saida}")