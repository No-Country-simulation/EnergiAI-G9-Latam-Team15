import { useState, useCallback } from "react";

const STORAGE_KEY = "energiai_historial";
const MAX_ITEMS = 20;

function cargarHistorial() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  } catch {
    return [];
  }
}

function guardarHistorial(items) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  } catch {
    // localStorage lleno o no disponible
  }
}

export default function useHistorial() {
  const [historial, setHistorial] = useState(cargarHistorial);

  const agregarAnalisis = useCallback((datosFormulario, resultado) => {
    const entrada = {
      id: Date.now(),
      fecha: new Date().toISOString(),
      datos: datosFormulario,
      resultado: {
        categoria: resultado.categoria,
        probabilidad: resultado.probabilidad,
        costo_estimado_mensual: resultado.costo_estimado_mensual,
        recomendaciones: resultado.recomendaciones,
      },
    };

    setHistorial((prev) => {
      const nuevo = [entrada, ...prev].slice(0, MAX_ITEMS);
      guardarHistorial(nuevo);
      return nuevo;
    });
  }, []);

  const limpiarHistorial = useCallback(() => {
    setHistorial([]);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  return { historial, agregarAnalisis, limpiarHistorial };
}
