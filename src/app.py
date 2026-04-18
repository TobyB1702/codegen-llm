from fastapi import FastAPI
import uvicorn

from src.routes import code_gen

app = FastAPI()

app.include_router(code_gen.router)


@app.get("/")
async def root():
    return {"message": "TV Show Assistant API is running"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()