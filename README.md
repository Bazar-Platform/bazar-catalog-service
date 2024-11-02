# Bazar Catalog Service

This is a Flask-based microservice that provides endpoints for querying and updating book information.

## Build and Run the Docker Container

### Step 1: Build the Docker Image

Navigate to the directory containing the Dockerfile (e.g., the root of `bazar-catalog-service`) and run the following
command:

```bash
docker build -t bazar-catalog-service:latest .
```

### Step 2: Run the Docker Container

To run the Docker container and expose the service on port 5001, use the following command:

```bash
docker run -p 5001:5001 bazar-catalog-service:latest
```

This command maps port `5001` of the host machine to port `5001` in the container, allowing access to the
`bazar-catalog-service` at `http://localhost:5001`.

### Usage

Once the container is running, you can access the following endpoints:

- **Get all books**: `GET /books`
- **Search books by subject**: `GET /search/<subject>`
- **Get book info by item number**: `GET /info/<item_number>`
- **Update book details**: `PUT /items/<item_number>`

For testing, you can use the provided `catalog-service.http` file to send HTTP requests directly from the IDE.
