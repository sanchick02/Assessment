# import libraries
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

warnings.filterwarnings('ignore')

# read the processed data
df = pd.read_csv('processed_data.csv')

# create a tfidf vectorizer object
tfidf = TfidfVectorizer()

# fit the vectorizer object on the tokenized product descriptions
tfidf.fit(df['Tokenized_Description'])

# transform the tokenized product descriptions
tfidf_matrix = tfidf.transform(df['Tokenized_Description'])

# compute the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# save the cosine similarity matrix to a csv file
pd.DataFrame(cosine_sim).to_csv('cosine_sim.csv', index=False, header=False)

# read the cosine similarity matrix
cosine_sim = pd.read_csv('cosine_sim.csv', header=None)

# create a series of product names
product_names = pd.Series(df['Product Name'])


# function to recommend products based on user query
def recommend_products(query):
    # if the query is not in the product names, return an error message
    # tokenize the user query
    query = word_tokenize(query)
    # transform the tokenized query
    query = tfidf.transform(query)
    # compute the cosine similarity between the user query and all product descriptions
    similarity_scores = cosine_similarity(query, tfidf_matrix)
    # get the indices of the top 3 most similar products
    indices = similarity_scores.argsort()[0][-3:]
    # get the product names corresponding to the indices
    product_names = df['Product Name'].iloc[indices]
    print("The most similar products are: ")
    product_names = product_names.to_string(index=False)

    # return the product names
    return product_names


# test the function
print(recommend_products('leather'))
print(recommend_products('Breathable'))
