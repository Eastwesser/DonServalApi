from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_donut(client: TestClient, test_db: Session):
    response = client.post(
        "/donuts/",
        json={
            "name": "Test Donut",
            "description": "Test Description",
            "price": 100,
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Donut"
    assert data["description"] == "Test Description"
    assert data["price"] == 100


def test_get_donut(client: TestClient, test_db: Session):
    # First, create a donut to retrieve
    response = client.post(
        "/donuts/",
        json={
            "name": "Another Donut",
            "description": "Another Description",
            "price": 200,
        }
    )
    donut_id = response.json()["id"]

    # Retrieve the donut
    response = client.get(f"/donuts/{donut_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Another Donut"
    assert data["description"] == "Another Description"
    assert data["price"] == 200


def test_update_donut(client: TestClient, test_db: Session):
    # First, create a donut to update
    response = client.post(
        "/donuts/",
        json={
            "name": "Update Donut",
            "description": "Update Description",
            "price": 300
        }
    )
    donut_id = response.json()["id"]

    # Update the donut
    response = client.put(
        f"/donuts/{donut_id}",
        json={
            "name": "Updated Donut",
            "description": "Updated Description",
            "price": 400,
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Donut"
    assert data["description"] == "Updated Description"
    assert data["price"] == 400


def test_delete_donut(client: TestClient, test_db: Session):
    response = client.post(
        "/donuts/",
        json={
            "name": "Delete Donut",
            "description": "Delete Description",
            "price": 500,
        }
    )
    donut_id = response.json()["id"]

    response = client.delete(f"/donuts/{donut_id}")
    print(response.text)

    assert response.status_code == 200

    response_json = response.json()
    print(response_json)

    assert response_json == {"message": "Donut deleted successfully"}
