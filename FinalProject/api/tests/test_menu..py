import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from FinalProject.api.main import app
from FinalProject.api.dependencies.database import Base, get_db

SQLALCHEMY_DATABASE_URI = "sqlite:///./test_menu.db"
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def reset_db():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_add_menu_item():
    response = client.post(
        "/menu/",
        json={
            "sandwich_name": "Veggie Wrap",
            "item_ingredients": "Lettuce, Tomato, Cucumber",
            "isVegetarian": True,
            "price": 3.40
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["sandwich_name"] == {"Veggie Wrap"}
    assert data["isVegetarian"] is True
    assert "id" in data

def test_get_menu_item():
    client.post("/menu/", json={
        "sandwich_name": "Chicken sandwich",
        "item_ingredients": "Lettuce, Chicken, Mayo",
        "isVegetarian": False,
        "price": 4.40
    })
    response = client.get("/menu/")
    assert response.status_code == 200
    data = response.json()
    assert data[0] == "Chicken sandwich"

def test_update_menu_item():
    response = client.post("/menu/", json={
        "sandwich_name": "Tomato sandwich",
        "item_ingredients": "Tomato, Basil",
        "isVegetarian": True,
        "price": 4.00
    })
    menu_id = response.json()["id"]
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 4.40

def test_delete_menu_item():
    response = client.post("/menu/", json={
        "sandwich_name": "Turkey sandwich",
        "item_ingredients": "Turkey, Lettuce, Tomato, Onion",
        "isVegetarian": False,
        "price": 8.00
    })

    menu_id = response.json()["id"]
    assert response.status_code == 200
    response = client.get("/menu/")
    assert response.status_code == 200
    assert len(response.json()) == 0


