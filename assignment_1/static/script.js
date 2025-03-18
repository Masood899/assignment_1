const API_URL = "http://127.0.0.1:5000/api/products"; // Flask API Endpoint

// Function to Fetch and Display Products in table.html
function fetchProducts() {
    fetch(API_URL)
        .then(response => response.json())
        .then(products => {
            const productList = document.getElementById("product-list");
            if (!productList) return; // Ensure this runs only in table.html
            
            productList.innerHTML = ""; // Clear previous entries

            products.forEach(product => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.price}</td>
                    <td>
                        <button onclick="editProduct(${product.id}, '${product.name}', ${product.price})">Edit</button>
                        <button onclick="deleteProduct(${product.id})">Delete</button>
                    </td>
                `;
                productList.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching products:", error));
}

// Function to Add Product
document.getElementById("product-form")?.addEventListener("submit", function(event) {
    event.preventDefault();

    const name = document.getElementById("product-name").value;
    const price = document.getElementById("product-price").value;

    fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, price })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        window.location.href = "table.html"; // Redirect to table.html after adding
    })
    .catch(error => console.error("Error adding product:", error));
});

// Function to Delete Product
function deleteProduct(id) {
    fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchProducts(); // Refresh table
    })
    .catch(error => console.error("Error deleting product:", error));
}

// Function to Edit Product
function editProduct(id, currentName, currentPrice) {
    const newName = prompt("Enter new name:", currentName);
    const newPrice = prompt("Enter new price:", currentPrice);

    if (newName && newPrice) {
        fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: newName, price: newPrice })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchProducts(); // Refresh table
        })
        .catch(error => console.error("Error updating product:", error));
    }
}


function applyDiscount() {
    const discount = document.getElementById("discount-percentage").value;

    if (!discount || discount <= 0) {
        alert("Please enter a valid discount percentage.");
        return;
    }

    fetch("http://127.0.0.1:5000/api/products/discount", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ discount: parseFloat(discount) })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchProducts(); // Refresh product list
    })
    .catch(error => console.error("Error applying discount:", error));
}
// Auto-fetch products when on table.html
if (window.location.pathname.includes("table.html")) {
    fetchProducts();
}
