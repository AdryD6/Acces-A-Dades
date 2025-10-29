import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📚 Dashboard Interactivo de Libros")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('datos_libros.csv')
        return df
    except FileNotFoundError:
        st.error("Error: No se encontró 'datos_libros.csv'. Ejecuta 'python scraper.py' primero.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['Rating_Num'] = df['Rating'].map(rating_map)

    st.sidebar.header("Opciones de Filtro")

    ratings_disponibles = sorted(df['Rating'].unique(), key=lambda x: rating_map.get(x, 0), reverse=True)
    rating_seleccionado = st.sidebar.multiselect(
        "Filtrar por Puntuación (Rating)",
        options=ratings_disponibles,
        default=ratings_disponibles
    )

    min_precio = df['Precio'].min()
    max_precio = df['Precio'].max()
    rango_precio = st.sidebar.slider(
        "Seleccionar Rango de Precio (£)",
        min_value=float(min_precio),
        max_value=float(max_precio),
        value=(float(min_precio), float(max_precio))
    )

    df_filtrado = df[
        (df['Rating'].isin(rating_seleccionado)) &
        (df['Precio'] >= rango_precio[0]) &
        (df['Precio'] <= rango_precio[1])
    ]

    st.subheader("Tabla de Resultados Filtrados")
    st.dataframe(df_filtrado[['Titulo', 'Precio', 'Rating']], use_container_width=True)

    st.subheader("Análisis de Precios por Puntuación")

    if not df_filtrado.empty:
        df_agrupado = df_filtrado.groupby('Rating')['Precio'].mean().reset_index()
        df_agrupado.columns = ['Rating', 'Precio Promedio (£)']
        
        df_agrupado['Order'] = df_agrupado['Rating'].map(rating_map)
        df_agrupado = df_agrupado.sort_values('Order', ascending=False)
        
        fig = px.bar(
            df_agrupado,
            x='Rating',
            y='Precio Promedio (£)',
            title='Precio Promedio por Nivel de Puntuación',
            color='Rating',
            category_orders={"Rating": df_agrupado['Rating'].tolist()}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Ajusta los filtros: No hay datos para el análisis.")