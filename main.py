from fastapi import FastAPI
from app.routers import applications, companies, contacts,interactions, offers

app = FastAPI(title="Stage Tracker API")
app.include_router(companies.router)
app.include_router(offers.router)
app.include_router(contacts.router)
app.include_router(interactions.router)
app.include_router(applications.router)
@app.get("/health")
def health():
    return {"status": "ok"}
