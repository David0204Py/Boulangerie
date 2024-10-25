import sqlite3
import streamlit as st
import matplotlib.pyplot as plt

#Correccion de librerias
# Funcion para cargar el archivo JavaScript
def load_js(file_name):
    with open(file_name) as f:
        st.markdown(f'<script>{f.read()}</script>', unsafe_allow_html=True)

# Llamando la función para cargar el JS
load_js('static/script.js')

# Función para cargar el archivo CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Llamando la funcion para cargar el CSS
load_css('static/styles.css')

# Conectando a la base de datos
conn = sqlite3.connect('base_datos.db')
cursor = conn.cursor()

# Mostrando el logo en la interfaz general
st.image('Icono_020_PNG_BP.png', width=400)

# Sistema de navegación
menu = ["Inicio", "Consultar Recetas", "Agregar Receta", "Modificar Inventario", "Visualización de Datos"]
selection = st.sidebar.selectbox("Bienvenido Chou. Usa el menú para navegar.", menu)

# Funciónes para cada página
def home():
    st.title("Bienvenido a Chou")
#    st.write("Selecciona una opción del menú para empezar.")

def consultar_recetas():
    st.title("Consultar Recetas")
    st.write("Aquí podrás consultar las recetas existentes.")
    # Consultar las recetas
    recetas = obtener_recetas()    
    # Mostrar las recetas en un dropdown
    receta_seleccionada = st.selectbox('Selecciona una receta', [r[1] for r in recetas])
    if receta_seleccionada:
        # Mostrar detalles de la receta seleccionada
        for receta in recetas:
            if receta[1] == receta_seleccionada:  # Comparar el nombre de la receta
                st.subheader(receta[1])  # Nombre de la receta
                st.write(f"**Nombre de Receta:** {receta[1]}")
                st.write(f"**Instrucciones:** {receta[7]}")
                st.write(f"**Tiempo de preparacion:** {receta[2]}")
                st.write(f"**Referencia:** {receta[5]}")
                st.write(f"**Pagina:** {receta[6]}")
                st.write("---")
    
    # Mostrar todas las recetas
    st.write("Lista de todas las recetas:")
    for receta in recetas:
        st.subheader(receta[1])  # Nombre de la receta
        st.write(f"**Ingredientes:** {receta[2]}")
        st.write(f"**Instrucciones:** {receta[7]}")
        st.write("---")

def agregar_receta():
    st.title("Agregar Receta")
    # Formulario para agregar nuevas recetas
    nombre = st.text_input("Nombre de la receta")
    ingredientes = st.text_area("Ingredientes")
    instrucciones = st.text_area("Instrucciones")
    if st.button("Agregar Receta"):
        agregar_receta_db(nombre, ingredientes, instrucciones)
        st.success("Receta agregada exitosamente!")

def modificar_inventario():
    st.title("Modificar Inventario")
    st.write("Aquí podrás modificar el inventario de ingredientes.")

def visualizacion_datos():
    st.title("Visualización de Datos")
    # Manejo de errores obteniendo recetas desde la base de datos
    try:
        recetas = obtener_recetas()
        if not recetas:
            st.write("No hay recetas en la base de datos para mostrar.")
            return
        # Extraer nombres de las recetas (están en la segunda columna)
        nombres = [receta[1] for receta in recetas if receta[1]]  # Filtrar valores nulos
        # Si hay nombres, continuar con la visualización
        if nombres:
            fig, ax = plt.subplots()
            ax.barh(nombres, [1] * len(nombres))  # Cada receta se muestra como una barra    
            ax.set_xlabel('Cantidad')
            ax.set_title('Distribución de Recetas')
            st.pyplot(fig)
        else:
            st.write("No hay nombres de recetas válidos para mostrar.")
    except Exception as e:
        st.error(f"Error al cargar las recetas: {e}")

# Función para agregar recetas a la base de datos
def agregar_receta_db(nombre, ingredientes, instrucciones):
    cursor.execute('''
        INSERT INTO recetas_BP (nombre, ingredientes, instrucciones)
        VALUES (?, ?, ?)
    ''', (nombre, ingredientes, instrucciones))
    conn.commit()

# Función para obtener todas las recetas
def obtener_recetas():
    cursor.execute("SELECT * FROM recetas_BP")
    return cursor.fetchall()

# Lógica para navegar entre páginas
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

# Cerrando la conexión a la base de datos
conn.close()

#--------------------------------------------
