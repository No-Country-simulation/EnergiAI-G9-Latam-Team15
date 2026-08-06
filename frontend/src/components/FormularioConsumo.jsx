import { useState, useEffect } from "react";

const TIPOS_INMUEBLE = [
  { value: "", label: "Seleccione tipo de inmueble" },
  { value: "Casa", label: "Casa" },
  { value: "Departamento", label: "Departamento" },
  { value: "Establecimiento", label: "Establecimiento" },
];

const TOOLTIPS = {
  consumo_kwh:
    "Cantidad de energía eléctrica que consumió en el último mes. Puede encontrarla en su factura de luz, generalmente bajo el concepto \"Consumo Total\".",
  cantidad_equipos:
    "Cantidad de electrodomésticos y dispositivos que mantiene conectados con regularidad (heladera, aire acondicionado, lavarropas, TV, computadoras, etc.).",
  tipo_inmueble:
    "El tipo de vivienda influye en el patrón de consumo. Un establecimiento comercial consume de forma diferente a una casa.",
  horas_alto_consumo:
    "Horas al día en las que sus equipos funcionan a máxima capacidad. Por ejemplo, si el aire acondicionado funciona 8 horas seguidas, son 8 horas de alto consumo.",
  uso_horario_pico:
    "El horario pico (18:00 a 22:00) es cuando la demanda eléctrica es mayor y el costo por kWh puede ser más elevado. Active el interruptor si consume energía en ese horario.",
};

function Tooltip({ text }) {
  return (
    <span className="tooltip-wrapper ml-1.5">
      <span
        className="tooltip-trigger"
        role="button"
        tabIndex="0"
        aria-label="Más información"
      >
        ?
      </span>
      <span className="tooltip-content">{text}</span>
    </span>
  );
}

export default function FormularioConsumo({ onAnalizar, cargando, datosIniciales }) {
  const [formulario, setFormulario] = useState({
    consumo_kwh: "",
    uso_horario_pico: false,
    cantidad_equipos: "",
    tipo_inmueble: "",
    horas_alto_consumo: "",
  });

  useEffect(() => {
    if (!datosIniciales) return;
    setFormulario({
      consumo_kwh: String(datosIniciales.consumo_kwh ?? ""),
      uso_horario_pico: Boolean(datosIniciales.uso_horario_pico),
      cantidad_equipos: String(datosIniciales.cantidad_equipos ?? ""),
      tipo_inmueble: datosIniciales.tipo_inmueble ?? "",
      horas_alto_consumo: String(datosIniciales.horas_alto_consumo ?? ""),
    });
  }, [datosIniciales]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormulario((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onAnalizar({
      consumo_kwh: Number(formulario.consumo_kwh),
      uso_horario_pico: formulario.uso_horario_pico,
      cantidad_equipos: Number(formulario.cantidad_equipos),
      tipo_inmueble: formulario.tipo_inmueble,
      horas_alto_consumo: Number(formulario.horas_alto_consumo),
    });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-2xl card-shadow p-6 md:p-8 space-y-6"
    >
      <div>
        <h2 className="text-lg font-bold text-gray-900">Datos de Consumo</h2>
        <p className="text-sm text-gray-400 mt-1">
          Complete los campos para obtener su análisis energético
        </p>
        {datosIniciales && (
          <p className="text-xs text-brand-600 bg-brand-50 border border-brand-200 rounded-lg px-3 py-1.5 mt-2 inline-block">
            Editando un análisis guardado: ajuste los datos y presione "Analizar Consumo".
          </p>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="space-y-1.5">
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Consumo mensual (kWh)
            <Tooltip text={TOOLTIPS.consumo_kwh} />
          </label>
          <input
            type="number"
            name="consumo_kwh"
            value={formulario.consumo_kwh}
            onChange={handleChange}
            required
            min="0"
            step="0.1"
            placeholder="Ej: 250"
            className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-gray-800 placeholder-gray-400 focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-100 outline-none transition-all text-sm"
          />
        </div>

        <div className="space-y-1.5">
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Cantidad de equipos
            <Tooltip text={TOOLTIPS.cantidad_equipos} />
          </label>
          <input
            type="number"
            name="cantidad_equipos"
            value={formulario.cantidad_equipos}
            onChange={handleChange}
            required
            min="0"
            placeholder="Ej: 12"
            className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-gray-800 placeholder-gray-400 focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-100 outline-none transition-all text-sm"
          />
        </div>

        <div className="space-y-1.5">
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Tipo de inmueble
            <Tooltip text={TOOLTIPS.tipo_inmueble} />
          </label>
          <select
            name="tipo_inmueble"
            value={formulario.tipo_inmueble}
            onChange={handleChange}
            required
            className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-gray-800 focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-100 outline-none transition-all text-sm"
          >
            {TIPOS_INMUEBLE.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-1.5">
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Horas de alto consumo al día
            <Tooltip text={TOOLTIPS.horas_alto_consumo} />
          </label>
          <input
            type="number"
            name="horas_alto_consumo"
            value={formulario.horas_alto_consumo}
            onChange={handleChange}
            required
            min="0"
            max="24"
            step="0.5"
            placeholder="Ej: 8"
            className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-gray-800 placeholder-gray-400 focus:border-brand-500 focus:bg-white focus:ring-2 focus:ring-brand-100 outline-none transition-all text-sm"
          />
        </div>
      </div>

      <div className="flex items-center gap-3 pt-1">
        <input
          type="checkbox"
          id="uso_horario_pico"
          name="uso_horario_pico"
          checked={formulario.uso_horario_pico}
          onChange={handleChange}
          className="toggle-switch"
        />
        <label
          htmlFor="uso_horario_pico"
          className="text-sm text-gray-500 cursor-pointer select-none flex items-center"
        >
          Uso en horario pico (18:00 - 22:00)
          <Tooltip text={TOOLTIPS.uso_horario_pico} />
        </label>
      </div>

      <button
        type="submit"
        disabled={cargando}
        className="w-full rounded-xl bg-brand-600 hover:bg-brand-700 active:scale-[0.98] disabled:bg-brand-300 text-white font-semibold py-3.5 px-6 transition-all duration-200 cursor-pointer disabled:cursor-wait text-sm tracking-wide flex items-center justify-center gap-2"
      >
        {cargando ? (
          <>
            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            Analizando...
          </>
        ) : (
          "Analizar Consumo"
        )}
      </button>
    </form>
  );
}
