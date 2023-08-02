import streamlit as st
import pickle
import pandas as pd
import requests

#function to fetch movie poster externally
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4bd490a31d83be98fa53606c0a32b614&language=en-US'.format(movie_id))
    data=response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


#driver function to recommend movies

def recommend(movie) :
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]


#storing movies names and posters in new lists
    recommendations=[]
    recommendations_poster=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommendations.append(movies.iloc[i[0]].title)
        recommendations_poster.append(fetch_poster(movie_id))

    return recommendations, recommendations_poster


#loading pickle dump created by 'movie recommender_system' file
movies_list=pickle.load(open('movies_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movies=pd.DataFrame(movies_list)


#creating a website using streamlit
#creating button and basic layout on website
st.title('Movie recommendation system')
selected_movie=st.selectbox('Choose movie you want to get recommendations for : ',movies['title'].values)


#if user presses recommend button on website, this code will execute
if st.button('Recommend'):
    names,poster=recommend(selected_movie)

    #creating a layout of results as names and poster of movies
    col1, col2, col3, col4, col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])

# print(movies_list['title'].values)

