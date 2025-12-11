from fastapi import FastAPI

from src.routes import code_gen

app = FastAPI()

app.include_router(code_gen.router)

@app.get("/")
async def root():
    return {"message": "News MCP API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)