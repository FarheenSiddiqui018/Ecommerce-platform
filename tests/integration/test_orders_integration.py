def test_create_order_integration(client):
    """
    Create a product, then create an order for that product.
    """
    # 1. Create a product
    product_payload = {
        "name": "Test Product",
        "description": "For ordering",
        "price": 20.0,
        "stock": 2
    }
    prod_response = client.post("/products", json=product_payload)
    assert prod_response.status_code == 201
    product = prod_response.json()

    # 2. Create an order with quantity 1
    order_payload = {
        "products": [
            {"product_id": product["id"], "quantity": 1}
        ]
    }
    order_response = client.post("/orders", json=order_payload)
    assert order_response.status_code == 201
    created_order = order_response.json()
    assert created_order["status"] == "completed"
    assert created_order["total_price"] == 20.0

    # 3. Verify the product stock was reduced to 1
    product_list_resp = client.get("/products")
    product_list = product_list_resp.json()
    updated_product = [p for p in product_list if p["id"] == product["id"]][0]
    assert updated_product["stock"] == 1


def test_create_order_insufficient_stock_integration(client):
    """
    Attempt to place an order that exceeds the product's stock.
    """
    # Create product with stock = 1
    product_payload = {
        "name": "Low Stock Product",
        "description": "Barely enough",
        "price": 50.0,
        "stock": 1
    }
    prod_response = client.post("/products", json=product_payload)
    assert prod_response.status_code == 201
    product = prod_response.json()

    # Attempt to buy quantity = 2 (more than in stock)
    order_payload = {
        "products": [
            {"product_id": product["id"], "quantity": 2}
        ]
    }
    order_response = client.post("/orders", json=order_payload)
    assert order_response.status_code == 400
    error = order_response.json()
    assert "Insufficient stock for product" in error["detail"]
