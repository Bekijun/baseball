function navigateTo(path) {
    window.location.href = "/" + path;
}

document.getElementById('sendBtn').addEventListener('click', askBot);
document.getElementById('keyword').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') askBot();
});

function appendMessage(text, sender) {
    const div = document.createElement('div');
    div.className = 'message ' + sender;
    div.innerText = text;
    document.getElementById('chatWindow').appendChild(div);
    document.getElementById('chatWindow').scrollTop = document.getElementById('chatWindow').scrollHeight;
}

function askBot() {
    const input = document.getElementById("keyword").value.trim();
    if (!input) return;

    appendMessage(input, 'user');
    document.getElementById("keyword").value = '';

    fetch("/ask-nl", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input })
    })
        .then(res => res.json())
        .then(data => {
            const answer = data.answer || '죄송해요, 응답을 받을 수 없었어요.';
            appendMessage(answer, 'bot');
        })
        .catch(err => {
            appendMessage("서버 오류: " + err, 'bot');
        });
}