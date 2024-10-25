import sqlite3
import streamlit as st

# Conectar a la base de datos
conn = sqlite3.connect('base_datos.db')
cursor = conn.cursor()

# Consultar las recetas
cursor.execute("SELECT * FROM recetas_BP")
recetas = cursor.fetchall()

# Mostrar las recetas en un dropdown
receta_seleccionada = st.selectbox('Selecciona una receta', [r[1] for r in recetas])

if receta_seleccionada:
    st.write(f"Receta seleccionada: {receta_seleccionada}")
