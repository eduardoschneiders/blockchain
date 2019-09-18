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

      block.nonce = randint(0, 10000)
      block.calculate_nonce()
      if block_chain.last_hash() == block.previous_hash:
        block_chain.blocks.append(block) # TODO: verify if block is valid
        for node_uri in nodes_uris:
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

@app.route('/internal/connect', methods=['POST'])
def connect_node():
  current_nodes = copy.copy(nodes_uris)
  current_nodes.append(self_uri)
  



  for node_uri in nodes_uris:
      response = requests.post(node_uri + '/internal/add_node', json={ 'node_uri': request.json['self_uri'] })
  
  nodes_uris.append(request.json['self_uri'])
  
  response = {
    'nodes_uris': current_nodes,
    'block_chain': object_to_json(block_chain)
  }

  return make_response(jsonify(response), 201)

@app.route('/internal/add_node', methods=['POST'])
def add_node():
  global nodes_uris
  nodes_uris.append(request.json['node_uri'])
  
  return make_response(jsonify({}), 201)

@app.route('/internal/mine_block', methods=['POST'])
def mine_block():
  # receive the block
  # receive the sender address
  # add block to the pool
  # verify its not calculated yet
  # calculate nonce
  # verify its not calculated yet again
  # add to blockchain
  # send to nodes new block

  block = json_to_object(request.json['block'])
  block_pool.put(block)

  return make_response(jsonify({}), 201)

@app.route('/internal/receive_block_chain', methods=['POST'])
def receive_block_chain():
  global block_chain
  block_chain = json_to_object(request.json['blockchain'])

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

  return make_response(jsonify(response), 201)

@app.route('/block', methods=['POST'])
def create_block():
  for transaction_data in request.json:
    sender_wallet = Wallet.find_by_username(transaction_data['username'], transaction_data['password'])
    receiver_wallet = Wallet.find_by_public_key(transaction_data['receiver_public_key'])

    transaction = Transaction(sender_wallet, receiver_wallet, transaction_data['amount'])
    builded_block = block_chain.build_block([transaction])
    serialized_builded_block = object_to_json(builded_block)

    for node_uri in nodes_uris:
      response = requests.post(node_uri + '/internal/mine_block', json={ 'block': serialized_builded_block })

    #send to machines

    #simulate other machine receiving the block
    #calculate nonce
    #update current blockchain on this machine
    #send new blockchain
    #update current blockchain on  machine
    # block_chain.blocks.append(builded_block) #TODO REMOVE THIS



  response = { "msg": "Block sended to calculate nonce" }

  return make_response(jsonify(response), 201)

app.run('0.0.0.0', port, debug=False)