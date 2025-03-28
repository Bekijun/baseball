package org.baseball.ood.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class HomeController {

    @GetMapping("/team")
    public String team(@RequestParam("name") String teamName) {
        return teamName;
    }
}