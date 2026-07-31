package com.energiai.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public record AnalisisEnergeticoRequestDTO(
        @NotNull(message = "El valor de consumo no puede ser nulo")
        @Positive(message = "El consumo debe ser un numero positivo")
        Double consumoKwh,

        Boolean usoHorarioPico,

        Integer cantidadEquipos,

        String tipoInmueble,

        Integer horasAltoConsumo,

        String periodo
) {}