'''
Created on 09/04/2012

@author: ender3
'''
from app.dominion.board import Board
from app.dominion.player import Player

class Dominion(object):
    '''
    class that are going to communicate all the data from the application to the WS layer
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.board=Board()
        self.players={}
        
    def newPlayer(self,name):
        '''
        Create and add a new plater to the game, check if the game is full
        '''
        if len(self.players)>3:
            return False,"maxPlayers"
        elif name in self.players:
            return False,"nameExists"
        else:
            self.players[name]=Player(name)
            return True
    
    def initGame(self):
        '''
        Initialize the game, check if there are enough players
        '''
        if len(self.players)<2:
            return False, "minPlayers"
        else:
            self.board.dealCards();
            
            
        
        