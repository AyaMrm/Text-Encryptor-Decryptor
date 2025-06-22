from flask import Flask, request, jsonify
from crypto.ceasar import ceasar_route
from crypto.vigenere import vigenere_route
from crypto.playfair import playfair_route
from crypto.railFence import railFence_route


app = Flask(__name__)
ceasar_route(app)
vigenere_route(app)
playfair_route(app)
railFence_route(app)

@app.route("/")
def home():
    return "Backend Op"


if __name__ == "__main__":
    app.run(debug=True)
