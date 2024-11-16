# Use the official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install git and necessary build dependencies for gRPC and Protobuf
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libprotobuf-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Clone the .proto files from the shared repository
RUN git clone https://github.com/Bazar-Platform/bazar-protos.git /protos-repository

# Create the directory for the generated gRPC files
RUN mkdir -p /app/src/protos

# Generate Python gRPC code from the .proto file and place it in /app/src/protos
RUN python -m grpc_tools.protoc \
    -I /protos-repository/protos \
    --python_out=/app/src/protos \
    --grpc_python_out=/app/src/protos \
    /protos-repository/protos/catalog.proto

# Add __init__.py to make the protos directory a Python package
RUN touch /app/src/protos/__init__.py

# Fix imports in catalog_pb2_grpc.py to use relative imports
RUN sed -i 's/^import catalog_pb2/from . import catalog_pb2/' /app/src/protos/catalog_pb2_grpc.py

# Copy the application source code into the container
COPY src/ /app/src/

# Debug: Show final structure of /app/src
RUN echo "Final /app/src structure:" && ls -R /app/src

# Set PYTHONPATH to include the src directory for module resolution
ENV PYTHONPATH=/app/src

# Expose the gRPC server port
EXPOSE 5001

# Run the gRPC server application
CMD ["python", "/app/src/app.py"]
