from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


# Test for creating a new donut
def test_create_donut(client: TestClient, test_db: Session):
    response = client.post(
        "/donuts/",
        json={
            "name": "Test Donut",  # Donut name
            "description": "Test Description",  # Donut description
            "price": 100,  # Donut price
        }
    )
    assert response.status_code == 200  # Check that the request was successful
    data = response.json()  # Parse the response JSON
    assert data["name"] == "Test Donut"  # Verify the name in the response
    assert data["description"] == "Test Description"  # Verify the description in the response
    assert data["price"] == 100  # Verify the price in the response


# Test for retrieving a donut by ID
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
    donut_id = response.json()["id"]  # Get the donut ID from the response

    # Retrieve the donut by its ID
    response = client.get(f"/donuts/{donut_id}")
    assert response.status_code == 200  # Check if the retrieval was successful
    data = response.json()  # Parse the response JSON
    assert data["name"] == "Another Donut"  # Verify the name in the response
    assert data["description"] == "Another Description"  # Verify the description in the response
    assert data["price"] == 200  # Verify the price in the response


# Test for updating an existing donut
def test_update_donut(client: TestClient, test_db: Session):
    # First, create a donut to update
    response = client.post(
        "/donuts/",
        json={
            "name": "Update Donut",  # Original name
            "description": "Update Description",  # Original description
            "price": 300  # Original price
        }
    )
    donut_id = response.json()["id"]  # Get the donut ID from the response

    # Update the donut's details
    response = client.put(
        f"/donuts/{donut_id}",
        json={
            "name": "Updated Donut",  # Updated name
            "description": "Updated Description",  # Updated description
            "price": 400,  # Updated price
        }
    )
    assert response.status_code == 200  # Check that the update was successful
    data = response.json()  # Parse the response JSON
    assert data["name"] == "Updated Donut"  # Verify the updated name
    assert data["description"] == "Updated Description"  # Verify the updated description
    assert data["price"] == 400  # Verify the updated price


# Test for deleting a donut
def test_delete_donut(client: TestClient, test_db: Session):
    # First, create a donut to delete
    response = client.post(
        "/donuts/",
        json={
            "name": "Delete Donut",  # Name of the donut to delete
            "description": "Delete Description",  # Description of the donut
            "price": 500,  # Price of the donut
        }
    )
    donut_id = response.json()["id"]  # Get the donut ID from the response

    # Delete the donut by its ID
    response = client.delete(f"/donuts/{donut_id}")
    print(response.text)  # Print the response text

    assert response.status_code == 200  # Check that the deletion was successful

    response_json = response.json()  # Parse the response JSON
    print(response_json)  # Print the parsed response JSON

    assert response_json == {"message": "Donut deleted successfully"}  # Verify the deletion message
