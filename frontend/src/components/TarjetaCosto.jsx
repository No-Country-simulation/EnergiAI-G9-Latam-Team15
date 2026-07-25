export default function TarjetaCosto({ costo }) {
  return (
    <div className="bg-white rounded-2xl card-shadow p-6 md:p-8 flex flex-col items-center justify-center gap-3">
      <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-[0.2em]">
        Costo Mensual Estimado
      </h3>

      <div className="flex items-baseline gap-1">
        <span className="text-lg font-semibold text-gray-400">$</span>
        <span className="text-5xl font-extrabold text-gray-900 tracking-tight">
          {Number(costo)
            .toLocaleString("es-AR", { minimumFractionDigits: 2 })
            .split(",")[0]}
        </span>
        <span className="text-2xl font-bold text-gray-900">
          ,{Number(costo).toFixed(2).split(".")[1]}
        </span>
      </div>

      <div className="flex items-center gap-2 text-xs text-gray-400 mt-1">
        <span className="w-1 h-1 rounded-full bg-gray-300" />
        <span>Tarifa base: $0,75 / kWh</span>
      </div>
    </div>
  );
}
