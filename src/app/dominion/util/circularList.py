'''
Created on 16/04/2012

@author: ender3
'''

class CircularList(object):
    '''
    classdocs
    '''
    def __init__(self, sequence=[]):
        self.list=sequence
        self.index=0

    def current(self):
        return self.list[self.index]
            
    def next(self, n=1):
        self.index = (self.index + n) % len(self.list)
        return self.list[self.index]
