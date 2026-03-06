from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, add_messages
import operator

# def reducer(a: list[str], b: list[str]) -> list[str]:
    # return a + b

class State(TypedDict):
    nodes_path: Annotated[list[str], operator.add]


# Node
def node_a(state: State) -> State:
    nodes_path = state['nodes_path']
    output_state: State = {"nodes_path": [*nodes_path, "node_a"]}
    return output_state

def node_b(state: State) -> State:
    nodes_path = state['nodes_path']
    output_state: State = {"nodes_path": [*nodes_path, "node_b"]}
    return output_state

# Builder Graph
builder = StateGraph(State)
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)

# CONNECT EDGES
builder.add_edge('__start__', 'node_a')
builder.add_edge('node_a', 'node_b')
builder.add_edge('node_b', '__end__')

# compile Graph
graph = builder.compile()

#generate graph image
# graph.get_graph().draw_mermaid_png(output_file_path="ex003_1.png")

# get result
response = graph.invoke({"nodes_path": []})
