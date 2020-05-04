from .mongohandler import *
import pandas as pd

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cosine_distances
from sklearn.metrics.pairwise import euclidean_distances as euclidean_distances

raw_corpus = lambda query, username : " ".join(list(iter_messages_from_user(query, username)))   

def user_similarity_matrix():
    USERSquery = get_USERSquery()
    usernames = [e['username'] for e in USERSquery]
    
    docs = {}
    for username in usernames:
        username = no_spaces(username).lower()
        docs.update({f"{username}":f"{raw_corpus(USERSquery, username)}"})
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(docs.values())
    m = sparse_matrix.todense()
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                    columns=count_vectorizer.get_feature_names(), 
                    index=docs.keys())

    # HERE WE ARE USING THE EUCLIDEAN DISTANCE, BUT OTHER METHODS OF DISTANCE CAN BE USED
    similarity_matrix = euclidean_distances(df,df)
    #sim_df = pd.DataFrame(similarity_matrix, columns=docs.keys(), index=docs.keys())
    #return sim_dif
    return pd.DataFrame(similarity_matrix, columns=docs.keys(), index=docs.keys())


def most_similar_users(username, similarity_matrix, top=3):
    similar_to_user = similarity_matrix[username]
    return similar_to_user.sort_values(ascending=True).iloc[1:3+1].to_json()