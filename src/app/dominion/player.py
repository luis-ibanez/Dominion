'''
Created on 09/04/2012

@author: ender3
'''

class Player(object):
    '''
    classdocs
    '''
    def __init__(self,name):
        '''
        Constructor
        '''
        self.name = name
        self.numActions = 0
        self.numBuys = 0
        self.coins = 0
        self.victoryPoints = 0
        self.gardens = 0
        self.deck=[]
        self.discard=[]
        self.hand=[]
        
    def endTurn(self):
        self.numActions=1
        self.numBuys=1
        self.coins=0
        
    def addCardToDeck(self,card):
        self.deck.append(card)
    
    def addCardsToDeck(self,cards):
        for card in cards.itervalues():
            self.addCardToDeck(card)
    
    def addCardToDiscard(self,card):
        self.discard.append(card)
    
    def addCardsToDiscard(self,cards):
        for card in cards.itervalues():
            self.addCardToDiscard(card)
            
    def addCardToHand(self,card):
        self.hand.append(card)
    
    def addCardsToHand(self,cards):
        for card in cards.itervalues():
            self.addCardToHand(card)

        