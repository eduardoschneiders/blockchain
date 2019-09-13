from transaction import Transaction
from wallet import Wallet
from blockchain import BlockChain

w1 = Wallet("x")
p_key = w1.public_key.exportKey()
print(p_key)
w = Wallet.findWallet(p_key)
print(vars(w))

w2 = Wallet("asdf")
w3 = Wallet("a")
w4 = Wallet("b")

w1.amount = 100

t1 = Transaction(w1, w2, 5)
t2 = Transaction(w1, w3, 5)
t3 = Transaction(w1, w4, 5)


block_chain = BlockChain()
block_chain.create_block([t1, t2, t3])

t4 = Transaction(w1, w2, 5)
t5 = Transaction(w1, w3, 5)
t6 = Transaction(w1, w4, 5)

block_chain.create_block([t4, t5, t6])




block_chain.print_blocks()
