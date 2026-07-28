import { useState, useEffect } from "react";

const CONFIG = {
  Ineficiente: { stroke: "#ef4444", strokeLight: "#fca5a5", label: "Ineficiente" },
  Moderado: { stroke: "#f59e0b", strokeLight: "#fcd34d", label: "Moderado" },
  Eficiente: { stroke: "#22c55e", strokeLight: "#86efac", label: "Eficiente" },
};

function GaugeCircular({ porcentaje, stroke }) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (porcentaje / 100) * circumference;

  return (
    <div className="relative w-36 h-36">
      <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
        <circle
          cx="60"
          cy="60"
          r={radius}
          fill="none"
          stroke="#e5e7eb"
          strokeWidth="10"
        />
        <circle
          cx="60"
          cy="60"
          r={radius}
          fill="none"
          stroke={stroke}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{
            transition:
              "stroke-dashoffset 1s cubic-bezier(0.22, 1, 0.36, 1), stroke 0.6s ease",
          }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-extrabold text-gray-900 leading-none">
          {porcentaje}
          <span className="text-lg">%</span>
        </span>
        <span className="text-[10px] font-medium text-gray-400 uppercase tracking-widest mt-1">
          Confianza
        </span>
      </div>
    </div>
  );
}

export default function SemaforoEficiencia({ categoria, probabilidad }) {
  const [prevCategoria, setPrevCategoria] = useState(categoria);
  const [displayCategoria, setDisplayCategoria] = useState(categoria);
  const config = CONFIG[displayCategoria] || CONFIG.Moderado;
  const porcentaje = Math.round(probabilidad * 100);

  useEffect(() => {
    if (categoria !== prevCategoria) {
      setDisplayCategoria(prevCategoria);
      const timer = setTimeout(() => {
        setDisplayCategoria(categoria);
        setPrevCategoria(categoria);
      }, 50);
      return () => clearTimeout(timer);
    }
  }, [categoria, prevCategoria]);

  return (
    <div className="bg-white rounded-2xl card-shadow p-6 md:p-8 flex flex-col items-center gap-5">
      <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-[0.2em]">
        Clasificacion
      </h3>

      <GaugeCircular porcentaje={porcentaje} stroke={config.stroke} />

      <div
        className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-semibold border transition-all duration-500 ease-out"
        style={{
          backgroundColor: `${config.stroke}10`,
          color: config.stroke,
          borderColor: `${config.stroke}30`,
        }}
      >
        <span
          className="w-2 h-2 rounded-full shrink-0 transition-colors duration-500"
          style={{ backgroundColor: config.stroke }}
        />
        {config.label}
      </div>

      <div className="w-full space-y-2">
        <div className="flex justify-between text-xs text-gray-400 font-medium">
          <span>0%</span>
          <span>Probabilidad de clasificacion</span>
          <span>100%</span>
        </div>
        <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-1000 ease-out"
            style={{
              width: `${porcentaje}%`,
              background: `linear-gradient(90deg, ${config.strokeLight}, ${config.stroke})`,
              transition: "width 1s ease-out, background 0.6s ease",
            }}
          />
        </div>
      </div>
    </div>
  );
}
