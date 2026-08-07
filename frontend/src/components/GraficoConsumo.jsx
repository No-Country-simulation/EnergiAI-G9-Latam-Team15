import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar,
  Cell,
} from "recharts";
import {
  COLORES_HEX,
  formatearFechaHoraCorta,
  formatearFechaHoraCompleta,
} from "../utils/constants";

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  const esFecha = !Number.isNaN(new Date(label).getTime());
  return (
    <div className="bg-gray-900 text-white text-xs rounded-lg px-3 py-2 shadow-lg">
      <p className="font-semibold mb-1">
        {esFecha ? formatearFechaHoraCompleta(label) : label}
      </p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color }}>
          {entry.name}: {entry.name === "Costo" ? `$${entry.value}` : entry.value}
        </p>
      ))}
    </div>
  );
}

export default function GraficoConsumo({ historial }) {
  if (!historial || historial.length < 2) return null;

  const datosLinea = [...historial]
    .sort((a, b) => new Date(a.fecha) - new Date(b.fecha))
    .map((h) => ({
      fecha: h.fecha,
      Costo: parseFloat(h.resultado.costo_estimado_mensual),
      Confianza: Math.round(h.resultado.probabilidad * 100),
    }));

  const conteo = { Eficiente: 0, Moderado: 0, Ineficiente: 0 };
  historial.forEach((h) => {
    conteo[h.resultado.categoria]++;
  });
  const datosBarra = Object.entries(conteo)
    .map(([nombre, cantidad]) => ({ nombre, cantidad }))
    .filter((d) => d.cantidad > 0);

  return (
    <div className="bg-white rounded-2xl card-shadow p-6 md:p-8 space-y-6">
      <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-[0.2em]">
        Evolución de tus análisis
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <p className="text-xs text-gray-400 font-medium">Costo mensual estimado</p>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={datosLinea}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
                <XAxis
                  dataKey="fecha"
                  tick={{ fontSize: 10, fill: "#9ca3af" }}
                  tickLine={false}
                  axisLine={{ stroke: "#e5e7eb" }}
                  interval="preserveStartEnd"
                  minTickGap={16}
                  tickMargin={8}
                  tickFormatter={(value) => formatearFechaHoraCorta(value)}
                />
                <YAxis
                  tick={{ fontSize: 10, fill: "#9ca3af" }}
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(v) => `$${v}`}
                />
                <Tooltip content={<CustomTooltip />} />
                <Line
                  type="monotone"
                  dataKey="Costo"
                  stroke="#6366f1"
                  strokeWidth={2}
                  dot={{ r: 4, fill: "#6366f1" }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="space-y-2">
          <p className="text-xs text-gray-400 font-medium">Clasificaciones obtenidas</p>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={datosBarra}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
                <XAxis
                  dataKey="nombre"
                  tick={{ fontSize: 10, fill: "#9ca3af" }}
                  tickLine={false}
                  axisLine={{ stroke: "#e5e7eb" }}
                />
                <YAxis
                  allowDecimals={false}
                  tick={{ fontSize: 10, fill: "#9ca3af" }}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="cantidad" name="Análisis" radius={[6, 6, 0, 0]}>
                  {datosBarra.map((entry) => (
                    <Cell key={entry.nombre} fill={COLORES_HEX[entry.nombre]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
