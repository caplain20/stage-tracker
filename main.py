from fastapi import FastAPI
from app.routers import companies

app = FastAPI(title="Stage Tracker API")
app.include_router(companies.router)

@app.get("/health")
def health():
    return {"status": "ok"}
