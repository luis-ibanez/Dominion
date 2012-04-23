'''
Created on 09/04/2012

@author: ender3
'''
import random
from card import Card, CardCollection

class Player(object):
    '''
    classdocs
    '''
    def __init__(self,name,board):
        '''
        Constructor
        '''
        self.board=board
        self.name = name
        self.numActions = 1
        self.numBuys = 1
        self.coins = 0
        self.victoryPoints = 0
        self.gardens = 0
        self.deck=[]
        self.discard=[]
        self.hand=[]
        self.limbo=[]
        
    def end_turn(self):
        self.numActions=1
        self.numBuys=1
        self.coins=0
        
    def initialize_deck(self,cards):
        self.deck=cards
        self.victoryPoints=7
        self.reset_deck()
        
    def add_new_card(self,card):
        self.discard.append(card)
        if(self.board.victory_cards.__contains__(card)):
            self.victoryPoints+=self.board.card_collection.get_card(card).points
        elif(card==Card.GARDENS):
            self.gardens+=1
    
    def add_cards_to_discard(self,cards):
        for card in cards:
            self.discard.append(card)
    
    def add_cards_to_deck(self,cards):
        for card in cards:
            self.deck.append(card)
    
    def add_cards_to_hand(self,cards):
        for card in cards:
            self.hand.append(card)
    
    def reset_deck(self):
        self.deck.extend(self.discard)
        random.shuffle(self.deck)
        
    def get_card_from_deck(self):
        if(1>len(self.deck)):
            self.reset_deck()
        card_name=self.deck.pop()
        self.hand.append(card_name)
        list =[]
        if(self.board.money_cards.__contains__(card_name)):
            self.coins+=self.board.card_collection.get_card(card_name).value
        return card_name
            
    def draw_cards(self,num_cards):
        card_names=[]
        for i in range(num_cards):
            card_names.append(self.get_card_from_deck())
        return card_names
        
    
    def discard_hand(self):
        self.discard.extend(self.hand)
        self.hand=[]
        
    def discard_card_from_hand(self, card):
        if (self.hand.__contains__(card)):
            self.hand.remove(card)
            cards=[card]
            self.add_cards_to_discard(cards)
        else:
            False,"You don\'t have that card in your hand" 
        
    def remove_card_from_hand(self,card):
        if (self.hand.__contains__(card)):
            self.hand.remove(card)
        else:
            False,"You don\'t have that card in your hand" 
            
    def discard_deck(self):
        self.discard.extend(self.deck)
        self.reset_deck()
        
    def put_card_on_top_deck(self,card):
        self.deck.append(card)
        
    def put_two_cards_on_limbo(self):
        self.limbo.extend(self.draw_cards(2))
        
    def get_card_from_limbo(self,card):
        if (self.limbo.__contains__(card)):
            self.limbo.remove(card)
            self.discard.extend(self.limbo)
            return card
        else:
            return False, "You don\'t have that card"
        
    def show_hand(self):
        return self.hand
    
    def get_status(self):
        return "Actions: "+str(self.numActions)+"\nBuys: " + str(self.numBuys) + "\nCoins: " + str(self.coins)
            
        
        
            
        
            
        
            
            

            

        