import math
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime(minV, maxV):
    prime = random.randint(minV, maxV)
    while not is_prime(prime):
        prime = random.randint(minV, maxV)
    return prime 

def gcd(a, b):
    if a == 0:
        return b, 0, 1
    pgcd, x1, y1 = gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return pgcd, x, y

def mod_inverse(e, phi):
    pgcd, x, _ = gcd(e, phi)
    if pgcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % phi + phi) % phi 

def generate_keypair():
    p = generate_prime(100, 1000)
    q = generate_prime(100, 1000)
    while p == q:
        q = generate_prime(100, 1000)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  
    while math.gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def rsaENC(public_key, plaintext):
    """Encrypt the plaintext using the public key, return as pure numeric string."""
    e, n = public_key
    if not plaintext:
        raise ValueError("Plaintext cannot be empty")
    cipher = [pow(ord(char), e, n) for char in plaintext]
    lengths = [len(str(num)) for num in cipher]
    length_str = ''.join(f"{l:02d}" for l in lengths)
    number_str = ''.join(f"{num:0{l}d}" for num, l in zip(cipher, lengths))
    return length_str + number_str

def rsaDEC(private_key, ciphertext):
    d, n = private_key
    if len(ciphertext) < 2:
        raise ValueError("Invalid ciphertext: too short")
    
    expected_length = len(ciphertext)
    length_bytes = expected_length * 2  
    
    if len(ciphertext) < length_bytes:
        raise ValueError(f"Invalid ciphertext: expected at least {length_bytes} digits for lengths, got {len(ciphertext)}")
    
    lengths = []
    for i in range(0, length_bytes, 2):
        length = int(ciphertext[i:i+2])
        if length == 0:
            raise ValueError("Invalid ciphertext: zero length found")
        lengths.append(length)
    
    number_part = ciphertext[length_bytes:]
    
    expected_digits = sum(lengths)
    if expected_digits != len(number_part):
        raise ValueError(f"Invalid ciphertext: expected {expected_digits} digits, got {len(number_part)}")
    
    cipher_numbers = []
    start = 0
    for length in lengths:
        num_str = number_part[start:start + length]
        if not num_str:
            raise ValueError("Invalid ciphertext: empty number segment")
        try:
            cipher_numbers.append(int(num_str))
        except ValueError as e:
            raise ValueError(f"Invalid number segment: {num_str}") from e
        start += length
    
    try:
        plain = [chr(pow(char, d, n)) for char in cipher_numbers]
    except ValueError as e:
        raise ValueError("Decryption failed: invalid ciphertext or private key") from e
    return ''.join(plain)

def rsa_route(app):
    @app.route("/rsa/encrypt", methods=["POST"])
    def rsa_encrypt():
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        text = data.get("text")
        e = data.get("e")
        n = data.get("n")
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        try:
            if e and n and e != 0 and n != 0:
                public_key = (int(e), int(n))
            else:
                public_key, _ = generate_keypair()
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid e or n values"}), 400
        
        try:
            encrypted = rsaENC(public_key, text)
            e, n = public_key
            return jsonify({"encrypted_message": encrypted, "public_key": {"e": e, "n": n}})
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/rsa/decrypt", methods=["POST"])
    def rsa_decrypt():
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        text = data.get("text")
        d = data.get("d")
        n = data.get("n")
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        try:
            if d and n and d != 0 and n != 0:
                private_key = (int(d), int(n))
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid d or n values"}), 400
        
        try:
            decrypted = rsaDEC(private_key, text)
            d, n = private_key
            return jsonify({"decrypted_message": decrypted, "private_key": {"d": d, "n": n}})
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

