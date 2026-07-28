import { COLORES_CLASES, formatearFechaCompleta } from "../utils/constants";

export default function HistorialAnalisis({ historial, onLimpiar }) {
  if (!historial || historial.length === 0) return null;

  return (
    <div className="bg-white rounded-2xl card-shadow p-6 md:p-8 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-[0.2em]">
          Historial de analisis
        </h3>
        <button
          onClick={onLimpiar}
          className="text-xs text-gray-400 hover:text-red-500 transition-colors font-medium cursor-pointer"
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
                <p className="text-[11px] text-gray-400 mt-0.5 truncate">
                  {entrada.datos.consumo_kwh} kWh &middot; {entrada.datos.tipo_inmueble} &middot; {formatearFechaCompleta(entrada.fecha)}
                </p>
              </div>
              <div className="text-right shrink-0">
                <span className="text-xs font-bold text-gray-600">
                  {Math.round(entrada.resultado.probabilidad * 100)}%
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
