import nltk
from nltk.corpus import words

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


if __name__ == "__main__":
    _, result = BruteForceDecryptor.caesar_brute_force(  # Testing sample result
        "Lzw xawdv osk wehlq wpuwhl xgj lzw dgfw ljww")

    print(result)
