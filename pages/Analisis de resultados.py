import sys 
import streamlit as st 
import plotly.express as px 
from pathlib import Path 
import pandas as pd

root = Path(__file__).parent.parent
sys.path.append(str(root))
from utils.dependencias import *

database_path = mapear_datos('Chinook', '.sqlite')
dataframes = cargar_datos(database_path) 

invoices_tbl = dataframes['Invoice']
customers_tbl = dataframes['Customer']
artists_tbl = dataframes['Artist']
albums_tbl = dataframes['Album']
tracks_tbl = dataframes['Track']
genres_tbl = dataframes['Genre']
invoice_tbl = dataframes['InvoiceLine']

st.header("Spotify / CETAV Wrapped 2024")

data = (
    invoice_tbl
    .merge(tracks_tbl, on='TrackId')
    .merge(genres_tbl, on='GenreId')
    .merge(albums_tbl, on='AlbumId')
    .merge(artists_tbl, on='ArtistId')
    .merge(invoices_tbl, on='InvoiceId')
    .merge(customers_tbl, on='CustomerId')
)

data = data.rename(columns={
    'Name': 'Artista',
    'Title': 'Álbum',
    'InvoiceDate': 'Fecha',
    'Quantity': 'Cantidad',
    'Name_y': 'Género',
    'Country': 'País',
    'Total': 'Total',
})

data['Fecha'] = pd.to_datetime(data['Fecha'])

st.sidebar.header("Filtros")

## Filtro por rango de fecha
min_date = data['Fecha'].min()
max_date = data['Fecha'].max()
date_range = st.sidebar.date_input(
    "Rango de Fechas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

## slider para ventas
min_sales = data['Total'].min()
max_sales = data['Total'].max()
sales_range = st.sidebar.slider(
    "Rango de Ventas Totales",
    min_value=float(min_sales),
    max_value=float(max_sales),
    value=(float(min_sales), float(max_sales)),
)


unique_country = data['País'].unique()
# Seleccionar 8 países de forma predeterminada
default_countries = unique_country
selected_country = st.sidebar.multiselect(
    "Países",
    options=unique_country,
    default=default_countries
)

## filter para artistas
unique_artist = data['Artista'].unique()
default_artists = unique_artist 
selected_artist = st.sidebar.multiselect(
    "Artistas",
    options=unique_artist,
    default=default_artists
)

## filter para género musical
unique_genre = data['Género'].unique()

default_genres = unique_genre 
selected_genre = st.sidebar.multiselect(
    "Género musical",
    options=unique_genre,
    default=default_genres
)

mask = (
    (data['Fecha'] >= pd.to_datetime(date_range[0])) &
    (data['Fecha'] <= pd.to_datetime(date_range[1])) &
    (data['Artista'].isin(selected_artist)) &
    (data['Género'].isin(selected_genre)) &
    (data['País'].isin(selected_country))
)

#Aplicar máscaras
mask = (
    (data['Fecha'] >= pd.to_datetime(date_range[0])) &
    (data['Fecha'] <= pd.to_datetime(date_range[1])) &
    (data['Total'] >= sales_range[0]) &
    (data['Total'] <= sales_range[1]) &
    (data['Artista'].isin(selected_artist)) &
    (data['Género'].isin(selected_genre)) &
    (data['País'].isin(selected_country))
)

data_filtered = data[mask]

# métricas
total_sales = data_filtered['Total'].sum()
total_artists = data_filtered['Artista'].nunique()
total_albumns = data_filtered['Álbum'].nunique()
total_tracks = data_filtered['TrackId'].nunique()
total_countries = data_filtered['País'].nunique()

st.subheader("Métricas Generales")

col1, col2, col3, col4= st.columns(4)
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Artistas 👤",
            value=total_artists
        )
    with col2:
        st.metric(
            label="Canciones 🎶",
            value=total_tracks
        )
    with col3:
        st.metric(
            label="Álbumes 📀",
            value=total_albumns
        )
    with col4:
        st.metric(
            label="Países 🌍",
            value=total_countries
        )
        
st.divider()

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
## Gráfico 1: Pie chart - Proporción de ventas por género
sales_by_genre = (
    data_filtered.groupby('Género', as_index=False)
    .agg({'Total': 'sum'})
)

