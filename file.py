import pandas as pd
import nltk
from nltk.tokenize import word_tokenize

import warnings

warnings.filterwarnings('ignore')

df = pd.read_csv('mini-product-recommender-dataset.csv')
df.head()

df.info()

df.isnull().sum()

df['Category'].value_counts()

df['Category'].fillna('Others', inplace=True)

df.isnull().sum()

# drop rows with missing values
df.dropna(inplace=True)

df.isnull().sum()

df.isnull().sum()

# #tokenize product description using nltk
# df['tokenized_desc'] = df['Description'].apply(word_tokenize)
# df.head()

tokenized_descriptions = []

for description in df['Description']:
    tokens = word_tokenize(description)
    tokenized_descriptions.append(tokens)

# Add the tokenized descriptions back to your DataFrame
df['Tokenized_Description'] = tokenized_descriptions
df.head()
# tokenize sentences
tokenized_sentences = []

for sentence in df['Description']:
    tokens = nltk.sent_tokenize(sentence)
    tokenized_sentences.append(tokens)
df['Tokenized_Sentences'] = tokenized_sentences
df.head()

# 2. Model Training:



from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Description'])
tfidf_matrix.shape

from sklearn.metrics.pairwise import cosine_similarity

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
cosine_sim.shape

indices = pd.Series(df.index, index=df['Product Name']).drop_duplicates()
indices[:10]


def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the product that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all products with that product
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the products based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 3 most similar products
    sim_scores = sim_scores[1:4]

    # Get the product indices
    product_indices = [i[0] for i in sim_scores]

    # Return the top 3 most similar products
    return df['Product Name'].iloc[product_indices]


get_recommendations('Smartphone A')