import os

from rich import print as rprint
from langchain.chat_models import init_chat_model

llm = init_chat_model(
  "gpt-4.1-mini",  # Nome do deployment
    base_url=f"{os.getenv('AZURE_OPENAI_ENDPOINT', '')}/openai/v1/"
)

response = llm.invoke("What is the capital of France?")
rprint(response)