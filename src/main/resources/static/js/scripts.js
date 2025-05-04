function navigateTo(path) {
    window.location.href = "/" + path;
}

let stats = JSON.parse(data.answer);  // 문자열 JSON이라면 파싱
let msg = `타율: ${stats.타율}, 홈런: ${stats.홈런}`;