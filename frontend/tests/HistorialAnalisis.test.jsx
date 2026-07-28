import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import HistorialAnalisis from "../src/components/HistorialAnalisis";

const mockHistorial = [
  {
    id: 1,
    fecha: "2026-07-25T10:30:00.000Z",
    datos: { consumo_kwh: 150, tipo_inmueble: "Casa" },
    resultado: { categoria: "Eficiente", probabilidad: 0.85, costo_estimado_mensual: "112.50" },
  },
  {
    id: 2,
    fecha: "2026-07-24T15:00:00.000Z",
    datos: { consumo_kwh: 350, tipo_inmueble: "Departamento" },
    resultado: { categoria: "Ineficiente", probabilidad: 0.7, costo_estimado_mensual: "262.50" },
  },
];

describe("HistorialAnalisis", () => {
  it("renderiza null si no hay historial", () => {
    const { container } = render(<HistorialAnalisis historial={[]} onLimpiar={vi.fn()} />);
    expect(container.innerHTML).toBe("");
  });

  it("muestra el titulo y boton limpiar", () => {
    render(<HistorialAnalisis historial={mockHistorial} onLimpiar={vi.fn()} />);
    expect(screen.getByText("Historial de analisis")).toBeInTheDocument();
    expect(screen.getByText("Limpiar")).toBeInTheDocument();
  });

  it("muestra todas las entradas del historial", () => {
    render(<HistorialAnalisis historial={mockHistorial} onLimpiar={vi.fn()} />);
    expect(screen.getByText("Eficiente")).toBeInTheDocument();
    expect(screen.getByText("Ineficiente")).toBeInTheDocument();
    expect(screen.getByText(/Casa/)).toBeInTheDocument();
    expect(screen.getByText(/Departamento/)).toBeInTheDocument();
  });

  it("llama a onLimpiar al hacer click en Limpiar", async () => {
    const onLimpiar = vi.fn();
    const user = userEvent.setup();
    render(<HistorialAnalisis historial={mockHistorial} onLimpiar={onLimpiar} />);

    await user.click(screen.getByText("Limpiar"));
    expect(onLimpiar).toHaveBeenCalledTimes(1);
  });
});
