'''
Created on 09/04/2012

@author: ender3
'''

from app.dominion.card import VictoryCard, ActionCard, MoneyCard


class Board(object):
    '''
    Represents the board of the game, contains all the cards and descriptions 
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.numCopper = 60
        self.numSilver = 40
        self.numGold = 30
        self.numEstate = 24
        self.numDuchy = 12
        self.numProvince = 12
        self.boardCards={}
        self.victoryCards={
                           "Estate" : VictoryCard("Estate",2,1),
                           "Duchy" : VictoryCard("Duchy",5,3),
                           "Province" : VictoryCard("Province",8,6),
                           "Curse" : VictoryCard("Curse",0,-1)
                           }
        self.moneyCards={
                         "Gold" : MoneyCard("Gold",6,3),
                         "Silver" : MoneyCard("Silver",3,2),
                         "Copper" : MoneyCard("Copper",0,1)
                         }
        self.actionCards={
                       "Cellar" : ActionCard("Cellar",2,"""Discard any number of cards. 
                       +1 Card per card discarded ""","action"),
                       "Chapel" : ActionCard("Chapel",2,"""Trash up to 4 cards from your hand.""","action"),
                       "Moat" : ActionCard("Moat",2,"""When another player plays an Attack
                        card, you may reveal this from your
                        hand. If you do, you are unaffected
                        by that Attack.""","reaction"),
                       "Chancellor" : ActionCard("Chancellor",3,"""You may immediately put your
                       deck into your discard pile."""),
                       "Village" : ActionCard("Village",3,"","action"),
                       "Woodcutter" : ActionCard("Woodcutter",3,"","action"),
                       "Workshop" : ActionCard("Workshop",3,"Gain a card costing up to $4.","action"),
                       "Bureaucrat" : ActionCard("Bureaucrat",4,"""Gain a silver card;
                       put it on top of your deck.
                       Each other player reveals a Victory card
                       from his hand and puts it on his deck
                       (or reveals a hand with no Victory cards).""","attack"),
                       "Feast" : ActionCard("Feast",4,"""Trash this card.
                       Gain a card costing up to $5.""", "action"),
                       "Gardens" : ActionCard("Gardens",4,""" Worth 1 Victory
                       for every 10 cards
                       in your deck (rounded down).""","victory"),
                       "Militia" : ActionCard("Militia",4,"""Each other player discards
                       down to 3 cards in his hand.""","attack"),
                       "Moneylender" : ActionCard("Moneylender",4,"""Trash a Copper from your hand.
                       If you do, +$3.""","action"),
                       "Remodel" : ActionCard("Remodel",4,"""Trash a card from your hand.
                       Gain a card costing up to $2 more
                       than the trashed card.""","action"),
                       "Smithy" : ActionCard("Smithy",4,"","action"),
                       "Spy" : ActionCard("Spy",4,"""Each player (including you) reveals
                       the top card of his deck and either
                       discards it or puts it back, your choice.""","attack"),
                       "Thief" : ActionCard("Thief",4,"""Each other player reveals the top
                       2 cards of his deck.
                       If they revealed any Treasure cards,
                       they trash one of them that you choose.
                       You may gain any or all of these
                       trashed cards. They discard the
                       other revealed cards.""","attack"),
                       "Throne Room" : ActionCard("Throne Room",4,"""Choose an Action card in your hand.
                       Play it twice.""","action"),
                       "Council Room" : ActionCard("Council Room",5,"","action"),
                       "Festival" : ActionCard("Festival",5,"","action"),
                       "Laboratory" : ActionCard("Laboratory",5,"","action"),
                       "Library" : ActionCard("Library",5,"""Draw until you have 7 cards in hand.
                       You may set aside any Action cards
                       drawn this way, as you draw them;
                       discard the set aside cards after you
                       finish drawing.""","action"),
                       "Market" : ActionCard("Market",5,"","action"),
                       "Mine": ActionCard("Mine",5,"""Trash a Treasure card from your hand.
                       Gain a Treasure card costing up to
                       $3 more; put it into your hand.""","action"),
                       "Witch" : ActionCard("Witch",5,"""Each other player gains a Curse card.""","attack"),
                       "Adventurer" : ActionCard("Adventurer",6,"""Reveal cards from your deck
                       until you reveal 2 Treasure cards.
                       Put those Treasure cards in your hand
                       and discard the other revealed cards.""","action")}
        
    def dealCards(self,numPlayers,curse):
        '''
        Initialization of the board
        '''
        #Treasury initialization
        self.boardCards["Gold"]=(self.numGold,MoneyCard["Gold"])
        self.boardCards["Silver"]=(self.numSilver,MoneyCard["Silver"])
        self.boardCards["Copper"]=(self.numCopper,MoneyCard["Copper"])
        self.boardCards["Estate"]=(self.numEstate,VictoryCard["Estate"])
        self.boardCards["Duchy"]=(self.numDuchy,VictoryCard["Duchy"])
        self.boardCards["Province"]=(self.numProvince,VictoryCard["Province"])
        #Kingdom carts initialization
        for i in range(10):
            name,card=self.actionCards.popitem()
            self.boardCards[name].append((10,card))
        #curse initialization
        if curse:
            self.boardCards["curse"]=(40-(4-numPlayers*10),VictoryCard["Curse"])
    
    def getCards(self,name,num):
        '''
        Return if is possible to deal a number of cards from one kind
        Decrements the number if it's possible
        '''
        numCard,card=self.boardCards[name]
        if numCard-num<0:
            return False,numCard
        numCard = numCard - num
        self.boardCards[name]=(numCard,card)
        return True,numCard
        
            