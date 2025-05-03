package org.baseball.ood.domain;

public class WeatherData {
    private String datetime;   // 예: 2025050316
    private String icon;       // 예: "맑음", "흐림"
    private String temp;       // 예: "14" (섭씨 온도)
    private String rain;       // 예: "0" 또는 "6.3"

    // ✅ Getter & Setter

    public String getDatetime() {
        return datetime;
    }

    public void setDatetime(String datetime) {
        this.datetime = datetime;
    }

    public String getIcon() {
        return icon;
    }

    public void setIcon(String icon) {
        this.icon = icon;
    }

    public String getTemp() {
        return temp;
    }

    public void setTemp(String temp) {
        this.temp = temp;
    }

    public String getRain() {
        return rain;
    }

    public void setRain(String rain) {
        this.rain = rain;
    }

    // ✅ 유틸리티 메서드: 시간만 뽑기 (예: "16시")
    public String getHour() {
        if (datetime != null && datetime.length() >= 10) {
            return datetime.substring(8) + "시";
        } else {
            return "";
        }
    }
}
