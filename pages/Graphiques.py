import streamlit as st
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Graphiques",
    page_icon="📊",
    layout="wide"
)

df_films = pd.read_csv("pages/data_P2_final.csv")




# réutiliser le CSS
with open("frontend/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Page Graphiques")
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.write("Nombre de Films Par Année")
st.markdown("<br>", unsafe_allow_html=True)




#  nmbr de films par années
df = pd.DataFrame({
    "Année": [1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025
],
    "Films": [331,312,330,340,385,390,442,510,542,548,498,509,497,532,532,584,592,685,696,674,688,709,720,671,760,885,1001,1107,1168,1300,1207,1403,1564,1769,1794,1786,1928,2060,2024,2048,1823,1875,2002,1072,36,5
]
})

st.line_chart(df.set_index("Année"))



col1, col2 = st.columns(2)


# >>> On fait un pie chart ici :
with col1:

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.write("Les Genres de Films")
    st.markdown("<br>", unsafe_allow_html=True)

    df_camembert = df_films.copy()

    df_camembert["genres"] = df_camembert["genres"].str.split(",")
    df_camembert = df_camembert.explode("genres")
    df_camembert["genres"] = df_camembert["genres"].str.strip()

    top5 = df_camembert["genres"].value_counts().head(5)

    fig, ax = plt.subplots(figsize=(4, 4))

    ax.pie(top5.values, labels=top5.index, autopct="%1.1f%%", startangle=360, radius=0.9)

    ax.set_title("Top 5 des genres")

    st.pyplot(fig, use_container_width=False)






# >>> On fait un subplot avec la durée des films en moyenne:
with col2:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.write("La Durée")
    st.markdown("<br>", unsafe_allow_html=True)

    df_films["runtimeMinutes"] = pd.to_numeric(df_films["runtimeMinutes"], errors="coerce")
    df_films = df_films.dropna(subset=["runtimeMinutes", "release_year"])

    df_films = df_films[df_films["release_year"] >= 1980]

# Créer les tranches de 5 ans
    df_films["year_5"] = (df_films["release_year"] // 5) * 5

# Moyenne de durée par tranche
    data_mean_films = df_films.groupby("year_5")["runtimeMinutes"].mean()

# Graphique
    fig, ax = plt.subplots(figsize=(4, 4))

    data_mean_films.plot(kind="bar", ax=ax)

    ax.set_title("Durée moyenne des films (par tranche de 5 ans)")
    ax.set_xlabel("Année")
    ax.set_ylabel("Durée (minutes)")

    st.pyplot(fig, use_container_width=False)






# Bar chart avec le top 20 nmbr film par acteur:

# --- Bar chart : Top 20 acteurs par nombre de films ---

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.write("Les Acteurs les Plus Populaires")
st.markdown("<br>", unsafe_allow_html=True)

actor_counts = (df_films.groupby("primaryName")["tconst"].nunique().reset_index(name="nb_films").sort_values("nb_films", ascending=False))

top_actors = actor_counts.head(20)

fig, ax = plt.subplots(figsize=(4, 6))

ax.barh(top_actors["primaryName"],top_actors["nb_films"])

ax.invert_yaxis()

ax.set_title("Top 20 acteurs par nombre de films")
ax.set_xlabel("Nombre de films")
ax.set_ylabel("Acteur")

st.pyplot(fig, use_container_width=False)






# >>> Bar chart Top 20 films avec la note la plus haute :

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.write("Les Mieux Notés")
st.markdown("<br>", unsafe_allow_html=True)

df_ratings = df_films[df_films["vote_count"] >= 500].copy()

top_movies = (df_ratings.sort_values("vote_average", ascending=False).head(20))

fig, ax = plt.subplots(figsize=(4, 6))

bars = ax.barh(top_movies["title"],top_movies["vote_average"])

ax.invert_yaxis()
ax.set_title("Top 20 des films les mieux notés (≥ 500 votes)")
ax.set_xlabel("Note moyenne")
ax.set_ylabel("Film")

# Affichage des valeurs sur les barres
for bar, note in zip(bars, top_movies["vote_average"]):
    ax.text(bar.get_width() + 0.05,bar.get_y() + bar.get_height() / 2,f"{note:.1f}",va="center")

st.pyplot(fig, use_container_width=False)


