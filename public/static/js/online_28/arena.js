// Create Websocket url
let url = `ws://${window.location.host}/ws/online_28/arena?${room_id}`;

// Connect with the websocket
const gameSocket = new WebSocket(url);

// on recieving information
gameSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    
    switch(data.type) {
        case "game_status":
            if(data.status == "failed") {
                window.location.href = '/online_28';
            } else {
                console.log("Game Conection successful")
            }
            break;
        case "role_info":
            if (data.data.role == "shuffler") {
                shuffler = data.data.value
                if (user_name == shuffler) {
                    document.getElementById('online-28-arena-shuffler-waiting-window').style.display = "none";
                    document.getElementById('online-28-arena-shuffler-window').style.display = "grid";
                    
                    const seed_boxes = document.getElementsByClassName('online-28-arena-shuffler-window-choice')

                    // set value of 3 seeds
                    data.data.extras.seed_choices.forEach(function(seed_value, seed_index) {
                        seed_boxes[seed_index].innerHTML = seed_value;
                        // seed_boxes[seed_index].
                    });

                }
            } else {
            }
            break;
        default:
            console.log("Incorrect Data type from web socket")
    }
}

gameSocket.onopen = function(e) {
    gameSocket.send(JSON.stringify({
        'type': 'shuffler_selection'
    }));
}

function select_seed() {

}