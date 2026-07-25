import { describe, it, expect, vi, beforeEach } from "vitest";
import { analizarConsumo } from "../src/services/apiService";

const mockFetch = vi.fn();
global.fetch = mockFetch;

describe("apiService", () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });

  const datosBase = {
    consumo_kwh: 250,
    uso_horario_pico: false,
    cantidad_equipos: 10,
    tipo_inmueble: "Casa",
    horas_alto_consumo: 6,
  };

  it("retorna datos del backend cuando responde OK", async () => {
    const mockResponse = {
      categoria: "Moderado",
      probabilidad: 0.8,
      costo_estimado_mensual: "187.50",
      recomendaciones: ["Reduzca el consumo"],
    };
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });

    const result = await analizarConsumo(datosBase);
    expect(result).toEqual(mockResponse);
    expect(mockFetch).toHaveBeenCalledWith(
      "http://localhost:8080/analisis-energetico",
      expect.objectContaining({ method: "POST" })
    );
  });

  it("usa mock cuando el backend falla", async () => {
    mockFetch.mockRejectedValue(new Error("Network error"));

    const result = await analizarConsumo(datosBase);
    expect(result).toHaveProperty("categoria");
    expect(result).toHaveProperty("recomendaciones");
  });

  it("usa mock cuando la respuesta no es OK", async () => {
    mockFetch.mockResolvedValue({ ok: false });

    const result = await analizarConsumo(datosBase);
    expect(result).toHaveProperty("categoria");
  });

  it("mock clasifica como Ineficiente para consumo > 300", async () => {
    mockFetch.mockRejectedValue(new Error("down"));

    const result = await analizarConsumo({ ...datosBase, consumo_kwh: 350 });
    expect(result.categoria).toBe("Ineficiente");
  });

  it("mock clasifica como Moderado para consumo entre 150 y 300", async () => {
    mockFetch.mockRejectedValue(new Error("down"));

    const result = await analizarConsumo({ ...datosBase, consumo_kwh: 200 });
    expect(result.categoria).toBe("Moderado");
  });

  it("mock clasifica como Eficiente para consumo < 150", async () => {
    mockFetch.mockRejectedValue(new Error("down"));

    const result = await analizarConsumo({ ...datosBase, consumo_kwh: 100 });
    expect(result.categoria).toBe("Eficiente");
  });

  it("mock calcula el costo correctamente", async () => {
    mockFetch.mockRejectedValue(new Error("down"));

    const result = await analizarConsumo({ ...datosBase, consumo_kwh: 200 });
    expect(result.costo_estimado_mensual).toBe("150.00");
  });

  it("mock genera recomendaciones de horario pico", async () => {
    mockFetch.mockRejectedValue(new Error("down"));

    const result = await analizarConsumo({ ...datosBase, uso_horario_pico: true });
    const picoRecs = result.recomendaciones.filter((r) => r.includes("pico"));
    expect(picoRecs.length).toBeGreaterThan(0);
  });
});
