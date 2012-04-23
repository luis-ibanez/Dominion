'''
Created on 09/04/2012

@author: ender3
'''
from app.dominion.board import Board
from app.dominion.player import Player
from app.dominion.util.circularList import CircularList
from app.dominion.card import Card

class Dominion(object):
    '''
    class that are going to communicate all the data from the application to the WS layer
    '''
    
    MAX_PLAYERS = 4
    STATE_OPEN = 1
    STATE_ACTION = 2
    STATE_BUY = 3
    STATE_FINISH = 4

    def __init__(self):
        '''
        Constructor
        '''
        self.board=Board()
        self.order=''
        self.admin=''
        
        self.players = {}
        self.number_of_players = Dominion.MAX_PLAYERS
        self.next_player = None
        self.state = self.STATE_OPEN
        self.templates = {'game' : 'dominion.html'}
        
    def newPlayer(self,name):
        '''
        Create and add a new plater to the game, check if the game is full
        '''
        if len(self.players)>3:
            return False,"maxPlayers"
        elif name in self.players:
            return False,"nameExists"
        else:
            self.players[name]=Player(name,self.board)
            return True
    
    def playerLeft(self,name):
        '''
        Create and add a new plater to the game, check if the game is full
        '''
        self.players.pop(name)
    
    def initGame(self):
        '''
        Initialize the game, check if there are enough players
        '''
        if len(self.players)<2:
            return False, "minPlayers"
        else:
            self.order=CircularList(self.players.keys())
            self.board.deal_cards(len(self.players))
            for player in self.players.itervalues():
                cards_deck=[]
                (result,card_num)=self.board.get_cards(Card.ESTATE, 3)
                if(result):
                    for i in range(3):
                        cards_deck.append(Card.ESTATE)
                (result,card_num)=self.board.get_cards(Card.COPPER, 7)
                if(result):
                    for i in range(7):
                        cards_deck.append(Card.COPPER)
                player.initialize_deck(cards_deck)
                player.draw_cards(5)
            self.state=self.STATE_ACTION
            return True  
        
    def end_action_phase(self):
        self.state=self.STATE_BUY
    
    def end_buy_phase(self):
        self.players[self.order.current()].discard_hand()
        self.players[self.order.current()].draw_cards(5)  
        self.order.next()
        self.state=self.STATE_ACTION
        
    def buy(self,card_name):
        if(self.board.board_cards.__contains__(card_name)):
            board_deck=self.board.board_cards[card_name]
            if(self.players[self.order.current()].coins >= self.board.card_collection.get_card(card_name).cost):
                if(card_name != Card.CURSE):
                    (result,num_cards_left)=self.board.get_cards(card_name, 1)
                    if(result):
                        self.players[self.order.current()].add_new_card(card_name)
                        self.players[self.order.current()].coins=self.players[self.order.current()].coins-self.board.card_collection.get_card(card_name).cost
                        return True,card_name
                    else:
                        return False,"There's no "+card_name+" left"
                else:
                    return False,"You cannot buy a Curse"
            else:
                return False, "You don't have enough money"
        else:
            return False, "That card is not on the board"
    def endGame(self):
        winner=''
        winner_points = 0
        message=''
        for player in self.players:
            if (player.victory_points>winner_points):
                winner = player.name
            if (player.victory_points==winner_points):
                winner = winner + ' and ' + player.name
            if (message==''):
                message = player.name+': '+player.victory_points
            else:
                message = message +' - ' +player.name+': '+player.victory_points
            