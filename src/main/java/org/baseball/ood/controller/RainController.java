package org.baseball.ood.controller;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.baseball.ood.domain.GameData;
import org.baseball.ood.domain.WeatherData;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Controller
public class RainController {

    private static final String JSON_PATH = "src/main/resources/static/data/rain-predict.json";

    @GetMapping("/rain-predict")
    public String showRainPredictPage(Model model) {
        ObjectMapper mapper = new ObjectMapper();
        List<GameData> games = new ArrayList<>();

        try {
            File file = new File(JSON_PATH);
            if (file.exists()) {
                games = mapper.readValue(file, new TypeReference<List<GameData>>() {});
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        model.addAttribute("games", games);
        return "rain-predict";
    }

    @GetMapping("/api/weather")
    @ResponseBody
    public List<WeatherData> getWeatherByTime(@RequestParam String time) {
        ObjectMapper mapper = new ObjectMapper();

        try {
            File file = new File(JSON_PATH);
            if (file.exists()) {
                List<GameData> games = mapper.readValue(file, new TypeReference<List<GameData>>() {});
                for (GameData game : games) {
                    String key = game.getDate() + game.getStart_time().replace(":", "") + game.getStadium();
                    if (key.equals(time)) {
                        return game.getWeather();
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return new ArrayList<>();
    }
}
