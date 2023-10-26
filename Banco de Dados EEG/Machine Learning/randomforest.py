from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pandas as pd
from numpy import ravel


with open('./filtrados/features/rotulos.csv', 'r') as arquivo_csv:
    y = pd.read_csv(arquivo_csv)
  
with open('./filtrados/features/features.csv', 'r') as arquivo1_csv:
    
    X = pd.read_csv(arquivo1_csv, decimal=',', sep=';')
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=100)
y_treino= ravel(y_treino)
# Passo 1: Criar uma instância do modelo Random Forest com os hiperparâmetros desejados
random_forest = RandomForestClassifier(n_estimators=100, random_state=42)  # Exemplo com 200 árvores

# Passo 2: Treinar o modelo com os dados de treinamento
random_forest.fit(X_treino, y_treino)

# Passo 3: Fazer previsões nos dados de teste
y_pred = random_forest.predict(X_teste)

# Passo 4: Avaliar o desempenho do modelo (por exemplo, calcular a acurácia)
acuracia = accuracy_score(y_teste, y_pred)
print(f'Acurácia do modelo: {acuracia}')
