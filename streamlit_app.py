import sqlite3
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

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
menu = ["Inicio", "Consultar recetas", "Agregar receta", "Inventario", "Registro de datos"]
selection = st.sidebar.selectbox("Bienvenido Chou. Usa el menú para navegar.", menu)

# Funciónes para cada página
def home():
    st.title("Bienvenido a Chou")
#    st.write("Selecciona una opción del menú para empezar.")

def consultar_recetas():
    st.title("Consultar Recetas")
    st.write("Aquí podrás consultar las recetas existentes.")

    # Filtro por nombre de receta
    recetas = obtener_recetas()
    filtro_nombre = st.text_input("Buscar por nombre de receta")
    recetas_filtradas = [receta for receta in recetas if filtro_nombre.lower() in receta[1].lower()]

    # Mostrar recetas filtradas
    for receta in recetas_filtradas:
        st.subheader(receta[1])
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

def Inventario():
    st.title("Inventario")
    st.write("Aquí podrás modificar el inventario de ingredientes.")
# Mostrar inventario
    cursor.execute("SELECT ingrediente, cantidad, unidad FROM inventario_BP")
    inventario_data = cursor.fetchall()
    df_inventario = pd.DataFrame(inventario_data, columns=["ID Ingrediente", "Ingrediente", "Cantidad", "Unidad"])
    st.table(df_inventario)

def visualizacion_datos():
    st.title("Visualización de Datos 1")
    # Consultar datos desde la base de datos y mostrar gráficos interactivos
    recetas = obtener_recetas()
    nombres = [receta[1] for receta in recetas]
    # Gráfico de cantidad de recetas
    fig1 = plt.figure()
    plt.barh(nombres, [1] * len(nombres))
    plt.xlabel('Cantidad de recetas')
    plt.title('Visualización de Recetas')
    st.pyplot(fig1)
    # Gráfico de costo de ingredientes
    cursor.execute("SELECT nombre_ingrediente, precio FROM ingredientes_BP")
    ingredientes_data = cursor.fetchall()
    df_ingredientes = pd.DataFrame(ingredientes_data, columns=["Ingrediente", "Precio"])
    fig2 = px.bar(df_ingredientes, x="Ingrediente", y="Precio", title="Costo de Ingredientes")
    st.plotly_chart(fig2)

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
elif selection == "Consultar recetas":
    consultar_recetas()
elif selection == "Agregar receta":
    agregar_receta()
elif selection == "Inventario":
    Inventario()
elif selection == "Registro de datos":
    visualizacion_datos()

# Cerrando la conexión a la base de datos
conn.close()

#--------------------------------------------

