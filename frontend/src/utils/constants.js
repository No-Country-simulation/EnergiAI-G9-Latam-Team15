export const COLORES_HEX = {
  Eficiente: "#22c55e",
  Moderado: "#f59e0b",
  Ineficiente: "#ef4444",
};

export const COLORES_CLASES = {
  Eficiente: { bg: "bg-emerald-50", text: "text-emerald-700", dot: "bg-emerald-500" },
  Moderado: { bg: "bg-amber-50", text: "text-amber-700", dot: "bg-amber-500" },
  Ineficiente: { bg: "bg-red-50", text: "text-red-700", dot: "bg-red-500" },
};

export function formatearFechaCorta(isoString) {
  const d = new Date(isoString);
  return d.toLocaleDateString("es-AR", { day: "2-digit", month: "short" });
}

export function formatearFechaHoraCorta(isoString) {
  const d = new Date(isoString);
  return d.toLocaleString("es-AR", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatearFechaHoraCompleta(isoString) {
  const d = new Date(isoString);
  return d.toLocaleString("es-AR", {
    weekday: "short",
    day: "2-digit",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatearFechaCompleta(isoString) {
  const d = new Date(isoString);
  return d.toLocaleDateString("es-AR", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
