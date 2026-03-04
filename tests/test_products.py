def test_create_product(client, user_token, mock_scraping):
    mock_scraping.return_value = {"price": 1000.0, "name": "Test Product"}
    
    response = client.post(
        "/products",
        json={"url": "https://amazon.com.br/dp/123", "target_price": 900.0},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200

def test_product_duplicate_url(client, user_token, mock_scraping):
    mock_scraping.return_value = {"price": 1000.0, "name": "Test Product"}
    
    response1 = client.post(
        "/products",
        json={"url": "https://amazon.com.br/dp/123", "target_price": 900.0},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response1.status_code == 200
    
    response2 = client.post(
        "/products",
        json={"url": "https://amazon.com.br/dp/123", "target_price": 800.0},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]

def test_create_product_invalid_url(client, user_token):
    response = client.post(
        "/products",
        json={"url": "invalid_url", "target_price": 900.0},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 400
    assert "Invalid Amazon URL" in response.json()["detail"]

def test_create_product_unauthorized(client):
    response = client.post(
        "/products",
        json={"url": "https://amazon.com.br/dp/123", "target_price": 900.0}
    )
    assert response.status_code == 401

def test_create_product_scraping_error(client, user_token, mock_scraping):
    mock_scraping.side_effect = Exception("Scraping failed")
    
    response = client.post(
        "/products",
        json={"url": "https://amazon.com.br/dp/123", "target_price": 900.0},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 500
    assert "Error scraping product data" in response.json()["detail"]

def test_get_products(client, user_token, products_data):
    
    response = client.get(
        "/products",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert response.json() == products_data

def test_get_products_unauthorized(client):
    response = client.get("/products")
    assert response.status_code == 401

def test_get_product(client, user_token, products_data):
    
    response = client.get(
        f"/products/{products_data[0]['id']}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert response.json() == products_data[0]

def test_get_product_not_found(client, user_token):
    response = client.get(
        "/products/999",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404

def test_get_product_unauthorized(client, products_data):
    response = client.get(f"/products/{products_data[0]['id']}")
    assert response.status_code == 401  

def test_delete_product(client, user_token, products_data):
    
    response = client.delete(
        f"/products/{products_data[0]['id']}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 204

def test_delete_product_not_found(client, user_token):
    response = client.delete(
        "/products/999",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404

def test_delete_product_unauthorized(client, products_data):
    response = client.delete(f"/products/{products_data[0]['id']}")
    assert response.status_code == 401

def test_update_product(client, user_token, products_data):
    
    response = client.put(
        f"/products/{products_data[0]['id']}",
        json={"url": "https://amazon.com.br/dp/123", "target_price": 900.0},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200

def test_update_product_not_found(client, user_token):
    response = client.put(
        "/products/999",
        json={"url": "https://amazon.com.br/dp/123", "target_price": 900.0},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404

def test_update_product_unauthorized(client, products_data):
    response = client.put(
        f"/products/{products_data[0]['id']}",
        json={"url": "https://amazon.com.br/dp/123", "target_price": 900.0}
    )
    assert response.status_code == 401

def test_update_product_invalid_url(client, user_token, products_data):
    response = client.put(
        f"/products/{products_data[0]['id']}",
        json={"url": "invalid_url", "target_price": 900.0},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 400
    assert "Invalid Amazon URL" in response.json()["detail"]