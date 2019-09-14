from flask import Flask, jsonify, make_response, request
from wallet import Wallet
from blockchain import BlockChain
from transaction import Transaction
import json

app = Flask(__name__)
app.config["DEBUG"] = True

block_chain = BlockChain()

@app.route('/info/wallets', methods=['GET'])
def wallets_info():
  return make_response(jsonify([wallet.to_string() for wallet in Wallet.wallets]), 200)

@app.route('/info/blockchain', methods=['GET'])
def blockchain_info():
  return make_response(jsonify([block.to_string() for block in block_chain.blocks]), 200)



@app.route('/wallets', methods=['POST'])
def create_wallet():
  wallet = Wallet(request.json['username'], request.json['password'])

  response = {
    "private_key": wallet.private_key.exportKey().decode(),
    "public_key": wallet.public_key.exportKey().decode(),
  }

  return make_response(jsonify(response), 201)

@app.route('/block', methods=['POST'])
def create_block():
  for transaction_data in request.json:
    sender_wallet = Wallet.find_by_username(transaction_data['username'], transaction_data['password'])
    receiver_wallet = Wallet.find_by_public_key(transaction_data['receiver_public_key'])

    transaction = Transaction(sender_wallet, receiver_wallet, transaction_data['amount'])
    block_chain.create_block([transaction])

  response = {}

  return make_response(jsonify(response), 201)

app.run('0.0.0.0', 8000, debug=True)