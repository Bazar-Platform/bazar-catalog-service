# Bazar Catalog Service

This is a Flask-based microservice that provides endpoints for querying and updating book information.

## Build and Run the Docker Compose

```bash
docker-compose up --build
```

### Usage

Once the container is running, you can access the following endpoints:

- **Get all books**: `GET /books`
- **Search books by subject**: `GET /search/<subject>`
- **Get book info by item number**: `GET /info/<item_number>`
- **Update book details**: `PUT /items/<item_number>`

For testing, you can use the provided `catalog-service.http` file to send HTTP requests directly from the IDE.
