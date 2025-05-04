package org.baseball.ood.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.*;

@RestController
public class FastAPIController {

    @Autowired
    private RestTemplate restTemplate;

    private final String fastapiUrl = "http://localhost:8088/query";

    @PostMapping("/ask")
    public ResponseEntity<Map<String, String>> askFastAPI(@RequestBody Map<String, String> request) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, String>> entity = new HttpEntity<>(request, headers);

            ResponseEntity<Map> response = restTemplate.postForEntity(fastapiUrl, entity, Map.class);

            if (response.getBody() == null || !response.getBody().containsKey("answer")) {
                Map<String, String> error = new HashMap<>();
                error.put("answer", "FastAPI 응답 오류");
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
            }

            String answer = (String) response.getBody().get("answer");
            Map<String, String> result = new HashMap<>();
            result.put("answer", answer);  // JSON 형식으로 응답
            return ResponseEntity.ok(result);

        } catch (Exception e) {
            e.printStackTrace();
            Map<String, String> error = new HashMap<>();
            error.put("answer", "서버 오류: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
}