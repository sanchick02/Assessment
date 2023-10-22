import webbrowser
from flask import Flask, render_template, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
from model_training import tfidf_matrix
from file import tfidf_vectorizer, df

app = Flask(__name__)


# Route to the home page
@app.route('/')
def home():
    # Go to index.html
    return render_template('index.html')


# Route to handle product recommendations
@app.route('/recommend_products', methods=['POST'])
def recommend_products():
    # Access the user query from the JavaScript code in index.html
    user_query = request.get_json().get('query')
    # Transform the user query
    user_query = tfidf_vectorizer.transform([user_query])
    # Compute the cosine similarity between the user query and all product descriptions
    similarity_scores = cosine_similarity(user_query, tfidf_matrix)
    # Get the indices of the top 3 most similar products
    indices = similarity_scores.argsort()[0][-3:]
    # Get the product names, descriptions, and prices corresponding to the indices
    product_names = df['Product Name'].iloc[indices]
    product_descriptions = df['Description'].iloc[indices]
    product_price = df['Price'].iloc[indices]
    # Convert the product_info DataFrame to a list of dictionaries
    product_info_list = []
    for i in range(len(product_names)):
        product_info = {}
        product_info['name'] = product_names.iloc[i]
        product_info['description'] = product_descriptions.iloc[i]
        product_info['price'] = product_price.iloc[i]
        # arrange the product based on the similarity score, the most similar product will be on top
        product_info_list.insert(0, product_info)
    # Return the product information as JSON
    return jsonify({'recommendations': product_info_list})


@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    user_query = request.get_json().get('query')
    # You can use various methods such as keyword matching or search algorithms.
    # For now, we will return the first 5 product names that contain the user query.
    suggestions = df[df['Product Name'].str.contains(user_query, case=False)]['Product Name'].iloc[:5].tolist()
    return jsonify({'suggestions': suggestions})


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    # open http://127.0.0.1:5000/ in the browser
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)


