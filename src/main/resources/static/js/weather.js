document.addEventListener("DOMContentLoaded", function () {
    const gameTime = window.gameTime || '2025050218';  // 기본값

    fetch(`/api/weather?time=${gameTime}`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("weather-container");
            if (container && data && Array.isArray(data)) {
                container.innerHTML = data.map(item => `
                    <div class="weather-item">
                        <p>${item.time}시</p>
                        <p>${item.temperature}°C</p>
                        <p>강수확률: ${item.rainPercent}%</p>
                        <p>강수량: ${item.rainAmount}mm</p>
                    </div>
                `).join('');
            }
        })
        .catch(error => console.error("날씨 데이터 오류:", error));
});
