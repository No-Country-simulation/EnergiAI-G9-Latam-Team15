package com.energiai.controller;

import com.energiai.dto.AnalisisRequestDTO;
import com.energiai.dto.AnalisisResponseDTO;
import com.energiai.service.AnalisisEnergeticoService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1")
@CrossOrigin(origins = "*")
public class AnalisisEnergeticoController {

    private final AnalisisEnergeticoService analisisService;

    public AnalisisEnergeticoController(AnalisisEnergeticoService analisisService) {
        this.analisisService = analisisService;
    }

    @GetMapping("/health")
    public ResponseEntity<String> probarEndpoint() {
        return ResponseEntity.ok("OK");
    }

    @PostMapping("/analisis-energetico")
    public ResponseEntity<AnalisisResponseDTO> calcularAnalisis(@Valid @RequestBody AnalisisRequestDTO request) {
        AnalisisResponseDTO respuesta = analisisService.procesarAnalisis(request);
        return ResponseEntity.ok(respuesta);
    }
}