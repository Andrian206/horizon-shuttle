const API_URL = '/api/workspace/chat';

// Update description when mode changes
document.getElementById('mode-selector').addEventListener('change', (e) => {
    const desc = document.getElementById('mode-description');
    const descriptions = {
        assistant: 'Tanya tentang SOP, kebijakan, informasi internal',
        draft: 'Buat broadcast, caption, email, pengumuman',
        insight: 'Analisis data dan rekomendasi bisnis'
    };
    desc.textContent = descriptions[e.target.value];
});

async function sendWorkspaceMessage() {
    const input = document.getElementById('chat-input');
    const mode = document.getElementById('mode-selector').value;
    const message = input.value.trim();
    const token = localStorage.getItem('token');

    if (!message) return;

    appendMessage('user', message);
    input.value = '';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                message: message,
                mode: mode
            })
        });

        if (response.status === 401) {
            logout();
            return;
        }

        const data = await response.json();
        appendMessage('bot', data.reply);

    } catch (error) {
        appendMessage('bot', 'Maaf, terjadi kesalahan.');
    }
}

function appendMessage(role, text) {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = role === 'user'
        ? 'bg-indigo-100 ml-auto max-w-[80%] p-3 rounded-lg'
        : 'bg-white mr-auto max-w-[80%] p-3 rounded-lg shadow';
    div.textContent = text;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

document.getElementById('chat-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendWorkspaceMessage();
});