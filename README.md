# Bazar Catalog Service

This is a Flask-based microservice that provides endpoints for querying and updating book information.

## Architecture

The Catalog Service uses a **primary-backup** replication architecture:

- The **primary** instance handles all read/write operations and pushes updates to the **backup** instance to maintain
  consistency.
- The **backup** instance remains in sync with the primary but is queried only during failover.

## Environment Variables

The following environment variables can be configured for the Catalog Service:

- **General Settings**:
    - `ROLE`: The role of the service instance (`primary` or `backup`).
    - `PORT`: The port on which the service runs.

- **Backup Settings** (for primary instance only):
    - `PEER_URL`: The URL of the backup service (e.g., `http://bazar-catalog-backup:5001`).

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
