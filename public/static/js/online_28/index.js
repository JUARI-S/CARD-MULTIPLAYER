function show_error(message) {
    var error_div = document.getElementById("online-28-room-error");
    error_div.innerHTML = message;
    error_div.style.display = "block";
}

// Utility function to send post request
async function sendPostRequest(url, data) {
    const csrftoken = getCookie('csrftoken'); // Function to retrieve CSRF token from cookies
    try{
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        })
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return {
            "status": "fail",
            "message": "Server Issue"
        };
    }
}

// Function to retrieve CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function join_room() {
    // Fetch room id
    var room_id = document.getElementById("room_id").value;

    // send post request to join_room with roomid
    var response = await sendPostRequest("/online_28/join_room/" + room_id, {});

    if(response["status"] == "success") {
        window.location.replace("/online_28/" + room_id);
    } else {
        show_error(response["message"]);
    }
}

async function create_room() {
    // send post request to create room returns the new room id
    var response = await sendPostRequest("/online_28/create_room", {});
    
    if(response["status"] == "success") {
        window.location.replace("/online_28/" + response["room_id"]);
    } else {
        show_error(response["message"]);
    }
}