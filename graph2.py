
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
from scipy.signal import butter, iirnotch, filtfilt, sosfilt
nome =  'T2.1Isac12'
with open(f'{nome}.csv', 'r') as arquivo_csv:
    leitor_csv = pd.read_csv(arquivo_csv)

y = []
j = "F3"
f0= 60
fs=512
t = np.arange(0, 57, 57/len(leitor_csv))
passo = np.arange(0, 53, 2)




# Plot do sinal cru
plt.plot(t,leitor_csv[j]) 
plt.ylim(-0.00005, 0.0005)
plt.xlim(0, 55)
plt.xticks(passo)
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude (Volts)')
plt.title('Sinal EEG CRU')
#plt.savefig(f'C:/Users/anacr/OneDrive/Área de Trabalho/IniciacaoCientifica/{j}sinaleegcru{nome}.png')
plt.show()


#FILTRO
b,a = iirnotch(f0,50, fs=fs)
x = filtfilt(b,a,leitor_csv[j])
sos = butter(5, [0.7, 70], 'bp', fs=fs, output='sos')
X = sosfilt(sos, x)

#Plotando o primeiro sinal já com o filtro passa-banda de 8-13Hz

plt.plot(t, X) 
plt.ylim(-0.0003,0.0003)
plt.xlim(0,55)
plt.xticks(passo)
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude (Volts)')
plt.title('Sinal com filtro Passa-banda 8-13Hz')
#plt.savefig(f'C:/Users/anacr/OneDrive/Área de Trabalho/IniciacaoCientifica/{j}sinalfiltropb{nome}.png')
plt.show()



# Cálculo da Transformada de Fourier
transformada = np.fft.fft(X)
frequencias = np.fft.fftfreq(len(transformada), 1/fs)

# Plot do espectro de frequência
plt.plot(frequencias, np.abs(transformada))
plt.xlabel('Frequência')
plt.ylabel('Magnitude')
plt.title('Sinal no domínio da Frequência')
#plt.savefig(f'C:/Users/anacr/OneDrive/Área de Trabalho/IniciacaoCientifica/{j}sinalfrequencia{nome}.png')
plt.show()

