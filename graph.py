from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import END, StateGraph
from chains import decipher_prompt
from typing import TypedDict, Dict, Any, List
from decryptors import BruteForceDecryptor
from models import Ciphers

DETECT_CIPHER = "detect_ciphers"
DECRYPTOR = "decryptor"


class GraphState(TypedDict):
    """The state of the graph."""
    question: str
    decrypted_ciphers: List[str]
    suspected_ciphers: List[str]
    probabilities: List[float]


def run_decryptor(state: GraphState) -> Dict[str, Any]:
    """Runs the decryptor."""

    print("--RUN DECRYPTOR--")

    suspected_ciphers = state["suspected_ciphers"]

    print("--DECRYPTOR: ", suspected_ciphers, "--")

    decrypted_ciphers = []

    for cipher in suspected_ciphers:
        if cipher == Ciphers.caesar:
            _, decrypted_cipher = BruteForceDecryptor.caesar_brute_force(
                state["question"])
        elif cipher == Ciphers.atbash:
            decrypted_cipher = BruteForceDecryptor.atbash_brute_force(
                state["question"])
        elif cipher == Ciphers.affine:
            decrypted_cipher = BruteForceDecryptor.affine_brute_force(
                state["question"])
        elif cipher == Ciphers.bacon:
            decrypted_cipher = BruteForceDecryptor.bacon_decrypt(
                state["question"])
        elif cipher == Ciphers.transposition:
            decrypted_cipher = BruteForceDecryptor.transposition_brute_force(
                state["question"])
        else:
            decrypted_cipher = "Unsupported cipher"

        decrypted_ciphers.append(decrypted_cipher)

    return {"question": state["question"], "suspected_ciphers": suspected_ciphers, "decrypted_ciphers": decrypted_ciphers, "probabilities": state["probabilities"]}


def get_cipher_type(state: GraphState) -> Dict[str, Any]:
    """Detects what cipher type a given text belongs to and extracts the relevant cipher text."""

    print("--GET CIPHER TYPE--")

    question = state["question"]

    response = decipher_prompt.invoke({"question": question})

    # Getting type of cipher
    suspected_ciphers = response.suspected_ciphers
    
    if Ciphers.unknown not in response.suspected_ciphers: # If cipher is not unknown
        question = response.new_question

    return {"question": question, "decrypted_cipher": "", "suspected_ciphers": suspected_ciphers, "probabilities": response.probabilities}


def decide_to_decrypt(state):
    """Decides whether to decrypt or not."""

    if Ciphers.unknown in state["suspected_ciphers"]:  # If cipher is unknown
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