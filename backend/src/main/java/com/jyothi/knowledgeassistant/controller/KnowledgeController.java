package com.jyothi.knowledgeassistant.controller;

import com.jyothi.knowledgeassistant.dto.QueryRequest;
import com.jyothi.knowledgeassistant.dto.QueryResponse;
import com.jyothi.knowledgeassistant.service.AiServiceClient;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:4200")
public class KnowledgeController {

    private final AiServiceClient aiServiceClient;

    public KnowledgeController(AiServiceClient aiServiceClient) {
        this.aiServiceClient = aiServiceClient;
    }

    @GetMapping("/health")
    public String health() {
        return "Backend is running";
    }

    @PostMapping("/query")
    public QueryResponse query(
            @Valid @RequestBody QueryRequest request
    ) {
        return aiServiceClient.askQuestion(request);
    }
}