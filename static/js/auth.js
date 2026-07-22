/**
 * Horizon Shuttle AI — Auth Utilities
 * Hardcode login + JWT session management
 */

const API_BASE = '';

// ═══════════════════════════════════════════════════════════════
// LOGIN
// ═══════════════════════════════════════════════════════════════

async function handleLogin(event) {
    event.preventDefault();
    hideError();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    
    if (!username || !password) {
        showError('Username dan password wajib diisi');
        return;
    }
    
    setLoading(true);
    
    try {
        const response = await fetch(`${API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            window.location.href = '/static/workspace.html';
        } else {
            showError(data.detail || 'Username atau password salah');
        }
        
    } catch (error) {
        showError('Gagal terhubung ke server. Coba lagi.');
    } finally {
        setLoading(false);
    }
}

// ═══════════════════════════════════════════════════════════════
// AUTH CHECK & LOGOUT
// ═══════════════════════════════════════════════════════════════

function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/static/login.html';
        return null;
    }
    return token;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/static/login.html';
}

// ═══════════════════════════════════════════════════════════════
// UI HELPERS (Login Page)
// ═══════════════════════════════════════════════════════════════

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    if (errorText) errorText.textContent = message;
    if (errorDiv) errorDiv.classList.remove('hidden');
    
    const form = document.getElementById('login-form');
    if (form) {
        form.classList.add('shake');
        setTimeout(() => form.classList.remove('shake'), 300);
    }
}

function hideError() {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) errorDiv.classList.add('hidden');
}

function setLoading(loading) {
    const btn = document.getElementById('login-btn');
    const btnText = document.getElementById('btn-text');
    const btnSpinner = document.getElementById('btn-spinner');
    
    if (btn) btn.disabled = loading;
    if (btnText) btnText.textContent = loading ? 'Memuat...' : 'Masuk';
    if (btnSpinner) btnSpinner.classList.toggle('hidden', !loading);
}

function togglePassword() {
    const input = document.getElementById('password');
    const icon = document.getElementById('eye-icon');
    if (!input || !icon) return;
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.textContent = 'visibility';
    } else {
        input.type = 'password';
        icon.textContent = 'visibility_off';
    }
}