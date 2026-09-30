package com.jyothi.knowledgeassistant.service;

import com.jyothi.knowledgeassistant.dto.QueryRequest;
import com.jyothi.knowledgeassistant.dto.QueryResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.Map;

@Service
public class AiServiceClient {

    private final RestClient restClient;

    public AiServiceClient(
            @Value("${ai.service.url}") String aiServiceUrl
    ) {
        this.restClient = RestClient.builder()
                .baseUrl(aiServiceUrl)
                .build();
    }

    public QueryResponse askQuestion(QueryRequest request) {

        Map<String, String> requestBody = Map.of(
                "query", request.query()
        );

        return restClient
                .post()
                .uri("/query")
                .contentType(MediaType.APPLICATION_JSON)
                .body(requestBody)
                .retrieve()
                .body(QueryResponse.class);
    }
}