package com.energiai.service;

import com.energiai.client.MlClient;
import com.energiai.dto.AnalisisRequestDTO;
import com.energiai.dto.AnalisisResponseDTO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AnalisisEnergeticoService {

    private static final Logger log = LoggerFactory.getLogger(AnalisisEnergeticoService.class);
    private static final double TARIFA_REFERENCIA_KWH = 0.75;

    private final MlClient mlClient;

    public AnalisisEnergeticoService(MlClient mlClient) {
        this.mlClient = mlClient;
    }

    public AnalisisResponseDTO procesarAnalisis(AnalisisRequestDTO request) {
        double costoEstimado = request.consumoKwh() * TARIFA_REFERENCIA_KWH;

        List<String> recomendaciones = List.of(
                "Reducir el uso de equipos durante los horarios pico",
                "Evaluar equipos con alto consumo energético",
                "Distribuir las actividades de mayor consumo a lo largo del día"
        );

        String categoria;
        double probabilidad;
        try {
            MlClient.Prediccion prediccion = mlClient.predecir(request);
            categoria = prediccion.categoria();
            probabilidad = prediccion.probabilidad();
        } catch (Exception e) {
            log.warn("ml-service no disponible, usando respuesta mock de fallback: {}", e.getMessage());
            categoria = "Ineficiente";
            probabilidad = 0.81;
        }

        return new AnalisisResponseDTO(
                categoria,
                probabilidad,
                recomendaciones,
                costoEstimado
        );
    }
}