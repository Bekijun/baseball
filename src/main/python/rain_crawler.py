from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import json
import time
import os
import re

STADIUM_TO_CODE = {
    "잠실": "09710720", "고척": "09530106", "수원": "02111135",
    "대전(신)": "07140111", "광주": "05170105", "대구": "06260123",
    "창원": "03127105", "사직": "08260109", "문학": "11177107", "울산": "10140102"
}

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JSON_PATH = "src/main/resources/static/data/rain-predict.json"
OUTPUT_JSON = os.path.join(BASE_DIR, "resources", "static", "data", "rain-predict.json")


def extract_hour(game_time):
    numbers = re.findall(r'\d+', game_time)
    return int(numbers[0]) if numbers else 18


def get_game_schedule(date_str):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        url = f"https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={date_str}&leagueId=1&seriesId=0&teamCode="
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "today-game")))
        time.sleep(2)

        game_elements = driver.find_elements(By.CSS_SELECTOR, ".today-game .game-cont")
        games = []
        for game in game_elements:
            try:
                away = game.get_attribute("away_nm")
                home = game.get_attribute("home_nm")
                stadium = game.get_attribute("s_nm")
                time_str = game.find_element(By.CSS_SELECTOR, ".top ul li:nth-child(3)").text
                games.append({"date": date_str, "away": away, "home": home, "stadium": stadium, "start_time": time_str})
            except:
                continue
        return games
    except:
        return []
    finally:
        driver.quit()


def get_weather_data(driver, stadium, date_str, game_time):
    code = STADIUM_TO_CODE.get(stadium)
    if not code:
        return []

    try:
        hour = extract_hour(game_time)
    except:
        return []

    hours = [(datetime.strptime(date_str, "%Y%m%d") + timedelta(hours=hour+i)).strftime("%Y%m%d%H") for i in range(-3, 3)]

    try:
        url = f"https://weather.naver.com/today/{code}?cpName=ACCUWEATHER"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr._cnTmpr")))
        time.sleep(2)

        result = []
        for h in hours:
            try:
                icon_elem = driver.find_element(By.CSS_SELECTOR, f"th[data-ymdt='{h}']")
                temp_elem = driver.find_element(By.CSS_SELECTOR, f"tr._cnTmpr td[data-ymdt='{h}']")
                rain_elem = driver.find_element(By.CSS_SELECTOR, f"tr._cnRainAmt td[data-ymdt='{h}']")
                result.append({
                    "datetime": h,
                    "icon": icon_elem.get_attribute("data-wetr-txt"),
                    "temp": temp_elem.text.replace("°", ""),
                    "rain": rain_elem.text.replace("mm", "")
                })
            except:
                continue
        return result
    except:
        return []


def load_existing_data():
    if not os.path.exists(JSON_PATH):
        return []
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_expected_hours(date_str, game_time):
    base_time = datetime.strptime(date_str + game_time, "%Y%m%d%H:%M")
    return [(base_time + timedelta(hours=i)).strftime("%Y%m%d%H") for i in range(-3, 3)]


def merge_weather_data(old_data, new_data, expected_hours):
    old_map = {w["datetime"]: w for w in old_data}
    new_map = {w["datetime"]: w for w in new_data}
    merged = []

    for h in expected_hours:
        if h in new_map:
            merged.append(new_map[h])
        elif h in old_map:
            merged.append(old_map[h])
        else:
            merged.append({"datetime": h, "icon": "정보없음", "temp": "-", "rain": "-"})
    return merged


def merge_game_data(old_games, new_games):
    merged = []
    for game in new_games:
        matched_old = next((g for g in old_games if g["date"] == game["date"]
                            and g["home"] == game["home"] and g["away"] == game["away"]), {})
        old_weather = matched_old.get("weather", [])
        expected_hours = generate_expected_hours(game["date"], game["start_time"])
        game["weather"] = merge_weather_data(old_weather, game.get("weather", []), expected_hours)
        merged.append(game)
    return merged


def collect_all():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)

    today_games = get_game_schedule(today.strftime("%Y%m%d"))
    tomorrow_games = get_game_schedule(tomorrow.strftime("%Y%m%d"))

    new_games = today_games + tomorrow_games

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        for game in new_games:
            game["weather"] = get_weather_data(driver, game["stadium"], game["date"], game["start_time"])
    finally:
        driver.quit()

    existing_games = load_existing_data()
    final_merged = merge_game_data(existing_games, new_games)

    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(final_merged, f, ensure_ascii=False, indent=2)

collect_all()
