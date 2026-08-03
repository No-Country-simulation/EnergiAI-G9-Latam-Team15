package com.energiai.service;

import com.energiai.dto.AnalisisRequestDTO;
import com.energiai.dto.AnalisisResponseDTO;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AnalisisEnergeticoService {

    private static final double TARIFA_REFERENCIA_KWH = 0.75;

    public AnalisisResponseDTO procesarAnalisis(AnalisisRequestDTO request) {
        double costoEstimado = request.consumoKwh() * TARIFA_REFERENCIA_KWH;

        List<String> recomendaciones = List.of(
                "Reducir el uso de equipos durante los horarios pico",
                "Evaluar equipos con alto consumo energético",
                "Distribuir las actividades de mayor consumo a lo largo del día"
        );

        return new AnalisisResponseDTO(
                "Ineficiente",
                0.81,
                recomendaciones,
                costoEstimado
        );
    }
}