import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import FormularioConsumo from "../src/components/FormularioConsumo";

describe("FormularioConsumo", () => {
  const mockOnAnalizar = vi.fn();

  beforeEach(() => {
    mockOnAnalizar.mockClear();
  });

  it("renderiza todos los campos del formulario", () => {
    render(<FormularioConsumo onAnalizar={mockOnAnalizar} cargando={false} />);

    expect(screen.getByText("Datos de Consumo")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Ej: 250")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Ej: 12")).toBeInTheDocument();
    expect(screen.getByDisplayValue("Seleccione tipo de inmueble")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Ej: 8")).toBeInTheDocument();
    expect(screen.getByRole("checkbox")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Analizar Consumo/i })).toBeInTheDocument();
  });

  it("renderiza los tooltips en cada campo", () => {
    render(<FormularioConsumo onAnalizar={mockOnAnalizar} cargando={false} />);

    const tooltips = screen.getAllByText("?");
    expect(tooltips.length).toBe(5);
  });

  it("envia los datos correctamente al submit", async () => {
    const user = userEvent.setup();
    render(<FormularioConsumo onAnalizar={mockOnAnalizar} cargando={false} />);

    await user.type(screen.getByPlaceholderText("Ej: 250"), "250");
    await user.type(screen.getByPlaceholderText("Ej: 12"), "12");
    await user.selectOptions(screen.getByDisplayValue("Seleccione tipo de inmueble"), "Casa");
    await user.type(screen.getByPlaceholderText("Ej: 8"), "8");
    await user.click(screen.getByRole("checkbox"));
    await user.click(screen.getByRole("button", { name: /Analizar Consumo/i }));

    expect(mockOnAnalizar).toHaveBeenCalledWith({
      consumo_kwh: 250,
      uso_horario_pico: true,
      cantidad_equipos: 12,
      tipo_inmueble: "Casa",
      horas_alto_consumo: 8,
    });
  });

  it("llama a onAnalizar con valores numericos correctos", async () => {
    const user = userEvent.setup();
    render(<FormularioConsumo onAnalizar={mockOnAnalizar} cargando={false} />);

    await user.type(screen.getByPlaceholderText("Ej: 250"), "100");
    await user.type(screen.getByPlaceholderText("Ej: 12"), "5");
    await user.selectOptions(screen.getByDisplayValue("Seleccione tipo de inmueble"), "Departamento");
    await user.type(screen.getByPlaceholderText("Ej: 8"), "4");
    await user.click(screen.getByRole("button", { name: /Analizar Consumo/i }));

    const calledWith = mockOnAnalizar.mock.calls[0][0];
    expect(typeof calledWith.consumo_kwh).toBe("number");
    expect(typeof calledWith.cantidad_equipos).toBe("number");
    expect(typeof calledWith.horas_alto_consumo).toBe("number");
  });

  it("muestra spinner y texto Analizando cuando cargando es true", () => {
    render(<FormularioConsumo onAnalizar={mockOnAnalizar} cargando={true} />);

    expect(screen.getByText("Analizando...")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Analizando/i })).toBeDisabled();
  });

  it("el boton esta habilitado cuando cargando es false", () => {
    render(<FormularioConsumo onAnalizar={mockOnAnalizar} cargando={false} />);

    expect(screen.getByRole("button", { name: /Analizar Consumo/i })).toBeEnabled();
  });

  it("no llama a onAnalizar si el formulario esta incompleto", async () => {
    const user = userEvent.setup();
    render(<FormularioConsumo onAnalizar={mockOnAnalizar} cargando={false} />);

    await user.type(screen.getByPlaceholderText("Ej: 250"), "250");
    await user.click(screen.getByRole("button", { name: /Analizar Consumo/i }));

    expect(mockOnAnalizar).not.toHaveBeenCalled();
  });
});
