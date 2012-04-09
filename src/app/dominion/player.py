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
        

        