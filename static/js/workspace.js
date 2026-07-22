/**
 * Horizon Shuttle AI — Workspace Chat (3 Mode)
 * Authenticated chat with mode selector
 */

const API_BASE = '';

// ═══════════════════════════════════════════════════════════════
// MODE CONFIGURATION
// ═══════════════════════════════════════════════════════════════

const MODE_CONFIG = {
    assistant: {
        icon: 'chat',
        label: 'Assistant',
        desc: 'Tanya tentang SOP, kebijakan, informasi internal',
        placeholder: 'Tanya tentang Horizon Shuttle...'
    },
    draft: {
        icon: 'edit',
        label: 'Draft',
        desc: 'Buat broadcast, caption, email, pengumuman',
        placeholder: 'Contoh: Buat pengumuman keterlambatan...'
    },
    insight: {
        icon: 'analytics',
        label: 'Insight',
        desc: 'Analisis data dan rekomendasi bisnis',
        placeholder: 'Contoh: Rute mana yang paling ramai?'
    }
};

// ═══════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════

let currentMode = 'assistant';
let isLoading = false;
let messages = [];

// ═══════════════════════════════════════════════════════════════
// AUTH CHECK
// ═══════════════════════════════════════════════════════════════

function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/static/login.html';
        return null;
    }
    
    // Display user name
    const userData = JSON.parse(localStorage.getItem('user') || '{}');
    const nameEl = document.getElementById('user-name');
    if (nameEl && userData.nama) nameEl.textContent = userData.nama;
    
    return token;
}

// ═══════════════════════════════════════════════════════════════
// SIDEBAR
// ═══════════════════════════════════════════════════════════════

let sidebarOpen = true;

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const main = document.getElementById('main-content');
    sidebarOpen = !sidebarOpen;
    
    if (window.innerWidth >= 768) {
        if (sidebarOpen) {
            sidebar.classList.remove('-translate-x-full');
            main.classList.remove('ml-0');
            main.classList.add('md:ml-[280px]');
        } else {
            sidebar.classList.add('-translate-x-full');
            main.classList.remove('md:ml-[280px]');
            main.classList.add('ml-0');
        }
    } else {
        sidebar.classList.toggle('-translate-x-full');
    }
}

// Mobile: hide sidebar by default
if (window.innerWidth < 768) {
    sidebarOpen = false;
    document.addEventListener('DOMContentLoaded', () => {
        const sidebar = document.getElementById('sidebar');
        const main = document.getElementById('main-content');
        if (sidebar) sidebar.classList.add('-translate-x-full');
        if (main) {
            main.classList.remove('md:ml-[280px]');
            main.classList.add('ml-0');
        }
    });
}

// ═══════════════════════════════════════════════════════════════
// MODE SWITCHING
// ═══════════════════════════════════════════════════════════════

function changeMode(mode) {
    currentMode = mode;
    const config = MODE_CONFIG[mode];
    
    // Update mode display in sidebar
    const iconEl = document.getElementById('mode-icon');
    const labelEl = document.getElementById('mode-label');
    const descEl = document.getElementById('mode-desc');
    const inputEl = document.getElementById('chat-input');
    
    if (iconEl) iconEl.textContent = config.icon;
    if (labelEl) labelEl.textContent = config.label;
    if (descEl) descEl.textContent = config.desc;
    if (inputEl) inputEl.placeholder = config.placeholder;
    
    // Update color accent
    const display = document.getElementById('current-mode-display');
    if (display) {
        display.className = `flex items-center gap-2 px-3 py-2 rounded-lg border border-white/40 mode-${mode}`;
    }
}

// ═══════════════════════════════════════════════════════════════
// CHAT UI HELPERS
// ═══════════════════════════════════════════════════════════════

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 128) + 'px';
}

function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

function showLoading(show) {
    const indicator = document.getElementById('loading-indicator');
    const btn = document.getElementById('send-btn');
    isLoading = show;
    
    if (indicator) indicator.classList.toggle('hidden', !show);
    if (btn) btn.disabled = show;
}

function appendMessage(role, content) {
    const container = document.getElementById('chat-messages');
    const welcome = document.getElementById('welcome-state');
    
    if (!container) return;
    
    // Hide welcome on first message
    if (messages.length === 0 && welcome) {
        welcome.classList.add('hidden');
        container.classList.remove('hidden');
    }
    
    const div = document.createElement('div');
    div.className = `message-anim flex ${role === 'user' ? 'justify-end' : 'justify-start'} w-full`;
    
    const bubble = document.createElement('div');
    bubble.className = `max-w-[85%] md:max-w-[70%] p-3.5 rounded-2xl text-sm leading-relaxed ${
        role === 'user' 
            ? 'bg-primary text-on-primary rounded-br-md' 
            : 'bg-white/60 backdrop-blur-sm text-on-surface border border-white/40 rounded-bl-md'
    }`;
    
    // Format: bold, lists, newlines
    let formatted = content
        .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
        .replace(/^\\* (.*$)/gm, '<li>$1</li>')
        .replace(/\\n/g, '<br>');
    
    bubble.innerHTML = formatted;
    div.appendChild(bubble);
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    
    messages.push({ role, content });
}

// ═══════════════════════════════════════════════════════════════
// API CALLS
// ═══════════════════════════════════════════════════════════════

async function sendMessage() {
    const token = checkAuth();
    if (!token) return;
    
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message || isLoading) return;
    
    input.value = '';
    input.style.height = 'auto';
    
    appendMessage('user', message);
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE}/api/workspace/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                message: message,
                mode: currentMode
            })
        });
        
        if (response.status === 401) {
            logout();
            return;
        }
        
        const data = await response.json();
        appendMessage('assistant', data.reply);
        
    } catch (error) {
        console.error('Error:', error);
        appendMessage('assistant', 'Maaf, terjadi kesalahan. Silakan coba lagi.');
    } finally {
        showLoading(false);
    }
}

function startNewChat() {
    messages = [];
    const container = document.getElementById('chat-messages');
    const welcome = document.getElementById('welcome-state');
    
    if (container) {
        container.innerHTML = '';
        container.classList.add('hidden');
    }
    if (welcome) welcome.classList.remove('hidden');
    
    const input = document.getElementById('chat-input');
    if (input) input.focus();
}

// ═══════════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    changeMode('assistant');
    
    const input = document.getElementById('chat-input');
    if (input) input.focus();
});