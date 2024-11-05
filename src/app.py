import grpc
from concurrent import futures
import time
from protos import catalog_pb2, catalog_pb2_grpc

# In-memory data store for books
books = [
    {"Book_ID": 1, "name": "How to get a good grade in DOS in 40 minutes a day", "topic": "distributed systems",
     "stock": 10, "price": 29.99},
    {"Book_ID": 2, "name": "RPCs for Noobs", "topic": "distributed systems", "stock": 15, "price": 29.99},
    {"Book_ID": 3, "name": "Xen and the Art of Surviving Undergraduate School", "topic": "undergraduate school",
     "stock": 5, "price": 29.99},
    {"Book_ID": 4, "name": "Cooking for the Impatient Undergrad", "topic": "undergraduate school", "stock": 50,
     "price": 29.99}
]


# Helper function to find a book by its ID
def find_book_by_id(book_id):
    return next((book for book in books if book["Book_ID"] == book_id), None)


# Define the CatalogService class that implements the gRPC service methods
class CatalogService(catalog_pb2_grpc.CatalogServiceServicer):
    def QueryByTopic(self, request, context):
        topic = request.topic
        filtered_books = [catalog_pb2.Book(
            book_id=book["Book_ID"],
            name=book["name"],
            topic=book["topic"],
            stock=book["stock"],
            price=book["price"]
        ) for book in books if book["topic"] == topic]
        return catalog_pb2.BooksResponse(books=filtered_books)

    def QueryByItem(self, request, context):
        book = find_book_by_id(request.book_id)
        if book:
            return catalog_pb2.BookResponse(book=catalog_pb2.Book(
                book_id=book["Book_ID"],
                name=book["name"],
                topic=book["topic"],
                stock=book["stock"],
                price=book["price"]
            ))
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Book not found')
            return catalog_pb2.BookResponse()

    def UpdateItem(self, request, context):
        book = find_book_by_id(request.book_id)
        if not book:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Item not found')
            return catalog_pb2.UpdateResponse()

        # Update book details
        if request.price:
            book['price'] = request.price
        if request.stock:
            book['stock'] = request.stock

        return catalog_pb2.UpdateResponse(message="Item updated successfully")


# Set up the gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    catalog_pb2_grpc.add_CatalogServiceServicer_to_server(CatalogService(), server)
    server.add_insecure_port('[::]:5001')
    print("Catalog Service running on port 5001")
    server.start()
    try:
        while True:
            time.sleep(86400)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
