package com.jyothi.knowledgeassistant.dto;

import jakarta.validation.constraints.NotBlank;

public record QueryRequest(
        @NotBlank(message = "Query cannot be empty")
        String query
) {
}