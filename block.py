import hashlib
import json
import datetime

class Block():
  def __init__(self, prev_hash, transactions):
    self.difficulty_level = 3
    self.nonce = 0
    self.hash = None
    self.previous_hash = prev_hash
    self.transactions = transactions
    self.date_time = datetime.datetime.now()
    self.hash = self.calculate_hash()
    
    

  def calculate_nonce(self):
    while(self.hash[0:self.difficulty_level] != '0' * self.difficulty_level):
      self.nonce += 1
      self.hash = self.calculate_hash()

  def calculate_hash(self):
    return hashlib.sha256(str(self.to_string()).encode()).hexdigest()

  def to_string(self):
    return {
      "difficulty_level": self.difficulty_level,
      "nonce": self.nonce,
      "hash": self.hash,
      "previous_hash": self.previous_hash,
      "transactions": [vars(transaction) for transaction in self.transactions],
      "date_time": str(self.date_time),
      "hash": self.hash
    }
