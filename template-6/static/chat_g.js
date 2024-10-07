document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    // Get roll number from the HTML element rendered by Flask
    const rollNumber = document.getElementById('roll-number').innerText;

    const createRoomButton = document.getElementById('create-room-btn');
    const joinRoomButton = document.getElementById('join-room-btn');
    const leaveRoomButton = document.getElementById('leave-room-btn');
    const sendButton = document.getElementById('send-button');
    const roomCodeInput = document.getElementById('room-code-input');
    const messageInput = document.getElementById('message');
    const messagesList = document.getElementById('messages-list');
    const currentRoomCode = document.getElementById('current-room-code');
    const currentRoomContainer = document.getElementById('current-room');

    let currentRoom = null;

    createRoomButton.addEventListener('click', () => {
        fetch('/create_room', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.room_code) {
                alert(`Room created with code: ${data.room_code}`);
                roomCodeInput.value = data.room_code;
            }
        })
        .catch(error => console.error('Error creating room:', error));
    });

    joinRoomButton.addEventListener('click', () => {
        const roomCode = roomCodeInput.value;
        fetch('/join_room', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ room_code: roomCode, roll_number: rollNumber })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                currentRoomCode.innerText = roomCode;
                currentRoomContainer.style.display = 'block';
                socket.emit('join', { room_code: roomCode, roll_number: rollNumber });
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error('Error joining room:', error));
    });

    leaveRoomButton.addEventListener('click', () => {
        const roomCode = currentRoomCode.innerText;
        socket.emit('leave', { room_code: roomCode, roll_number: rollNumber });
        currentRoomContainer.style.display = 'none';
        currentRoomCode.innerText = '';
    });

    sendButton.addEventListener('click', () => {
        const message = messageInput.value;
        const roomCode = currentRoomCode.innerText;
        if (message && roomCode) {
            socket.emit('message', { room_code: roomCode, roll_number: rollNumber, message });
            messageInput.value = '';
        }
    });

    socket.on('message', (data) => {
        const li = document.createElement('li');
        li.innerText = data;
        messagesList.appendChild(li);
    });
});