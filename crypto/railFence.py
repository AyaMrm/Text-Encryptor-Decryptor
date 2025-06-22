from flask import Flask, request, jsonify

def railFenceENC(text, key):
    if key == 1:
        return text

    table = [['' for _ in range(len(text))] for _ in range(key)]

    row = 0
    direction = 1  # 1 -> le bas, -1 ->> le haut

    for col in range(len(text)):
        table[row][col] = text[col]

        if row == 0:
            direction = 1
        elif row == key - 1:
            direction = -1

        row += direction

    result = ''
    for r in range(key):
        for c in range(len(text)):
            if table[r][c] != '':
                result += table[r][c]

    return result

def railFenceDEC(text, key):
    if key == 1:
        return text

    table = [['' for _ in range(len(text))] for _ in range(key)]

    row = 0
    direction = 1
    for col in range(len(text)):
        table[row][col] = '*'  
        if row == 0:
            direction = 1
        elif row == key - 1:
            direction = -1
        row += direction

    index = 0
    for r in range(key):
        for c in range(len(text)):
            if table[r][c] == '*' and index < len(text):
                table[r][c] = text[index]
                index += 1

    result = ''
    row = 0
    direction = 1
    for col in range(len(text)):
        result += table[row][col]
        if row == 0:
            direction = 1
        elif row == key - 1:
            direction = -1
        row += direction

    return result


def railFence_route(app):
    @app.route("/railFence/encrypt", methods=['POST'])
    def railFence_encrypt():
        data = request.get_json()
        text = data.get('text')
        key = data.get('key')
        if not isinstance (text, str) or not isinstance(key, int):
            return jsonify({"error": "invalid Input !!"})
        encrypted = railFenceENC(text, key)
        return jsonify({"Encrypted Message": encrypted})
    @app.route("/railFence/decrypt", methods=['POST'])
    def railFence_decrypt():
        data = request.get_json()
        text = data.get('text')
        key = data.get('key')
        if not isinstance (text, str) or not isinstance(key, int):
            return jsonify({"error": "invalid Input !!"})
        decrypted = railFenceDEC(text, key)
        return jsonify({"Decrypted Message": decrypted})
