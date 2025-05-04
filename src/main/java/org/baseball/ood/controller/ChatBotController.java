package org.baseball.ood.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class ChatBotController {

    @GetMapping("/chatbot")
    public String chatbotPage() {
        return "chatbot";
    }
}