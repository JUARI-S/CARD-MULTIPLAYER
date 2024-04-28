function showTab(tabName) {
    var loginForm = document.getElementById('loginForm');
    var registerForm = document.getElementById('registerForm');
    var loginTab = document.querySelector('.tab:nth-child(1)');
    var registerTab = document.querySelector('.tab:nth-child(2)');

    if (tabName === 'login') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        loginTab.classList.add('active');
        registerTab.classList.remove('active');
    } else if (tabName === 'register') {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        loginTab.classList.remove('active');
        registerTab.classList.add('active');
    }
}

// By default, show the login tab
showTab('login');