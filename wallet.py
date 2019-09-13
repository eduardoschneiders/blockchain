import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import base64

class Wallet():
  wallets = []

  def __init__(self, username):
    self.amount = 0
    self.username = username
    self.private_key, self.public_key = self.rsakeys()
    self.wallets.append(self)

  def rsakeys(self):  
    length=1024  
    privatekey = RSA.generate(length, Random.new().read)  
    publickey = privatekey.publickey()  
    return privatekey, publickey

  def sign(self, data):
    return base64.b64encode(str((self.private_key.sign(data,''))[0]).encode())

  def to_string(self):
    return { 
      "amount": self.amount,
      "username": self.username,
      "private_key": self.private_key.exportKey(),
      "public_key": self.public_key.exportKey()
    }

  @classmethod
  def findWallet(cls, publickey):
    for wallet in cls.wallets:
      if wallet.public_key.exportKey() == publickey:
        return wallet