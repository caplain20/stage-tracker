from fastapi import FastAPI

app = FastAPI(title="Stage Tracker API")

@app.get("/health")
def health():
    return {"status": "ok"}