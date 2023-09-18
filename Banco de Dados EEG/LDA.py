from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pandas as pd
from sklearn.model_selection import train_test_split

with open('./filtrados/features/rotulos.csv', 'r') as arquivo_csv:
    y = pd.read_csv(arquivo_csv)
  
with open('./filtrados/features/features.csv', 'r') as arquivo1_csv:
    
    X = pd.read_csv(arquivo1_csv, decimal=',', sep=';')
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=100)

lda = LinearDiscriminantAnalysis()
lda.fit(X_treino, y_treino)
y_pred = lda.predict(X_teste)