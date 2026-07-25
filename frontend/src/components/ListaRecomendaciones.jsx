export default function ListaRecomendaciones({ recomendaciones }) {
  if (!recomendaciones || recomendaciones.length === 0) return null;

  return (
    <div className="bg-white rounded-2xl card-shadow p-6 md:p-8 space-y-4">
      <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-[0.2em]">
        Recomendaciones
      </h3>

      <ul className="space-y-3">
        {recomendaciones.map((rec, idx) => (
          <li
            key={idx}
            className="flex items-start gap-3 p-3 rounded-xl bg-gray-50/80 hover:bg-gray-50 transition-colors"
          >
            <span
              className="mt-0.5 w-6 h-6 rounded-lg bg-brand-100 text-brand-700 flex items-center justify-center text-xs font-bold shrink-0"
            >
              {idx + 1}
            </span>
            <span className="text-sm text-gray-600 leading-relaxed">{rec}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
