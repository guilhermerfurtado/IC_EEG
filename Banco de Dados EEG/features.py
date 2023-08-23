#FEATURES
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
from scipy.signal import butter, iirnotch, filtfilt, sosfilt
import os

lista_arquivos = [i for i in os.listdir('./filtrados') if i.find('.csv') != -1]


for nome_arquivo in lista_arquivos:

    with open(f'./filtrados/{nome_arquivo}', 'r') as arquivo_csv:
        leitor_csv = pd.read_csv(arquivo_csv)
        
    channels = list(leitor_csv.head())[:-1]

    times = [8, 23, 39, 52]
    intervalo_inicio = 8
    intervalo_meio1 = 24
    intervalo_meio2 = 40
    intervalo_fim = 52

    for canal in channels:
        for i in range(3): 
            dados = leitor_csv[(leitor_csv['Tempo'] >= times[i]) & (leitor_csv['Tempo'] <= times[i+1])]
            print(len(dados))
        
        print('-----------------')
        