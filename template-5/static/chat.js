document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-button');
    const messagesDiv = document.getElementById('messages-list');
    const recipientInput = document.getElementById('recipient');
    const messageInput = document.getElementById('message');
    const emojiButton = document.getElementById('emoji-button');
    const emojiPicker = document.getElementById('emoji-picker');
    let isFetching = false;

    const emojis = ['😊', '😂', '😍', '😒', '😢', '😎', '😡', '😱']; // Add more emojis as needed

    function createEmojiOptions() {
        emojis.forEach(emoji => {
            const span = document.createElement('span');
            span.textContent = emoji;
            span.addEventListener('click', () => {
                messageInput.value += emoji;
                emojiPicker.style.display = 'none';
            });
            emojiPicker.appendChild(span);
        });
    }

    createEmojiOptions();

    function fetchMessages() {
        if (isFetching) return;
        isFetching = true;

        const recipient = recipientInput.value.trim();
        if (recipient) {
            fetch(`/get_messages?recipient=${recipient}`)
                .then(response => response.json())
                .then(data => {
                    messagesDiv.innerHTML = '';
                    data.forEach(msg => {
                        const messageElement = document.createElement('div');
                        messageElement.classList.add('message');
                        messageElement.textContent = `${msg.sender}: ${msg.message} (${msg.timestamp})`;
                        messagesDiv.appendChild(messageElement);
                    });
                })
                .catch(error => {
                    console.error('Error fetching messages:', error);
                })
                .finally(() => {
                    isFetching = false;
                });
        } else {
            isFetching = false;
        }
    }

    sendButton.addEventListener('click', () => {
        const recipient = recipientInput.value.trim();
        const message = messageInput.value.trim();
        if (recipient && message) {
            fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    recipient: recipient,
                    message: message,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    messageInput.value = ''; // Clear the input field after sending
                    // Trigger refresh in other tabs
                    localStorage.setItem('chat-refresh', Date.now().toString());
                } else {
                    console.error('Failed to send message:', data.message);
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
        }
    });

    emojiButton.addEventListener('click', () => {
        emojiPicker.style.display = emojiPicker.style.display === 'none' ? 'block' : 'none';
    });

    window.addEventListener('storage', (event) => {
        if (event.key === 'chat-refresh') {
            fetchMessages(); // Refresh messages on other tabs
        }
    });

    fetchMessages();
    setInterval(fetchMessages, 5000);
});
