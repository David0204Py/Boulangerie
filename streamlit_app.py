import sqlite3
import streamlit as st

# Función para cargar el archivo CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Conectar a la base de datos
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Cargar estilos CSS
load_css('static/styles.css')

# Crear la interfaz Streamlit
st.title("App de Recetas")

# Ejemplo de menú de navegación
st.markdown("""
<nav>
   <ul>
      <li><a href="#">Consultar Recetas</a></li>
      <li><a href="#">Agregar Receta</a></li>
      <li><a href="#">Modificar Inventario</a></li>
      <li><a href="#">Visualización de Datos</a></li>
   </ul>
</nav>
""", unsafe_allow_html=True)

# Mostrar contenido en la interfaz
st.write("Bienvenido a la app de recetas. Usa el menú para navegar.")

# Consultar las recetas
cursor.execute("SELECT * FROM recetas_BP")
recetas = cursor.fetchall()

# Mostrar las recetas en un dropdown
receta_seleccionada = st.selectbox('Selecciona una receta', [r[1] for r in recetas])

if receta_seleccionada:
    st.write(f"Receta seleccionada: {receta_seleccionada}")
