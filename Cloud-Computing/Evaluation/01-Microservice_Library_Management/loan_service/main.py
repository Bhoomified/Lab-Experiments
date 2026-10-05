import asyncio
import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Local defaults; Docker Compose overrides these with the service names
BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL", "http://127.0.0.1:8001")
MEMBER_SERVICE_URL = os.getenv("MEMBER_SERVICE_URL", "http://127.0.0.1:8002")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ONE shared HTTP client for the whole app: connections to the other
    # services are kept open and reused instead of opened for every request.
    app.state.client = httpx.AsyncClient(
        timeout=httpx.Timeout(5.0),
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=50),
    )
    yield
    await app.state.client.aclose()


app = FastAPI(title="Library Loan Service", lifespan=lifespan)

loans = {}  # loan_id -> loan


class BorrowRequest(BaseModel):
    book_id: int
    member_id: int


async def call_service(method: str, url: str, service_name: str, not_found: str):
    """Call another microservice and turn its errors into clean HTTP errors."""
    try:
        response = await app.state.client.request(method, url)
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail=f"{service_name} unavailable")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=not_found)
    if response.status_code == 409:
        raise HTTPException(status_code=400, detail="Book is not available")
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"{service_name} returned an error")
    return response.json()


async def get_book_and_member(book_id: int, member_id: int):
    # Book Service and Member Service are called IN PARALLEL, not one after the other
    return await asyncio.gather(
        call_service("GET", f"{BOOK_SERVICE_URL}/books/{book_id}",
                     "Book Service", "Book not found"),
        call_service("GET", f"{MEMBER_SERVICE_URL}/members/{member_id}",
                     "Member Service", "Member not found"),
    )


@app.get("/")
async def home():
    return {"service": "Loan Service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/loans")
async def get_loans():
    return list(loans.values())


# Read-only end-to-end request (Client -> Loan -> Book + Member).
# It changes nothing, so it is the endpoint to use for load testing.
@app.get("/loans/check/{book_id}/{member_id}")
async def check_eligibility(book_id: int, member_id: int):
    book, member = await get_book_and_member(book_id, member_id)
    return {
        "book_title": book["title"],
        "book_available": book["available"],
        "member_name": member["name"],
        "member_active": member["active"],
        "can_borrow": book["available"] and member["active"],
    }


@app.post("/loans/borrow")
async def borrow_book(request: BorrowRequest):
    book, member = await get_book_and_member(request.book_id, request.member_id)

    if not member["active"]:
        raise HTTPException(status_code=400, detail="Member is not active")

    # Atomic reserve in Book Service: fails with "not available" if someone
    # else borrowed the book in the meantime (no double borrowing).
    await call_service("POST", f"{BOOK_SERVICE_URL}/books/{request.book_id}/reserve",
                       "Book Service", "Book not found")

    loan_id = len(loans) + 1
    loan = {
        "loan_id": loan_id,
        "book_id": request.book_id,
        "book_title": book["title"],
        "member_id": request.member_id,
        "member_name": member["name"],
        "status": "borrowed",
    }
    loans[loan_id] = loan
    return {"message": "Book borrowed successfully", "loan": loan}


@app.post("/loans/return/{loan_id}")
async def return_book(loan_id: int):
    loan = loans.get(loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan["status"] == "returned":
        raise HTTPException(status_code=400, detail="Book already returned")

    # Mark first so two simultaneous returns of the same loan can't both run
    loan["status"] = "returned"
    try:
        await call_service("POST", f"{BOOK_SERVICE_URL}/books/{loan['book_id']}/release",
                           "Book Service", "Book not found")
    except HTTPException:
        loan["status"] = "borrowed"  # undo if Book Service failed
        raise

    return {"message": "Book returned successfully", "loan": loan}
