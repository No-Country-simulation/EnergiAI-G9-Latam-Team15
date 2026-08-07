import { COLORES_CLASES, formatearFechaCompleta } from "../utils/constants";

export default function HistorialAnalisis({ historial, onLimpiar, onEditar, onEliminar }) {
  if (!historial || historial.length === 0) return null;

  return (
    <div className="bg-white rounded-2xl card-shadow p-6 md:p-8 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-[0.2em]">
          Historial de análisis
        </h3>
        <button
          onClick={onLimpiar}
          className="no-pdf text-xs text-gray-400 hover:text-red-500 transition-colors font-medium cursor-pointer"
        >
          Limpiar
        </button>
      </div>

      <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
        {historial.map((entrada) => {
          const cat = entrada.resultado.categoria;
          const colores = COLORES_CLASES[cat] || COLORES_CLASES.Moderado;
          return (
            <div
              key={entrada.id}
              className="flex items-center gap-3 p-3 rounded-xl bg-gray-50/80 hover:bg-gray-50 transition-colors"
            >
              <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${colores.dot}`} />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${colores.bg} ${colores.text}`}>
                    {cat}
                  </span>
                  <span className="text-xs text-gray-400">
                    ${parseFloat(entrada.resultado.costo_estimado_mensual).toLocaleString("es-AR")}
                    /mes
                  </span>
                </div>
                <p className="text-[11px] text-gray-400 mt-0.5 break-words">
                  {entrada.datos.consumo_kwh} kWh &middot; {entrada.datos.tipo_inmueble} &middot; {formatearFechaCompleta(entrada.fecha)}
                </p>
              </div>
              <div className="no-pdf flex items-center gap-1 shrink-0">
                <span className="text-xs font-bold text-gray-600 mr-1">
                  {Math.round(entrada.resultado.probabilidad * 100)}%
                </span>
                {onEditar && (
                  <button
                    onClick={() => onEditar(entrada)}
                    aria-label="Editar análisis"
                    className="p-1.5 rounded-lg text-gray-400 hover:text-brand-600 hover:bg-brand-50 transition-colors cursor-pointer"
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z" />
                    </svg>
                  </button>
                )}
                {onEliminar && (
                  <button
                    onClick={() => onEliminar(entrada.id)}
                    aria-label="Eliminar análisis"
                    className="p-1.5 rounded-lg text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors cursor-pointer"
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="3 6 5 6 21 6" />
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                      <line x1="10" y1="11" x2="10" y2="17" />
                      <line x1="14" y1="11" x2="14" y2="17" />
                    </svg>
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
