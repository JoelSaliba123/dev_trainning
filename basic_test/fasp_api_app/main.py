from datetime import datetime
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "success": True,
        "message": "Welcome to backup API"
    }

@app.get("/get_timestamp")
def get_timestamp():
    timestamp = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    return {
        "success": True,
        "message": timestamp
    }

if __name__ == "__main__":
    uvicorn.run(app, port=3000)
