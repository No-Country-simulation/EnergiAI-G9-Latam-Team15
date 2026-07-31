package com.energiai.AnalisisEnergeticoController;

import com.energiai.dto.AnalisisEnergeticoRequestDTO;
import com.energiai.dto.AnalisisEnergeticoResponseDTO;
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

    @PostMapping("/analisis-energetico")
    public ResponseEntity<AnalisisEnergeticoResponseDTO> analizarConsumo(
            @Valid @RequestBody AnalisisEnergeticoRequestDTO request) {

        AnalisisEnergeticoResponseDTO respuesta = analisisService.procesarAnalisis(request);
        return ResponseEntity.ok(respuesta);
    }

    @GetMapping("/health")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("EnergiAI Backend corriendo correctamente");
    }
}