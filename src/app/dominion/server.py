'''
Created on 15/04/2012

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

games = []
users = {}
listeners = {}

# Defines method for get user cookie
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

# Main handler check is user logged in
class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.render("dominion.html", user=name)

# WebSockets handler add user to listeners set and push messages 
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        name = tornado.escape.xhtml_escape(self.get_secure_cookie("user"))
        self.listeners[name]=self
        self.sendToEveryone(self.newMessage("New Player: "+name, 'Dominion'))
        if(self.admin == ''):
            self.sendToPlayer(self.newMessage("You are the admin", 'Dominion'), name)
            self.admin=name
        
    def on_close(self):
        name = tornado.escape.xhtml_escape(self.get_secure_cookie("user"))
        self.listeners.pop(name)
        if (len(self.listeners)>0):
            self.sendToEveryone(self.newMessage("Player left: "+name, name))
            if(self.admin == name):
                self.admin = self.listeners.keys()[0]
        else:
            self.admin=''
        
    def on_message(self, message):
        message = tornado.escape.json_decode(message)
        new_message = self.newMessage(message['body'], message['author'])
        if (message['body'].strip().startswith('/')):
            command = message['body'].split()
            #if command chat received
            if (command[0].strip() == '/chat'):
                if (self.listeners.__contains__(command[1])):
                    new_message = self.newMessage(message['body'][len(command[0])+1:], message['author'])
                    self.sendToPlayer(new_message, command[1])
                else:
                    new_message = self.newMessage('User '+command[1]+' doesn\'t exist', 'Dominion')
                    self.sendToPlayer(new_message, message['author'])
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
                new_message = self.newMessage('Game starting...', 'Dominion')
                self.sendToEveryone(new_message)
                for name in self.listeners.iterkeys():
                    self.game.newPlayer(name)
                self.game.initGame()
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
    
    def sendToEveryone(self,message):
        for waiter in self.listeners.itervalues():
                    try:
                        waiter.write_message(message)
                    except:
                        logging.error('Error sending message', exc_info=True)
    
    def sendToPlayer(self,message,player):
        waiter = self.listeners[player]
        waiter.write_message(message)
        
    def newMessage(self,message,author):
        new_message = {
            'body': message,
            'author': author,
            'time': time.time(),
        }
        return new_message

# User logut action
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")

# User login action via post data
class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        if not users.has_key(self.get_argument('name')):
            users[self.get_argument('name')] = {}
        self.redirect("/")
        
class QuitHandler(BaseHandler):
    def get(self):
        user = users[self.get_current_user()]
        user['player'].left = True
        del user['player']
        del user['game']
        self.redirect('/')
 
# Lobby access       
class LobbyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if not users.has_key(self.get_current_user()):
            self.redirect('/logout')
            return
        if users[self.get_current_user()].has_key('game'):
            game = users[self.get_current_user()]['game']
            player = users[self.get_current_user()]['player']
            self.redirect('/' + str(id(game)) + '/' + str(id(player)))
            return
        self.render("lobby.html", user=self.get_current_user(), games=games)

# Create new game
class NewGameHandler(BaseHandler):
    def get(self):
        game = Dominion()
        game.url = '/' + str(id(game))
        games.append(game)
        application.add_handlers(r'.*$', [(r'/' + str(id(game)), NewPlayerHandler, {'game': game})])
        self.redirect('/' + str(id(game)))
        
# Create new player
class NewPlayerHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        self.game = kwargs['game']
        super(NewPlayerHandler, self).__init__(*args)

    def get(self):
        player=self.get_current_user()
        self.game.newPlayer(player)
        users[self.get_current_user()]['player'] = player
        users[self.get_current_user()]['game'] = self.game
        application.add_handlers(r'.*$', [(self.request.uri + '/' + str(id(player)), WSHandler, {'player': player})])
        self.render("dominion.html", user=str(id(player)), game=str(id(self.game)))

class PlayerInfo(BaseHandler):
    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player')
        self.template = kwargs.pop('template')
        super(PlayerInfo, self).__init__(*args, **kwargs)

    def get(self):
        self.render("dominion.html", player=self.player)

class PlayerWebSocket(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player')
        print 'Creating a new playersocket for %s' % self.player.name
        self.player.socket = self
        self.player.left = False
        super(PlayerWebSocket, self).__init__(*args, **kwargs)

    def open(self):
        print '%s joined' % (self.player.name)

    def on_close(self):
        print '%s left - removing them from the game' % (self.player.name)
        self.player.left = True
        if all([player.left for player in self.player.game.players]):
            try:
                games.remove(self.player.game)
            except:
                print 'Tried to remove a player that was NOT in the game'
                pass

    def on_message(self, message):
        print '%s received "%s"' % (self.player.name, message)
        try:
            params = message.split(' ')
            self.player.callbacks[params[0]](message=' '.join(params[1:]))
        except Exception, e:
            self.player.socket.write_message('Uncaught:' + str(e))

settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
    "static_path": os.path.join(os.path.dirname(__file__), 'static'),
    'login_url'    : '/login',
}

# Application routing
application = tornado.web.Application([
    (r'/', LobbyHandler),
    (r'/new', NewGameHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/dominion", WSHandler),
    
], **settings)

# Application initialization on 8666 socket
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8666)
    tornado.ioloop.IOLoop.instance().start()
    
