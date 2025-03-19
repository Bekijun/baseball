package org.baseball.ood.controller;


import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
@Controller
public class HomeController {

    @GetMapping("home")
    public String home(Model model) {
        model.addAttribute("data", "롯데");
        return "/home"; //home.html 실행
    }
 }
