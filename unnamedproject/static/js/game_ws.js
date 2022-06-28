var game_socket = undefined;

function connect_game(game_id, token) {
    var wrapper = document.getElementById("game-wrapper");
    game_socket = io();
    game_socket.on("connect", function () {
        game_socket.emit("join", {
            token: token,
            game_id: game_id,
        });
    });
    game_socket.on("update", function (data) {
        wrapper.innerHTML = data;
    });
}

function start_game(game_id, token) {
    game_socket.emit("start_game", {
        token: token,
        game_id: game_id,
    });
}

function play_card(game_id, token, played_card) {
    game_socket.emit("play_card", {
        token: token,
        game_id: game_id,
        played_card: played_card,
    });
}

function draw_card(game_id, token) {
    game_socket.emit("draw_card", {
        token: token,
        game_id: game_id,
    });
}

function chat(game_id, token) {
    var message = document.getElementById('chattextbox').value;
    if(message){
    game_socket.emit("chat", {
        token: token,
        game_id: game_id,
        message: message
    });
}}