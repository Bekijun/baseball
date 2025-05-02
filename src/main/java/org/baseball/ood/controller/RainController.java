package org.baseball.ood.controller;

import org.baseball.ood.domain.GameData;
import org.baseball.ood.domain.WeatherData;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@Controller
public class RainController {

    @GetMapping("/rain-predict")
    public String showRainPredictPage(Model model) {
        List<GameData> games = new ArrayList<>();

        for (int i = 0; i < 5; i++) {
            GameData game = new GameData();
            game.setTime("15:00");
            game.setLocation("서울");
            game.setHomeTeamName("두산 베어스");
            game.setAwayTeamName("LG 트윈스");
            game.setHomeTeamLogo("/images/doosan.png");
            game.setAwayTeamLogo("/images/lg.png");
            game.setRainProbability(80);
            game.setGameTime("2025050218" + i);

            games.add(game);
        }

        model.addAttribute("games", games);
        return "rain-predict";
    }

    @GetMapping("/api/weather")
    @ResponseBody
    public List<WeatherData> getWeatherByTime(@RequestParam String time) {
        List<WeatherData> list = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            WeatherData data = new WeatherData();
            data.setTime((12 + i) + ":00");
            data.setIconUrl("/images/cloud.png");
            data.setTemperature((6 - i) + "°C");
            data.setPrecipitation("0." + i + "mm");
            list.add(data);
        }
        return list;
    }
}
