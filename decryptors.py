import nltk
from nltk.corpus import words
import string
import math

nltk.download('words') # Download English word list

english_words = set(words.words()) # Set of valid English words


class BruteForceDecryptor:
    
    @staticmethod
    def caesar_brute_force(cipher_text):
        """Brute force decrypts a Caesar cipher using a list of English words."""

        possible_decryptions = []

        for shift in range(26):
            decrypted = ""
            for char in cipher_text:
                if char.isalpha():
                    shift_base = ord('A') if char.isupper() else ord('a')
                    decrypted += chr((ord(char) - shift_base -
                                     shift) % 26 + shift_base)
                else:
                    decrypted += char

            # Count how many words are valid English words
            word_count = sum(1 for word in decrypted.split()
                             if word.lower() in english_words)
            possible_decryptions.append((shift, decrypted, word_count))

        # Sort by number of valid English words (descending)
        possible_decryptions.sort(key=lambda x: x[2], reverse=True)

        # Return the most likely decryption
        best_shift, best_decryption, _ = possible_decryptions[0]
        return best_shift, best_decryption
    
    @staticmethod
    def atbash_brute_force(cipher_text):
        """Decrypts Atbash cipher by applying fixed mapping."""

        alphabet = string.ascii_uppercase
        reversed_alphabet = alphabet[::-1]
        atbash_map = {original: reversed for original, reversed in zip(alphabet, reversed_alphabet)}
        decrypted = ''.join(atbash_map.get(char.upper(), char) for char in cipher_text)
        word_count = sum(1 for word in decrypted.split() if word.lower() in english_words)

        return decrypted, word_count

    @staticmethod
    def _modinv(a, m):
        """Compute modular inverse of a under modulus m."""
        # Extended Euclidean Algorithm
        def egcd(x, y):
            if y == 0:
                return (x, 1, 0)
            g, s, t = egcd(y, x % y)
            return (g, t, s - (x // y) * t)

        g, x, _ = egcd(a, m)
        if g != 1:
            raise ValueError(f"No modular inverse for a={a} under modulus {m}")
        return x % m

    @staticmethod
    def affine_brute_force(cipher_text):
        """Brute force decrypts an Affine cipher over all valid a, b pairs."""

        # valid a values are those coprime with 26
        valid_a = [a for a in range(1,26) if math.gcd(a,26)==1]
        candidates = []
        for a in valid_a:
            a_inv = BruteForceDecryptor._modinv(a,26)
            for b in range(26):
                decrypted = []
                for c in cipher_text:
                    if c.isalpha():
                        base = ord('A') if c.isupper() else ord('a')
                        y = ord(c) - base
                        x = (a_inv * (y - b)) % 26
                        decrypted.append(chr(x + base))
                    else:
                        decrypted.append(c)
                plain = ''.join(decrypted)
                score = sum(1 for w in plain.split() if w.lower() in english_words)
                candidates.append((a, b, plain, score))
        results = sorted(candidates, key=lambda x: x[3], reverse=True)

        return results[0]

    @staticmethod
    def bacon_decrypt(cipher_text):
        """Brute-force decode Bacon's cipher."""
        bacon_map = {format(i, '05b'): chr(65 + i) for i in range(26)}
        chunks = cipher_text.replace(" ", "")
        decrypted = ""

        for i in range(0, len(chunks), 5):
            chunk = chunks[i:i+5]
            decrypted += bacon_map.get(chunk, "?")

        return decrypted
    
    @staticmethod
    def transposition_brute_force(cipher_text):
        """Try reversing and see if valid text appears."""

        reversed_text = cipher_text[::-1]
        return reversed_text

if __name__ == "__main__":
    _, result = BruteForceDecryptor.caesar_brute_force(  # Testing sample result
        "Lzw xawdv osk wehlq wpuwhl xgj lzw dgfw ljww")
    
    # print(BruteForceDecryptor.affine_brute_force("ZRC SLASG UZPESG QWXVWMRZ"))

    print(result)
