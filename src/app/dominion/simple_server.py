'''
Created on 22/04/2012

@author: ender3
'''
import os
import time
import logging
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
from app.dominion.dominion import Dominion

users = {}
game = Dominion()

# Defines method for get user cookie
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

# Main handler check is user logged in
class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if not users.has_key(self.get_current_user()):
            self.redirect('/logout')
            return
        if not self.current_user:
            self.redirect("/login")
            return
        self.render("dominion.html", user=self.get_current_user())

# WebSockets handler add user to listeners set and push messages 
class WSHandler(tornado.websocket.WebSocketHandler):
    
    listeners = {}
    
    def open(self):
        name = tornado.escape.xhtml_escape(self.get_secure_cookie("user"))
        self.listeners[name]=self
        users[name]['websocket']=self
        self.sendToEveryone(self.newMessage("New Player: "+name, 'Dominion'))
        if(game.admin == ''):
            self.sendToPlayer(self.newMessage("You are the admin", 'Dominion'), name)
            game.admin=name
        
    def on_close(self):
        name = tornado.escape.xhtml_escape(self.get_secure_cookie("user"))
        self.listeners.pop(name)
        users.pop(name)
        if (len(users)>0):
            self.sendToEveryone(self.newMessage("Player left: "+name, 'Dominion'))
            if(game.admin == self.get_current_user()):
                game.admin = self.users.keys()[0]
        else:
            game.admin=''
        
    def on_message(self, message):
        message = tornado.escape.json_decode(message)
        new_message = self.newMessage(message['body'], message['author'])
        if (message['body'].strip().startswith('/')):
            command = message['body'].split()
            #if command chat received
            if (command[0].strip() == '/chat'):
                if (self.listeners.__contains__(command[1])):
                    new_message = self.newMessage(message['body'][len(command[0])+2+len(command[1]):], message['author']+'-private')
                    self.sendToPlayer(new_message, command[1])
                else:
                    new_message = self.newMessage('User '+command[1]+' doesn\'t exist', 'Dominion')
                    self.sendToPlayer(new_message, message['author'])
            #command players
            elif (command[0].strip() == '/players'):
                names = ''
                for name in self.listeners.iterkeys():
                    if names == '':
                        names = name
                    else:
                        names += ' - '+name 
                new_message = self.newMessage('Players('+str(len(self.listeners))+'): '+names, 'Dominion')
                self.sendToEveryone(new_message)
            #if command start received
            elif (command[0].strip() == '/start'):
                name = tornado.escape.xhtml_escape(self.get_secure_cookie("user"))
                if(game.state==game.STATE_OPEN):
                    if(name != game.admin):
                        new_message = self.newMessage('You are not the admin, you can\'t start the game', 'Dominion')
                        self.sendToPlayer(new_message, name)
                    else:
                        if(len(game.players)>1):
                            new_message = self.newMessage('Game starting...', 'Dominion')
                            self.sendToEveryone(new_message)
                            if(game.initGame()):
                                self.sendToEveryone(self.dominion_message('Game started!'))
                                self.send_board_to_everyone()
                                self.send_hand_to_everyone()
                                self.send_turn()
                                self.send_status_to_player(game.order.current())
                                   
                        else:
                            new_message = self.newMessage('Not enough players', 'Dominion')
                            self.sendToEveryone(new_message)
                else:
                    self.sendToPlayer(self.dominion_message('Game is already started'),name)
            #command hand
            elif (command[0].strip() == '/hand'):
                name = tornado.escape.xhtml_escape(self.get_secure_cookie("user"))
                self.send_hand_to_player(name)
            #command board
            elif (command[0].strip() == '/board'):
                name = tornado.escape.xhtml_escape(self.get_secure_cookie("user"))
                self.send_board_to_player(name)
            #command status
            elif (command[0].strip() == '/status'):
                name = tornado.escape.xhtml_escape(self.get_secure_cookie("user"))
                self.send_status_to_player(name)
            #command pass
            elif (command[0].strip() == '/pass'):
                name = tornado.escape.xhtml_escape(self.get_secure_cookie("user"))
                if(name==game.order.current()):
                    if(game.state==game.STATE_ACTION):
                        game.end_action_phase()
                        self.sendToEveryone(self.dominion_message(name + ' pass, start buy phase'))
                    else:
                        self.sendToPlayer(self.dominion_message('You are not in action phase'), name)
                else:
                    self.sendToPlayer(self.dominion_message('It\'s not tour turn'), name)
            #command endturn
            elif (command[0].strip() == '/endturn'):
                name = tornado.escape.xhtml_escape(self.get_secure_cookie("user"))
                if(name==game.order.current()):
                    if(game.state==game.STATE_BUY):
                        game.end_buy_phase()
                        self.send_turn()
                        self.send_hand_to_everyone()
                        self.send_status_to_player(game.order.current())
                    else:
                        self.sendToPlayer(self.dominion_message('You are not in buy phase'), name)
                else:
                    self.sendToPlayer(self.dominion_message('It\'s not tour turn'), name)
            #command play 
            elif (command[0].strip() == '/play'):
                name = tornado.escape.xhtml_escape(self.get_secure_cookie("user"))
                self.send_status_to_player(name)
            #command buy
            elif (command[0].strip() == '/buy'):
                name = tornado.escape.xhtml_escape(self.get_secure_cookie("user"))
                card_name = message['body'][len(command[0])+1:]
                (result,message)=game.buy(card_name)
                if(not result):
                    self.sendToPlayer(self.dominion_message(message) , name)
                else:
                    self.sendToPlayer(self.dominion_message("you have bought a "+card_name) , name)
                self.send_status_to_player(name)
                
        else:
            self.sendToEveryone(new_message)
                        
                
    def send_action(self, action, body):
        new_message = {
            'action': action,
            'body': body,
            'author': 'Dominion',
            'time': time.time(),
        }
        for waiter in self.listeners.itervalues():
            try:
                waiter.write_message(new_message)
            except:
                logging.error('Error sending message', exc_info=True)
                
    def send_hand_to_everyone(self):
        for player in game.players:
            self.send_hand_to_player(player)
    
    def send_hand_to_player(self,player):
        message=''
        hand = game.players[player].show_hand()
        for card_name in hand:
            if (message == ''):
                message = card_name
            else:
                message = message +' - '+card_name
        self.sendToPlayer(self.dominion_message('Hand: '+message),player)
        
    def send_board_to_everyone(self):
        for player in game.players:
            self.send_board_to_player(player)
    
    def send_board_to_player(self,player):
        self.sendToPlayer(self.dominion_message('Board: '+game.board.kingdom_cards),player)
        
    def send_status_to_player(self,player):
        self.sendToPlayer(self.dominion_message('Status: '+game.players[player].get_status()),player)
                
    
    def sendToEveryone(self,message):
        for user in users.itervalues():
            try:
                user['websocket'].write_message(message)
            except:
                logging.error('Error sending message', exc_info=True)
    
    def sendToPlayer(self,message,player):
        waiter = users[player]['websocket']
        waiter.write_message(message)
        
    def newMessage(self,message,author):
        new_message = {
            'body': message,
            'author': author,
            'time': time.time(),
        }
        return new_message
    
    def dominion_message(self,message):
        return self.newMessage(message, 'Dominion')
    
    def send_turn(self):
        self.sendToEveryone(self.dominion_message('Turn: '+game.order.current()))
   
# User logout action
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")   
    
# User login action via post data
class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
    def post(self):
        if(self.get_argument("name") == 'Dominion'):
            self.redirect("/login")
            return
        else:
            self.set_secure_cookie("user", self.get_argument("name"))
            if not users.has_key(self.get_argument('name')):
                users[self.get_argument('name')] = {}
                game.newPlayer(self.get_argument('name'))
            self.redirect("/")
    


# Application settings
settings = {
    "cookie_secret" : "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "template_path" : os.path.join(os.path.dirname(__file__), 'templates'),
    "static_path" : os.path.join(os.path.dirname(__file__), 'static'),
    "login_url" : "/login",
}

# Application routing
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/dominion", WSHandler),
    
], **settings)

# Application initialization on 8666 socket
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8666)
    tornado.ioloop.IOLoop.instance().start()