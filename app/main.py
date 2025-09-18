from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/investigate")
async def investigate():
    return {"target": "example.com", "status": "stub"}
