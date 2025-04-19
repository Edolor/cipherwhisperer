from dotenv import load_dotenv
from graph import kernel

load_dotenv()

if __name__ == "__main__":
    # Test (valid caesar cipher)
    # print(kernel.invoke(input={"question": "What is the decrypted cipher text for: Vi jgy wjjf nvo ji ocz ypnot nczga"}))

    # Test (valid atbash cipher)
    # print(kernel.invoke(input={"question": "What is the decrypted cipher text for: GSV XZG QFNKVW LEVI GSV UVMXV"}))
    # print(kernel.invoke(input={"question": "What is the decrypted cipher text for: IZRMWILKH VXSLVW LM GSV ILLUGLK"}))

    # Test (valid affine cipher)
    # print(kernel.invoke(input={"question": "What is the decrypted cipher text for: ZRC SLASG UZPESG QWXVWMRZ"}))
    
    # Test (valid Bacon)
    # print(kernel.invoke(input={"question": "What is the decrypted cipher text for: 00001 00000 01101 00000 01101 00000 10010 01100 01110 01110 10011 00111 01000 00100 10110 01000 10011 00111 00100 10111 10011 10001 00000 00111 01110 01101 00100 11000"}))
    
    # Test (valid Transposition)
    print(kernel.invoke(input={"question": "What is the decrypted cipher text for: dray eht ssorca detrad lerriuqs A"}))
    
    # Test (french)
    # print(kernel.invoke(input={"question": "What is the decrypted cipher text for: Je t'aime au-delà de toute mesure"})) # Should not work as it is french