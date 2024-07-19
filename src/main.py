from fastapi import FastAPI

app = FastAPI(title="DSM Bot")

@app.get("/")

async def root():
    return {"message": "Welcome to DSM Bot"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
