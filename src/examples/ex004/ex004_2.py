from typing import Annotated, Sequence, TypedDict
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import Messages
from rich import print
from rich.markdown import Markdown
import threading

llm = init_chat_model("google_genai:gemini-2.5-flash")

def reducer(a: Messages,b: Messages):
    return add_messages(a,b)

# 1 - create state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages, reducer]

# 2 - define nodes
def call_llm(state: AgentState) -> AgentState:
    llm_result = llm.invoke(state["messages"])
    return {"messages": [llm_result]}

# 3 - create stateGraph
builder = StateGraph(AgentState, context_schema=None, input_schema=AgentState, output_schema=AgentState)

# 4 - add nodes and edges
builder.add_node("call_llm", call_llm)
builder.add_edge(START, 'call_llm')
builder.add_edge('call_llm', END)

checkpointer = InMemorySaver()
config = RunnableConfig(configurable={"thread_id": threading.get_ident()})
graph = builder.compile(checkpointer=checkpointer)

if __name__ == '__main__':
    while True:
        
        user_input = input("Digite aqui sua mensagem: ")
        print(Markdown("---"))

        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Bye 👋")
            print(Markdown("---"))
            break

        human_message = HumanMessage(user_input)
        result = graph.invoke({"messages": [human_message]}, config=config) 

        print(Markdown(str(result['messages'][-1].content)))
        print(Markdown("---"))
        

