#FEATURES
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
from scipy.signal import butter, iirnotch, filtfilt, sosfilt
import os




times = [8, 23, 39, 52]
pessoas = ['Amanda','Braz','PedroB','PedroF']
directory_name = 'features'


channels = ['E1','Pz','Fp1','T6','F7','O2','Fz','F8','A1','F3','C4','T5','P4','Fp2','Oz','O1','T3','A2','C3','Cz','F4','T4','P3'] 

matriz_final = []
for canal in channels:
    mav = []  # mean absolute value
    rms = []  # root mean square
    var = []  # variance
    fmn = []  # frequency mean
    fmd = []  # frequency median
    for nome in pessoas:
        lista_arquivos = [i for i in os.listdir('./filtrados') if i.find(f'{nome}') != -1]
        # print(len(lista_arquivos))
        for nome_arquivo in lista_arquivos:
            
            

            with open(f'./filtrados/{nome_arquivo}', 'r') as arquivo_csv:
                leitor_csv = pd.read_csv(arquivo_csv)
                
            
            for i in range(3): 
                
                dados = leitor_csv[(leitor_csv['Tempo'] >= times[i]) & (leitor_csv['Tempo'] <= times[i+1])][canal]
                
                mav.append(np.mean(np.abs(dados)))
                rms.append(np.sqrt(np.mean(dados ** 2))) 
                var.append(np.sum((dados-np.mean(dados))**2)/(dados.shape[0]-1))
                fft_result = np.fft.fft(dados)
                spectre = np.abs(fft_result)
                positive_spectre = spectre[:len(spectre) // 2]
                fmn.append(np.mean(positive_spectre))
                fmd.append(np.median(positive_spectre))
                df=pd.DataFrame({f'{canal} mav': mav})
                df1=pd.DataFrame({f'{canal} rms': rms})
                

    mav_array = np.array(mav)
    rms_array = np.array(rms)
    var_array = np.array(var)
    fmn_array = np.array(fmn)
    fmd_array = np.array(fmd)

    feat = np.vstack((mav_array, rms_array, var_array, fmn_array, fmd_array)).T
    matriz_final.append(feat)

    print(feat.shape)


matriz_final = np.hstack(matriz_final)
print(matriz_final.shape)
# print(len(matriz_final))
nome_saida = f'./filtrados/{directory_name}/features.csv'
with open(nome_saida, mode='w', newline='') as arquivo_csv:
    escritor = csv.writer(arquivo_csv)
    escritor.writerows(zip(matriz_final))
    
