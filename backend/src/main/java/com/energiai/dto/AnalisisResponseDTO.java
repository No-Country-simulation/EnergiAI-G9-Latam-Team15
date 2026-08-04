package com.energiai.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public record AnalisisResponseDTO(
        String categoria,
        Double probabilidad,
        List<String> recomendaciones,

        @JsonProperty("costo_estimado_mensual")
        Double costoEstimadoMensual
) {}