document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', () => {
            const chatType = button.getAttribute('data-chat-type');
            const rollNumber = "{{ roll_number }}"; // Ensure this value is available in the HTML
            
            let url;
            if (chatType === 'private') {
                //URL private chat ke liye 
                url = `http://127.0.0.1:5001/chat?roll_number=${encodeURIComponent(rollNumber)}`;
            } else if (chatType === 'group') {
                // URL group chat ke liye 
                url = `http://127.0.0.1:5002/group_chat?roll_number=${encodeURIComponent(rollNumber)}`;
            }

            if (url) {
                window.location.href = url;
            }
        });
    });
});
