import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import GraficoConsumo from "../src/components/GraficoConsumo";

const mockHistorialLargo = [
  { id: 1, fecha: "2026-07-20T10:00:00Z", resultado: { categoria: "Eficiente", probabilidad: 0.9, costo_estimado_mensual: "112.50" } },
  { id: 2, fecha: "2026-07-22T10:00:00Z", resultado: { categoria: "Moderado", probabilidad: 0.7, costo_estimado_mensual: "225.00" } },
  { id: 3, fecha: "2026-07-25T10:00:00Z", resultado: { categoria: "Eficiente", probabilidad: 0.85, costo_estimado_mensual: "150.00" } },
];

describe("GraficoConsumo", () => {
  it("renderiza null si hay menos de 2 analisis", () => {
    const { container } = render(
      <GraficoConsumo historial={[mockHistorialLargo[0]]} />
    );
    expect(container.innerHTML).toBe("");
  });

  it("renderiza null si historial esta vacio", () => {
    const { container } = render(<GraficoConsumo historial={[]} />);
    expect(container.innerHTML).toBe("");
  });

  it("muestra el titulo y los graficos con 2 o mas analisis", () => {
    render(<GraficoConsumo historial={mockHistorialLargo} />);
    expect(screen.getByText("Evolución de tus análisis")).toBeInTheDocument();
    expect(screen.getByText("Costo mensual estimado")).toBeInTheDocument();
    expect(screen.getByText("Clasificaciones obtenidas")).toBeInTheDocument();
  });

  it("renderiza los contenedores de los graficos", () => {
    const { container } = render(<GraficoConsumo historial={mockHistorialLargo} />);
    const charts = container.querySelectorAll(".recharts-responsive-container");
    expect(charts.length).toBeGreaterThanOrEqual(2);
  });
});
