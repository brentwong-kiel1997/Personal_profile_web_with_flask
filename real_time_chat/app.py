from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['username']
    username = session.get('username', 'Guest')
    return render_template('chat.html', username=username)

@socketio.on('message')
def handleMessage(msg):
    username = msg.get('username', 'Anonymous')
    message = msg.get('message', '')
    emit('message', {'username': username, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
