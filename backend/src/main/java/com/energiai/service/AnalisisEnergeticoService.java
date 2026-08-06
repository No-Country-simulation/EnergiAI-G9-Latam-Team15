package com.energiai.service;

import com.energiai.client.MlClient;
import com.energiai.dto.AnalisisRequestDTO;
import com.energiai.dto.AnalisisResponseDTO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
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

        List<String> recomendaciones = generarRecomendaciones(request, categoria);

        double ahorroConservador = round2(costoEstimado * 0.03);
        double ahorroMedio = round2(costoEstimado * 0.05);
        double ahorroAlto = round2(costoEstimado * 0.08);

        return new AnalisisResponseDTO(
                categoria,
                probabilidad,
                recomendaciones,
                costoEstimado,
                ahorroConservador,
                ahorroMedio,
                ahorroAlto
        );
    }

    private double round2(double valor) {
        return Math.round(valor * 100.0) / 100.0;
    }

    private List<String> generarRecomendaciones(AnalisisRequestDTO request, String categoria) {
        List<String> recomendaciones = new ArrayList<>();
        boolean pico = request.usoHorarioPico();
        int horasAlto = request.horasAltoConsumo();
        double consumo = request.consumoKwh();
        String tipo = request.tipoInmueble();

        // Regla 1: Ineficiente + horario pico
        if ("Ineficiente".equals(categoria) && pico) {
            recomendaciones.add("Tu consumo es elevado y se concentra en el horario de mayor precio de la tarifa. Para reducir tu factura, evita usar electrodomesticos de alto consumo (lavadoras, secadoras, hornos electricos, carga de vehiculos) en horas pico (18:00 a 22:00). Programa el uso de estos equipos mas tarde o mas temprano, cuando la energia es mas barata.");
        }

        // Regla 2: horas de alto consumo diario (umbral ajustado a escala diaria, ver nota en commit)
        if (horasAlto > 6 && !"Eficiente".equals(categoria)) {
            recomendaciones.add("Tu perfil muestra varias horas de alto consumo durante el dia. Revisa si tienes equipos que permanecen encendidos mas tiempo del necesario, apaga equipos en areas desocupadas y evita que esten encendidos todo el dia.");
        }

        // Regla 3: consumo mensual alto (umbral: percentil 75 real del dataset = 231 kWh, misma escala que el request)
        if (consumo > 231 && !"Eficiente".equals(categoria)) {
            recomendaciones.add("Tu consumo mensual esta por encima de la mayoria de los usuarios. Identifica los equipos que mas consumen (hornos, secadoras, calentadores, refrigeradores) y aprovecha los modos \"Eco\" o de ahorro. Evita el uso simultaneo de varios equipos: incluso pequenos cambios tienen un gran impacto en tu consumo total.");
        }

        // Regla 4: Moderado + horario pico
        if ("Moderado".equals(categoria) && pico) {
            recomendaciones.add("Tu consumo en general es moderado, pero sigues utilizando parte de la energia en horas pico. Intenta mover tareas (lavar ropa, planchar, cargar dispositivos) fuera del horario de 18:00 a 22:00, o usa el modo diferido de tus equipos si lo tienen.");
        }

        // Regla 5: Eficiente + horario pico
        if ("Eficiente".equals(categoria) && pico) {
            recomendaciones.add("Mantienes un perfil de consumo eficiente, lo cual es genial. Si quieres ahorrar aun mas, desplaza algunas tareas a horario temprano o nocturno y apaga por completo los equipos en modo standby cuando no los uses.");
        }

        // Regla 6: diferenciacion por tipo de inmueble (siempre aplica)
        if ("Pequeño establecimiento".equals(tipo)) {
            recomendaciones.add("Como pequeno establecimiento, presta especial atencion al horario comercial pico (16:00 a 20:00), la iluminacion de vitrinas y letreros, los equipos de refrigeracion/exhibicion, y planifica tu produccion o servicio para evitar concentrar actividad en las horas mas costosas.");
        } else {
            recomendaciones.add("En tu hogar, enfocate en la iluminacion, el uso eficiente del refrigerador y la lavadora, la calefaccion, y apagar computadoras y electrodomesticos cuando no esten en uso.");
        }

        if (recomendaciones.isEmpty()) {
            recomendaciones.add("Tu consumo energetico es eficiente. Sigue manteniendo tus buenos habitos de uso.");
        }
        return recomendaciones;
    }
}