#FEATURES
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
from scipy.signal import butter, iirnotch, filtfilt, sosfilt
import os



matriz_base = np.zeros((72, 46))
times = [8, 23, 39, 52]
pessoas = ['Amanda','Braz','PedroB','PedroF']
# pessoas = ['Amanda']
directory_name = 'features'


channels = ['E1','Pz','Fp1','T6','F7','O2','Fz','F8','A1','F3','C4','T5','P4','Fp2','Oz','O1','T3','A2','C3','Cz','F4','T4','P3'] 
# channels = ['E1'] 
matriz_final = []
for canal in channels:
    for nome in pessoas:
        mav = []  # mean absolute value
        rms = []  # root mean square
        lista_arquivos = [i for i in os.listdir('./filtrados') if i.find(f'{nome}') != -1]
        # print(len(lista_arquivos))
        for nome_arquivo in lista_arquivos:
            
            

            with open(f'./filtrados/{nome_arquivo}', 'r') as arquivo_csv:
                leitor_csv = pd.read_csv(arquivo_csv)
                
            
            for i in range(3): 
                
                dados = leitor_csv[(leitor_csv['Tempo'] >= times[i]) & (leitor_csv['Tempo'] <= times[i+1])][canal]
                
                mav.append(np.mean(np.abs(dados)))
                rms.append(np.sqrt(np.mean(dados ** 2))) 
                df=pd.DataFrame({f'{canal} mav': mav})
                df1=pd.DataFrame({f'{canal} rms': rms})
                

    mav_array = np.array(mav)
    rms_array = np.array(rms)

    feat = np.vstack((mav_array, rms_array)).T
    matriz_final.append(feat)

    print(feat.shape)

    nome_saida = f'./filtrados/{directory_name}/{nome}_features.csv'

# matriz_final = np.array(matriz_final)
print(len(matriz_final))

