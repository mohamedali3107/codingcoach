document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chat = document.getElementById('chat');

    // Function to scroll conversation to the bottom
    function scrollConversation() {
        conversation.scrollTop = chat.scrollHeight;
    }

    // Function to submit the form
    function submitForm() {
        chatForm.submit();
    }

    document.querySelectorAll('.markdown-content').forEach(el => {
        el.innerHTML = marked(el.textContent);
    });

    
    // Event listener to submit the form when Enter key is pressed
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            submitForm();
        }
    });

    // Focus on the user input field
    userInput.focus();

    // Scroll conversation to the bottom initially
    scrollChat();

    // Example usage of addCodeMessage
    // addCodeMessage("Your code goes here");

    // Example usage of copyToClipboard
    // copyToClipboard("Content to copy");
});

// Function to add a code message to the conversation
function addCodeMessage(content) {
    const conversation = document.getElementById('chat');
    const codeMessage = document.createElement('div');
    codeMessage.className = 'code-messages';
    codeMessage.innerHTML = `<p>ChatBot: <pre>${content}</pre></p>`;
    conversation.appendChild(codeMessage);
    scrollChat(); // Scroll to the bottom after adding the message
}

// Function to copy content to clipboard
function copyCode() {
    const codeElement = document.querySelector('.language-any code');
    const codeToCopy = codeElement.textContent;

    const textarea = document.createElement('textarea');
    textarea.value = codeToCopy;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);

    alert('Code copied to clipboard!');
}
