import streamlit as st
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Ejemplo de Matplotlib en Streamlit")

# Datos de ejemplo
nombres = ['Receta 1', 'Receta 2', 'Receta 3']
valores = [1, 2, 3]

# Crear un gráfico
fig, ax = plt.subplots()
ax.barh(nombres, valores)

# Mostrar el gráfico en Streamlit
st.pyplot(fig)