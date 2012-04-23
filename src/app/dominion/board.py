'''
Created on 09/04/2012

@author: ender3
'''
import random
from card import VictoryCard, ActionCard, MoneyCard, Card, CardCollection


class Board(object):
    '''
    Represents the board of the game, contains all the cards and descriptions 
    '''
    NUM_COPPER = 60
    NUM_SILVER = 40
    NUM_GOLD = 30
    NUM_ESTATE = 24
    NUM_DUCHY = 12
    NUM_PROVINCE = 12
    NUM_KINGDOM_CARDS = 10
    NUM_DECK_CARDS = 10

    def __init__(self):
        '''
        Constructor
        '''
        self.card_collection = CardCollection()
        self.kingdom_cards = ''
        self.board_cards={}
        self.number_decks_empty = 0
        self.victory_cards=[
                           Card.ESTATE,
                           Card.DUCHY,
                           Card.PROVINCE,
                           Card.CURSE
                           ]
        self.money_cards=[
                         Card.GOLD,
                         Card.SILVER,
                         Card.COPPER
                         ]
        self.action_cards=[
                           Card.CELLAR,
                           Card.CHAPEL,
                           Card.MOAT,
                           Card.CHANCELLOR,
                           Card.VILLAGE,
                           Card.WOODCUTTER,
                           Card.WORKSHOP,
                           Card.BUREAUCRAT,
                           Card.FEAST,
                           Card.GARDENS,
                           Card.MILITIA,
                           Card.MONEYLENDER,
                           Card.REMODEL,
                           Card.SMITHY,
                           Card.SPY,
                           Card.THIEF,
                           Card.THRONE_ROOM,
                           Card.COUNCIL_ROOM,
                           Card.FESTIVAL,
                           Card.LABORATORY,
                           Card.LIBRARY,
                           Card.MARKET,
                           Card.MINE,
                           Card.WITCH,
                           Card.ADVENTURER
                           ]
        
    def deal_cards(self,num_players):
        '''
        Initialization of the board
        '''
        #Treasury initialization
        self.board_cards[Card.GOLD]=Board.NUM_GOLD
        self.board_cards[Card.SILVER]=Board.NUM_SILVER
        self.board_cards[Card.COPPER]=Board.NUM_COPPER
        self.board_cards[Card.ESTATE]=Board.NUM_ESTATE
        self.board_cards[Card.DUCHY]=Board.NUM_DUCHY
        self.board_cards[Card.PROVINCE]=Board.NUM_PROVINCE
        #Kingdom carts initialization
        curse = False
        for i in range(Board.NUM_KINGDOM_CARDS):
            name = random.choice(self.action_cards)
            
            if (self.kingdom_cards==''):
                self.kingdom_cards=name
            else:
                self.kingdom_cards=self.kingdom_cards + ' - ' +name
            self.board_cards[name]=Board.NUM_DECK_CARDS
            self.action_cards.remove(name)
            if name == Card.WITCH:
                curse=True
        #curse initialization
        if curse:
            self.board_cards[Card.CURSE]=(40-(4-num_players*10))
    
    def get_cards(self,card_name,num_cards):
        '''
        Return if is possible to deal a number of cards from one kind
        Decrements the number if it's possible
        '''
        card_names=[]
        if(num_cards<1):
            return False,self.board_cards[card_name]
        num_cards_left=self.board_cards[card_name]
        if(num_cards_left<num_cards):
            return False,self.board_cards[card_name]
        else:
            self.board_cards[card_name]=num_cards_left-num_cards
            return True,self.board_cards[card_name]
            