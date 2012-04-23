'''
Created on 09/04/2012

@author: ender3
'''

class Card(object):
    '''
    Object which represents a card in the game
    '''
    ESTATE = 'Estate'
    DUCHY = 'Duchy'
    PROVINCE = 'Province'
    CURSE = 'Curse'
    
    GOLD = 'Gold'
    SILVER = 'Silver'
    COPPER = 'Copper'
    
    CELLAR = 'Cellar'
    CHAPEL = 'Chapel'
    MOAT = 'Moat'
    CHANCELLOR = 'Chancellor'
    VILLAGE = 'Village'
    WOODCUTTER = 'Woodcutter'
    WORKSHOP = 'Workshop'
    BUREAUCRAT = 'Bureaucrat'
    FEAST = 'Feast'
    GARDENS = 'Gardens'
    MILITIA = 'Militia'
    MONEYLENDER = 'Moneylender'
    REMODEL = 'Remodel'
    SMITHY = 'Smithy'
    SPY = 'Spy'
    THIEF = 'Thief'
    THRONE_ROOM = 'Throne Room'
    COUNCIL_ROOM = 'Council Room'
    FESTIVAL = 'Festival'
    LABORATORY = 'Laboratory'
    LIBRARY = 'Library'
    MARKET = 'Market'
    MINE = 'Mine'
    WITCH = 'Witch'
    ADVENTURER = 'Adventurer'
    
    
    
    def __init__(self,name,cost):
        '''
        Constructor
        '''
        self.name = name
        self.cost = cost

class ActionCard(Card):
    '''
    Especialization of card which represents an action card
    '''
    def __init__(self,name,cost,desc,typeCard):
        '''
        Constructor
        '''
        Card.__init__(self,name,cost)
        self.desc=desc
        self.typeCard=typeCard
        
class MoneyCard(Card):
    '''
    Especialization of card which represents a Money Card
    '''
    def __init__(self,name,cost,value):
        '''
        Constructor
        '''
        Card.__init__(self,name,cost)
        self.value=value
     
class VictoryCard(Card):
    '''
    Especialization of card which represents a victory card
    '''
    def __init__(self,name,cost,points):
        '''
        Constructor
        '''
        Card.__init__(self,name,cost)
        self.points=points
        
class CardCollection(object):
    def __init__(self):
        self.cards_dominion={
                            Card.ESTATE : VictoryCard("Estate",2,1),
                            Card.DUCHY : VictoryCard("Duchy",5,3),
                            Card.PROVINCE : VictoryCard("Province",8,6),
                            Card.CURSE : VictoryCard("Curse",0,-1),
                            Card.GOLD : MoneyCard("Gold",6,3),
                            Card.SILVER : MoneyCard("Silver",3,2),
                            Card.COPPER : MoneyCard("Copper",0,1),
                            Card.CELLAR : ActionCard("Cellar",2,"""Discard any number of cards. 
                            +1 Card per card discarded ""","action"),
                            Card.CHAPEL : ActionCard("Chapel",2,"""Trash up to 4 cards from your hand.""","action"),
                            Card.MOAT : ActionCard("Moat",2,"""When another player plays an Attack
                            card, you may reveal this from your
                            hand. If you do, you are unaffected
                            by that Attack.""","reaction"),
                            Card.CHANCELLOR : ActionCard("Chancellor",3,"""You may immediately put your
                            deck into your discard pile.""","action"),
                            Card.VILLAGE : ActionCard("Village",3,"","action"),
                            Card.WOODCUTTER : ActionCard("Woodcutter",3,"","action"),
                            Card.WORKSHOP : ActionCard("Workshop",3,"Gain a card costing up to $4.","action"),
                            Card.BUREAUCRAT : ActionCard("Bureaucrat",4,"""Gain a silver card;
                            put it on top of your deck.
                            Each other player reveals a Victory card
                            from his hand and puts it on his deck
                            (or reveals a hand with no Victory cards).""","attack"),
                            Card.FEAST : ActionCard("Feast",4,"""Trash this card.
                            Gain a card costing up to $5.""", "action"),
                            Card.GARDENS : ActionCard("Gardens",4,""" Worth 1 Victory
                            for every 10 cards
                            in your deck (rounded down).""","victory"),
                            Card.MILITIA : ActionCard("Militia",4,"""Each other player discards
                            down to 3 cards in his hand.""","attack"),
                            Card.MONEYLENDER : ActionCard("Moneylender",4,"""Trash a Copper from your hand.
                            If you do, +$3.""","action"),
                            Card.REMODEL : ActionCard("Remodel",4,"""Trash a card from your hand.
                            Gain a card costing up to $2 more
                            than the trashed card.""","action"),
                            Card.SMITHY : ActionCard("Smithy",4,"","action"),
                            Card.SPY : ActionCard("Spy",4,"""Each player (including you) reveals
                            the top card of his deck and either
                            discards it or puts it back, your choice.""","attack"),
                            Card.THIEF : ActionCard("Thief",4,"""Each other player reveals the top
                            2 cards of his deck.
                            If they revealed any Treasure cards,
                            they trash one of them that you choose.
                            You may gain any or all of these
                            trashed cards. They discard the
                            other revealed cards.""","attack"),
                            Card.THRONE_ROOM : ActionCard("Throne Room",4,"""Choose an Action card in your hand.
                            Play it twice.""","action"),
                            Card.COUNCIL_ROOM : ActionCard("Council Room",5,"","action"),
                            Card.FESTIVAL : ActionCard("Festival",5,"","action"),
                            Card.LABORATORY : ActionCard("Laboratory",5,"","action"),
                            Card.LIBRARY : ActionCard("Library",5,"""Draw until you have 7 cards in hand.
                            You may set aside any Action cards
                            drawn this way, as you draw them;
                            discard the set aside cards after you
                            finish drawing.""","action"),
                            Card.MARKET : ActionCard("Market",5,"","action"),
                            Card.MINE: ActionCard("Mine",5,"""Trash a Treasure card from your hand.
                            Gain a Treasure card costing up to
                            $3 more; put it into your hand.""","action"),
                            Card.WITCH : ActionCard("Witch",5,"""Each other player gains a Curse card.""","attack"),
                            Card.ADVENTURER : ActionCard("Adventurer",6,"""Reveal cards from your deck
                            until you reveal 2 Treasure cards.
                            Put those Treasure cards in your hand
                            and discard the other revealed cards.""","action")}
    
    def get_card(self,name_card):
        return self.cards_dominion[name_card]
    
    
    
    
    
    