import { useState, useRef } from "react";
import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";
import FormularioConsumo from "../components/FormularioConsumo";
import SemaforoEficiencia from "../components/SemaforoEficiencia";
import TarjetaCosto from "../components/TarjetaCosto";
import ListaRecomendaciones from "../components/ListaRecomendaciones";
import GraficoConsumo from "../components/GraficoConsumo";
import HistorialAnalisis from "../components/HistorialAnalisis";
import useHistorial from "../hooks/useHistorial";
import { analizarConsumo } from "../services/apiService";

const ULTIMO_RESULTADO_KEY = "energiai_ultimo_resultado";

function cargarUltimoResultado() {
  try {
    const data = localStorage.getItem(ULTIMO_RESULTADO_KEY);
    return data ? JSON.parse(data) : null;
  } catch {
    return null;
  }
}

function guardarUltimoResultado(datos, resultado) {
  try {
    localStorage.setItem(
      ULTIMO_RESULTADO_KEY,
      JSON.stringify({ datos, resultado, guardadoEn: Date.now() })
    );
  } catch {
    // localStorage lleno o no disponible
  }
}

export default function Home() {
  const [ultimoResultado] = useState(cargarUltimoResultado);
  const [resultado, setResultado] = useState(ultimoResultado?.resultado ?? null);
  const [cargando, setCargando] = useState(false);
  const [descargando, setDescargando] = useState(false);
  const resultadoRef = useRef(null);
  const pdfRef = useRef(null);
  const { historial, agregarAnalisis, actualizarAnalisis, limpiarHistorial, eliminarAnalisis } = useHistorial();
  const [datosParaEditar, setDatosParaEditar] = useState(null);
  const [idEnEdicion, setIdEnEdicion] = useState(null);

  const handleAnalizar = async (datos) => {
    setCargando(true);
    try {
      const respuesta = await analizarConsumo(datos);
      setResultado(respuesta);
      setDatosParaEditar(null);
      if (idEnEdicion && historial.some((entrada) => entrada.id === idEnEdicion)) {
        actualizarAnalisis(idEnEdicion, datos, respuesta);
      } else {
        agregarAnalisis(datos, respuesta);
      }
      setIdEnEdicion(null);
      guardarUltimoResultado(datos, respuesta);
      setTimeout(() => {
        resultadoRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    } catch {
    } finally {
      setCargando(false);
    }
  };

  const handleNuevoAnalisis = () => {
    setResultado(null);
    setDatosParaEditar(null);
    setIdEnEdicion(null);
    localStorage.removeItem(ULTIMO_RESULTADO_KEY);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleLimpiarTodo = () => {
    limpiarHistorial();
    setResultado(null);
    setDatosParaEditar(null);
    setIdEnEdicion(null);
    localStorage.removeItem(ULTIMO_RESULTADO_KEY);
  };

  const handleEditarAnalisis = (entrada) => {
    setIdEnEdicion(entrada.id);
    setDatosParaEditar(entrada.datos);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleEliminarAnalisis = (id) => {
    eliminarAnalisis(id);
    if (idEnEdicion === id) {
      setIdEnEdicion(null);
      setDatosParaEditar(null);
    }
  };

  const handleDescargarPDF = async () => {
    const node = pdfRef.current;
    if (!node || descargando) return;
    setDescargando(true);
    try {
      node.classList.add("generando-pdf");
      const canvas = await html2canvas(node, {
        scale: 2,
        backgroundColor: "#f4f6f8",
        useCORS: true,
      });
      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF("p", "mm", "a4");
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      const margin = 10;
      const contentWidth = pageWidth - margin * 2;
      const contentHeight = pageHeight - margin * 2;

      const totalImgHeight = (canvas.height * contentWidth) / canvas.width;
      const sourceSliceHeight = (contentHeight / totalImgHeight) * canvas.height;

      let sourceY = 0;
      let page = 0;

      while (sourceY < canvas.height) {
        if (page > 0) pdf.addPage();

        const sliceHeight = Math.min(sourceSliceHeight, canvas.height - sourceY);
        const sliceCanvas = document.createElement("canvas");
        sliceCanvas.width = canvas.width;
        sliceCanvas.height = sliceHeight;
        const ctx = sliceCanvas.getContext("2d");
        ctx.drawImage(
          canvas,
          0, sourceY, canvas.width, sliceHeight,
          0, 0, canvas.width, sliceHeight
        );

        const sliceData = sliceCanvas.toDataURL("image/png");
        const sliceImgHeight = (sliceHeight * contentWidth) / canvas.width;
        pdf.addImage(sliceData, "PNG", margin, margin, contentWidth, sliceImgHeight);

        sourceY += sliceHeight;
        page++;
      }
      pdf.save("EnergiAI-Resultado.pdf");
    } catch {
    } finally {
      node.classList.remove("generando-pdf");
      setDescargando(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f4f6f8]">
      <header className="glass border-b border-gray-200/60 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <img src="/logo_energiAI.png" alt="EnergiAI logo" className="w-12 h-12 rounded-lg object-contain" />
            <h1 className="text-lg font-bold text-gray-900 tracking-tight">
              EnergiAI
            </h1>
            <span className="hidden sm:inline text-[10px] bg-brand-50 text-brand-700 border border-brand-200 rounded-full px-2 py-0.5 font-semibold uppercase tracking-wider">
              Hackathon ONE
            </span>
          </div>
          <div className="text-[11px] text-gray-400 font-medium hidden sm:block">
            Alura + Oracle
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-10 space-y-10">
        <section className="text-center space-y-3 max-w-xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight leading-tight">
            Análisis Energético
            <span className="text-brand-600"> Inteligente</span>
          </h2>
          <p className="text-gray-400 text-sm sm:text-base leading-relaxed">
            Ingrese los datos de su consumo y reciba una clasificación de
            eficiencia energética, el costo mensual estimado y recomendaciones
            personalizadas para ahorrar energía.
          </p>
        </section>

        <FormularioConsumo
          onAnalizar={handleAnalizar}
          cargando={cargando}
          datosIniciales={datosParaEditar}
        />

        {(resultado || historial.length > 0) && (
          <section ref={resultadoRef} className="space-y-6 animate-fadeIn scroll-mt-24">
            <div className="flex justify-end gap-3">
              <button
                onClick={handleNuevoAnalisis}
                className="btn-descargar-pdf"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19" />
                  <line x1="5" y1="12" x2="19" y2="12" />
                </svg>
                Nuevo análisis
              </button>
              <button
                onClick={handleDescargarPDF}
                disabled={descargando}
                className="btn-descargar-pdf"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" y1="15" x2="12" y2="3" />
                </svg>
                {descargando ? "Generando..." : "Descargar PDF"}
              </button>
            </div>

            <div ref={pdfRef} className="space-y-6">
              {resultado && (
                <>
                  <div className="flex items-center gap-3 mb-2">
                    <img src="/logo_energiAI.png" alt="" className="w-8 h-8 rounded-lg object-contain" />
                    <div>
                      <h3 className="text-base font-bold text-gray-900">EnergiAI &mdash; Resultado del Análisis</h3>
                      <p className="text-xs text-gray-400">{new Date().toLocaleDateString("es-AR", { year: "numeric", month: "long", day: "numeric" })}</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <SemaforoEficiencia
                      categoria={resultado.categoria}
                      probabilidad={resultado.probabilidad}
                    />
                    <TarjetaCosto costo={resultado.costo_estimado_mensual} />
                  </div>
                  <ListaRecomendaciones
                    recomendaciones={resultado.recomendaciones}
                  />
                </>
              )}

              {historial.length > 0 && (
                <>
                  <GraficoConsumo historial={historial} />
                  <HistorialAnalisis
                    historial={historial}
                    onLimpiar={handleLimpiarTodo}
                    onEditar={handleEditarAnalisis}
                    onEliminar={handleEliminarAnalisis}
                  />
                </>
              )}
            </div>
          </section>
        )}
      </main>

      <footer className="border-t border-gray-200/60 mt-12">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="text-xs text-gray-400 font-medium">
            EnergiAI &copy; {new Date().getFullYear()}
          </div>
          <div className="text-[11px] text-gray-300 font-medium">
            Hackathon ONE &mdash; Alura + Oracle
          </div>
        </div>
      </footer>
    </div>
  );
}
