from flask import Flask, request, jsonify

def vigenereENC(text, key):
    result = []
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha() :
            ofc = ord('A') if char.isupper() else ord('a')
            k = ord(key[key_index % len(key)])- ord('A')
            encrypted = chr((ord(char)-ofc +k)% 26 + ofc)
            result.append(encrypted)
            key_index+=1
        else:
            result.append(char)
    return ''.join(result)
    
def vigenereDEC(text, key):
    result = []
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha() :
            ofc = ord('A') if char.isupper() else ord('a')
            k = ord(key[key_index % len(key)])- ord('A')
            encrypted = chr((ord(char)-ofc -k)% 26 + ofc)
            result.append(encrypted)
            key_index+=1
        else:
            result.append(char)
    return ''.join(result)

def vigenere_route(app):
    @app.route('/vigenere/encrypt', methods=['POST'])
    def vigenere_encrypt():
        data = request.get_json()
        text = data.get('text')
        key = data.get('key')
        if not isinstance(text, str) or not isinstance(key, str):
            return jsonify({"error": "Invalid Input !!"})
        encrypted = vigenereENC(text, key)
        return jsonify({"Encrypted Message": encrypted})
    
    @app.route('/vigenere/decrypt', methods=['POST'])
    def vigenere_decrypt():
        data = request.get_json()
        text = data.get('text')
        key = data.get('key')
        if not isinstance(text, str) or not isinstance(key, str):
            return jsonify({"error":"Invalid Input !!"})
        decrypted = vigenereDEC(text, key)
        return jsonify({"Decrypted Message": decrypted})