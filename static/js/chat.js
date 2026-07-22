// ============================================
// Horizon AI — Public Chat Logic
// ============================================

const API_URL = '/api/chat/public';

/**
 * Kirim pesan ke public chat API (tanpa auth).
 */
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();

    if (!message) return;

    appendMessage('user', message);
    input.value = '';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        appendMessage('bot', data.reply);

    } catch (error) {
        appendMessage('bot', 'Maaf, terjadi kesalahan. Silakan coba lagi nanti.');
    }
}

/**
 * Tambahkan bubble chat ke container.
 */
function appendMessage(role, text) {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');

    div.className = role === 'user'
        ? 'bg-blue-500 text-white ml-auto max-w-[80%] p-3 rounded-lg'
        : 'bg-white mr-auto max-w-[80%] p-3 rounded-lg shadow';

    div.textContent = text;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// Event listener untuk Enter key
document.getElementById('chat-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
