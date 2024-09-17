import streamlit as st
import pickle
import requests
import os
from main import preprocess_data
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")

# Load the movies and similarity data
if not os.path.exists('similarity.pkl') or not os.path.exists('movies_list.pkl'):
    preprocess_data()
movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies['title'].values

# Streamlit header and selectbox
st.header("Movie Recommender System")
selectvalue = st.selectbox("Select a movie", movies_list)

def Poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    if movie in movies['title'].values:
        index = movies[movies['title'] == movie].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        recommended_movies = []
        recommend_poster = []
        for i in distance[1:6]: 
            recommended_movies.append(movies.iloc[i[0]].title)
            recommend_poster.append(Poster(movies.iloc[i[0]]['id']))  # Access 'id' column directly
        return recommended_movies, recommend_poster
    else:
        return [f"The movie '{movie}' is not in the dataset."]

if st.button("Show recommendations"):
    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])