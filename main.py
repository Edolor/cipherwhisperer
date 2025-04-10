from dotenv import load_dotenv
from graph import kernel

load_dotenv()

if __name__ == "__main__":
    # Test (valid cipher)
    # print(kernel.invoke(input={"question": "What is the decrypted cipher text for: Lzw xawdv osk wehlq wpuwhl xgj lzw dgfw ljww"}))
    
    # Test (french)
    print(kernel.invoke(input={"question": "What is the decrypted cipher text for: Je t'aime au-delà de toute mesure"})) # Should not work as it is french