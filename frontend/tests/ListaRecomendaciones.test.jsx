import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import ListaRecomendaciones from "../src/components/ListaRecomendaciones";

describe("ListaRecomendaciones", () => {
  it("muestra la lista de recomendaciones", () => {
    const recs = [
      "Reduzca el consumo general",
      "Apague los equipos en stand-by",
      "Evite el uso en horario pico",
    ];
    render(<ListaRecomendaciones recomendaciones={recs} />);

    expect(screen.getByText("Recomendaciones")).toBeInTheDocument();
    expect(screen.getByText(recs[0])).toBeInTheDocument();
    expect(screen.getByText(recs[1])).toBeInTheDocument();
    expect(screen.getByText(recs[2])).toBeInTheDocument();
  });

  it("numera las recomendaciones correctamente", () => {
    const recs = ["Recomendacion A", "Recomendacion B", "Recomendacion C"];
    render(<ListaRecomendaciones recomendaciones={recs} />);

    expect(screen.getByText("1")).toBeInTheDocument();
    expect(screen.getByText("2")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument();
  });

  it("renderiza null si no hay recomendaciones", () => {
    const { container } = render(<ListaRecomendaciones recomendaciones={[]} />);
    expect(container.innerHTML).toBe("");
  });

  it("renderiza null si recomendaciones es undefined", () => {
    const { container } = render(<ListaRecomendaciones />);
    expect(container.innerHTML).toBe("");
  });
});
