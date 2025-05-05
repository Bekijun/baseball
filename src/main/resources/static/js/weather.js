document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".game-card");

    fetch("/data/rain-percent.json")
        .then(res => res.json())
        .then(data => {
            const probMap = {};
            data.forEach(item => {
                const key = `${item.date}-${item.home}-${item.away}`;
                probMap[key] = item.probability;
            });

            cards.forEach(card => {
                const gameTime = card.getAttribute("data-time");
                const gameDate = card.getAttribute("data-date");
                const home = card.getAttribute("data-home");
                const away = card.getAttribute("data-away");
                const key = `${gameDate}-${home}-${away}`;
                const probability = probMap[key];

                const probDiv = card.querySelector(".rain-probability");
                if (probDiv) {
                    probDiv.textContent = (probability !== undefined && probability >= 0)
                        ? `${probability}%`
                        : `예측불가`;
                }

                const weatherDiv = card.querySelector(".weather-info");
                fetch(`/api/weather?time=${gameTime}&t=${Date.now()}`)
                    .then(response => response.json())
                    .then(data => {
                        if (Array.isArray(data)) {
                            weatherDiv.innerHTML = data.map(item => `
                                <div class="weather-cell">
                                    <span>${item.datetime.substring(8)}시</span>
                                    <img src="/images/weather/${item.icon || 'unknown'}.svg"
                                         alt="${item.icon}"
                                         onerror="this.onerror=null;this.src='/images/weather/unknown.svg';">
                                    <span>${item.temp}℃</span>
                                    <span>${item.rain}mm</span>
                                </div>
                            `).join('');
                        } else {
                            weatherDiv.innerHTML = "<p>날씨 정보 없음</p>";
                        }
                    })
                    .catch(() => {
                        weatherDiv.innerHTML = "<p>날씨 불러오기 실패</p>";
                    });
            });
        })
        .catch(() => {
            console.error("확률 데이터 요청 실패");
        });
});
