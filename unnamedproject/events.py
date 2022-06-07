from unnamedproject import socketio
from flask_socketio import send, emit

@socketio.on('connect')
def handle_connect():
    print("connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("disconnected")

@socketio.on('message')
def handle_message(message):
    send(message)

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json)