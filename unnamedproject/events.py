from unnamedproject import socketio
from flask_socketio import send, emit, join_room, leave_room

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
    send(json, to="test")

@socketio.on("join")
def on_join(data):
    user = data["user"]
    room = data["room"]
    print(f"client {user} wants to join: {room}")
    join_room(room)
    emit("room_message", f"Welcome to {room}, {user}", room=room)