import { renderHook, act } from "@testing-library/react";
import { describe, it, expect, beforeEach } from "vitest";
import useHistorial from "../src/hooks/useHistorial";

const mockResultado = {
  categoria: "Eficiente",
  probabilidad: 0.85,
  costo_estimado_mensual: "112.50",
  recomendaciones: ["Mantenga sus buenas practicas"],
};

const mockDatos = {
  consumo_kwh: 150,
  uso_horario_pico: false,
  cantidad_equipos: 8,
  tipo_inmueble: "Casa",
  horas_alto_consumo: 4,
};

describe("useHistorial", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("inicia con historial vacio", () => {
    const { result } = renderHook(() => useHistorial());
    expect(result.current.historial).toEqual([]);
  });

  it("agrega un analisis al historial", () => {
    const { result } = renderHook(() => useHistorial());

    act(() => {
      result.current.agregarAnalisis(mockDatos, mockResultado);
    });

    expect(result.current.historial.length).toBe(1);
    expect(result.current.historial[0].resultado.categoria).toBe("Eficiente");
    expect(result.current.historial[0].datos.consumo_kwh).toBe(150);
  });

  it("el analisis nuevo va primero", () => {
    const { result } = renderHook(() => useHistorial());

    act(() => {
      result.current.agregarAnalisis(mockDatos, mockResultado);
    });
    act(() => {
      result.current.agregarAnalisis(mockDatos, { ...mockResultado, categoria: "Moderado" });
    });

    expect(result.current.historial.length).toBe(2);
    expect(result.current.historial[0].resultado.categoria).toBe("Moderado");
    expect(result.current.historial[1].resultado.categoria).toBe("Eficiente");
  });

  it("persiste en localStorage", () => {
    const { result } = renderHook(() => useHistorial());

    act(() => {
      result.current.agregarAnalisis(mockDatos, mockResultado);
    });

    const stored = JSON.parse(localStorage.getItem("energiai_historial"));
    expect(stored.length).toBe(1);
    expect(stored[0].resultado.categoria).toBe("Eficiente");
  });

  it("carga historial existente de localStorage", () => {
    const entrada = {
      id: 1,
      fecha: new Date().toISOString(),
      datos: mockDatos,
      resultado: mockResultado,
    };
    localStorage.setItem("energiai_historial", JSON.stringify([entrada]));

    const { result } = renderHook(() => useHistorial());
    expect(result.current.historial.length).toBe(1);
  });

  it("limpia el historial", () => {
    const { result } = renderHook(() => useHistorial());

    act(() => {
      result.current.agregarAnalisis(mockDatos, mockResultado);
    });
    expect(result.current.historial.length).toBe(1);

    act(() => {
      result.current.limpiarHistorial();
    });
    expect(result.current.historial.length).toBe(0);
    expect(localStorage.getItem("energiai_historial")).toBeNull();
  });

  it("limita a 20 entradas", () => {
    const { result } = renderHook(() => useHistorial());

    for (let i = 0; i < 25; i++) {
      act(() => {
        result.current.agregarAnalisis(mockDatos, mockResultado);
      });
    }

    expect(result.current.historial.length).toBe(20);
  });
});
