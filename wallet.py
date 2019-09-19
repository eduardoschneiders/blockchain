from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384
import base64
import copy


class Wallet():
  wallets = []

  def __init__(self, username, password):
    self.amount = 0
    self.username = username
    self.password = password
    self.wallets.append(self)
    self.private_key, self.public_key = self.rsa_keys()


  def rsa_keys(self):  
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()
    return private_key, public_key

  def import_key(self, private_key):
    self.private_key = private_key
    self.public_key = private_key.publickey()

  def sign(self, data):
    signer = pkcs1_15.new(RSA.import_key(self.private_key.export_key()))
    digest = SHA384.new()
    digest.update(str.encode(data))
    return base64.b64encode(str(signer.sign(digest)).encode()).decode()

  def to_string(self):
    return { 
      "amount": self.amount,
      "username": self.username,
      "private_key": self.private_key.exportKey().decode(),
      "public_key": self.public_key.exportKey().decode()
    }

  def auth(self, username, password):
    return self.username == username and self.password == password

  @classmethod
  def find_by_username(cls, username, password):
    for wallet in cls.wallets:
      if wallet.auth(username, password):
        return wallet
    raise Exception("Wallet not found for username: " + username)

  @classmethod
  def find_by_public_key(cls, public_key):
    for wallet in cls.wallets:
      if wallet.public_key.exportKey().decode() == public_key:
        return wallet
    raise Exception("Wallet not found for public_key: " + public_key)

  @classmethod
  def build_from_key(cls, private_key):
    key = RSA.import_key(private_key)
    wallet = Wallet()
    wallet.import_key(key)
    return wallet

  @classmethod
  def verify(cls, signature, public_key, data):
    True

  def prepare_to_export(self):
    dump_wallet = copy.copy(self)
    dump_wallet.public_key = None
    dump_wallet.private_key = dump_wallet.private_key.export_key().decode()
    return dump_wallet

  def prepare_to_import(self):
    self.private_key = RSA.importKey(self.private_key)
    self.public_key = self.private_key.publickey()
    return self

  @classmethod
  def export_wallets(cls):
    return [wallet.prepare_to_export() for wallet in Wallet.wallets]

  @classmethod
  def import_wallets(cls, wallets):
    wallets = [wallet.prepare_to_import() for wallet in wallets]
    Wallet.wallets = wallets