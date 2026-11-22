import pandas as pd
import streamlit as st
import numpy as np


st.set_page_config(
    page_title="Mercado Laboral IA",
    layout="centered"
)


st.title("Análisis del Mercado Laboral en IA")
st.write("Bienvenido al análisis de ofertas laborales relacionadas con la Inteligencia Artificial.")


archivo = st.file_uploader(
    "Sube el archivo AI Job Market Dataset",
    type=["csv"]
)

if archivo:

    datos = pd.read_csv(archivo)

    st.success("Dataset cargado correctamente")

    st.subheader("Datos del mercado laboral")
    st.dataframe(datos)

   
    st.subheader("Filtrar por experiencia")

    experiencia = st.selectbox(
        "Selecciona el nivel de experiencia",
        ["Todos", "Entry", "Mid", "Senior"]
    )


    if experiencia == "Entry":
        datos = datos[datos["experience_level"] == "Entry"]

    elif experiencia == "Mid":
        datos = datos[datos["experience_level"] == "Mid"]

    elif experiencia == "Senior":
        datos = datos[datos["experience_level"] == "Senior"]

    
    salarios = datos["salary"].to_numpy()

  
    total = np.sum(salarios)
    promedio = np.mean(salarios)
    mediana = np.median(salarios)
    minimo = np.min(salarios)
    maximo = np.max(salarios)

  
    st.subheader("Estadísticas de salarios")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total de salarios", f"{total:,.0f}")
    col2.metric("Promedio", f"{promedio:,.0f}")
    col3.metric("Mediana", f"{mediana:,.0f}")
    col4.metric("Mínimo", f"{minimo:,.0f}")
    col5.metric("Máximo", f"{maximo:,.0f}")

   
    st.subheader("Comparación de salarios por experiencia")

    entry = datos[datos["experience_level"] == "Entry"]
    mid = datos[datos["experience_level"] == "Mid"]
    senior = datos[datos["experience_level"] == "Senior"]

    salario_entry = entry["salary"].mean()
    salario_mid = mid["salary"].mean()
    salario_senior = senior["salary"].mean()

    grafico = pd.DataFrame({
        "Salario promedio": [
            salario_entry,
            salario_mid,
            salario_senior
        ]
    }, index=["Entry", "Mid", "Senior"])

    st.bar_chart(grafico)

    # Habilidades tecnológicas
    st.subheader("Habilidades tecnológicas más solicitadas")

    python = datos["skills_python"].mean() * 100
    sql = datos["skills_sql"].mean() * 100
    ml = datos["skills_ml"].mean() * 100
    deep_learning = datos["skills_deep_learning"].mean() * 100
    cloud = datos["skills_cloud"].mean() * 100

    habilidades = pd.DataFrame({
        "Porcentaje de ofertas": [
            python,
            sql,
            ml,
            deep_learning,
            cloud
        ]
    }, index=[
        "Python",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Cloud"
    ])

    st.bar_chart(habilidades)

    # Mostrar las 10 ofertas con salarios más altos
    st.subheader("10 ofertas con salarios más altos")

    top10 = datos.sort_values(
        "salary",
        ascending=False
    ).head(10)

    st.dataframe(top10[[
        "job_title",
        "country",
        "salary",
        "experience_level"
    ]])

else:

    st.warning(
        "Por favor, sube el archivo CSV para continuar con el análisis."
    )