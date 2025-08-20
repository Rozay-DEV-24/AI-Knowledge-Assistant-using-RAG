const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const clearBtn = document.getElementById('clear-btn'); 

const API_URL = 'http://127.0.0.1:5000/query';

let chatHistory = [];

// Function to render Markdown text
function renderMarkdown(text) {
    return marked.parse(text, { breaks: true }); // Use breaks:true for line breaks
}

async function sendMessage() {
    const question = userInput.value.trim();
    if (question === '') return;

    // --- Create and display user message ---
    const userMessageElem = document.createElement('div');
    userMessageElem.classList.add('message', 'user-message');
    userMessageElem.innerText = question;
    chatBox.appendChild(userMessageElem);

    userInput.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    // --- Create bot message container ---
    const botMessageElem = document.createElement('div');
    botMessageElem.classList.add('message', 'bot-message');
    botMessageElem.innerHTML = '<span class="loading-indicator"></span>'; // Loading dots
    chatBox.appendChild(botMessageElem);
    chatBox.scrollTop = chatBox.scrollHeight;

    // --- Fetch and process the stream ---
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';
        botMessageElem.innerHTML = ''; // Clear loading indicator

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            
            // Check for our special SOURCES signal
            if (chunk.startsWith("SOURCES:")) {
                const sourcesJson = chunk.substring(8);
                const sources = JSON.parse(sourcesJson);
                displaySources(sources);
            } else {
                fullResponse += chunk;
                // Render markdown in real-time
                botMessageElem.innerHTML = renderMarkdown(fullResponse);
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    } catch (error) {
        botMessageElem.innerHTML = 'Sorry, something went wrong. Please try again.';
        console.error('Error:', error);
    }
}

// --- NEW FUNCTION TO DISPLAY SOURCES ---
function displaySources(sources) {
    const sourcesContainer = document.createElement('div');
    sourcesContainer.classList.add('sources-container');
    
    let sourcesHtml = '<p>Sources:</p>';
    sources.forEach(source => {
        // Extract just the file name from the path
        const fileName = source.split(/[\\/]/).pop();
        sourcesHtml += `<span class="source-tag">${fileName}</span>`;
    });
    
    sourcesContainer.innerHTML = sourcesHtml;
    chatBox.appendChild(sourcesContainer);
}
// ------------------------------------

function addMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    messageElement.innerText = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const question = userInput.value.trim();
    if (question === '') return;

    // --- Add user message to history ---
    chatHistory.push(`User: ${question}`);

    // Display user message
    const userMessageElem = document.createElement('div');
    userMessageElem.classList.add('message', 'user-message');
    userMessageElem.innerHTML = renderMarkdown(question); // Render user message as markdown too
    chatBox.appendChild(userMessageElem);
    userInput.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    // Create bot message container
    const botMessageElem = document.createElement('div');
    botMessageElem.classList.add('message', 'bot-message');
    botMessageElem.innerHTML = '<span class="loading-indicator"></span>';
    chatBox.appendChild(botMessageElem);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            // --- MODIFIED: Send the question AND the history ---
            body: JSON.stringify({ 
                question: question,
                history: chatHistory 
            }),
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';
        botMessageElem.innerHTML = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            
            if (chunk.startsWith("SOURCES:")) {
                const sourcesJson = chunk.substring(8);
                const sources = JSON.parse(sourcesJson);
                displaySources(sources);
            } else {
                fullResponse += chunk;
                botMessageElem.innerHTML = renderMarkdown(fullResponse);
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        // --- Add final bot message to history ---
        chatHistory.push(`Assistant: ${fullResponse}`);

    } catch (error) {
        botMessageElem.innerHTML = 'Sorry, something went wrong. Please try again.';
        console.error('Error:', error);
    }
}

// --- NEW: Function to clear the chat ---
function clearChat() {
    chatHistory = []; // Reset history array
    chatBox.innerHTML = ''; // Clear the visual chat box
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') sendMessage();
});
clearBtn.addEventListener('click', clearChat); 

// sendBtn.addEventListener('click', sendMessage);
// userInput.addEventListener('keypress', (event) => {
//     if (event.key === 'Enter') {
//         sendMessage();
//     }
// });