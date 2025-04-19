from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
from models import Ciphers

system_role_propmts = {  # Reference: https://github.com/RobustNLP/CipherChat/blob/main/prompts_and_demonstrations.py
    "baseline": f"You are all all round expert in these ciphers ({Ciphers.caesar}, {Ciphers.atbash}, {Ciphers.affine}, {Ciphers.bacon}, {Ciphers.transposition}), your job is to detect if a given text is or has a cipher from the list below and conform to some output. The rules for the chipers are as follows:\n",

    f"{Ciphers.atbash}": f'[{Ciphers.atbash}]: The Atbash Cipher is a simple substitution cipher that originated from the Hebrew Alphabet, but can be applied to any alphabet. The essence of this cipher is the reversal of the alphabet.\nIn the Atbash Cipher, the first letter of the alphabet is replaced by the last letter, the second letter with the second-last letter, and so on. For example, using the English alphabet, A would be replaced by Z, B would be replaced by Y, C would be replaced by X, and so forth. \nPlain: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z\nCipher: Z Y X W V U T S R Q P O N M L K J I H G F E D C B A\nThe name "Atbash" comes from the first four characters of the Hebrew Alphabet: Aleph, Beth, Shin, and Tav, where Aleph was mapped to Tav and Beth was mapped to Shin.\nIt\'s important to note that Atbash is a monoalphabetic substitution cipher, meaning that each letter in the alphabet is replaced by exactly one other letter.\n',
    f"{Ciphers.affine}": f'[{Ciphers.affine}]: The Affine Cipher is a type of monoalphabetic substitution cipher, wherein each letter in the alphabet is mapped to its numeric equivalent, encrypted using a simple mathematical function, and then converted back to a letter.\nThe encryption function for a single letter is:\n  E(x) = (a*x + b) mod 26\nHere, "x" is the letter\'s index (0 for A, 1 for B, etc.), "a" and "b" are the keys of the cipher. The key "a" must be chosen such that it is coprime with 26.\nFor example, with a = 5 and b = 8:\n- Plaintext:  ABCDEFGHIJKLMNOPQRSTUVWXYZ\n- Ciphertext: IWTLAXCHMRWBZEQDUNYOCSJVKF\nTo decrypt, the modular inverse of "a" is used:\n  D(x) = a_inv * (x - b) mod 26\nThe Affine Cipher is more secure than Caesar due to its two-key structure, but still vulnerable to frequency analysis.\n',
    f"{Ciphers.caesar}": f'[{Ciphers.caesar}]: The Caesar Cipher, recognized as one of the pioneer cryptographic methods, embodies simplicity. This particular substitution cipher technique involves a systematic displacement of each letter in the plaintext, or the unencrypted text. This displacement could be up or down the alphabet, based on a predetermined number of spaces. \nTaking, for instance, a shift of one position, the letter \'A\' would be substituted by \'B\', \'B\' would morph into \'C\', and so forth. To provide a lucid example, consider a displacement of three positions:\n- Plaintext:  ABCDEFGHIJKLMNOPQRSTUVWXYZ\n- Ciphertext: DEFGHIJKLMNOPQRSTUVWXYZABC\nGiven this, when tasked with encrypting the word "HELLO", the application of the Caesar Cipher with a shift of three positions would yield "KHOOR".\n',
    f"{Ciphers.bacon}": f'[{Ciphers.bacon}]: The Bacon Cipher, also known as the Baconian Cipher, is a method of steganography developed by Francis Bacon. It encodes each letter of the alphabet using a binary pattern of five letters, typically represented with "A" and "B", or "0" and "1".\nFor example:\nA = AAAAA (00000), B = AAAAB (00001), C = AAABA (00010), ..., Z = BBAAB (11011)\nThe encoded binary sequences can be hidden in text using two different typefaces, letter cases, or any binary-distinguishable mechanism.\nExample:\n- Plaintext: HELLO\n- Binary: AABBA ABBAA BAABA BAABA ABBAB\nThe cipher is more about hiding a message in another than about cryptographic complexity. Modern adaptations often use \'0\' and \'1\' in place of \'A\' and \'B\'.\n',
    f"{Ciphers.transposition}": f'[{Ciphers.transposition}]: The Transposition Cipher is a classical encryption technique that works by rearranging the positions of the letters in the plaintext, without altering the actual letters used.\nUnlike substitution ciphers that replace characters, transposition simply changes their order.\nOne of the simplest forms is the reverse cipher:\n- Plaintext: HELLO\n- Ciphertext: OLLEH\nMore complex transpositions involve writing the message into a matrix and permuting rows or columns. For example, with a key of 4:\nPlaintext: WEAREDISCOVEREDFLEEATONCE\nWritten in 4 columns:\nW E A R\nE D I S\nC O V E\nR E D F\nL E E A\nT O N C\nE\nThen reading column-wise based on a key order produces the ciphertext.\n',
}


class GetCipherType(BaseModel):
    """Detects what cipher type a given text belongs to and extracts the relevant cipher text."""

    suspected_ciphers: List[str] = Field(
        description=f"The highly likely cipher types of the text above 70% confidence level. Supported ciphers: '{Ciphers.caesar}', '{Ciphers.atbash}', '{Ciphers.affine}', '{Ciphers.bacon}', '{Ciphers.transposition}'. If the cipher is not known then return only '{Ciphers.unknown}' in the list. Ensure to evaluate all ciphers and include them if they match above 70%",
    )

    probabilities: List[float] = Field(
        description=f"The probabilities of the cipher types above. Must be in the same order as 'suspected_ciphers'.",
    )
    
    new_question: str = Field(
        description="Extracted cipher text from user input. If 'unknown' then empty string. E.g., if you get this question: 'What is the decrypted cipher text for: some-cipher-text' then you should return 'some-cipher-text'",
    )


get_cipher_prompt = ChatPromptTemplate.from_messages([
    ("system", system_role_propmts["baseline"] +
     system_role_propmts[Ciphers.atbash] + 
     system_role_propmts[Ciphers.affine] + 
     system_role_propmts[Ciphers.caesar] + 
     system_role_propmts[Ciphers.bacon] + 
     system_role_propmts[Ciphers.transposition]),
    ("human",
     "{question}"),
])

# Initialize llm
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

structured_llm_decryptor = llm.with_structured_output(GetCipherType) # We get the "cipher" or "unknown" and a "new question"

# To be used in our chain
decipher_prompt = get_cipher_prompt | structured_llm_decryptor