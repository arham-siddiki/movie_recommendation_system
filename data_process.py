import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import warnings
warnings.filterwarnings("ignore")
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import pickle
import requests

# data preprocessing---------------------------------------------->>>>>>
movies = pd.read_csv("tmdb_5000_movies.csv")
credit = pd.read_csv("tmdb_5000_credits.csv")

# concatenating both the datasets on the basis of title
movies = movies.merge(credit, on='title')

# selecting only useful columns from dataset
''' 
    genres
    id
    keyword
    title
    overview
    cast
    crew
'''
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)


# print(movies.isnull().sum())
# print(movies.duplicated().sum())

# converting string to list
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L


# converting string to list
def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L


def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L


# fixing the 'genres', 'keywords', 'cast' and 'crew' columns
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# removing spaces
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

# creating new column('tag')-->concatOf('overview','genres','keywords','cast','crew')
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
# print(movies.head().to_string())

new_df = movies[['movie_id', 'title', 'tags']]

# converting list to string
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'].apply(lambda x: x.lower())

# print(new_df['tags'][0])


# vectorization---------------------------------------------->>>>>>
ps = PorterStemmer()


def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


new_df['tags'] = new_df['tags'].apply(stem)



# text vectorization
# bag of words
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# calculating distances of each vector form each vector
similarity = cosine_similarity(vectors)

#driver function to recoomend movies

def recommend(movie) :
    movie_index=new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    for i in movies_list:
        print(new_df.iloc[i[0]].title)

#creating a pickle dump to be used by driver python file

# pickle.dump(new_df.to_dict(),open('movies_dict.pkl','wb'))

# pickle.dump(similarity,open('similarity.pkl', 'wb'))

#asking for sample recommendation

recommend('Batman Begins')


