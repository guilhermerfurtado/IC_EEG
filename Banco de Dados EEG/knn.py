from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import numpy as np
from numpy import ravel
import pandas as pd

with open('./filtrados/features/rotulos_mov.csv', 'r') as arquivo_csv:
    y = pd.read_csv(arquivo_csv)
  
with open('./filtrados/features/featuresimagina.csv', 'r') as arquivo1_csv:
    
    X = pd.read_csv(arquivo1_csv, decimal=',', sep=';')
X = np.array(X)
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=100)
y_treino= ravel(y_treino)

# Passo 1: Criar uma instância do classificador KNN (por exemplo, com K=3)
knn = KNeighborsClassifier(n_neighbors=3)

# Passo 2: Treinar o modelo com os dados de treinamento
knn.fit(X_treino, y_treino)

# Passo 3: Fazer previsões nos dados de teste
y_pred = knn.predict(X_teste)

# Passo 4: Avaliar o desempenho do modelo (por exemplo, calcular a acurácia)
acuracia = accuracy_score(y_teste, y_pred)
print(f'Acurácia do modelo: {acuracia}')
