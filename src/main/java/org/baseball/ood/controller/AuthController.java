package org.baseball.ood.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class AuthController {

    @GetMapping("/index")
    public String index() {
        return "index";
    }

    @GetMapping("/home")
    public String homePage() {
        return "home";
    }

    @GetMapping("/signup")
    public String signup() {
        return "signup";
    }

    @PostMapping("/home")
    public String home(@RequestParam("username") String username,
                        @RequestParam("password") String password,
                        Model model) {

        if ("admin".equals(username) && "1234".equals(password)) { // 디비랑 연결 안 한 거라서 나중에 디비 연결한 걸로 고쳐야 됨
            model.addAttribute("username", username);
            return "home";
        } else {
            model.addAttribute("error", "아이디 또는 비밀번호가 틀렸습니다.");
            return "index";
        }
    }
}