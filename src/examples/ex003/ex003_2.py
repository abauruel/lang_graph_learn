from dataclasses import dataclass
from typing import Literal, TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
import operator

@dataclass
class State():
    nodes_path: Annotated[list[str], operator.add]
    current_number: int = 0


# Node
def node_a(state: State) -> State:
    output_state: State = State(nodes_path=["node_a"], current_number=state.current_number)
    return output_state

def node_b(state: State) -> State:
    output_state: State = State(nodes_path=["node_b"], current_number=state.current_number)
    return output_state

def node_C(state: State) -> State:
    output_state: State = State(nodes_path=["node_c"], current_number=state.current_number)
    return output_state

# conditional function
def the_conditional(state: State) -> Literal["goes_to_node_b", "goes_to_node_c"]:
    if state.current_number >=50:
        return "goes_to_node_c"
    return "goes_to_node_b"

# Builder Graph
builder = StateGraph(State)
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_node("node_b", node_C)


# CONNECT EDGES
builder.add_edge(START, 'node_a')
builder.add_conditional_edges("node_a", the_conditional, {"goes_to_node_b": "node_b", "goes_to_node_c": "node_c"})
builder.add_edge('node_b', END)
builder.add_edge('node_c', END)

# compile Graph
graph = builder.compile()

#generate graph image
# graph.get_graph().draw_mermaid_png(output_file_path="ex003_1.png")

# get result
response = graph.invoke(State(nodes_path=[]))

print(f"{response=}")
