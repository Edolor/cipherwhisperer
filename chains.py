from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from models import Ciphers

system_role_propmts = {  # Reference: https://github.com/RobustNLP/CipherChat/blob/main/prompts_and_demonstrations.py
    "baseline": "You are all all round expert in ciphers, more info on your skills will come soon.",

    f"{Ciphers.caesar}": 'You are an expert on The Caesar Cipher, your job is to detect if a given text is or has a caesar cipher and conform to some output. Rules for Caesar Cipher: \nThe Caesar Cipher, recognized as one of the pioneer cryptographic methods, embodies simplicity. This particular substitution cipher technique involves a systematic displacement of each letter in the plaintext, or the unencrypted text. This displacement could be up or down the alphabet, based on a predetermined number of spaces. \nTaking, for instance, a shift of one position, the letter \'A\' would be substituted by \'B\', \'B\' would morph into \'C\', and so forth. To provide a lucid example, consider a displacement of three positions:\n- Plaintext:  ABCDEFGHIJKLMNOPQRSTUVWXYZ\n- Ciphertext: DEFGHIJKLMNOPQRSTUVWXYZABC\nGiven this, when tasked with encrypting the word "HELLO", the application of the Caesar Cipher with a shift of three positions would yield "KHOOR". \nThe cipher\'s nomenclature can be traced back to Julius Caesar, who, according to historical records, used it as a means to communicate effectively with his generals. Despite the relative simplicity enabling the Caesar Cipher to be broken easily, it maintains efficacy under specific conditions, particularly when the parties involved keep the shift count confidential.',
}


class GetCipherType(BaseModel):
    """Detects what cipher type a given text belongs to and extracts the relevant cipher text."""

    cipher: str = Field(
        description=f"The cipher type of the text. Supported ciphers: '{Ciphers.caesar}' or 'unknown'.",
    )

    new_question: str = Field(
        description="Extracted cipher text from user input. If 'unknown' then empty string. E.g., if you get this question: 'What is the decrypted cipher text for: Hwt spcrts vgprtujaan prgdhh iwt uaddg' then you should return 'Hwt spcrts vgprtujaan prgdhh iwt uaddg'",
    )


get_cipher_prompt = ChatPromptTemplate.from_messages([
    ("system", system_role_propmts["baseline"] +
     system_role_propmts[Ciphers.caesar] + " Your goal is to find the cipher text from a given users message if any."),
    ("human",
     "{question}"),
])

# Initialize llm
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

structured_llm_decryptor = llm.with_structured_output(GetCipherType) # We get the "cipher" or "unknown" and a "new question"

# To be used in our chain
decipher_prompt = get_cipher_prompt | structured_llm_decryptor