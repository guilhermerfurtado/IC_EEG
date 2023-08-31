from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.model_selection import train_test_split

with open('rotulos.csv', 'r') as arquivo_csv:
    y = pd.read_csv(arquivo_csv)
with open('features.csv', 'r') as arquivo1_csv:
    X = pd.read_csv(arquivo1_csv)
# Inicialize o modelo SVM com os parâmetros desejados
svm_model = SVC(kernel='linear', C=1.0)  # Você pode ajustar o tipo de kernel e outros parâmetros

# Treine o modelo SVM usando os dados de treinamento
svm_model.fit(X_treino, y_treino)

# Faça previsões usando os dados de teste
y_pred = svm_model.predict(X_test)

# Calcule a acurácia do modelo usando as previsões e os rótulos reais
accuracy = accuracy_score(y_test, y_pred)
print(f'Acurácia do modelo: {accuracy:.2f}')
