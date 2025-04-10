from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import END, StateGraph
from chains import decipher_prompt
from typing import TypedDict, Dict, Any
from decryptors import BruteForceDecryptor
from models import Ciphers

DETECT_CIPHER = "detect_cipher"
DECRYPTOR = "decryptor"


class GraphState(TypedDict):
    """The state of the graph."""
    question: str
    cipher: str
    decrypted_cipher: str


def run_decryptor(state: GraphState) -> Dict[str, Any]:
    """Runs the decryptor."""

    print("--RUN DECRYPTOR--")

    cipher = state["cipher"]

    print("--DECRYPTOR: " + cipher + "--")

    if state["cipher"] == Ciphers.caesar:
        _, decrypted_cipher = BruteForceDecryptor.caesar_brute_force(
            state["question"])
    else:
        decrypted_cipher = "Unsupported cipher"

    return {"question": state["question"], "cipher": cipher, "decrypted_cipher": decrypted_cipher}


def get_cipher_type(state: GraphState) -> Dict[str, Any]:
    """Detects what cipher type a given text belongs to and extracts the relevant cipher text."""

    print("--GET CIPHER TYPE--")

    question = state["question"]

    response = decipher_prompt.invoke({"question": question})

    # Getting type of cipher
    cipher = Ciphers.caesar if response.cipher == Ciphers.caesar else "unknown"
    
    if cipher == Ciphers.caesar: # If cipher is know then extract cipher from only cipher text
        question = response.new_question

    return {"question": question, "cipher": cipher, "decrypted_cipher": ""}


def decide_to_decrypt(state):
    """Decides whether to decrypt or not."""

    if state["cipher"] == "unknown":  # If cipher is unknown
        return END

    return DECRYPTOR


graph = StateGraph(GraphState) # Creating graph

graph.add_node(DETECT_CIPHER, get_cipher_type)  # Detecting cipher

graph.add_node(DECRYPTOR, run_decryptor)  # Running decryptor

graph.set_entry_point(DETECT_CIPHER) # Setting entry point

# Determine whether to decrypt or not
graph.add_conditional_edges(DETECT_CIPHER, decide_to_decrypt,
                            path_map={
                                END: END,
                                DECRYPTOR: DECRYPTOR})

graph.add_edge(DECRYPTOR, END) # Adding edge

kernel = graph.compile() # Compiling graph

mermaid_code = kernel.get_graph().draw_mermaid() # Getting mermaid code

with open("graph.mmd", "w") as f: # Writing mermaid code put the text in 'graph.mmd' on this site (https://mermaid.live/)
    f.write(mermaid_code)

kernel.get_graph().print_ascii() # Printing graph in terminal for your viewing pleasure