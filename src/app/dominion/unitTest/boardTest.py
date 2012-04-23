'''
Created on 22/04/2012

@author: ender3
'''
import unittest
import random
from app.dominion.board import Board
from app.dominion.card import Card



class Test(unittest.TestCase):

    def setUp(self):
        self.board=Board()
        self.num_players=4
        

    def test_board_initialization(self):
        # make sure the shuffled sequence does not lose any elements
        self.assertEqual(len(self.board.action_cards), 25)
        self.assertEqual(len(self.board.money_cards), 3)
        self.assertEqual(len(self.board.victory_cards), 4)
        
    def test_deal_cards(self):
        self.board.deal_cards(self.num_players)
        self.assertEqual(self.board.board_cards[Card.GOLD], self.board.NUM_GOLD)
        self.assertEqual(self.board.board_cards[Card.SILVER], self.board.NUM_SILVER)
        self.assertEqual(self.board.board_cards[Card.COPPER], self.board.NUM_COPPER)
        self.assertEqual(self.board.board_cards[Card.ESTATE], self.board.NUM_ESTATE)
        self.assertEqual(self.board.board_cards[Card.DUCHY], self.board.NUM_DUCHY)
        self.assertEqual(self.board.board_cards[Card.PROVINCE], self.board.NUM_PROVINCE)
        
        self.assertEqual(len(self.board.action_cards), 15)
        
    def test_get_cards(self):
        self.board.deal_cards(self.num_players)
        
        self.assertEqual(self.board.get_cards(Card.GOLD, 0), (False, self.board.NUM_GOLD))
        self.assertEqual(self.board.get_cards(Card.GOLD, -1), (False, self.board.NUM_GOLD))
        
        self.assertEqual(self.board.get_cards(Card.GOLD, 1),(True,self.board.NUM_GOLD-1))
        self.assertEqual(self.board.get_cards(Card.GOLD, 1),(True,self.board.NUM_GOLD-2))
        self.assertEqual(self.board.get_cards(Card.GOLD, 1),(True,self.board.NUM_GOLD-3))
        self.assertEqual(self.board.get_cards(Card.GOLD, 1),(True,self.board.NUM_GOLD-4))
        self.assertEqual(self.board.get_cards(Card.GOLD, 1),(True,self.board.NUM_GOLD-5))
        self.assertEqual(self.board.get_cards(Card.GOLD, 5),(True,self.board.NUM_GOLD-10))
        self.assertEqual(self.board.get_cards(Card.GOLD, 10),(True,self.board.NUM_GOLD-20))
        self.assertEqual(self.board.get_cards(Card.GOLD, 5),(True,self.board.NUM_GOLD-25))
        self.assertEqual(self.board.get_cards(Card.GOLD, 6),(False,self.board.NUM_GOLD-25))
        self.assertEqual(self.board.get_cards(Card.GOLD, 5),(True,self.board.NUM_GOLD-30))
        self.assertEqual(self.board.get_cards(Card.GOLD, 1),(False,self.board.NUM_GOLD-30))

if __name__ == "__main__":
    unittest.main()
