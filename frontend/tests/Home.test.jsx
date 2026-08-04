import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach } from "vitest";
import Home from "../src/pages/Home";
import * as apiService from "../src/services/apiService";

vi.mock("../src/services/apiService", () => ({
  analizarConsumo: vi.fn(),
}));

describe("Home", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it("renderiza el header con el logo y titulo", () => {
    render(<Home />);
    expect(screen.getByRole("heading", { name: "EnergiAI" })).toBeInTheDocument();
    expect(screen.getByText("Hackathon ONE")).toBeInTheDocument();
  });

  it("renderiza la seccion hero", () => {
    render(<Home />);
    expect(screen.getByRole("heading", { name: /Analisis Energetico/i })).toBeInTheDocument();
    expect(screen.getByText(/Ingrese los datos/i)).toBeInTheDocument();
  });

  it("renderiza el formulario", () => {
    render(<Home />);
    expect(screen.getByText("Datos de Consumo")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Analizar Consumo/i })).toBeInTheDocument();
  });

  it("no muestra resultados antes de analizar", () => {
    render(<Home />);
    expect(screen.queryByText("Clasificacion")).not.toBeInTheDocument();
    expect(screen.queryByText("Costo Mensual Estimado")).not.toBeInTheDocument();
    expect(screen.queryByText("Recomendaciones")).not.toBeInTheDocument();
  });

  it("muestra resultados despues de enviar el formulario", async () => {
    apiService.analizarConsumo.mockResolvedValue({
      categoria: "Eficiente",
      probabilidad: 0.85,
      costo_estimado_mensual: "112.50",
      recomendaciones: ["Mantenga sus buenas practicas", "Siga usando equipos eficientes"],
    });

    const user = userEvent.setup();
    render(<Home />);

    await user.type(screen.getByPlaceholderText("Ej: 250"), "150");
    await user.type(screen.getByPlaceholderText("Ej: 12"), "8");
    await user.selectOptions(screen.getByDisplayValue("Seleccione tipo de inmueble"), "Casa");
    await user.type(screen.getByPlaceholderText("Ej: 8"), "6");
    await user.click(screen.getByRole("button", { name: /Analizar Consumo/i }));

    expect(await screen.findByText("Clasificacion")).toBeInTheDocument();
    expect(screen.getAllByText("Eficiente").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("Costo Mensual Estimado")).toBeInTheDocument();
    expect(screen.getByText("Mantenga sus buenas practicas")).toBeInTheDocument();
    expect(screen.getByText("Siga usando equipos eficientes")).toBeInTheDocument();
  });

  it("muestra el boton de descargar PDF cuando hay resultados", async () => {
    apiService.analizarConsumo.mockResolvedValue({
      categoria: "Moderado",
      probabilidad: 0.7,
      costo_estimado_mensual: "225.00",
      recomendaciones: ["Reduzca su consumo"],
    });

    const user = userEvent.setup();
    render(<Home />);

    await user.type(screen.getByPlaceholderText("Ej: 250"), "300");
    await user.type(screen.getByPlaceholderText("Ej: 12"), "10");
    await user.selectOptions(screen.getByDisplayValue("Seleccione tipo de inmueble"), "Departamento");
    await user.type(screen.getByPlaceholderText("Ej: 8"), "8");
    await user.click(screen.getByRole("button", { name: /Analizar Consumo/i }));

    expect(await screen.findByText("Descargar PDF")).toBeInTheDocument();
  });

  it("muestra spinner durante la carga", async () => {
    let resolvePromise;
    apiService.analizarConsumo.mockImplementation(
      () => new Promise((resolve) => { resolvePromise = resolve; })
    );

    const user = userEvent.setup();
    render(<Home />);

    await user.type(screen.getByPlaceholderText("Ej: 250"), "200");
    await user.type(screen.getByPlaceholderText("Ej: 12"), "5");
    await user.selectOptions(screen.getByDisplayValue("Seleccione tipo de inmueble"), "Casa");
    await user.type(screen.getByPlaceholderText("Ej: 8"), "4");
    await user.click(screen.getByRole("button", { name: /Analizar Consumo/i }));

    expect(await screen.findByText("Analizando...")).toBeInTheDocument();

    resolvePromise({
      categoria: "Eficiente",
      probabilidad: 0.9,
      costo_estimado_mensual: "150.00",
      recomendaciones: [],
    });
  });

  it("muestra el footer con copyright", () => {
    render(<Home />);
    expect(screen.getByText(/EnergiAI ©/)).toBeInTheDocument();
    expect(screen.getByText(/Hackathon ONE — Alura \+ Oracle/)).toBeInTheDocument();
  });

  it("muestra boton nuevo analisis y historial vacio cuando no hay historial", () => {
    render(<Home />);
    expect(screen.queryByText("Nuevo analisis")).not.toBeInTheDocument();
  });

  it("muestra nuevo analisis y historial despues de analizar", async () => {
    apiService.analizarConsumo.mockResolvedValue({
      categoria: "Eficiente",
      probabilidad: 0.85,
      costo_estimado_mensual: "112.50",
      recomendaciones: ["Prueba"],
    });

    const user = userEvent.setup();
    render(<Home />);

    await user.type(screen.getByPlaceholderText("Ej: 250"), "150");
    await user.type(screen.getByPlaceholderText("Ej: 12"), "8");
    await user.selectOptions(screen.getByDisplayValue("Seleccione tipo de inmueble"), "Casa");
    await user.type(screen.getByPlaceholderText("Ej: 8"), "6");
    await user.click(screen.getByRole("button", { name: /Analizar Consumo/i }));

    expect(await screen.findByText("Nuevo analisis")).toBeInTheDocument();
    expect(screen.getByText("Historial de analisis")).toBeInTheDocument();
  });
});
