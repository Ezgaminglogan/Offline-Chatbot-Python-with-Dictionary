document.addEventListener('DOMContentLoaded', function () {
    const chatBox = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('sendBtn');
    const userInput = document.getElementById('userInput');

    // Function to append messages to the chat box
    function appendMessage(message, className) {
        const msg = document.createElement('div');
        msg.className = 'chat-message ' + className + ' fade-in';
        msg.innerText = message;
        chatBox.appendChild(msg);
        
        // Auto-scroll to the bottom after the message is added
        msg.scrollIntoView({ behavior: "smooth", block: "end" });
    }

    // Handle sending a message
    sendBtn.addEventListener('click', function () {
        const message = userInput.value;
        if (message) {
            appendMessage(message, 'user-message');

            // Send the message to the backend (Python)
            eel.get_response(message)((response) => {
                appendMessage(response, 'bot-message');
            });

            userInput.value = ''; // Clear input after sending
        }
    });

    // Allow pressing Enter to send message
    userInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            sendBtn.click();
        }
    });
});
