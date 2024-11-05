# Use the official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install git and necessary build dependencies for gRPC and Protobuf
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Clone the .proto files from the shared repository
RUN git clone https://github.com/Bazar-Platform/bazar-protos.git /protos-repository

# Create the src/protos folder for gRPC generated files
RUN mkdir -p src/protos

# Generate Python code from catalog.proto and place it in src/protos
RUN python -m grpc_tools.protoc -I/protos-repository/protos --python_out=src --grpc_python_out=src /protos-repository/protos/catalog.proto

# Copy the application source code into the container, maintaining structure
COPY src/ /app/src/

# Set PYTHONPATH to include src for module resolution
ENV PYTHONPATH=/app/src

# Expose the gRPC server port
EXPOSE 5001

# Run the gRPC server application
CMD ["python", "/app/src/app.py"]
