
import pandas as pd
import streamlit as st
import numpy as np

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Mercado Laboral IA",
    page_icon="🤖",
    layout="wide"
)

# DISEÑO Y COLORES
st.markdown("""
<style>
.stApp {
    background-color: #0e1525;
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.tarjeta {
    background-color: #19263d;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #304563;
    text-align: center;
}
.tarjeta h3 {
    color: #9db8df !important;
    font-size: 15px;
}
.tarjeta h2 {
    color: #45c4e8 !important;
    font-size: 27px;
}
</style>
""", unsafe_allow_html=True)

# ENCABEZADO
st.title("🤖 Mercado Laboral en Inteligencia Artificial")
st.write("Explora las tendencias, salarios y habilidades que buscan las empresas en el sector de la IA.")

st.markdown("---")

# CARGAR ARCHIVO
archivo = st.file_uploader(
    "📂 Carga el archivo del mercado laboral",
    type=["csv"]
)

if archivo:

    datos_completos = pd.read_csv(archivo)
    datos = datos_completos.copy()

    st.success("Dataset cargado correctamente")

    # FILTRO
    st.sidebar.title("⚙️ Filtros")
    experiencia = st.sidebar.selectbox(
        "Nivel de experiencia",
        ["Todos", "Entry", "Mid", "Senior"]
    )

    if experiencia == "Entry":
        datos = datos[datos["experience_level"] == "Entry"]

    elif experiencia == "Mid":
        datos = datos[datos["experience_level"] == "Mid"]

    elif experiencia == "Senior":
        datos = datos[datos["experience_level"] == "Senior"]

    # INDICADORES
    st.subheader("📊 Resumen general")

    salarios = datos["salary"].to_numpy()

    cantidad = len(datos)
    promedio = np.mean(salarios)
    maximo = np.max(salarios)
    minimo = np.min(salarios)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="tarjeta">
            <h3>Ofertas laborales</h3>
            <h2>{cantidad:,}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="tarjeta">
            <h3>Salario promedio</h3>
            <h2>{promedio:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="tarjeta">
            <h3>Salario máximo</h3>
            <h2>{maximo:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="tarjeta">
            <h3>Salario mínimo</h3>
            <h2>{minimo:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # GRÁFICO DE SALARIOS
    st.subheader("💰 Salario promedio por experiencia")

    entry = datos_completos[datos_completos["experience_level"] == "Entry"]
    mid = datos_completos[datos_completos["experience_level"] == "Mid"]
    senior = datos_completos[datos_completos["experience_level"] == "Senior"]

    salario_entry = entry["salary"].mean()
    salario_mid = mid["salary"].mean()
    salario_senior = senior["salary"].mean()

    grafico_salarios = pd.DataFrame({
        "Salario promedio": [
            salario_entry,
            salario_mid,
            salario_senior
        ]
    }, index=["Entry", "Mid", "Senior"])

    st.bar_chart(grafico_salarios)

    st.markdown("---")

    # HABILIDADES
    st.subheader("🧠 Habilidades tecnológicas más solicitadas")

    python = datos["skills_python"].mean() * 100
    sql = datos["skills_sql"].mean() * 100
    ml = datos["skills_ml"].mean() * 100
    deep = datos["skills_deep_learning"].mean() * 100
    cloud = datos["skills_cloud"].mean() * 100

    habilidades = pd.DataFrame({
        "Porcentaje de ofertas": [
            python, sql, ml, deep, cloud
        ]
    }, index=[
        "Python",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Cloud"
    ])

    st.bar_chart(habilidades)

    st.markdown("---")

    # MEJORES SALARIOS
    st.subheader("🏆 Ofertas laborales con mayores salarios")

    top10 = datos.sort_values(
        "salary",
        ascending=False
    ).head(10)

    st.dataframe(
        top10[[
            "job_title",
            "country",
            "salary",
            "experience_level"
        ]],
        use_container_width=True,
        hide_index=True
    )

    # DATOS COMPLETOS
    with st.expander("🔎 Ver todos los datos del dataset"):
        st.dataframe(datos, use_container_width=True)

    st.markdown("---")
    st.caption("Proyecto académico | Análisis del mercado laboral en inteligencia artificial")

else:
    st.info("👆 Sube el archivo CSV para comenzar el análisis.")
