#Diego Morales A00836320

#Importación de librerías
import streamlit as st
import pandas as pd

#Seteo de la página (cosas sencillas como el título y el layout)
st.set_page_config(page_title="Testing Streamlit - Diego Morales_A00836320", layout="centered")
st.title("Testing Streamlit - Diego Morales_A00836320 👋")

#Subir el archivo
archivo = st.file_uploader("Sube el archivo XLSX", type="xlsx")

#Para evitar que truene
if archivo is None:
    st.info("Inserta el xlsx")
    st.stop()

#Se crea un dataframe para tener ese archivo en memoria
df = pd.read_excel(archivo) 

#Se selecciona solo para filtrar por región
Region = df["REGION"].unique().tolist()
Region.sort()

#Texto para filtrar por región
st.subheader("Filtrado por región")

#Se selecciona filtrar por región o mostrar tabla completa
Filtro = st.selectbox("Selecciona la región:", ["Todas"] + Region)

#Si elige "Todas" mostramos la tabla completa
if Filtro == "Todas":
    filtered_df = df
else:
    filtered_df = df[df["REGION"] == Filtro]

#Desplegado del dataframe filtrado
st.write(filtered_df)

#Gráficas
st.subheader("Gráficas por Región (Barras)")

# Separación y agrupación de datos por región para las gráficas según tipo de métrica
regiones = (
    df
    .groupby("REGION", as_index=False)[["UNIDADES VENDIDAS", "VENTAS TOTALES"]]
    .sum()
)

regiones_porcentaje = (
    df
    .groupby("REGION", as_index=False)[["PORCENTAJE DE VENTAS"]]
    .mean()
)
#Gráficas de barras por cada una de las métricas
st.subheader("Gráfica de Unidades Vendidas por Región")
st.bar_chart(data=regiones, x="REGION", y="UNIDADES VENDIDAS")

st.subheader("Gráfica de Ventas Totales por Región")
st.bar_chart(data=regiones, x="REGION", y="VENTAS TOTALES")

st.subheader("Gráfica de Porcentaje de Ventas por Región")
st.bar_chart(data=regiones_porcentaje, x="REGION", y="PORCENTAJE DE VENTAS")

#Mostrar datos de un vendedor específico
st.subheader("Datos por Vendedor (en general)")
Vendedores = df["ID"].unique().tolist()
Vendedores.sort()

#Se selecciona el vendedor para poder hacer el filtrado y mostrar la información
Vendedor_seleccionado = st.selectbox("Selecciona el vendedor:", Vendedores)
datos_vendedor = df[df["ID"] == Vendedor_seleccionado]
st.write(datos_vendedor)

#Pequeño titulo para las gráficas
st.subheader("Gráfica de datos (A elección del usuario)")

#Selección de columnas
columnas_numericas = filtered_df.select_dtypes(include=['float', 'int']).columns.tolist()

#Selección de ejes de columnas con un selectbox
x_column = st.selectbox("Selecciona la columna del eje x", columnas_numericas)
y_column = st.selectbox("Selecciona la columna del eje y", columnas_numericas)

#Condición para generar la gráfica y si no, se espera a que se cargue el archivo
if st.button("Generar Gráfica"):
    st.line_chart(filtered_df.set_index(x_column)[y_column])
else:
    with st.spinner("Esperando la carga del archivo..."):
        st.empty()
    #st.write("Waiting on file upload...")

#KPIS
st.subheader("Indicadores de la Región Seleccionada")

#Métricas clave principales según la región seleccionada
st.metric("Total Unidades Vendidas", int(filtered_df["UNIDADES VENDIDAS"].sum()))
st.metric("Total Ventas", round(filtered_df["VENTAS TOTALES"].sum(), 2))
st.metric("Promedio % de Ventas", round(filtered_df["PORCENTAJE DE VENTAS"].mean(), 2))
