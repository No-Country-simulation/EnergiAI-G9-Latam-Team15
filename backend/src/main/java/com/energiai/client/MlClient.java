package com.energiai.client;

import com.energiai.dto.AnalisisRequestDTO;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class MlClient {

    private final RestClient restClient;

    public MlClient(RestClient.Builder builder, @Value("${ml.service.url:http://localhost:8000}") String mlServiceUrl) {
        this.restClient = builder.baseUrl(mlServiceUrl).build();
    }

    public record Prediccion(String categoria, Double probabilidad) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    private record PredictResponse(String categoria, Double probabilidad) {}

    public Prediccion predecir(AnalisisRequestDTO request) {
        PredictResponse response = restClient.post()
                .uri("/predict")
                .body(request)
                .retrieve()
                .body(PredictResponse.class);
        return new Prediccion(response.categoria(), response.probabilidad());
    }
}
