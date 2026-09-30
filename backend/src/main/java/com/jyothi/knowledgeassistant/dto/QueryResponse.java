package com.jyothi.knowledgeassistant.dto;

import java.util.List;

public record QueryResponse(
        String answer,
        List<Source> sources
) {
    public record Source(
            String source,
            String page
    ) {
    }
}