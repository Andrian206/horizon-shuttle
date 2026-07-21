// Check auth on workspace pages
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/static/login.html';
    }
    return token;
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/static/login.html';
}

// Call checkAuth on workspace pages
if (window.location.pathname.includes('workspace')) {
    checkAuth();
}