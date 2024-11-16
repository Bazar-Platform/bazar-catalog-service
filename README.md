# Bazar Catalog Service

This is a microservice that provides endpoints for querying and updating book information.

## Setup

Before running the service, you’ll need to generate the gRPC code from the `.proto` files to ensure the service can
communicate with other services.

### Generate gRPC Code Locally

To generate the necessary gRPC code for Python, follow these steps:

1. **Clone or Pull the Latest `.proto` Files**
   ```bash
   git clone https://github.com/Bazar-Platform/bazar-protos.git
   ```
   Or if you already have the repository:
   ```bash
   cd bazar-protos
   git pull
   cd ..
   ```

2. **Generate the Python Code**  
   Run the following command to generate the gRPC code for `catalog.proto`:
   ```bash
   cd src
   mkdir -p protos
   python -m grpc_tools.protoc -I../bazar-protos/protos --python_out=protos --grpc_python_out=protos ../bazar-protos/protos/catalog.proto
   ```
   This command will create the following files in the `src/protos` folder:
    - `catalog_pb2.py`: Contains the message classes.
    - `catalog_pb2_grpc.py`: Contains the gRPC client and server classes.

## Development

### Build abd Run the Docker Image

```bash
docker build -t bazar-catalog-service:latest .
docker run -p 5001:5001 bazar-catalog-service:latest
```

### Usage

Once the container is running, you can access the following endpoints:

- **Call `QueryByTopic`** (replace `"distributed systems"` with your topic):
  ```bash
  grpcurl -plaintext -d '{ "topic": "distributed systems" }' localhost:5001 bazar.CatalogService.QueryByTopic
  ```

- **Call `QueryByItem`** (replace `1` with your `book_id`):
  ```bash
  grpcurl -plaintext -d '{ "book_id": 1 }' localhost:5001 bazar.CatalogService.QueryByItem
  ```

- **Call `UpdateItem`** (replace values with appropriate data):
  ```bash
  grpcurl -plaintext -d '{ "book_id": 1, "stock": 5, "price": 19.99 }' localhost:5001 bazar.CatalogService.UpdateItem
  ```

For testing, you can also create a client application that connects to the gRPC server and calls these methods
programmatically.