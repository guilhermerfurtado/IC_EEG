from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from numpy import ravel

with open('./filtrados/features/rotulos_mov.csv', 'r') as arquivo_csv:
    y = pd.read_csv(arquivo_csv)
  
with open('./filtrados/features/featuresimagina.csv', 'r') as arquivo1_csv:
    
    X = pd.read_csv(arquivo1_csv, decimal=',', sep=';')
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=100)
y_treino= ravel(y_treino)
lda = LinearDiscriminantAnalysis()
lda.fit(X_treino, y_treino)
y_pred = lda.predict(X_teste)

accuracy = accuracy_score(y_teste, y_pred)
print(f'Acurácia do modelo: {accuracy:.2f}')