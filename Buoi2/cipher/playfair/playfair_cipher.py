class PlayfairCipher:
    def __init__(self):
        self.matrix = []

    def create_playfair_matrix(self, key):
        # Remove duplicates and convert to uppercase
        key = key.upper().replace("J", "I")  # Playfair often replaces J with I
        seen = set()
        key = ''.join(char for char in key if char not in seen and char.isalpha() and (seen.add(char) or True))

        # Add remaining letters of the alphabet (excluding J)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for char in alphabet:
            if char not in key:
                key += char

        # Create 5x5 matrix
        self.matrix = [key[i:i+5] for i in range(0, 25, 5)]
        return self.matrix

    def find_position(self, char):
        # Find the position of a character in the matrix
        for i in range(5):
            for j in range(5):
                if self.matrix[i][j] == char:
                    return i, j
        return None

    def playfair_encrypt(self, text, matrix):
        self.matrix = matrix
        # Preprocess text: remove non-alpha chars, convert to uppercase, replace J with I
        text = ''.join(char for char in text.upper() if char.isalpha()).replace("J", "I")
        # If text length is odd, add a padding character (X)
        if len(text) % 2 != 0:
            text += "X"

        # Break into digraphs and handle same-letter pairs
        digraphs = []
        i = 0
        while i < len(text):
            if i + 1 < len(text):
                if text[i] == text[i + 1]:
                    digraphs.append(text[i] + "X")
                    i += 1
                else:
                    digraphs.append(text[i] + text[i + 1])
                    i += 2
            else:
                digraphs.append(text[i] + "X")
                i += 1

        # Encrypt each digraph
        encrypted_text = ""
        for digraph in digraphs:
            row1, col1 = self.find_position(digraph[0])
            row2, col2 = self.find_position(digraph[1])

            if row1 == row2:  # Same row
                encrypted_text += self.matrix[row1][(col1 + 1) % 5]
                encrypted_text += self.matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  # Same column
                encrypted_text += self.matrix[(row1 + 1) % 5][col1]
                encrypted_text += self.matrix[(row2 + 1) % 5][col2]
            else:  # Rectangle
                encrypted_text += self.matrix[row1][col2]
                encrypted_text += self.matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, text, matrix):
        self.matrix = matrix
        # Preprocess text: remove non-alpha chars, convert to uppercase
        text = ''.join(char for char in text.upper() if char.isalpha())

        # Break into digraphs, padding with 'X' if odd length
        if len(text) % 2 != 0:
            text += 'X'
        digraphs = [text[i:i+2] for i in range(0, len(text), 2)]

        # Decrypt each digraph
        decrypted_text = ""
        for digraph in digraphs:
            if len(digraph) == 2:  # Ensure valid digraph
                row1, col1 = self.find_position(digraph[0])
                row2, col2 = self.find_position(digraph[1])

                if row1 == row2:  # Same row
                    decrypted_text += self.matrix[row1][(col1 - 1) % 5]
                    decrypted_text += self.matrix[row2][(col2 - 1) % 5]
                elif col1 == col2:  # Same column
                    decrypted_text += self.matrix[(row1 - 1) % 5][col1]
                    decrypted_text += self.matrix[(row2 - 1) % 5][col2]
                else:  # Rectangle
                    decrypted_text += self.matrix[row1][col2]
                    decrypted_text += self.matrix[row2][col1]

        # Remove padding 'X' if added
        if len(text) > len(decrypted_text):
            decrypted_text = decrypted_text.rstrip('X')

        return decrypted_text