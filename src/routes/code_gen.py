from fastapi import APIRouter

from src.routes.services.agent import ask_agent

router = APIRouter(prefix="/code_gen")


@router.get("/request_code_gen")
async def request_code_gen(query: str):
    return await ask_agent(query)