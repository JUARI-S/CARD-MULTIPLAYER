// Create Websocket url
let url = `wss://${window.location.host}/ws/online_28/lobby?${room_id}`;

// Connect with the websocket
const lobbySocket = new WebSocket(url);

// on recieving information
lobbySocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    
    switch(data.type) {
        case "lobby_status":
            if(data.status == "failed") {
                window.location.href = '/online_28'; 
            } else {
                console.log("Lobby Conection successful")
            }
            break;
        case "lobby_info":

            // room is going to be deleted
            if (data.team_a_players.length == 0 && data.team_b_players.length == 0) {
                // leave room
                leave_room();
            }
            
            team_a_player_boxes = document.getElementsByClassName('online-28-lobby-players-team-a');
            team_b_player_boxes = document.getElementsByClassName('online-28-lobby-players-team-b');

            // Reset team a player information
            for (let i = 0; i < team_a_player_boxes.length; i++) {
                team_a_player_boxes[i].innerHTML = " -- ";
                team_a_player_boxes[i].style.backgroundColor = '#cecece';
            }

            // Reset team b player information
            for (let i = 0; i < team_b_player_boxes.length; i++) {
                team_b_player_boxes[i].innerHTML = " -- ";
                team_b_player_boxes[i].style.backgroundColor = '#cecece';
            }

            // Decorate team a player cards
            data.team_a_players.forEach(function(player_name, index) {
                team_a_player_boxes[index].innerHTML = player_name;
                team_a_player_boxes[index].style.color = "white";
                if(player_name == user_name){
                    team_a_player_boxes[index].style.backgroundColor = '#0260ec';
                } else {
                    team_a_player_boxes[index].style.backgroundColor = '#089ff0';
                }
            });

            // Decorate team b player cards
            data.team_b_players.forEach(function(player_name, index) {
                team_b_player_boxes[index].innerHTML = player_name;
                team_b_player_boxes[index].style.color = "white";
                if(player_name == user_name){
                    team_b_player_boxes[index].style.backgroundColor = '#0260ec';
                } else {
                    team_b_player_boxes[index].style.backgroundColor = '#089ff0';
                }
            });
            break;
        case "start_game":
            // redirect to arena page
            window.location.href = `/online_28/${room_id}/arena`; 
            break;
        case "error":
            show_error(data.message);
            break;
        default:
            console.log("Incorrect Data type from web socket")
    }
}

function change_team() {
    remove_error();
    lobbySocket.send(JSON.stringify({
        'type': 'change_team'
    }));
}

function leave_room() {
    // send a websocket message of leaving the room
    lobbySocket.send(JSON.stringify({
        'type': 'leave_room'
    }));
    // redirect to previous page
    window.location.href = '/online_28'; 
}

function delete_room() {
    // send a websocket message of deleting the room
    lobbySocket.send(JSON.stringify({
        'type': 'delete_room'
    }));
}

function play() {
    remove_error()
    // send a websocket message to start the game
    lobbySocket.send(JSON.stringify({
        'type': 'start_game'
    }));
}

function show_error(message) {
    error_div = document.getElementById("online-28-lobby-error");
    error_div.innerHTML = message;
    error_div.style.display = "block";
}

function remove_error() {
    error_div = document.getElementById("online-28-lobby-error");
    error_div.style.display = "none";
}