from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage, ToolMessage
from langchain.tools import BaseTool, tool
from pydantic_core import ValidationError
from rich import print
import os

# Create tool
@tool
def multiply(a: float, b: float) -> float:
    """Multiplies a * b and returns the result.
    
    Args:
        a (float): The first number to multiply.
        b (float): The second number to multiply.
    Returns:
        float: The result of multiplying a and b.
    """

    return a * b    

@tool
def divide(a: float, b: float) -> float:
    """Divides a by b and returns the result.
    
    Args:
        a (float): The dividend.
        b (float): The divisor.
    Returns:
        float: The result of dividing a by b.
    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

llm = init_chat_model(
    "gpt-4.1-mini",  # Nome do deployment
    base_url=f"{os.getenv('AZURE_OPENAI_ENDPOINT', '')}/openai/v1/"
)

system_message = SystemMessage("" \
'You are a helpful assistant. You have access to tools. When the user asks.'
'for something, fisrt look if you have a tool that solves that problem.')

human_message = HumanMessage(content="Ola, sou o John quanto é 25 vezes 10 dividido por 2?")
messages: list[BaseMessage] = [system_message, human_message]

result = llm.invoke(messages)

# tool list
tools: list[BaseTool] = [multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}

llm_with_tools = llm.bind_tools(tools)

llm_response = llm_with_tools.invoke(messages)
messages.append(llm_response)

if isinstance(llm_response, AIMessage) and getattr(llm_response, 'tool_calls', None):
    # Process ALL tool calls, not just the last one
    for call in llm_response.tool_calls:
        name, args, id_ = call['name'], call['args'], call['id']
        try:
            content = tools_by_name[name].invoke(args)
            status = "success"
        except (KeyError, IndexError, TypeError, ValidationError, ValueError) as error:
            content = f'Please, fix your mistakes: {error}'
            status = "error"

        tool_message = ToolMessage(content=str(content), tool_call_id=id_, status=status)
        messages.append(tool_message)

    llm_response = llm_with_tools.invoke(messages)
    messages.append(llm_response)

print(messages)