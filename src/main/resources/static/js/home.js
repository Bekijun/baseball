function navigateToPage() {
    const clubSelect = document.getElementById("clubSelect").value;

    if (clubSelect) {
        window.location.href = `/team?name=${clubSelect}`;
    }
}

function navigateToLogin() {
    window.location.href = "/login";
}