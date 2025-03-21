function navigateToSignup() {
    window.location.href = "/signup";
}

function navigateToLogin() {
    window.location.href = "/";
}

function signup() {
    const username = document.getElementById("signup-username").value;
    const password = document.getElementById("signup-password").value;
    const confirmPassword = document.getElementById("signup-password-confirm").value;

    if (!username || !password || !confirmPassword) {
        alert("모든 필드를 입력해 주세요.");
        return;
    }

    if (password !== confirmPassword) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
    }

    alert("회원가입이 완료되었습니다!");
    navigateToLogin();
}
