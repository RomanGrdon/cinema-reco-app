import streamlit as st
import pandas as pd
import numpy as np
import joblib # >>> Joblib permet de charger le model ML et le Scaler déjà 'train' (évite de re train a chaque lancement du site)

# >>> On configure la page 
st.set_page_config(page_title="PasThé - Le Meilleur Film", page_icon="🐔", layout="wide")

# >>> On charge et on affiche le CSS
with open("frontend/style.css",encoding="utf-8") as f: # >>> On donne le chemin d'acces en local (dans nos fichiers)
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True) # >>> Ici on injecte le css dans la page, 'unsafe_etc...' autorise Streamlite à interpreter le css

# >>> On charge et on affiche le HTML
with open("frontend/index.html",encoding="utf-8") as f: # idem
    st.markdown(f.read(), unsafe_allow_html=True) # idem

# >>> On charge le DF
df = pd.read_parquet("artifacts/movies.parquet") # >>> Depuis le fichier '.parquet' > Permet de stocker les données dans un fichier otpi
X_features = pd.read_parquet("artifacts/X_features.parquet") # >>> DF de X features (.parquet = donnée en binaire uniquement)

# >>> On charge le model KNN déjà train :
model = joblib.load("artifacts/knn_model.joblib")
# >>> On charge le model StandarScaler déjà Train:
scaler = joblib.load("artifacts/scaler.joblib")

st.markdown("<br><br>", unsafe_allow_html=True) # >>> Espace

# >>> Ici on fait un menu déroulant pour le choix du films, triés ordre Alpha et convertis en STR (pas d'écris, on clique donc aps d'erreur de saisi)
film = st.selectbox("Choisis un film",df["title"].astype(str).sort_values().tolist())

st.markdown("<br>", unsafe_allow_html=True)

# >>> Ici on fait une barre pour choisir le nombre de reco afficher "Slide"
k = st.slider("Nombre de recommandations",min_value=3,max_value=12,value=6)

st.markdown("<br><br>", unsafe_allow_html=True)

# >>> On cherche l’index du film choisi dans le DataFrame df
# >>> On crée un masque booléen pour trouver la ligne où le titre correspond
# >>> (Cet index sera ensuite utilisé pour récupérer la même ligne dans X_features)
idx_ref = df.index[df["title"].astype(str) == film][0] 

# >>> On standardise les features
X_scaled = scaler.transform(X_features)

# >>> On selectionne le film de réf (on l'isole)
x_ref = X_scaled[idx_ref].reshape(1, -1) # >>> Recup une ligne (film choisi), reshape au format scikit-learn

# >>> On cherche les films les plus proches
distances, indices = model.kneighbors(x_ref,n_neighbors=k + 1) # >>> k+1 pour ne pas afficher lui même

# >>> Ici on supprime le premier film de la liste (lui même) avec [1:]
rec_idx = indices[0][1:]
rec_dist = distances[0][1:]

# >>> On fait le tableau des reco
reco = df.loc[rec_idx, ["title","url","overview", "runtimeMinutes", "genres"]].copy()
#reco["distance"] = np.round(rec_dist, 3) #>>>> Si on veut afficher un tableau avec les distances)
reco = reco.rename(columns={"title": "Film recommandé"})

# >>> On affiche les reco

BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

cards_html = '<div class="cards-container">'

image_none = "https://raw.githubusercontent.com/RomanGrdon/Image-Pasth-/main/Pasthe.png"

for x, row in reco.iterrows():   # >>> Ce qu'on veut afficher dans les cartes des films recommandés :
    titre = row["Film recommandé"]
    img_path = row["url"]
    overview = row["overview"]
    runtime = row["runtimeMinutes"]
    genres = row["genres"]

       # >>> Gestion image (affiche ou placeholder)
    if (pd.isna(img_path) or img_path in ["/", "", " "] or not str(img_path).startswith("/")): 

        image_html = f'<img src="{image_none}" style="width:120px; border-radius:8px; margin-bottom:8px;">'
    else:
        image_html = f'<img src="{BASE_IMAGE_URL + img_path}" style="width:120px; border-radius:8px; margin-bottom:8px;">'

    if pd.isna(overview):
        overview = "Résumé non disponible." # On gere si résumé ou pas

    if pd.isna(runtime):
        runtime = "Durée inconnue" # Idem pour la durée
    else:
        runtime = f"{int(runtime)} min"
        
    if pd.isna(genres) or genres == "": # Idem pour genre
        genres = "Genre inconnu"


    cards_html += (
        '<div class="card">'
        f'{image_html}'
        f'<h4>{titre}</h4>'
        f'<p><b>Genre :</b> {genres}</p>'
        f'<p><b>Durée :</b> {runtime}</p>'
        f'<p>{overview}</p>'
        '</div>'
    )

cards_html += '</div>'

st.markdown(cards_html, unsafe_allow_html=True)




