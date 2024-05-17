// Stages
const Stages = Object.freeze({ 
    SHUFFLER_WAITING: "shuffler-waiting",
    SHUFFLER_SEED_SELECTION: "shuffler-seed-selection",
    BID_INFO: "bid-info",
    BID_CHALLENGER: "bid-challenger",
    TRUMP_WAITING: "trump-waiting",
    TRUMP_SELECTION: "trump-selection",
    GAME: "game",
});

// Create Websocket url
let url = `wss://${window.location.host}/ws/online_28/arena?${room_id}`;

let cards = [
    {suit: 'club', number: '9'},
    {suit: 'spade', number: 'A'},
    {suit: 'heart', number: 'K'},
    {suit: 'diamond', number: '7'},
]

// Connect with the websocket
const gameSocket = new WebSocket(url);

// Just after the websocker connects
gameSocket.onopen = function(e) {
    if( owner ) {
        // Owner send the shuffler selection process request
        gameSocket.send(JSON.stringify({
            'type': 'shuffler_selection'
        }));
    }
}

// on recieving information
gameSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    console.log(data);
    switch(data.type) {
        case "game_status":
            if(data.status == "failed") {
                window.location.href = '/online_28';
            } else {
                console.log("Game Connection successful");
                add_log("Client Connected");
            }
            break;
        case "role_info":
            switch(data.role_info.role) {
                case "shuffler":
                    shuffler = data.role_info.value;
                    if (user_name == shuffler) {
                        update_stage(Stages.SHUFFLER_SEED_SELECTION, data.role_info.extras);
                    } else {
                        update_stage(Stages.SHUFFLER_WAITING, {});
                    }
                    add_log(`[SHUFFLER] : ${shuffler}`);
                    break;
                case "bid":
                    bid_challenger = data.role_info.extras.challenger;
                    if(user_name == bid_challenger) {
                        update_stage(Stages.BID_CHALLENGER, data.role_info.extras);
                    } else {
                        update_stage(Stages.BID_INFO, data.role_info.extras);
                    }
                    break;
                case "trump_selecter":
                    trump_selecter = data.role_info.value;
                    if(user_name == trump_selecter) {
                        update_stage(Stages.TRUMP_SELECTION, data.role_info.extras);
                    } else {
                        update_stage(Stages.TRUMP_WAITING, data.role_info.extras);
                    }
                    break;
                default:
                    add_log("Invalid role broadcasted");
            }
            break;
        case "cards":
            // Distribute the given cards
            update_my_deck(data.cards);
            break;
        case "trump_open":
            update_stage(Stages.GAME, data);
            break;
        case "trump_closed":
            update_stage(Stages.GAME, data);
            break;
        case "game_info":
            const curr_player_name = data.game_info.curr_player;
            const cards_played = data.game_info.cards_played;
            if(user_name == curr_player_name) {
                document.getElementById("move-status").innerHTML = `Your's Move`;
                update_playing_cards_state(cards_played);
            } else {
                document.getElementById("move-status").innerHTML = `${curr_player_name} Move`;
                update_playing_cards_state(cards_played);
            }
        case "error":
            add_log(`[ERROR] : ${data.message}`);
            break;
        default:
            add_log("[ERROR] : Incorrect Message type from web socket")
    }
}

