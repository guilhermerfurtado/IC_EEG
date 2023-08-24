#FEATURES
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
from scipy.signal import butter, iirnotch, filtfilt, sosfilt
import os

mav = []  # mean absolute value
rms = []  # root mean square
# zcs = []  # zero crossing
# scc = []  # slope sign changes
# wal = []  # waveform length

# var = []  # variance
# fmn = []  # frequency mean
# fmd = []  # frequency median
directory_name = 'features'
lista_arquivos = [i for i in os.listdir('./filtrados') if i.find('.csv') != -1]


for nome_arquivo in lista_arquivos:

    with open(f'./filtrados/{nome_arquivo}', 'r') as arquivo_csv:
        leitor_csv = pd.read_csv(arquivo_csv)
        
    channels = list(leitor_csv.head())[:-1]
    print(channels)

    times = [8, 23, 39, 52]

    for canal in channels:
        for i in range(3): 
            dados = leitor_csv[(leitor_csv['Tempo'] >= times[i]) & (leitor_csv['Tempo'] <= times[i+1])][canal]
            print(dados.shape)

            mav.append(np.mean(np.abs(dados)))
            rms.append(np.sqrt(np.mean(dados ** 2)))
            leitor_csv.to_csv(f'./{directory_name}/{nome_arquivo}_features.csv', index=False)

            print(mav,i,canal)


            # zcs.append(np.where(np.diff(np.sign(dados)))[0].shape[0])
            # scc.append(np.count_nonzero(np.diff(np.sign(np.diff(dados))) != 0))
            # wal.append(np.sum(np.abs(np.diff(dados))))

            # var.append(np.sum((dados-np.mean(dados))**2)/(dados.shape[0]-1))

            # fft_result = np.fft.fft(dados)
            # spectre = np.abs(fft_result)
            # positive_spectre = spectre[:len(spectre) // 2]
            # fmn.append(np.mean(positive_spectre))
            # fmd.append(np.median(positive_spectre))
    

        