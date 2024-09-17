import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pickle

def preprocess_data():
    movies = pd.read_csv('dataset.csv')

    movies = movies[['id', 'title', 'overview', 'genre', 'original_language', 'popularity', 'release_date', 'vote_average', 'vote_count']]

    movies['overview'] = movies['overview'].fillna('')
    movies['genre'] = movies['genre'].fillna('')

    movies['tags'] = movies['overview'] + ' ' + movies['genre']

    new_data = movies.drop(columns=['overview', 'genre'])

    cv = CountVectorizer(max_features=10000, stop_words='english')
    vector = cv.fit_transform(new_data['tags']).toarray()

    similarity = cosine_similarity(vector)

    pickle.dump(new_data, open('movies_list.pkl', 'wb'))
    pickle.dump(similarity, open('similarity.pkl', 'wb'))
    pickle.load(open('movies_list.pkl', 'rb'))


    def recommend(movie):
        if movie in new_data['title'].values:
            index = new_data[new_data['title'] == movie].index[0]
            distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
            
            for i in distance[1:6]:  
                print(new_data.iloc[i[0]].title)
        else:
            print(f"The movie '{movie}' is not in the dataset.")
    
    #recommend('Toy Story')
