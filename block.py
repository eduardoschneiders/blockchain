import hashlib
import json
import datetime

class Block():
  def __init__(self, prev_hash, transactions, public_key):
    self.difficulty_level = 3
    self.nonce = 0
    self.hash = None
    self.previous_hash = prev_hash
    self.transactions = transactions
    self.public_key = public_key
    self.date_time = datetime.datetime.now()
    self.hash = self.calculate_hash()
    self.signature = self.create_signature()
    

  def calculate_nonce(self):
    while(self.hash[0:self.difficulty_level] != '0' * self.difficulty_level):
      self.nonce += 1
      self.hash = self.calculate_hash()

  def calculate_hash(self):
    return hashlib.sha256(str(vars(self))).hexdigest()

  def create_signature():
