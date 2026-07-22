// ============================================
// Horizon AI Workspace — Chat Logic
// Dipisahkan dari inline script workspace.html
// untuk modularitas.
// ============================================

const WORKSPACE_API_URL = '/api/workspace/chat';

/**
 * Cek autentikasi — redirect ke login jika token tidak ada.
 */
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/static/login.html';
        return null;
    }
    return token;
}

/**
 * Logout — hapus token dan redirect.
 */
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/static/login.html';
}

/**
 * Kirim pesan ke workspace chat API (dengan auth + mode).
 */
async function sendWorkspaceMessage() {
    const input = document.getElementById('chat-input');
    const mode = document.getElementById('mode-selector').value;
    const message = input.value.trim();
    const token = checkAuth();

    if (!message) return;

    appendWorkspaceMessage('user', message);
    input.value = '';

    try {
        const response = await fetch(WORKSPACE_API_URL, {
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
        appendWorkspaceMessage('bot', data.reply);

    } catch (error) {
        appendWorkspaceMessage('bot', 'Maaf, terjadi kesalahan.');
        console.error('Workspace API error:', error);
    }
}

/**
 * Tambahkan bubble ke container workspace.
 */
function appendWorkspaceMessage(role, text) {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');

    div.className = role === 'user'
        ? 'bg-indigo-100 ml-auto max-w-[80%] p-3 rounded-lg'
        : 'bg-white mr-auto max-w-[80%] p-3 rounded-lg shadow';

    div.textContent = text;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// Mode descriptions
const MODE_DESCRIPTIONS = {
    assistant: 'Tanya tentang SOP, kebijakan, informasi internal',
    draft: 'Buat broadcast, caption, email, pengumuman',
    insight: 'Analisis data dan rekomendasi bisnis'
};

// Init
document.addEventListener('DOMContentLoaded', () => {
    const modeSelector = document.getElementById('mode-selector');
    if (modeSelector) {
        modeSelector.addEventListener('change', (e) => {
            const desc = document.getElementById('mode-description');
            if (desc) {
                desc.textContent = MODE_DESCRIPTIONS[e.target.value] || '';
            }
        });
    }
});
