import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import SemaforoEficiencia from "../src/components/SemaforoEficiencia";

describe("SemaforoEficiencia", () => {
  it("muestra la categoria Ineficiente", () => {
    render(<SemaforoEficiencia categoria="Ineficiente" probabilidad={0.85} />);
    expect(screen.getByText("Clasificacion")).toBeInTheDocument();
    expect(screen.getByText("Ineficiente")).toBeInTheDocument();
  });

  it("muestra la categoria Moderado", () => {
    render(<SemaforoEficiencia categoria="Moderado" probabilidad={0.7} />);
    expect(screen.getByText("Moderado")).toBeInTheDocument();
  });

  it("muestra la categoria Eficiente", () => {
    render(<SemaforoEficiencia categoria="Eficiente" probabilidad={0.92} />);
    expect(screen.getByText("Eficiente")).toBeInTheDocument();
  });

  it("muestra el porcentaje de confianza", () => {
    const { container } = render(
      <SemaforoEficiencia categoria="Ineficiente" probabilidad={0.85} />
    );
    const spans = container.querySelectorAll(".text-3xl.font-extrabold span");
    expect(spans.length).toBe(1);
    expect(spans[0].textContent).toBe("%");
    const numSpan = container.querySelector(".text-3xl.font-extrabold");
    expect(numSpan.textContent).toContain("85");
  });

  it("redondea el porcentaje correctamente", () => {
    const { container } = render(
      <SemaforoEficiencia categoria="Moderado" probabilidad={0.856} />
    );
    const numSpan = container.querySelector(".text-3xl.font-extrabold");
    expect(numSpan.textContent).toContain("86");
  });

  it("muestra la barra de progreso con ancho correcto", () => {
    const { container } = render(
      <SemaforoEficiencia categoria="Eficiente" probabilidad={0.75} />
    );
    const bar = container.querySelector("[style*='width: 75%']");
    expect(bar).toBeInTheDocument();
  });

  it("muestra el label de probabilidad", () => {
    render(<SemaforoEficiencia categoria="Moderado" probabilidad={0.5} />);
    expect(screen.getByText("Probabilidad de clasificacion")).toBeInTheDocument();
  });
});
