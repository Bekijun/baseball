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

    private final String FASTAPI_URL = "http://localhost:8088/nl_query";

    @PostMapping("/ask-nl")
    public ResponseEntity<Map<String, String>> askFastAPINatural(@RequestBody Map<String, String> payload) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, String>> request = new HttpEntity<>(payload, headers);

            ResponseEntity<Map> response = restTemplate.postForEntity(FASTAPI_URL, request, Map.class);

            if (response.getBody() == null || !response.getBody().containsKey("answer")) {
                Map<String, String> error = new HashMap<>();
                error.put("answer", "FastAPI 응답 오류: 데이터 없음");
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
            }

            Map<String, String> result = new HashMap<>();
            result.put("answer", (String) response.getBody().get("answer"));
            return ResponseEntity.ok(result);

        } catch (Exception e) {
            e.printStackTrace();
            Map<String, String> error = new HashMap<>();
            error.put("answer", "서버 오류: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
}