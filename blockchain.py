from block import Block
class BlockChain:
  def __init__(self):
    self.blocks = []

  def create_block(self, transactions):
    block = Block(self.last_hash(), transactions)
    block.calculate_nonce()
    self.blocks.append(block)

  def last_hash(self):
    if len(self.blocks) >= 1:
      return self.blocks[-1].hash
    else:
      return None

  def print_blocks(self):
    for block in self.blocks:
      print(vars(block))
      for transaction in block.transactions:
        print(vars(transaction))



block_chain = BlockChain()
# block_chain.create_block(['asasdfas asdf asdf df'])
# block_chain.create_block(['xpto'])
# block_chain.create_block(['Foo Bar'])
# block_chain.print_blocks()
