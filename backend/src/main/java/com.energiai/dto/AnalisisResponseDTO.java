package com.energiai.dto;

public record AnalisisEnergeticoResponseDTO(
        Double consumoKwh,
        Double estimacionCosto,
        Double prediccionMlKwh,
        String recomendacion,
        String estado,
        String categoria
) {}