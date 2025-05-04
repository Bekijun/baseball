package org.baseball.ood.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.stereotype.Controller;

@Controller
public class HomeController {

    @GetMapping("/index")
    public String index() {
        return "index";
    }
}