function update_stage(stage_name, extras) {
    // Update stage name
    const title_div = document.getElementById("online-28-arena-game-stage-title");
    title_div.innerHTML = `Stage - ${stage_name}`;

    // Make all the stage div invisible
    Array.from(document.getElementsByClassName("online-28-arena-game-stage")).forEach(div => {
        div.style.display = "none";
    });

    // Make current stage visible
    document.getElementById(stage_name).style.display = "grid";

    // Add stage specific information
    switch (stage_name) {
        case Stages.SHUFFLER_WAITING:
            document.getElementById("shuffler-waiting").innerHTML = `Waiting for ${shuffler} to<br>select the seed ...`;
            break;
        case Stages.SHUFFLER_SEED_SELECTION:
            const seeds = extras.seed_choices;
            Array.from(document.getElementsByClassName("online-28-arena-shuffler-window-choice")).forEach(function(div, index) {
                div.innerHTML = seeds[index];
            });
            break;
        case Stages.BID_INFO:
            document.getElementById("bid-info-bidder").innerHTML = `Bidder - ${extras.bidder}`;
            document.getElementById("bid-info-bid-value").innerHTML = `Bid Value - ${extras.bid_value}`;
            document.getElementById("bid-info-bid-challenger").innerHTML = `Challenger - ${extras.challenger}`;
            break;
        case Stages.BID_CHALLENGER:
            document.getElementById("bid-challenger-bidder").innerHTML = `Bidder - ${extras.bidder}`;
            document.getElementById("bid-challenger-bid-value").innerHTML = `Bid Value - ${extras.bid_value}`;
            break;
        case Stages.TRUMP_WAITING:
            document.getElementById("trump-waiting").innerHTML = `Waiting for ${trump_selecter} to<br>select the trump ...`;

            // set target points for both teams
            document.getElementById("team_a-target-points").innerHTML = `Target Points - ${extras.team_a_target}`;
            document.getElementById("team_b-target-points").innerHTML = `Target Points - ${extras.team_b_target}`;
            break;
        case Stages.TRUMP_SELECTION:
            // set target points for both teams
            document.getElementById("team_a-target-points").innerHTML = `Target Points - ${extras.team_a_target}`;
            document.getElementById("team_b-target-points").innerHTML = `Target Points - ${extras.team_b_target}`;
            break;
        case Stages.GAME:
            if (extras.type == "trump_open") {
                document.getElementById("trump-closed").style.display = "none";
                document.getElementById("trump-open").style.display = "flex";
                document.getElementById("trump").style.backgroundImage = `url(/static/images/cards/${extras.trump}_suit.png)`;
            } else {
                document.getElementById("trump-open").style.display = "none";
                document.getElementById("trump-closed").style.display = "flex";
            }
            break;
        default:
            add_log("Invalid stage")
    }
}

function update_playing_cards_state(cards_played) {

}

function update_cards(cards) {
    // update playing cards
}

function update_my_deck(cards) {
    // update my deck
    const deck_cards_div = document.getElementsByClassName("online-28-arena-player-card");
    cards.forEach(function(card, index) {
        deck_cards_div[index].style.backgroundImage = `url(/static/images/cards/${card.suit}/${card.number}.png)`;
    });
}

function select_seed(seed_index) {
    if(shuffler == user_name) {
        gameSocket.send(JSON.stringify({
            'type': 'seed_selection',
            'seed_index': seed_index
        }));
    }
}

function bid_challenge() {
    if(bid_challenger == user_name) {
        // Shuffler will send the seed index
        gameSocket.send(JSON.stringify({
            'type': 'bid_challenge'
        }));
    }
}

function bid_pass() {
    if(bid_challenger == user_name) {
        gameSocket.send(JSON.stringify({
            'type': 'bid_pass'
        }));
    }
}

function select_trump(suit_index) {
    gameSocket.send(JSON.stringify({
        'type': 'trump_selection',
        'trump_suit_index': suit_index
    }));
}

function disclose_trump() {
    // game logic checks
    if(curr_player) {
        gameSocket.send(JSON.stringify({
            'type': 'disclose_trump',
        }));
    }
}

function play_card(card) {
    if(curr_player) {
        gameSocket.send(JSON.stringify({
            'type': 'play_card',
            'card': card
        }));
    }
}

function add_log(message) {
    const logs_div = document.getElementById("online-28-arena-game-logs");

    // Create a new log div element
    var log_div = document.createElement('div');
    log_div.className = "online-28-arena-game-log"
    log_div.textContent = message;

    logs_div.appendChild(log_div);

    // Scroll the log window to the bottom
    logs_div.scrollTop = logs_div.scrollHeight;
}