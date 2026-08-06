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

function construirResultado(resultado) {
  return {
    categoria: resultado.categoria,
    probabilidad: resultado.probabilidad,
    costo_estimado_mensual: resultado.costo_estimado_mensual,
    recomendaciones: resultado.recomendaciones,
  };
}

export default function useHistorial() {
  const [historial, setHistorial] = useState(cargarHistorial);

  const agregarAnalisis = useCallback((datosFormulario, resultado) => {
    const entrada = {
      id: `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`,
      fecha: new Date().toISOString(),
      datos: datosFormulario,
      resultado: construirResultado(resultado),
    };

    setHistorial((prev) => {
      const nuevo = [entrada, ...prev].slice(0, MAX_ITEMS);
      guardarHistorial(nuevo);
      return nuevo;
    });
  }, []);

  const actualizarAnalisis = useCallback((id, datosFormulario, resultado) => {
    setHistorial((prev) => {
      const actualizada = {
        id,
        fecha: new Date().toISOString(),
        datos: datosFormulario,
        resultado: construirResultado(resultado),
      };
      const nuevo = [
        actualizada,
        ...prev.filter((entrada) => entrada.id !== id),
      ].slice(0, MAX_ITEMS);
      guardarHistorial(nuevo);
      return nuevo;
    });
  }, []);

  const limpiarHistorial = useCallback(() => {
    setHistorial([]);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  const eliminarAnalisis = useCallback((id) => {
    setHistorial((prev) => {
      const nuevo = prev.filter((entrada) => entrada.id !== id);
      guardarHistorial(nuevo);
      return nuevo;
    });
  }, []);

  return {
    historial,
    agregarAnalisis,
    actualizarAnalisis,
    limpiarHistorial,
    eliminarAnalisis,
  };
}
