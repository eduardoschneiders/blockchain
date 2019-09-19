class Transaction():
  def __init__(self, sender, receiver, amount):
    self.amount = amount
    self.signature = sender.sign(str(vars(self)))
    self.sender_public_key = sender.public_key.exportKey().decode()

    self.receiver_public_key = receiver.public_key.exportKey().decode()

  def make_transaction(self, sender_wallet, receiver_wallet):
    sender_wallet.amount -= self.amount
    receiver_wallet.amount += self.amount

    
