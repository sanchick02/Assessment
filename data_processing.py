import pandas as pd
from nltk.tokenize import word_tokenize

import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv('datasets/processed_data.csv')
df.head()

# tokenize the product descriptions so that the model can understand the text based on user query
df['Tokenized_Description'] = df['Description'].apply(word_tokenize)
# convert all words to lowercase
df['Tokenized_Description'] = df['Tokenized_Description'].apply(lambda x: [word.lower() for word in x])
# remove , from the tokenized descriptions
df['Tokenized_Description'] = df['Tokenized_Description'].apply(lambda x: [word for word in x if word != ','])

# save the processed data to a csv file and first row is header
df.to_csv('datasets/processed_data.csv', index=False, header=True)

# read the processed data
df_new = pd.read_csv('datasets/processed_data.csv')
print(df_new.head())