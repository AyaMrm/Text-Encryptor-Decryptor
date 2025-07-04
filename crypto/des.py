from flask import Flask, request, jsonify

#verifier et elle marche 

#les tables importante pour DES 
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

P = [16, 7, 20, 21,
     29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2, 8, 24, 14,
     32, 27, 3, 9,
     19, 13, 30, 6,
     22, 11, 4, 25]

S_BOX = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def permute(block, table):
    return [block[i - 1] for i in table]

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def key_schedule(key):
    key = permute(key, PC1)
    C, D = key[:28], key[28:]
    subkeys = []
    for shift in SHIFT_TABLE:
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        subkey = permute(C + D, PC2)
        subkeys.append(subkey)
    return subkeys

def s_box_substitution(expanded):
    output = []
    for i in range(8):
        block = expanded[i*6:(i+1)*6]
        row = (block[0] << 1) + block[5]
        col = (block[1] << 3) + (block[2] << 2) + (block[3] << 1) + block[4]
        val = S_BOX[i][row][col]
        output.extend([int(b) for b in format(val, '04b')])
    return output

def f_function(R, subkey):
    expanded = permute(R, E)
    xored = [expanded[i] ^ subkey[i] for i in range(48)]
    substituted = s_box_substitution(xored)
    return permute(substituted, P)

def des_round(L, R, subkey):
    L_new = R
    R_new = [L[i] ^ f_function(R, subkey)[i] for i in range(32)]
    return L_new, R_new

def des_encrypt_block(plaintext_block, key):
    plaintext_block = [int(b) for b in format(plaintext_block, '064b')]
    key = [int(b) for b in format(key, '064b')]
    block = permute(plaintext_block, IP)
    L, R = block[:32], block[32:]
    subkeys = key_schedule(key)
    for i in range(16):
        L, R = des_round(L, R, subkeys[i])
    block = R + L
    ciphertext = permute(block, IP_INV)
    return int(''.join(map(str, ciphertext)), 2)

def des_decrypt_block(ciphertext_block, key):
    ciphertext_block = [int(b) for b in format(ciphertext_block, '064b')]
    key = [int(b) for b in format(key, '064b')]
    block = permute(ciphertext_block, IP)
    L, R = block[:32], block[32:]
    subkeys = key_schedule(key)[::-1]
    for i in range(16):
        L, R = des_round(L, R, subkeys[i])
    block = R + L
    plaintext = permute(block, IP_INV)
    return int(''.join(map(str, plaintext)), 2)

def pkcs5_pad(text):
    pad_len = 8 - (len(text) % 8)
    return text + bytes([pad_len] * pad_len)

def pkcs5_unpad(text):
    pad_len = text[-1]
    return text[:-pad_len]

def text_to_blocks(text):
    blocks = []
    for i in range(0, len(text), 8):
        block = text[i:i+8]
        if len(block) < 8:
            block = pkcs5_pad(block)
        block_int = int.from_bytes(block, 'big')
        blocks.append(block_int)
    return blocks

def blocks_to_text(blocks):
    text = b''
    for block in blocks:
        text += block.to_bytes(8, 'big')
    return pkcs5_unpad(text)

def des_encrypt_text(plaintext, key):
    if isinstance(key, str):
        key = key.encode('utf-8')
        if len(key) < 8:
            key = pkcs5_pad(key)
        key = int.from_bytes(key[:8], 'big')

    plaintext_bytes = plaintext.encode('utf-8')
    plaintext_bytes = pkcs5_pad(plaintext_bytes)
    
    blocks = text_to_blocks(plaintext_bytes)
    ciphertext_blocks = [des_encrypt_block(block, key) for block in blocks]
    
    ciphertext = b''
    for block in ciphertext_blocks:
        ciphertext += block.to_bytes(8, 'big')
    
    return ciphertext.hex()

def des_decrypt_text(text, key):

    if isinstance(key, str):
        key = key.encode('utf-8')
        if len(key) < 8:
            key = pkcs5_pad(key)
        key = int.from_bytes(key[:8], 'big')

    text_bytes = bytes.fromhex(text)
    
    blocks = text_to_blocks(text_bytes)
    plaintext_blocks = [des_decrypt_block(block, key) for block in blocks]
    
    plaintext = blocks_to_text(plaintext_blocks)
    return plaintext.decode('utf-8')


def des_route(app):
    @app.route("/des/encrypt", methods= ["POST"])
    def des_encrypt():
        data = request.get_json()
        text = data.get("text")
        key = data.get("key")
        if not text or not key:
            return jsonify({"error":"Text and key are required"}), 400
        encrypted = des_encrypt_text(text, key)
        return jsonify({"Encrypted Message": encrypted})
    @app.route("/des/decrypt", methods= ["POST"])
    def des_decrypt():
        data = request.get_json()
        text = data.get("text")
        key = data.get("key")
        if not text or not key:
            return jsonify({"error":"Text and key are required"}), 400
        encrypted = des_decrypt_text(text, key)
        return jsonify({"Encrypted Message": encrypted})