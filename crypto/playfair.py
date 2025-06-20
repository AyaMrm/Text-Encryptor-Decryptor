from flask import Flask, request, jsonify

#cette function pour preparer l key 
def key_preparation(key):
    key = key.upper().replace("J", "I")
    result=[]
    seen = set()
    #pour ajouter les lettre de la key sans repitition 
    for char in key:
        if char.isalpha() and char not in seen :
            result.append(char)
            seen.add(char)
    #ajoute les autre elem de la grid sans repitition
    for char in "QWERTYUIOPASFDGHJKLZXCVBNM":
        if char not in seen:
            result.append(char)
            seen.add(char)
    grid = [result[i*5:(i+1)*5] for i in range(5)]
    return grid
    
def position(grid, char):
    for row in range(5):
        for col in range(5):
            if grid[row][col] == char:
                return row, col
    return None, None     

def text_preparation(text):
    text = text.upper().replace("J", "I")
    clean = [c for c in text if c.isalpha()]
    i=0
    result = []
    while i<len(clean):
        a = clean[i]
        b = clean[i+1] if i+1<len(clean) else "X"
        if a==b:
            result.append((a, "X"))
            i+=1
        else:
            result.append(a)
            result.append(b)
            i+=2
    return result

def playfairENC(text, key):
    grid = key_preparation(key)
    pairs = text_preparation(text)
    encrypted = ""
    for (a,b ) in pairs :
        row1, col1 = position(grid, a)
        row2, col2 = position(grid, b)
        if row1==row2:
            encrypted += grid[row1][(col1+1)%5]
            encrypted += grid[row2][(col2+1)%5]
        elif col1==col2:
            encrypted += grid[(row1+1)%5][col1]
            encrypted += grid[(row2+1)%5][col2]
        else:
            encrypted += grid[row1][col2]
            encrypted += grid[row2][col1]
    return encrypted

def playfairDEC(text, key):
    grid = key_preparation(key)
    pairs = text_preparation(text)
    decrypted = ""
    for (a, b) in pairs :
        row1, col1 = position(grid, a)
        row2, col2 = position(grid, b)
        if row1==row2:
            decrypted += grid[row1][(col1-1)%5]
            decrypted += grid[row2][(col2-1)%5]
        elif col1==col2:
            decrypted += grid[(row1-1)%5][col1]
            decrypted += grid[(row2-1)%5][col2]
        else:
            decrypted += grid[row1][col2]
            decrypted += grid[row2][col1]
    return decrypted

def playfair_route(app):
    @app.route("/playfair/encrypt", methods=["POST"])
    def playfair_encrypt():
        data = request.get_json()
        text = data.get("text")
        key = data.get("key")
        if not isinstance(text, str) or not isinstance(key, str):
            return jsonify({"error":"Invalid Input !"})
        encrypted = playfairENC(text, key)
        return jsonify({"Encrypted Message":encrypted})
    
    @app.route("/playfair/decrypt", methods=['POST'])
    def playfair_decrypt():
        data = request.get_json()
        text = data.get("text")
        key = data.get("key")
        if not isinstance(text, str) or not isinstance(key, str):
            return jsonify({"error":"Invalid Input !"})
        decrypted = playfairDEC(text, key)
        return jsonify({"Decrypted Message": decrypted})