'''
Created on 09/04/2012

@author: ender3
'''

class Card(object):
    '''
    Object which represents a card in the game
    '''
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