import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Título da página
st.title('Exemplo Streamlit: Gráfico Aleatório')

# Geração de dados aleatórios
data = pd.DataFrame(np.random.randn(100, 2), columns=['A', 'B'])

# Checkbox para exibir ou não o dataframe
if st.checkbox('Mostrar DataFrame'):
    st.write(data)  # Mostra o dataframe

# Criando um gráfico de dispersão
st.subheader('Gráfico de Dispersão')
plt.scatter(data['A'], data['B'])
st.pyplot()  # Mostra o gráfico no Streamlit
