'''
Created on 11/04/2012

@author: ender3
'''
from dominion import Dominion
import sys

def main():
    dominion=Dominion()
    dominion.newPlayer("ender")
    dominion.newPlayer("pepe")
    dominion.initGame()
    

if __name__ == "__main__":
    sys.exit(main())