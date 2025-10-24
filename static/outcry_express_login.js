// Login Page JavaScript
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const loginButton = document.querySelector('.login-button');

    // Form submission handler
    loginForm.addEventListener('submit', handleLogin);

    // Input validation
    emailInput.addEventListener('input', validateEmail);
    passwordInput.addEventListener('input', validatePassword);

    // Enter key handling
    passwordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleLogin(e);
        }
    });
});

function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const loginButton = document.querySelector('.login-button');
    
    // Clear previous messages
    clearMessages();
    
    // Validate inputs
    if (!validateEmail()) {
        showError('Please enter a valid email address');
        return;
    }
    
    if (!validatePassword()) {
        showError('Password must be at least 6 characters long');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    
    // Simulate login process (replace with actual API call)
    setTimeout(() => {
        // For demo purposes, accept any email/password combination
        if (email && password) {
            // Simulate successful login
            showSuccess('Login successful! Redirecting...');
            
            // Store login state (in a real app, this would be handled by the server)
            localStorage.setItem('outcry_express_logged_in', 'true');
            localStorage.setItem('outcry_express_user_email', email);
            
            // Redirect to main app after a short delay
            setTimeout(() => {
                window.location.href = '/outcry-express-mobile';
            }, 1500);
        } else {
            showError('Invalid email or password');
            setLoadingState(false);
        }
    }, 1500);
}

function validateEmail() {
    const email = document.getElementById('email').value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && !emailRegex.test(email)) {
        document.getElementById('email').classList.add('invalid');
        return false;
    } else {
        document.getElementById('email').classList.remove('invalid');
        return true;
    }
}

function validatePassword() {
    const password = document.getElementById('password').value;
    
    if (password && password.length < 6) {
        document.getElementById('password').classList.add('invalid');
        return false;
    } else {
        document.getElementById('password').classList.remove('invalid');
        return true;
    }
}

function setLoadingState(loading) {
    const loginButton = document.querySelector('.login-button');
    
    if (loading) {
        loginButton.classList.add('loading');
        loginButton.disabled = true;
        loginButton.textContent = 'Signing In...';
    } else {
        loginButton.classList.remove('loading');
        loginButton.disabled = false;
        loginButton.textContent = 'Sign In';
    }
}

function showError(message) {
    clearMessages();
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const form = document.getElementById('loginForm');
    form.insertBefore(errorDiv, form.firstChild);
}

function showSuccess(message) {
    clearMessages();
    
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    
    const form = document.getElementById('loginForm');
    form.insertBefore(successDiv, form.firstChild);
}

function clearMessages() {
    const existingMessages = document.querySelectorAll('.error-message, .success-message');
    existingMessages.forEach(message => message.remove());
}

function forgotPassword() {
    const email = document.getElementById('email').value.trim();
    
    if (!email) {
        showError('Please enter your email address first');
        document.getElementById('email').focus();
        return;
    }
    
    // Show loading state
    const forgotButton = document.querySelector('.forgot-password-btn');
    const originalText = forgotButton.textContent;
    forgotButton.textContent = 'Sending...';
    forgotButton.disabled = true;
    
    // Simulate password reset process
    setTimeout(() => {
        showSuccess('Password reset instructions sent to your email');
        forgotButton.textContent = originalText;
        forgotButton.disabled = false;
    }, 2000);
}

// Check if user is already logged in
function checkLoginStatus() {
    const isLoggedIn = localStorage.getItem('outcry_express_logged_in');
    if (isLoggedIn === 'true') {
        // Redirect to main app if already logged in
        window.location.href = '/outcry-express-mobile';
    }
}

// Initialize login status check
checkLoginStatus();

// Handle back button and page refresh
window.addEventListener('beforeunload', () => {
    // In a real app, you might want to clear sensitive data
});

// Handle visibility change (when user switches tabs)
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        checkLoginStatus();
    }
});
