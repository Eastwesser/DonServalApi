# DonServalApi

This is a FastAPI application for managing donuts. It allows you to create, retrieve, and upload images for donuts.

## Installation

Clone the repository:


git clone https://github.com/Eastwesser/DonServalApi.git
cd DonServalApi

## Create a virtual environment and activate it:


python -m venv .venv
source .venv/bin/activate # On Windows use `.venv\Scripts\activate`

## Install the dependencies:

`pip install -r requirements.txt`

## Create a .env file in the root directory and add your database URL:

`DATABASE_URL=postgresql://username:password@localhost:5432/database`

## Run Alembic migrations to set up the database schema:

`alembic upgrade head`

## Running the Application

To run the FastAPI application, use the following command:

`uvicorn main:app --reload`

The application will be available at http://127.0.0.1:8000.

# API Endpoints
## Create a Donut
URL: /donuts/
Method: POST
Request Body:
`{
  "name": "Chocolate",
  "description": "Classic donut covered in exquisite Belgian chocolate."
}`
Response:
`{
  "id": 1,
  "name": "Chocolate",
  "description": "Classic donut covered in exquisite Belgian chocolate."
}`

## Upload an Image for a Donut

URL: /donuts/{donut_id}/upload-image/
Method: POST
Request Body: `file`
Response:
`{
  "info": "Image uploaded successfully"
}`

## Get a Donut by ID

URL: /donuts/{donut_id}
Method: GET
Response:
`{
  "id": 1,
  "name": "Chocolate",
  "description": "Classic donut covered in exquisite Belgian chocolate."
}`

## Get a Donut Image

URL: /donuts/{donut_id}/image
Method: GET
Response: `Image File`

## Docker

Ensure you have Docker and Docker Compose installed.

Build the Docker images:

`docker-compose build`

Run the containers:

`docker-compose up -d`

This will start the bot and the PostgreSQL database in detached mode.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.
