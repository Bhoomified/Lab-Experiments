from fastapi import FastAPI, HTTPException

app = FastAPI(title="Library Book Service")

# Stored in a dict (keyed by id) so every lookup is O(1) instead of a list scan
books = {
    1: {"id": 1, "title": "The Alchemist", "author": "Paulo Coelho", "available": True},
    2: {"id": 2, "title": "1984", "author": "George Orwell", "available": True},
    3: {"id": 3, "title": "Clean Code", "author": "Robert C. Martin", "available": True},
}


def find_book(book_id: int) -> dict:
    book = books.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/")
async def home():
    return {"service": "Book Service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/books")
async def get_books():
    return list(books.values())


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    return find_book(book_id)


# Atomic check-and-set: there is no "await" between the check and the update,
# so two simultaneous borrow requests can never reserve the same book.
@app.post("/books/{book_id}/reserve")
async def reserve_book(book_id: int):
    book = find_book(book_id)
    if not book["available"]:
        raise HTTPException(status_code=409, detail="Book is not available")
    book["available"] = False
    return book


@app.post("/books/{book_id}/release")
async def release_book(book_id: int):
    book = find_book(book_id)
    book["available"] = True
    return book


# Kept from the original version so earlier demos/screenshots still work
@app.put("/books/{book_id}/availability")
async def update_availability(book_id: int, available: bool):
    book = find_book(book_id)
    book["available"] = available
    return book
