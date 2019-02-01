from bitshares.blockchain import Blockchain
from bitshares import BitShares
from bitshares.memo import Memo
from random import seed
from random import randint
import btsDiceRatios

def play_game(account, amountBet, userRoll):

  memo = Memo('bts-dice-game', account)

  nodeForConnections = 'wss://api.bitsharesdex.com'

  blockchain = Blockchain(
    node=nodeForConnections,
    mode='head'
  )

  bitshares = BitShares(
    node=nodeForConnections,
    nobroadcast=False,
  )

  blockNum = blockchain.get_current_block_num()

  userGuess = userRoll
  seed(blockNum * (userGuess + 1))
  
  diceRatios = btsDiceRatios
  winRatio = diceRatios.get_ratio(userGuess)

  value = randint(1, 100)
  correctGuess = value < int(userGuess)

  bitshares.wallet.unlock('superSecretPassword')

  if winRatio is None:
    print('You submitted something not correct to this contract.')
  elif correctGuess:
    winningAmount = winRatio * amountBet
    winningString = "Correct! You guessed {0} and rolled {1}. You won {2:.5f} BTS.".format(userRoll, value, winningAmount)
    bitshares.transfer(account, winningAmount, 'BTS', winningString, account='bts-dice-game')
    print(winningString)
  else:
    losingString = "Incorrect. You guessed {0} and rolled {1}.".format(userRoll, value)
    bitshares.transfer(account, 0.00001, 'BTS', losingString, account='bts-dice-game')
    print('You guessed incorrectly. Your guess was {a} and you rolled {b}.'.format(a=userRoll, b=value))
