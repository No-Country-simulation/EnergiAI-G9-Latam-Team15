import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import TarjetaCosto from "../src/components/TarjetaCosto";

describe("TarjetaCosto", () => {
  it("muestra el titulo y la tarifa base", () => {
    render(<TarjetaCosto costo="187.50" />);

    expect(screen.getByText("Costo Mensual Estimado")).toBeInTheDocument();
    expect(screen.getByText("Tarifa base: $0,75 / kWh")).toBeInTheDocument();
  });

  it("muestra el costo formateado correctamente", () => {
    render(<TarjetaCosto costo="187.50" />);
    expect(screen.getByText("187")).toBeInTheDocument();
    expect(screen.getByText(",50")).toBeInTheDocument();
  });

  it("muestra el simbolo de pesos", () => {
    render(<TarjetaCosto costo="200" />);
    expect(screen.getByText("$")).toBeInTheDocument();
  });

  it("maneja costos grandes", () => {
    render(<TarjetaCosto costo="1250.75" />);
    expect(screen.getByText("1.250")).toBeInTheDocument();
    expect(screen.getByText(",75")).toBeInTheDocument();
  });
});