fig_pie_genre = px.pie(
    sales_by_genre,
    names='Género',
    values='Total',
    title='Proporción de Ventas por Género Musical',
    labels={'Género': 'Género', 'Total': 'Total Ventas'},
    color_discrete_sequence=px.colors.sequential.Viridis
)
st.plotly_chart(fig_pie_genre)

container = st.container(border=True)
container.write("El gráfico anterior muestra la proporción de ventas según el género musical, "
                "lo que permite identificar los géneros más vendidos. Esta información es clave para optimizar las "
                "estrategias de marketing y la gestión del inventario, enfocándose en los géneros con mayor demanda.")
st.divider()

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

## Gráfico 2: Línea - Evolución de ventas totales por fecha
sales_by_date = (
    data_filtered.groupby('Fecha', as_index=False)
    .agg({'Total': 'sum'})
)

fig_line_sales = px.line(
    sales_by_date,
    x='Fecha',
    y='Total',
    title='Evolución de Ventas Totales por Fecha',
    labels={'Fecha': 'Fecha', 'Total': 'Total Ventas'},
    color_discrete_sequence=px.colors.sequential.Teal
)
st.plotly_chart(fig_line_sales)


container = st.container(border=True)
container.write("El gráfico de línea muestra la evolución de las ventas totales a lo largo del tiempo, "
                "permitiendo identificar patrones y tendencias. Esto es fundamental para ajustar las estrategias de ventas "
                "y la planificación de inventarios, especialmente para identificar temporadas de alta demanda.")
st.divider()

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

## Gráfico 3: Barras horizontales - Métrica seleccionada por artista

metrics_per_artist = (
    data_filtered.groupby('Artista', as_index=False)
    .agg({'Total': 'sum'})
    .sort_values(by='Total', ascending=False)
)

fig_barras = px.bar(
    metrics_per_artist,
    x='Total',
    y='Artista',
    orientation='h',
    title='Total por Artista',
    labels={'Total': 'Total', 'Artista': 'Artista'},
    color='Total',
    color_continuous_scale='Plasma'
)
st.plotly_chart(fig_barras)

container = st.container(border=True)
container.write("El gráfico anterior muestra los artistas más exitosos según el total de ventas. "
                "Esto puede ayudar a identificar qué artistas generan más ingresos, y así orientar las campañas de marketing.")
st.divider()

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

## Gráfico 4: Dispersión - Métrica seleccionada vs. cantidad de pistas
metrics_by_track = (
    data_filtered.groupby('Álbum', as_index=False)
    .agg({'Cantidad': 'sum', 'Total': 'sum'})
)

fig_dispersion = px.scatter(
    metrics_by_track,
    x='Cantidad',
    y='Total',
    size='Total',
    color='Álbum',
    title='Ventas vs Canciones', 
    labels={'Cantidad': 'Cantidad de Pistas', 'Total': 'Total', 'Álbum': 'Álbum'},
    color_continuous_scale='Cividis'
)
st.plotly_chart(fig_dispersion)

container = st.container(border=True)
container.write("Este gráfico muestra la relación entre el número de pistas de un álbum y su total de ventas. "
                "El análisis de estos datos puede ofrecer perspectivas sobre si la cantidad de canciones influye en el volumen de ventas.")
st.divider()

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

## Gráfico 5: Barras verticales - Ventas por país
metrics_country = (
    data_filtered.groupby('País', as_index=False)
    .agg({'Total': 'sum'})
    .sort_values(by='Total', ascending=False)
)

fig_barras = px.bar(
    metrics_country,
    x='País',
    y='Total',
    title='Total de Ventas por País',
    labels={'Total': 'Total Ventas', 'País': 'País'},
    color='Total',
    color_continuous_scale='Plasma' 
)

fig_barras.update_layout(
    xaxis_tickangle=-45
)

st.plotly_chart(fig_barras)

container = st.container(border=True)
container.write(
    "Este gráfico revela el total de ventas por país, permitiéndonos identificar "
    "los países con mayor contribución a las ventas. Con esta información, podemos destacar "
    "las regiones más fuertes en términos de consumo musical y observar cómo varían las preferencias a nivel global."
)
st.divider()
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

st.caption("Git commit -m 'Rex-on-a'")