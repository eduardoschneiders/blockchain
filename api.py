#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from flask import Flask, jsonify, make_response, request
from wallet import Wallet
from blockchain import BlockChain
from transaction import Transaction
from util import *
import json, sys, threading
import requests
import copy
import pickle
import base64
import queue
import time
from random import randint

app = Flask(__name__)
# app.config["DEBUG"] = True

def block_miner(queue):
  global block_chain
  while True:
    while queue.qsize() > 0:
      block = queue.get()
      block.nonce = randint(0, 10000) # TODO: remove this
      block.calculate_nonce()

      if block_chain.last_hash() == block.previous_hash:
        block_chain.blocks.append(block)
        Wallet.update_wallets([block])

        print('====== Found a nounce \\o/')
        for node_uri in nodes_uris:
          print('Sending to ' + node_uri)
          response = requests.post(node_uri + '/internal/receive_block_chain', json={ 'blockchain': object_to_json(block_chain) })
    time.sleep(1)

port = str(sys.argv[1])
self_uri = 'http://0.0.0.0:' + port
nodes_uris = []
block_chain = BlockChain()
block_pool = queue.Queue()
thread_pool_for_blocks = threading.Thread(target=block_miner, args=(block_pool,))
thread_pool_for_blocks.start()

if len(sys.argv) > 2:
  node_uri_to_connect = sys.argv[2]

  response = requests.post(node_uri_to_connect + '/internal/connect', json={ 'self_uri': self_uri })
  nodes_uris = response.json()['nodes_uris']
  block_chain = json_to_object(response.json()['block_chain'])
  Wallet.import_wallets(json_to_object(response.json()['wallets']))

@app.route('/internal/connect', methods=['POST'])
def connect_node():
  current_nodes = copy.copy(nodes_uris)
  current_nodes.append(self_uri)
  
  for node_uri in nodes_uris:
      response = requests.post(node_uri + '/internal/add_node', json={ 'node_uri': request.json['self_uri'] })
  
  nodes_uris.append(request.json['self_uri'])
  
  response = {
    'nodes_uris': current_nodes,
    'block_chain': object_to_json(block_chain),
    'wallets': object_to_json(Wallet.export_wallets())
  }

  return make_response(jsonify(response), 201)

@app.route('/internal/add_node', methods=['POST'])
def add_node():
  global nodes_uris
  nodes_uris.append(request.json['node_uri'])
  
  return make_response(jsonify({}), 201)

@app.route('/internal/mine_block', methods=['POST'])
def mine_block():
  block = json_to_object(request.json['block'])
  block_pool.put(block)

  return make_response(jsonify({}), 201)

@app.route('/internal/receive_block_chain', methods=['POST'])
def receive_block_chain():
  global block_chain
  candidate_block_chain = json_to_object(request.json['blockchain'])
  received_blocks = candidate_block_chain.blocks[len(block_chain.blocks):]

  if block_chain.is_valid(candidate_block_chain):
    Wallet.update_wallets(received_blocks)
    block_chain = candidate_block_chain

    return make_response(jsonify({}), 201)
  else:
    return make_response(jsonify({}), 400)

@app.route('/internal/sync_wallets', methods=['POST'])
def sync_wallets():
  Wallet.import_wallets(json_to_object(request.json['wallets']))

  return make_response(jsonify({}), 201)

@app.route('/info/wallets', methods=['GET'])
def wallets_info():
  return make_response(jsonify([wallet.to_string() for wallet in Wallet.wallets]), 200)

@app.route('/info/nodes', methods=['GET'])
def nodes_info():
  return make_response(jsonify(nodes_uris), 200)

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

  for node_uri in nodes_uris:
    requests.post(node_uri + '/internal/sync_wallets', json={ 'wallets': object_to_json(Wallet.export_wallets()) })

  return make_response(jsonify(response), 201)

@app.route('/block', methods=['POST'])
def create_block(): #TODO validate amount on wallet
  for transaction_data in request.json:
    sender_wallet = Wallet.find_by_username(transaction_data['username'], transaction_data['password'])
    receiver_wallet = Wallet.find_by_public_key(transaction_data['receiver_public_key'])

    transaction = Transaction(sender_wallet, receiver_wallet, transaction_data['amount'])
    builded_block = block_chain.build_block([transaction])
    serialized_builded_block = object_to_json(builded_block)

    for node_uri in nodes_uris:
      response = requests.post(node_uri + '/internal/mine_block', json={ 'block': serialized_builded_block })

  response = { "msg": "Block sended to calculate nonce" }

  return make_response(jsonify(response), 201)

app.run('0.0.0.0', port, debug=False)