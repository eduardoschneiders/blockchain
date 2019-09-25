from wallet import Wallet
from transaction import Transaction
import pdb;

sender_wallet = Wallet('eduardo', 'password')
receiver_wallet = Wallet('matheus', 'password')

transaction = Transaction(sender_wallet, receiver_wallet, 5)
transaction.verify_signature()
pdb.set_trace()

