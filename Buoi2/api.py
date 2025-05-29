from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.playfair import PlayfairCipher
from cipher.vigenere import VigenereCipher
from cipher.transposition import TranspositionCipher
from cipher.railfence import RailFenceCipher

app = Flask(__name__)

# CAESAR CIPHER ALGORITHM
caesar_cipher = CaesarCipher()

# PLAYFAIR CIPHER ALGORITHM
playfair_cipher = PlayfairCipher()

# VIGENERE CIPHER ALGORITHM
vigenere_cipher = VigenereCipher()

# TRANSPOSITION CIPHER ALGORITHM
transposition_cipher = TranspositionCipher()

# RAIL FENCE CIPHER ALGORITHM
railfence_cipher = RailFenceCipher()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Cipher API"})

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    plain_text = data["plain_text"]
    try:
        key = int(data["key"])
        if key < 0:
            return jsonify({"error": "Key must be a non-negative integer"}), 400
    except ValueError:
        return jsonify({"error": "Invalid key: Key must be a valid integer"}), 400
    except KeyError:
        return jsonify({"error": "Missing key in request"}), 400

    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({"encrypted_message": encrypted_text})

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    cipher_text = data["cipher_text"]
    try:
        key = int(data["key"])
        if key < 0:
            return jsonify({"error": "Key must be a non-negative integer"}), 400
    except ValueError:
        return jsonify({"error": "Invalid key: Key must be a valid integer"}), 400
    except KeyError:
        return jsonify({"error": "Missing key in request"}), 400

    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({"decrypted_message": decrypted_text})

@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    data = request.json
    key = data['key']
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({'playfair_matrix': playfair_matrix})

@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(plain_text, playfair_matrix)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, playfair_matrix)
    return jsonify({'decrypted_text': decrypted_text})

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    try:
        key = int(key)
        if key <= 0:
            return jsonify({"error": "Key must be a positive integer"}), 400
    except ValueError:
        return jsonify({"error": "Invalid key: Key must be a valid integer"}), 400
    encrypted_text = transposition_cipher.encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    try:
        key = int(key)
        if key <= 0:
            return jsonify({"error": "Key must be a positive integer"}), 400
    except ValueError:
        return jsonify({"error": "Invalid key: Key must be a valid integer"}), 400
    decrypted_text = transposition_cipher.decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    try:
        key = int(key)
        if key <= 1:
            return jsonify({"error": "Key must be an integer greater than 1"}), 400
    except ValueError:
        return jsonify({"error": "Invalid key: Key must be a valid integer"}), 400
    encrypted_text = railfence_cipher.encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    try:
        key = int(key)
        if key <= 1:
            return jsonify({"error": "Key must be an integer greater than 1"}), 400
    except ValueError:
        return jsonify({"error": "Invalid key: Key must be a valid integer"}), 400
    decrypted_text = railfence_cipher.decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)