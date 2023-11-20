import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
from scipy.signal import butter, iirnotch, filtfilt, sosfilt
import os



f0= 60
fs=512
listanomes = ['T2_Franco', 'T2_CaioF', 'T2_JosePedro']

for nome in listanomes:
    for x in range(1,17):

        numero_formatado = '{:02d}'.format(x)  # Formata o número com dois dígitos, adicionando zeros à esquerda se necessário
        nome_csv = f'{nome}{numero_formatado}'
        nome_arquivo = f'{nome_csv}.csv'
    

        
        
        with open(nome_arquivo, 'r') as arquivo_csv:
            leitor_csv = pd.read_csv(arquivo_csv)
        

        
        channels = list(leitor_csv.head())[:-1]
    
        for canal in channels:
            b,a = iirnotch(f0,50, fs=fs)
            x = filtfilt(b,a,leitor_csv[canal])
            sos = butter(5, [0.7, 70], 'bp', fs=fs, output='sos')
            leitor_csv[canal] = sosfilt(sos, x)


        directory_name = "filtrados"

        # Check if the directory already exists
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
        
        leitor_csv.to_csv(f'./{directory_name}/{nome_csv}_filtrado.csv', index=False)

        print(f'{nome_csv}_filtrado.csv')

