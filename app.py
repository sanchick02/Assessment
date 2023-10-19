from pyexpat import model

from flask import Flask
from flask import request, jsonify

from file import tfidf_vectorizer, df

app = Flask(__name__)


@app.route('/')
def recommend_products():
    try:
        user_query = request.json['query']  # Assuming user query is sent as JSON
        user_query_vector = tfidf_vectorizer.transform([user_query])
        similarity_scores = model.predict(user_query_vector)
        top_n_indices = similarity_scores.argsort()[-3:][::-1]

        recommendations = df.iloc[top_n_indices][['Product Name', 'Description']].to_dict(orient='records')
        # return jsonify({'recommendations': recommendations})
        return "HEllo"
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run()
