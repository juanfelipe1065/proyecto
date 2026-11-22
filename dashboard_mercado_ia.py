
import streamlit as st
import pandas as pd


st.title("Mercado laboral en Inteligencia Artificial")
st.write("Dashboard para explorar ofertas laborales, salarios y habilidades.")


archivo = st.file_uploader(
    "Sube el archivo AI Job Market Dataset.csv",
    type="csv"
)

if archivo is not None:

    df = pd.read_csv(archivo)

    st.success("Dataset cargado correctamente")

    
    st.sidebar.header("Filtros")

    experiencias = ["Todos"] + sorted(df["experience_level"].dropna().unique().tolist())

    experiencia = st.sidebar.selectbox(
        "Nivel de experiencia",
        experiencias
    )

    paises = ["Todos"] + sorted(df["country"].dropna().unique().tolist())

    pais = st.sidebar.selectbox(
        "País",
        paises
    )

  
    datos = df.copy()

    if experiencia != "Todos":
        datos = datos[datos["experience_level"] == experiencia]

    if pais != "Todos":
        datos = datos[datos["country"] == pais]

   
    st.header("Resumen del mercado laboral")

    columna1, columna2, columna3 = st.columns(3)

    columna1.metric("Ofertas laborales", len(datos))

    if len(datos) > 0:

        columna2.metric(
            "Salario promedio",
            f"{datos['salary'].mean():,.0f}"
        )

        columna3.metric(
            "Experiencia promedio",
            f"{datos['years_experience'].mean():.1f} años"
        )

       
        st.header("Datos del dataset")

        st.dataframe(datos.head(10))

        
        st.header("Salario promedio según experiencia")

        niveles = ["Entry", "Mid", "Senior"]
        salarios = []

        for nivel in niveles:

            grupo = datos[datos["experience_level"] == nivel]

            if len(grupo) > 0:
                salarios.append(grupo["salary"].mean())
            else:
                salarios.append(0)

        grafica_salarios = pd.DataFrame({
            "Nivel de experiencia": niveles,
            "Salario promedio": salarios
        })

        st.bar_chart(
            grafica_salarios,
            x="Nivel de experiencia",
            y="Salario promedio"
        )

        
        st.header("Habilidades tecnológicas solicitadas")

        habilidades = [
            "skills_python",
            "skills_sql",
            "skills_ml",
            "skills_deep_learning",
            "skills_cloud"
        ]

        nombres_habilidades = [
            "Python",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "Cloud"
        ]

        porcentajes = []

        for habilidad in habilidades:
            porcentajes.append(datos[habilidad].mean() * 100)

        grafica_habilidades = pd.DataFrame({
            "Habilidad": nombres_habilidades,
            "Porcentaje de ofertas": porcentajes
        })

        st.bar_chart(
            grafica_habilidades,
            x="Habilidad",
            y="Porcentaje de ofertas"
        )

       
        st.header("Cargos laborales más frecuentes")

        cargos = datos["job_title"].value_counts().head(6)

        st.bar_chart(cargos)

        st.header("Consultar ofertas por salario")

        st.write(
            "Selecciona el salario mínimo para consultar "
            "las ofertas laborales disponibles."
        )

        salario_minimo = st.slider(
            "Selecciona el salario mínimo",
            min_value=0,
            max_value=210000,
            value=50000,
            step=10000
        )

        ofertas_salario = datos[
            datos["salary"] >= salario_minimo
        ]

        st.write(
            "Cantidad de ofertas encontradas:",
            len(ofertas_salario)
        )

        st.dataframe(
            ofertas_salario[
                ["job_title", "country", "salary"]
            ].head(10)
        )

        
        st.header("Ofertas laborales que requieren Python")

        st.write(
            "Activa la casilla para visualizar las ofertas "
            "laborales que incluyen Python como habilidad."
        )

        mostrar_python = st.checkbox(
            "Mostrar ofertas que requieren Python"
        )

        if mostrar_python:

            ofertas_python = datos[
                datos["skills_python"] == 1
            ]

            st.write(
                "Cantidad de ofertas que requieren Python:",
                len(ofertas_python)
            )

            st.dataframe(
                ofertas_python[
                    ["job_title", "country", "salary"]
                ].head(10)
            )

    else:
        st.warning(
            "No hay registros que coincidan con los filtros seleccionados."
        )

else:
    st.info(
        "Para comenzar, sube el archivo CSV en el espacio de arriba."
    )
