from langchain_ollama import ChatOllama
from mcp_use import MCPAgent, MCPClient
from pydantic import BaseModel, Field

import os
import sys
import traceback

class ResponseTemplate(BaseModel):
    final_answer: str = Field(description="Final answer to the user's question.")

def user_question(question: str) -> str:
    query_message = f"""
    You are a helpful movie recommendation assistant. You provide insights into the data 

    Answer user questions but keep them short and concise.

    user question {question}
    """
    return query_message


async def ask_ollama(question):
    server_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "mcp_server.py"))
    CONFIG = {
        "mcpServers": {
            "MovieAnalysis": {
                "command": sys.executable,        # ensures same Python interpreter is used
                "args": ["-u", server_path],     # -u for unbuffered IO (helps with IPC)
                # optional: set cwd so relative imports/data paths in the server work
                "cwd": os.path.dirname(server_path)
            }
        }
    }

    client = MCPClient.from_dict(CONFIG)

    """Example function to demonstrate usage of ChatOllama."""
    llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0)


    client = MCPClient.from_dict(CONFIG)
    agent= MCPAgent(llm=llm, client=client, max_steps=5, )

    response = await agent.run(user_question(question))

    return response