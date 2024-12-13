function validateForm() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const errorMessage = document.getElementById('errorMessage');

    if (!username || !password) {
        errorMessage.classList.remove('d-none');
        errorMessage.textContent = 'Both fields are required.';
        return;
    }

    if (username === 'admin' && password === 'admin123') {
        window.location.href = 'image_upload.html';
    } else {
        errorMessage.classList.remove('d-none');
        errorMessage.textContent = 'Invalid username or password. Please try again.';
    }
}