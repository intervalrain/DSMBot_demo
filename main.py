from fastapi import FastAPI
from src.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
