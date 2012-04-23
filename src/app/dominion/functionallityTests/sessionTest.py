'''
Created on 15/04/2012

@author: ender3
'''
import os
from flask import Flask, session, redirect, url_for, escape, request
from app.dominion.dominion import Dominion

app = Flask(__name__)

app.dominion=Dominion()

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/error/<errorNum>')
def error(errorNum):
    if errorNum == '1':
        return 'Already exists a player with that name'
    else:
        return 'Unidentified Error'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] in app.dominion.players:
            return redirect(url_for('error/1'))
        else:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if its there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dominion')
def dominion():
    if 'username' in session:
        app.dominion.newPlayer(session['username'])
        return '%s, wait until game starts' % escape(session['username'])
    return 'You are not logged in'

# set the secret key.  keep this really secret:
app.secret_key = 'uUnw\xd2|\r\x99W%n\x8e\x9abb2\x85\xb7P\xc6\x8a%\x7f$'

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)