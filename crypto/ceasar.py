from flask import Flask, request, jsonify

app = Flask(__name__)

def ceasar(text, key):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if(char.isupper()):
            result += chr((ord(char)-ord('A')+ key)% 26 + ord('A'))
        elif char.islower():
            result += chr((ord(char)-ord('a')+ key)% 26 + ord('a'))
        else:
            result += char
    return result

def ceasar_route(app):
    @app.route('/ceasar/encrypt', methods=["POST"])
    def encrypt_ceasar():
        data = request.get_json()
        text = data.get('text')
        key = data.get('key')
        if not isinstance(text, str) or not isinstance(key, int):
            return jsonify({"error":"Invalid input!"}), 400
        encrypted = ceasar(text, key)
        return jsonify({"encrypted Message": encrypted})
    
    @app.route('/ceasar/decrypt', methods=["POST"])
    def decrypt_ceasar():
        data = request.get_json()
        text = data.get('text')
        key = data.get('key')
        if not isinstance(text, str) or not isinstance(key, int):
            return jsonify({"error":"Invalid input!"}), 400
        decrypted = ceasar(text, -key)
        return jsonify({"Decrypted Message": decrypted})
