'''
Created on 11/04/2012

@author: ender3
'''
from app.dominion.dominion import Dominion
from bottle import route, run
import sys

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

    def main():
        dominion=Dominion()
        dominion.newPlayer("ender")
        dominion.newPlayer("pepe")
        dominion.initGame()
    
    @route('/todo')
    def todo_list():
        return "hola"

run()

if __name__ == "__main__":
    sys.exit(main())