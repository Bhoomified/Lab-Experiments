from fastapi import FastAPI, HTTPException

app = FastAPI(title="Library Member Service")

# Stored in a dict (keyed by id) so every lookup is O(1) instead of a list scan
members = {
    1: {"id": 1, "name": "Sneha", "email": "sneha@library.com", "active": True},
    2: {"id": 2, "name": "Rahul", "email": "rahul@library.com", "active": True},
    3: {"id": 3, "name": "Ananya", "email": "ananya@library.com", "active": True},
}


@app.get("/")
async def home():
    return {"service": "Member Service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/members")
async def get_members():
    return list(members.values())


@app.get("/members/{member_id}")
async def get_member(member_id: int):
    member = members.get(member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member
