const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8080";

function generarRecomendaciones(consumo_kwh, uso_horario_pico, horas_alto_consumo) {
  const recomendaciones = [];

  if (consumo_kwh > 300) {
    recomendaciones.push(
      "Reduzca el consumo general: se recomienda revisar electrodomésticos de alto consumo como aires acondicionados y calentadores."
    );
    recomendaciones.push(
      "Considere instalar paneles solares para compensar el alto consumo energético."
    );
  }

  if (consumo_kwh > 150) {
    recomendaciones.push(
      "Apague los equipos en modo stand-by: el consumo fantasma puede representar hasta un 10% de su factura."
    );
  }

  if (uso_horario_pico) {
    recomendaciones.push(
      "Evite el uso de electrodomésticos de alto consumo en horario pico (18:00 - 22:00). Reorganice tareas pesadas a horarios fuera de pico."
    );
    recomendaciones.push(
      "Solicite una tarifa horaria diferenciada a su proveedor de energía para ahorrar en horarios pico."
    );
  }

  if (horas_alto_consumo > 6) {
    recomendaciones.push(
      "Reduzca las horas de alto consumo: intente limitar el uso de equipos de alto consumo a menos de 4 horas diarias."
    );
  }

  recomendaciones.push(
    "Mantenga los electrodomésticos con etiquetas de eficiencia energética A o superior."
  );

  if (consumo_kwh < 150) {
    recomendaciones.push(
      "Excelente nivel de consumo. Continúe con sus buenas prácticas de ahorro energético."
    );
  }

  return recomendaciones;
}

function generarMockResponse(datos) {
  const { consumo_kwh, uso_horario_pico, horas_alto_consumo } = datos;

  let categoria;
  if (consumo_kwh > 300) {
    categoria = "Ineficiente";
  } else if (consumo_kwh >= 150) {
    categoria = "Moderado";
  } else {
    categoria = "Eficiente";
  }

  const costo_estimado = (consumo_kwh * 0.75).toFixed(2);

  const recomendaciones = generarRecomendaciones(
    consumo_kwh,
    uso_horario_pico,
    horas_alto_consumo
  );

  return {
    categoria,
    probabilidad: 0.85,
    costo_estimado_mensual: costo_estimado,
    recomendaciones,
  };
}

export async function analizarConsumo(datos) {
  try {
    const response = await fetch(`${API_URL}/api/v1/analisis-energetico`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });

    if (!response.ok) throw new Error("Error en la respuesta del servidor");

    return await response.json();
  } catch {
    return generarMockResponse(datos);
  }
}
