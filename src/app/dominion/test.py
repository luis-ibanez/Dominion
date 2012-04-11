'''
Created on 11/04/2012

@author: ender3
'''
from app.dominion.dominion import Dominion
import sys

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main():
    dominion=Dominion()
    dominion.newPlayer("ender")
    dominion.newPlayer("pepe")
    dominion.initGame()
    

if __name__ == "__main__":
    sys.exit(main())