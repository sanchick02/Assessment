// // script.js
// function recommendProducts() {
//     var query = document.getElementById('query').value;
//     fetch('/recommend_products', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ query: query })
//     })
//     .then(response => response.json())
//     .then(data => {
//         const recommendations = document.getElementById('recommendations');
//         recommendations.innerHTML = '';
//         data.recommendations.forEach(function(product, index) {
//             const productInfo = document.createElement('div');
//             productInfo.classList.add('product-info');
//             productInfo.innerHTML = `
//                 <p class="product-name">${product.name}</p>
//                 <p class="product-description">${product.description}</p>
//                 <p class="product-price">$${product.price}</p>
//             `;
//             recommendations.appendChild(productInfo);
//         });
//     });
// }

// script.js

// script.js
// script.js
// script.js
// script.js
// script.js
let productsData = [];

function showSuggestions() {
    const query = document.getElementById('query').value;

    // Check if the query is empty
    if (query.trim() === '') {
        document.getElementById('suggestions').style.display = 'none';
        return;
    }

    fetch('/get_suggestions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        const suggestions = document.getElementById('suggestions');
        suggestions.innerHTML = '';
        if (data.suggestions.length > 0) {
            suggestions.style.display = 'block';
            data.suggestions.forEach(suggestion => {
                const suggestionItem = document.createElement('div');
                suggestionItem.classList.add('suggestion-item');
                suggestionItem.textContent = suggestion;
                suggestionItem.onclick = function() {
                    document.getElementById('query').value = suggestion;
                    suggestions.style.display = 'none';
                };
                suggestions.appendChild(suggestionItem);
            });
        } else {
            suggestions.style.display = 'none';
        }
    });
}

function recommendProducts() {
    const query = document.getElementById('query').value;

    // Check if the query is empty and show an error message
    if (query.trim() === '') {
        alert('Please enter a query before recommending products.');
        return;
    }

    fetch('/recommend_products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        productsData = data.recommendations;
        displayProducts();
    });
}

function displayProducts() {
    const recommendations = document.getElementById('recommendations');
    recommendations.innerHTML = '';
    productsData.forEach(product => {
        const productInfo = document.createElement('div');
        productInfo.classList.add('product-info');
        productInfo.innerHTML = `
            <p class="product-name">${product.name}</p>
            <p class="product-description">${product.description}</p>
            <p class="product-price">$${product.price}</p>
        `;
        recommendations.style.display = 'block'; // Show the recommendation box
        recommendations.appendChild(productInfo);
    });
}
