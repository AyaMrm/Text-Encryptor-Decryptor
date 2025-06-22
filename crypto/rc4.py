from flask import Flask, request, jsonify

def ksa(key):
    s = list(range(256)) 
    k = [ord(char) for char in key] 
    j = 0
    for i in range(256):
        j = (j + s[i] + k[i % len(k)]) % 256
        s[i], s[j] = s[j], s[i] 
    return s

def prga(s, length):
    i = 0
    j = 0
    result = []
    for _ in range(length):
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i] 
        r = s[(s[i] + s[j]) % 256]
        result.append(r)
    return result

def rc4(text, key):
    s = ksa(key)
    key_stream = prga(s, len(text))
    encrypted = []
    for i in range(len(text)):
        c = text[i]
        cascii = ord(c)
        k = key_stream[i]
        xored = cascii ^ k
        encrypted.append(chr(xored))
    return ''.join(encrypted)

def rc4_route(app):
    @app.route("/rc4/encrypt", methods=['POST'])
    def rc4_encrypt():
        data = request.get_json()
        text = data.get('text')
        key = data.get('key')  
        if not text or not key:
            return jsonify({"error": "Both text and key are required"}), 400
        encrypted = rc4(text, key)
        return jsonify({"Encrypted Message": encrypted})

    @app.route("/rc4/decrypt", methods=['POST'])
    def rc4_decrypt():
        data = request.get_json()
        text = data.get('text')
        key = data.get('key')  
        if not text or not key:
            return jsonify({"error": "Both text and key are required"}), 400
        decrypted = rc4(text, key)  
        return jsonify({"Decrypted Message": decrypted})
