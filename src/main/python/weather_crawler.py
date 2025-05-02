from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import json

def fetch_naver_weather_filtered():
    game_start = datetime.strptime("2025050218", "%Y%m%d%H")

    valid_datetimes = [(game_start + timedelta(hours=i)).strftime("%Y%m%d%H") for i in range(-3, 3)]

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        url = "https://weather.naver.com/today/09140104"
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr.thead._cnTimeTable"))
        )

        th_elements = driver.find_elements(By.CSS_SELECTOR, "tr.thead._cnTimeTable > th._cnItemTime")

        weather_data = []

        for th in th_elements:
            ymdt = th.get_attribute("data-ymdt")
            if ymdt not in valid_datetimes:
                continue

            time_text = th.find_element(By.CLASS_NAME, "time").text
            temperature = th.get_attribute("data-tmpr")
            weather_text = th.get_attribute("data-wetr-txt")
            icon_class = th.find_element(By.CLASS_NAME, "ico").get_attribute("class")

            weather_data.append({
                "time": time_text,
                "temperature": temperature,
                "weather": weather_text,
                "datetime": ymdt,
                "icon_class": icon_class
            })

        # JSON 저장
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f" 에러 발생: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_naver_weather_filtered()
