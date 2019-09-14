class Transaction():
  def __init__(self, sender, receiver, amount):
    self.amount = amount
    self.signature = sender.sign(str(vars(self)))
    self.sender_public_key = sender.public_key.exportKey().decode()

    self.receiver_public_key = receiver.public_key.exportKey().decode()
    self.data_transaction(sender, receiver, amount)

  def data_transaction(self, sender, receiver, amount):
    sender.amount -= amount
    receiver.amount += amount

    
