import streamlit as st
import pickle
import requests



API_KEY = "6e5f210f9131ae0fb692cb326f0c9bea"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get('poster_path')
        if not poster_path:
            return "https://via.placeholder.com/300x450?text=No+Poster"

        return "https://image.tmdb.org/t/p/w500/" + poster_path

    except requests.exceptions.RequestException as e:
        print("TMDB request failed:", e)
        return "https://via.placeholder.com/300x450?text=Error"


def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distance=similarity[movie_index]
    movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

st.header('Movie  Recommendation system')

movies=pickle.load(open('movies.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values,
)


if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    for idx, col in enumerate([col1, col2, col3, col4, col5]):
        col.text(recommended_movie_names[idx])
        col.image(recommended_movie_posters[idx])




