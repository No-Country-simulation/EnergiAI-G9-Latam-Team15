package com.energiai.client;

import com.energiai.dto.AnalisisRequestDTO;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class MlClient {

    private final RestClient restClient;

    public MlClient(RestClient.Builder builder, @Value("${ml.service.url:http://localhost:8000}") String mlServiceUrl) {
        this.restClient = builder.baseUrl(mlServiceUrl).build();
    }

    public record Prediccion(String categoria, Double probabilidad, Double scoreEficiencia) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    private record PredictResponse(
            String categoria,
            Double probabilidad,
            @JsonProperty("score_eficiencia") Double scoreEficiencia
    ) {}

    public Prediccion predecir(AnalisisRequestDTO request) {
        PredictResponse response = restClient.post()
                .uri("/predict")
                .body(request)
                .retrieve()
                .body(PredictResponse.class);
        return new Prediccion(response.categoria(), response.probabilidad(), response.scoreEficiencia());
    }
}
