from fastapi import FastAPI, HTTPException
app = FastAPI()

SERVICE={"status":{"status": "PENDING"}}

@app.get("/api/loan/{status}")
def get_status(status: str):
    service=SERVICE.get(status)
    if service is None:
        raise HTTPException(status_code=404, detail="Service is Unavailable")