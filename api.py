from flask import Flask, jsonify, make_response, request
from wallet import Wallet
import json

app = Flask(__name__)
app.config["DEBUG"] = True

books = {}

@app.route('/info/wallets', methods=['GET'])
def home():
  return make_response(jsonify([w.to_string() for w in Wallet.wallets]), 200)

@app.route('/wallets', methods=['POST'])
def create_wallet():
  w = Wallet(request.form.get('username'))

  response = { 
    "private_key": w.private_key.exportKey(),
    "public_key": w.public_key.exportKey(),
    "username": w.username,
  }

  return make_response(jsonify(response), 201)

@app.route('/block', methods=['POST'])
def create_block():
  for transaction_data in request.json:
    print((transaction_data))
  return make_response(jsonify({'response': 'asdf'}), 201)

  w = Wallet(request.form.get('username'))

  response = { 
    "private_key": w.private_key.exportKey(),
    "public_key": w.public_key.exportKey(),
    "username": w.username,
  }

  return make_response(jsonify(response), 201)

app.run()