from deepagents import create_deep_agent
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.1",
    temperature=0
)

from src.routes.services.tools import average_rating, get_column_names, search_shows, top_shows

_TOOLS = [get_column_names, average_rating, search_shows, top_shows]

_SYSTEM_PROMPT = (
    "You are a helpful TV show recommendation assistant with access to a dataset of top-rated shows. "
    "Use your tools to answer questions accurately. Keep answers short and concise."
)


def _build_agent():
    return create_deep_agent(
        model=llm,
        tools=_TOOLS,
        system_prompt=_SYSTEM_PROMPT,
    )


async def ask_agent(question: str) -> str:
    agent = _build_agent()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content
