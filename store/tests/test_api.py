import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from store.models import Category, Product

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    x=User.objects.create_user(username=f"testuser_{User.objects.count()}", password="testpasses")
    return User.objects.create_user(username="testuser", password="testpasses")

@pytest.fixture
def category():
    return Category.objects.create(name="Electronics", description="Electronic items")

@pytest.fixture
def product(category):
    return Product.objects.create(name="Laptop", description="A powerful laptop", price=1000.00, category=category, stock=5)




@pytest.mark.django_db
def test_create_category(client, category):
    response = client.post("/api/categories/", {"name": "Books", "description": "Reading materials"})
    assert response.status_code == 201
    response = client.get("/api/categories/")
    assert response.status_code == 200
    response = client.get(f"/api/categories/{category.id}/")
    assert response.status_code == 200
    response = client.put(f"/api/categories/{category.id}/",   {"name": "Books_1", "description": "Reading materials"})
    assert response.status_code == 200
    response = client.delete(f"/api/categories/{category.id}/")
    assert response.status_code == 204
    
    
    

@pytest.mark.django_db
def test_create_product(client, category, product):
    response = client.post("/api/products/", {"name": "Phone", "description": "Smartphone", "price": 500, "category": category.id, "stock": 10})
    assert response.status_code == 201
    response = client.get("/api/products/")
    assert response.status_code == 200
    response = client.put(f"/api/categories/{product.id}/",   {"name": "Phone_1", "description": "Smartphone", "price": 500, "category": category.id, "stock": 10})
    assert response.status_code == 200
    response = client.delete(f"/api/categories/{product.id}/")
    assert response.status_code == 204
    


@pytest.mark.django_db
def test_create_order(client, user, product):
    # client.force_authenticate(user=user)
    response = client.post("/api/orders/", {"user": user.id, "products": [product.id]})
    assert response.status_code == 201
    assert response.data["total_amount"] == product.price

@pytest.mark.django_db
def test_order_with_insufficient_stock(client, user, product):
    product.stock = 0
    product.save()
    client.force_authenticate(user=user)
    response = client.post("/api/orders/", {"user": user.id, "products": [product.id]})
    # print('response content:', response.content.decode('utf-8'))
    assert response.status_code == 400
    assert "out of stock" in str(response.data)
