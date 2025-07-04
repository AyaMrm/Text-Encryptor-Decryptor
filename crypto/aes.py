from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

#elle marcheee

def get_cipher(key_str, mode_str, iv=None):
    try:
        key = key_str.encode('utf-8')
        if len(key) not in (16, 24, 32):
            raise ValueError("La clé doit être de 16, 24 ou 32 octets après encodage UTF-8.")
        
        mode = mode_str.upper()
        if mode not in ("ECB", "CBC"):
            raise ValueError("Mode de chiffrement non supporté : choisissez 'ECB' ou 'CBC'.")

        if mode == "ECB":
            return AES.new(key, AES.MODE_ECB)
        else:  # mode == "CBC"
            if iv is None:
                iv = get_random_bytes(AES.block_size)
            return AES.new(key, AES.MODE_CBC, iv), iv
    except Exception as e:
        raise ValueError(f"Erreur lors de la création du chiffreur : {str(e)}")

def aes_route(app):
    @app.route("/aes/encrypt", methods=["POST"])
    def encrypt():
        data = request.get_json()
        if not data:
            return jsonify({"error": "Requête JSON invalide"}), 400

        plaintext = data.get("text")
        key = data.get("key")
        mode = data.get("mode", "ECB").upper()
        output_format = data.get("output", "base64").lower()

        if not plaintext or not key:
            return jsonify({"error": "Les champs 'text' et 'key' sont requis"}), 400
        if mode not in ("ECB", "CBC"):
            return jsonify({"error": "Mode doit être 'ECB' ou 'CBC'"}), 400
        if output_format not in ("base64", "text"):
            return jsonify({"error": "Format de sortie doit être 'base64' ou 'text'"}), 400

        try:
            if mode == "CBC":
                cipher, iv = get_cipher(key, mode)
            else:
                cipher = get_cipher(key, mode)
                iv = None

            padded_text = pad(plaintext.encode('utf-8'), AES.block_size)
            encrypted = cipher.encrypt(padded_text)

            if output_format == "text":
                try:
                    ciphertext = encrypted.decode('utf-8')
                except UnicodeDecodeError:
                    return jsonify({"error": "Le résultat chiffré ne peut pas être converti en texte lisible. Utilisez 'base64'."}), 400
            else:
                ciphertext = base64.b64encode(encrypted).decode('utf-8')

            result = {
                "ciphertext": ciphertext,
                "mode": mode,
                "output": output_format
            }
            if iv and mode == "CBC":
                result["iv"] = base64.b64encode(iv).decode('utf-8')

            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": f"Erreur de chiffrement : {str(e)}"}), 400

    @app.route("/aes/decrypt", methods=["POST"])
    @app.route("/aes/decrypt", methods=["POST"])
    def decrypt():
        data = request.get_json()
        if not data:
            return jsonify({"error": "Requête JSON invalide"}), 400

        ciphertext_input = data.get("ciphertext")
        key = data.get("key")
        mode = data.get("mode", "ECB").upper()
        iv_b64 = data.get("iv")
        output_format = data.get("output", "text").lower()

        if not ciphertext_input or not key:
            return jsonify({"error": "Les champs 'ciphertext' et 'key' sont requis"}), 400
        if mode not in ("ECB", "CBC"):
            return jsonify({"error": "Mode doit être 'ECB' ou 'CBC'"}), 400
        if mode == "CBC" and not iv_b64:
            return jsonify({"error": "Le champ 'iv' est requis pour le mode CBC"}), 400
        if output_format not in ("base64", "text"):
            return jsonify({"error": "Format de sortie doit être 'base64' ou 'text'"}), 400

        try:
            if output_format == "base64":
                try:
                    ciphertext = base64.b64decode(ciphertext_input)
                except Exception:
                    return jsonify({"error": "Le ciphertext n'est pas un base64 valide"}), 400
            else:
                ciphertext = ciphertext_input.encode('utf-8')

            iv = None
            if mode == "CBC":
                try:
                    iv = base64.b64decode(iv_b64)
                except Exception:
                    return jsonify({"error": "L'IV n'est pas un base64 valide"}), 400

            result = get_cipher(key, mode, iv) if mode == "CBC" else get_cipher(key, mode)
            cipher = result[0] if mode == "CBC" else result  # Extraire cipher du tuple si CBC

            decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
            plaintext = decrypted.decode('utf-8')

            return jsonify({"plaintext": plaintext}), 200
        except Exception as e:
            return jsonify({"error": f"Erreur de déchiffrement : {str(e)}"}), 400

