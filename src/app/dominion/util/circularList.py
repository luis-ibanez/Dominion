'''
Created on 16/04/2012

@author: ender3
'''

class CircularList(object):
    '''
    classdocs
    '''
    def __init__(self, sequence=[]):
        super(CircularList, self).__init__(sequence)
        self.position = 0

    def current(self):
        return self[self.position]
            
    def next(self, n=1):
        self.position = (self.position + n) % len(self)
        return self[self.position]
