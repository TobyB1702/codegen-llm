from fastapi import APIRouter, HTTPException

from src.routes.services.ollama import ask_ollama


router = APIRouter(prefix="/code_gen")


@router.get("/request_code_gen")
async def request_code_gen(query: str):

    return await ask_ollama(query)