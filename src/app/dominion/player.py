'''
Created on 09/04/2012

@author: ender3
'''
import random

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
    
    def addCardsToDeck(self,cards):
        for card in cards.itervalues():
            self.addCardToDeck(card)
    
    def addCardsToDiscard(self,cards):
        for card in cards.itervalues():
            self.addCardToDiscard(card)
    
    def addCardsToHand(self,cards):
        for card in cards.itervalues():
            self.addCardToHand(card)
    
    def resetDeck(self):
        self.deck.extend(self.discard)
        random.shuffle(self.deck)
        
    def getCardFromDeck(self):
        if(1>len(self.deck)):
            self.resetDeck()
        cardName=self.deck.pop()
        self.hand.append(cardName)
        return cardName
            
    def drawCards(self,numCards):
        cards = []
        for i in range(numCards):
            cards.append(self.getCardFromDeck())
        return cards
            
        
            
            

            

        