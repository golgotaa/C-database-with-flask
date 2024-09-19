document.addEventListener("DOMContentLoaded", function() {
    fetchCategories();

    document.getElementById("addCategoryForm").addEventListener("submit", function(event) {
        event.preventDefault();
        addCategory();
    });

    document.getElementById("searchCategoryForm").addEventListener("submit", function(event) {
        event.preventDefault();
        searchCategories();
    });
});

function fetchCategories() {
    fetch('/categories')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("categoriesTableBody");
            tableBody.innerHTML = "";

            data.forEach(category => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${category.id}</td>
                    <td>${category.amount}</td>
                    <td>${category.type}</td>
                    <td>${category.description}</td>
                    <td>${new Date(category.date).toLocaleDateString()}</td>
                `;

                tableBody.appendChild(row);
            });
        });
}

function addCategory() {
    const amount = parseFloat(document.getElementById("amount").value);
    const type = document.getElementById("type").value;
    const description = document.getElementById("description").value;
    const date = document.getElementById("date").value;

    const category = {
        amount: amount,
        type: type,
        description: description,
        date: date
    };

    fetch('/categories', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(category)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Category added') {
            document.getElementById("addCategoryForm").reset();
            fetchCategories();
        } else {
            alert("Error adding category: " + data.message);
        }
    });
}

function searchCategories() {
    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;

    fetch(`/categories/search?start_date=${startDate}&end_date=${endDate}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("categoriesTableBody");
            tableBody.innerHTML = "";

            data.forEach(category => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${category.id}</td>
                    <td>${category.amount}</td>
                    <td>${category.type}</td>
                    <td>${category.description}</td>
                    <td>${new Date(category.date).toLocaleDateString()}</td>
                `;

                tableBody.appendChild(row);
            });
        });
}
