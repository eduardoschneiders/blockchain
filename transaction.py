from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384
import base64, copy
import pdb

class Transaction():
  def __init__(self, sender, receiver, amount):
    self.amount = amount
    self.sender_public_key = sender.public_key.export_key().decode()
    self.receiver_public_key = receiver.public_key.export_key().decode()
    self.signature = sender.sign(str(vars(self)))

  def verify(self):
    digest = SHA384.new()
    data = copy.copy(vars(self))
    del data['signature']
    digest.update(str.encode(str(data)))
    key = RSA.import_key(self.sender_public_key)
    pkcs1_15.new(key).verify(digest, base64.b64decode(self.signature))

  def make_transaction(self, sender_wallet, receiver_wallet):
    sender_wallet.amount -= self.amount
    receiver_wallet.amount += self.amount

    
