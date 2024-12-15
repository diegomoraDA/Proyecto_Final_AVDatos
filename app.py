import streamlit as st 
import plotly.express as px 
import time
import sqlite3

# General Information Section
st.title("Chinook como proveedor de datos musicales")
container = st.container()
container.write("**Author:** Juan Diego Vasquez M.")
container.write("**Published:** December 9th, 2024")

# Objective Section
container = st.container()
container.write("### Objetivo del Informe")
container.write(
    "El objetivo del informe es analizar patrones de consumo y tendencias de ventas en la tienda de música digital Chinook, "
    "con el fin de ofrecer insights clave que apoyen la toma de decisiones comerciales, como optimización de inventarios y estrategias de marketing."
)

# Database Section
container = st.container()
container.write("### Base de Datos")
container.write(
    "La base de datos utilizada es Chinook_Sqlite, seleccionada por su estructura de tablas con relaciones que permiten un análisis profundo en áreas de música, artistas y ventas."
)

# Purpose Section
container = st.container()
container.write("### Propósito")
container.write(
    "A través de la visualización de datos, se busca proporcionar información valiosa que permita entender mejor el comportamiento "
    "de los mercados, las preferencias de los clientes, y otros datos de valor relacionados con las ventas."
)

# Specific Objectives Section
container = st.container()
container.write("### Objetivos Específicos")
container.write("- Determinar los géneros musicales más vendidos para entender la distribución de las ventas en la base de datos.")
container.write("- Mostrar la evolución de los ingresos mensuales para observar patrones y tendencias a lo largo del tiempo.")
container.write("- Analizar la relación entre la duración de las canciones y las ventas para determinar si existe alguna correlación significativa.")

# Adding Key Questions
container = st.container()
container.write("### Preguntas Clave")
container.write("#### ¿Cómo varían las ventas totales a lo largo del tiempo?")
container.write(
    "Se busca identificar patrones estacionales en las ventas de música, lo que permitirá planificar mejor los lanzamientos "
    "de productos y las campañas de marketing."
)
container.write("#### ¿Cuál es la relación entre el número de pistas en un álbum y las ventas totales de ese álbum?")
container.write(
    "Este análisis tiene como objetivo identificar el número óptimo de pistas que favorezca un mayor volumen de ventas, "
    "lo cual es clave para los productores y artistas al decidir la estructura de los álbumes."
)
container.write("#### ¿Qué factores o períodos han influido más en las ventas por artista y por álbum?")
container.write(
    "A través de la comparación de ventas entre artistas, géneros y años, se pretende encontrar correlaciones que permitan "
    "entender mejor el comportamiento de los consumidores y predecir períodos de alta demanda."
)
container.write("#### ¿Cómo la digitalización y las plataformas de streaming afectan las ventas de música?")
container.write(
    "Analizando el comportamiento de las ventas a lo largo de los años, se identificarán los años clave en los que las plataformas "
    "de streaming y otros factores tecnológicos influyeron en el rendimiento de las ventas."
)