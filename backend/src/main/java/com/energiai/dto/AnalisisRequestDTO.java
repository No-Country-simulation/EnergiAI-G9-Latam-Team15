package com.energiai.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;

public record AnalisisRequestDTO(

        @NotNull(message = "El consumo en kWh es obligatorio")
        @Positive(message = "El consumo debe ser un valor positivo")
        @JsonProperty("consumo_kwh")
        Double consumoKwh,

        @NotNull(message = "Indicar si usa horario pico, es obligatorio")
        @JsonProperty("uso_horario_pico")
        Boolean usoHorarioPico,

        @NotNull(message = "La cantidad de equipos es obligatoria")
        @Positive(message = "La cantidad de equipos debe ser mayor a cero")
        @JsonProperty("cantidad_equipos")
        Integer cantidadEquipos,

        @NotNull(message = "El tipo de inmueble es obligatorio")
        @JsonProperty("tipo_inmueble")
        String tipoInmueble,

        @NotNull(message = "Las horas de alto consumo son obligatorias")
        @PositiveOrZero(message = "Las horas no pueden ser negativas")
        @JsonProperty("horas_alto_consumo")
        Integer horasAltoConsumo
) {}