import sqlite3
import streamlit as st

# Cargar JavaScript (si se requiere)
def load_js(file_name):
    with open(file_name) as f:
        st.markdown(f'<script>{f.read()}</script>', unsafe_allow_html=True)

# Llamamos la función para cargar el JS
load_js('static/script.js')

# Función para cargar el archivo CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Mostrar logo en la interfaz
st.image('Icono_020_PNG_BP.png', width=400)

# Conectar a la base de datos
conn = sqlite3.connect('base_datos.db')
cursor = conn.cursor()

# Cargar los estilos CSS
load_css('static/styles.css')

# Sistema de navegación
menu = ["Inicio", "Consultar Recetas", "Agregar Receta", "Modificar Inventario", "Visualización de Datos"]
selection = st.sidebar.selectbox("Bienvenido Chou. Usa el menú para navegar.", menu)

# Función para cada página
def home():
    st.title("Bienvenido a Chou")
#    st.write("Selecciona una opción del menú para empezar.")

def consultar_recetas():
    st.title("Consultar Recetas")
    # Aquí podemos cargar las recetas desde la base de datos
    st.write("Aquí podrás consultar las recetas existentes.")
    # Consultar las recetas
    cursor.execute("SELECT * FROM recetas_BP")
    recetas = cursor.fetchall()
    # Mostrar las recetas en un dropdown
    receta_seleccionada = st.selectbox('Selecciona una receta', [r[1] for r in recetas])
    if receta_seleccionada:
        st.write(f"Receta seleccionada: {receta_seleccionada}")


def agregar_receta(nombre, ingredientes, instrucciones):
    st.title("Agregar Receta")
    # Aquí pondríamos un formulario para agregar una receta
    st.write("Formulario para agregar nuevas recetas.")
    # Función para agregar recetas a la base de datos
    cursor.execute('''
        INSERT INTO recetas (nombre, ingredientes, instrucciones)
        VALUES (?, ?, ?)
    ''', (nombre, ingredientes, instrucciones))
    conn.commit()

def modificar_inventario():
    st.title("Modificar Inventario")
    st.write("Aquí podrás modificar el inventario de ingredientes.")

def visualizacion_datos():
    st.title("Visualización de Datos")
    st.write("Gráficos y estadísticas sobre las recetas.")

# Lógica para cambiar de página
if selection == "Inicio":
    home()
elif selection == "Consultar Recetas":
    consultar_recetas()
elif selection == "Agregar Receta":
    agregar_receta()
elif selection == "Modificar Inventario":
    modificar_inventario()
elif selection == "Visualización de Datos":
    visualizacion_datos()

# Cerrar la conexión a la base de datos
conn.close()

#--------------------------------------------
