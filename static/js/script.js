const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatHistory = document.getElementById('chat-history');

chatForm.addEventListener('submit', sendMessage);

function sendMessage(event) {
    event.preventDefault();

    const message = chatInput.value;
    chatInput.value = '';

    if (message.trim() === '') {
        return;
    }

    disableInputAndButton();

    appendMessage('User', message);

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `question=${encodeURIComponent(message)}`,
    })
        .then(response => response.text())
        .then(data => {
            appendMessage('CourseGenie', data);
            enableInputAndButton();
        })
        .catch(error => {
            console.error('Error:', error);
            enableInputAndButton();
        });
}

function appendMessage(role, content) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message';
    messageElement.innerHTML = `<strong>${role}: </strong>${content}`;
    chatHistory.appendChild(messageElement);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function disableInputAndButton() {
    chatInput.disabled = true;
    chatInput.setAttribute('placeholder', 'Responding....');
    chatInput.style.cursor = 'not-allowed';
    chatForm.querySelector('button').disabled = true;
}

function enableInputAndButton() {
    chatInput.disabled = false;
    chatInput.setAttribute('placeholder', 'Type your message...');
    chatInput.style.cursor = 'text';
    chatForm.querySelector('button').disabled = false;
}
