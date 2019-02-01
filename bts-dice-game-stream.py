from bitshares.blockchain import Blockchain
from bitshares.account import Account
from bitshares.asset import Asset
from bitshares.memo import Memo
import btsDiceGameTransactions

nodeForConnections = 'wss://api.bitsharesdex.com'

blockchain = Blockchain(
  node=nodeForConnections,
  mode='head'
)

btsDGT = btsDiceGameTransactions

memo = Memo()
memo.blockchain.wallet.unlock('superSecretPassword')

for op in blockchain.stream(['transfer']):
  payee = Account(op['to']).name
  if payee == 'bts-dice-game':
    payor = Account(op['from']).name
    decryptedMemo = int(memo.decrypt(op['memo']))
    amount = op['amount']['amount'] / 100000
    btsDGT.play_game(payor, amount, decryptedMemo)
