import pandas as pd
import streamlit as st

st.title("Mercado laboral en Inteligencia Artificial")
st.write("Análisis de ofertas laborales, salarios y habilidades.")

def promedio(columna):
    """Calcula el promedio de una columna numérica."""
    return columna.mean()



def filtrar_experiencia(tabla, nivel):
    """Filtra los datos según el nivel de experiencia elegido."""
    if nivel == "Todos":
        return tabla
    else:
        return tabla[tabla["experience_level"] == nivel]


archivo = st.file_uploader("Sube el archivo CSV", type="csv")

if archivo is not None:
    datos = pd.read_csv(archivo)
    st.success("Archivo cargado correctamente")

    st.sidebar.header("Filtros")
    nivel = st.sidebar.selectbox("Experiencia", ["Todos", "Entry", "Mid", "Senior"])
    pais = st.sidebar.selectbox("País", ["Todos"] + sorted(datos["country"].unique().tolist()))

    datos = filtrar_experiencia(datos, nivel)

    if pais != "Todos":
        datos = datos[datos["country"] == pais]

    if len(datos) > 0:
        st.header("Resumen de los datos")
        c1, c2, c3 = st.columns(3)
        c1.metric("Ofertas", len(datos))
        c2.metric("Salario promedio", f"{promedio(datos['salary']):,.0f}")
        c3.metric("Experiencia promedio", f"{promedio(datos['years_experience']):.1f} años")

        st.header("1. Salario promedio por experiencia (barras)")
        niveles = ["Entry", "Mid", "Senior"]
        salarios = []

        for nombre in niveles:
            grupo = datos[datos["experience_level"] == nombre]
            if len(grupo) > 0:
                salarios.append(promedio(grupo["salary"]))
            else:
                salarios.append(0)

        tabla_salarios = pd.DataFrame({"Nivel": niveles, "Salario promedio": salarios})
        st.bar_chart(tabla_salarios, x="Nivel", y="Salario promedio")

        st.header("2. Ofertas por año (líneas)")
        ofertas_anuales = datos["job_posting_year"].value_counts().sort_index()
        st.line_chart(ofertas_anuales)

        st.header("3. Salario promedio por año (área)")
        salario_anual = datos.groupby("job_posting_year")["salary"].mean()
        st.area_chart(salario_anual)

        st.header("Cargos más frecuentes")
        st.dataframe(datos["job_title"].value_counts().head(6))

        st.header("Widget 1: consultar ofertas por salario")
        minimo = st.slider("Salario mínimo", 0, 210000, 50000, 10000)
        ofertas = datos[datos["salary"] >= minimo]
        st.write("Ofertas encontradas:", len(ofertas))
        st.dataframe(ofertas[["job_title", "country", "salary"]].head(10))

        st.header("Widget 2: ofertas con Python")
        mostrar = st.checkbox("Mostrar ofertas que requieren Python")
        if mostrar:
            python = datos[datos["skills_python"] == 1]
            st.write("Ofertas con Python:", len(python))
            st.dataframe(python[["job_title", "country", "salary"]].head(10))

        st.header("Primeros registros")
        st.dataframe(datos.head(10))
    else:
        st.warning("No hay ofertas con los filtros seleccionados.")
else:
    st.info("Sube el archivo CSV para comenzar.")
