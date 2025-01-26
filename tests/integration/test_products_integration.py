def test_list_products_empty(client):
    """
    When no products exist, /products should return an empty list.
    """
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


def test_create_product_integration(client):
    """
    Test the POST /products endpoint with valid data.
    """
    payload = {
        "name": "Laptop",
        "description": "High performance laptop",
        "price": 999.99,
        "stock": 10,
    }
    response = client.post("/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Laptop"
    assert data["stock"] == 10

    # Verify it's retrievable via GET /products
    response2 = client.get("/products")
    assert response2.status_code == 200
    products = response2.json()
    assert len(products) == 1
    assert products[0]["name"] == "Laptop"


def test_create_product_integration_negative_price(client):
    """
    Test that the endpoint returns a 400 error for negative price.
    """
    payload = {
        "name": "Negative Price",
        "description": "Invalid data",
        "price": -10.0,
        "stock": 10,
    }
    response = client.post("/products", json=payload)
    assert response.status_code == 400
    assert "Price cannot be negative" in response.json()["detail"]
