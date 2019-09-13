class Transaction():
  def __init__(self, sender, receiver, amount):
    self.sender = sender
    self.receiver = receiver
    self.amount = amount
    self.signature = sender.sign(str(vars(self)))
    self.public_key = sender.public_key
    self.sender.amount -= amount
    self.receiver.amount += amount

    
