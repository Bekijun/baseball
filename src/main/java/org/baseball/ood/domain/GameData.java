package org.baseball.ood.domain;

import java.util.List;

public class GameData {
    private String date;
    private String away;
    private String home;
    private String stadium;
    private String start_time;
    private List<WeatherData> weather;

    // 로고 경로 (컨트롤러에서 세팅)
    private String homeTeamLogo;
    private String awayTeamLogo;

    // ✅ Getter & Setter

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getAway() {
        return away;
    }

    public void setAway(String away) {
        this.away = away;
    }

    public String getHome() {
        return home;
    }

    public void setHome(String home) {
        this.home = home;
    }

    public String getStadium() {
        return stadium;
    }

    public void setStadium(String stadium) {
        this.stadium = stadium;
    }

    public String getStart_time() {
        return start_time;
    }

    public void setStart_time(String start_time) {
        this.start_time = start_time;
    }

    public List<WeatherData> getWeather() {
        return weather;
    }

    public void setWeather(List<WeatherData> weather) {
        this.weather = weather;
    }

    public String getHomeTeamLogo() {
        return homeTeamLogo;
    }

    public void setHomeTeamLogo(String homeTeamLogo) {
        this.homeTeamLogo = homeTeamLogo;
    }

    public String getAwayTeamLogo() {
        return awayTeamLogo;
    }

    public void setAwayTeamLogo(String awayTeamLogo) {
        this.awayTeamLogo = awayTeamLogo;
    }

    // ✅ 가공된 필드 (날짜 + 시작 시간 → 게임 식별용 키)
    public String getGameTime() {
        return date + start_time.replace(":", "");
    }
}
