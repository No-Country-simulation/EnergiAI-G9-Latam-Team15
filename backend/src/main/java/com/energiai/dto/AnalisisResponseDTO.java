package com.energiai.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public record AnalisisResponseDTO(
        String categoria,
        Double probabilidad,
        List<String> recomendaciones,

        @JsonProperty("costo_estimado_mensual")
        Double costoEstimadoMensual,

        @JsonProperty("ahorro_potencial_conservador")
        Double ahorroConservador,

        @JsonProperty("ahorro_potencial_medio")
        Double ahorroMedio,

        @JsonProperty("ahorro_potencial_alto")
        Double ahorroAlto,

        @JsonProperty("score_eficiencia")
        Double scoreEficiencia,

        @JsonProperty("prioridad")
        Double prioridad
) {}