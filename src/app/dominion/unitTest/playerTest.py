"""
Created on 23/04/2012

@author: ender3
"""
import unittest
import random
from app.dominion.player import Player
from app.dominion.card import Card
from app.dominion.board import Board


class Test(unittest.TestCase):


    def setUp(self):
        self.player=Player('test',Board())
        self.cards_deck_init = [Card.GOLD,Card.SILVER,Card.COPPER]
        self.cards_hand_init = [Card.GOLD,Card.SILVER,Card.COPPER]
        self.cards_discart_init = [Card.GARDENS]
        
    def test_deck_draw_order(self):
        self.player.add_cards_to_deck(self.cards_deck_init)
        self.player.add_cards_to_discard(self.cards_discart_init)
        self.assertEqual(self.player.get_card_from_deck(),Card.COPPER)
        self.assertEqual(self.player.get_card_from_deck(),Card.SILVER)
        self.assertEqual(self.player.get_card_from_deck(),Card.GOLD)
        self.assertEqual(self.player.get_card_from_deck(),Card.GARDENS)
        
    def test_victory_points_count(self):
        self.player.add_new_card(Card.ESTATE)
        self.assertEqual(self.player.victoryPoints,1)
        self.player.add_new_card(Card.DUCHY)
        self.assertEqual(self.player.victoryPoints,4)
        self.player.add_new_card(Card.PROVINCE)
        self.assertEqual(self.player.victoryPoints,10)
        self.player.add_new_card(Card.CURSE)
        self.assertEqual(self.player.victoryPoints,9)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()