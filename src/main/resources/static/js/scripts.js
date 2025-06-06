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

// script.js

document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.bg-slide');
    const sections = document.querySelectorAll('#content section');
    const titleEl = document.getElementById('text-title');
    const descEl = document.getElementById('text-desc');

    // 1) 초기 활성화 (첫 번째 요소)
    slides[0].classList.add('active');
    const firstSec = sections[0];
    titleEl.innerText = firstSec.querySelector('h1').innerText;
    descEl.innerText = firstSec.querySelector('p').innerText;

    // 2) IntersectionObserver 옵션 설정
    const options = {
        root: null,          // 뷰포트를 기준
        rootMargin: '0px',
        threshold: 0.5       // 섹션의 50% 이상 화면에 보여질 때 콜백
    };

    const observer = new IntersectionObserver(onIntersect, options);
    sections.forEach(sec => observer.observe(sec));

    function onIntersect(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const idx = parseInt(entry.target.getAttribute('data-index'), 10);

                // (1) 배경 이미지 전환
                slides.forEach((slide, i) => {
                    if (i === idx) {
                        slide.classList.add('active');
                    } else {
                        slide.classList.remove('active');
                    }
                });

                // (2) 텍스트 전환
                const newTitle = entry.target.querySelector('h1').innerText;
                const newDesc = entry.target.querySelector('p').innerText;

                // 잠시 기존 텍스트를 숨김
                titleEl.style.opacity = '0';
                descEl.style.opacity = '0';

                setTimeout(() => {
                    // 새로운 텍스트 삽입
                    titleEl.innerText = newTitle;
                    descEl.innerText = newDesc;

                    // 애니메이션 재실행
                    titleEl.style.animation = 'none';
                    descEl.style.animation = 'none';
                    requestAnimationFrame(() => {
                        titleEl.style.animation = '';
                        descEl.style.animation = '';
                    });
                }, 300); // 0.3초 뒤에 새 텍스트로 바꿔 페이드인
            }
        });
    }
});
