import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Airbnb Project", layout="wide")

st.markdown(
    """
    <style>
    .main-title {
        color: #E74C3C;
        font-size: 40px;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="main-title">Analiza Turismului și a Facilităților </h1>', unsafe_allow_html=True)

section = st.sidebar.radio("Navigați la:",
                           ["Introducere",
                            "Explorare Date",
                            "Statistici și Agregari",
                            "Filtrare Interactiva"
                            ])

if 'df_airbnb' not in st.session_state:
    df = pd.read_csv('listim.csv')

    df['Pret_Noapte'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)
    df['Cartier'] = df['neighbourhood_cleansed']
    df['Rating'] = df['review_scores_rating']
    df['Nume_Locatie'] = df['name']

    st.session_state.df_airbnb = df[['Nume_Locatie', 'Cartier', 'Pret_Noapte', 'Rating']].dropna()

if section == "Introducere":
    st.header("1. Bun venit!")
    st.write(""" Analiza AirBnb. """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_Bélo.svg", width=200)

elif section == "Explorare Date":
    st.header("2. Vizualizare set de date")
    df = st.session_state.df_airbnb

    st.write(f"Setul de date conține {len(df)} inregistrari valide.")
    st.dataframe(df.head(10))

elif section == "Statistici și Agregari":
    st.header("3. Statistici și Agregari")
    df = st.session_state.df_airbnb

    st.write("Analiza prețului mediu și a rating-ului pe fiecare cartier:")

    agregare = df.groupby('Cartier').agg({
        'Pret_Noapte': 'mean',
        'Rating': 'mean',
        'Nume_Locatie': 'count'
    }).rename(columns={'Nume_Locatie': 'Nr_Locatii'})

    st.dataframe(agregare.style.highlight_max(axis=0, color='#F1948A'))

    st.write("Statistici generale (Describe):")
    st.table(df[['Pret_Noapte', 'Rating']].describe())

elif section == "Filtrare Interactiva":
    st.header("4. Widget-uri Interactive")

    df = st.session_state.df_airbnb

    interval_pret = st.slider("Selecteaza intervalul de pret:", 30, 3100, (30, 3100))

    cartiere_alese = st.multiselect("Alege cartierele:", df['Cartier'].unique(), default=df['Cartier'].unique()[:3])

    mask = (df['Pret_Noapte'] >= interval_pret[0]) & \
           (df['Pret_Noapte'] <= interval_pret[1]) & \
           (df['Cartier'].isin(cartiere_alese))

    df_filtrat = df[mask]

    st.write(f"Rezultate gasite: {len(df_filtrat)}")
    st.dataframe(df_filtrat)