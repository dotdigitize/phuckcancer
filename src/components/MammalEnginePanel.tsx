export default function MammalEnginePanel() {
  return (
    <section className="panel">
      <h2 className="text-xl font-semibold text-clinical-navy">MAMMAL Biomedical AI Engine</h2>
      <dl className="mt-4 grid grid-cols-2 gap-3 text-sm">
        <dt className="font-semibold text-slate-500">Status</dt><dd>Disabled by default</dd>
        <dt className="font-semibold text-slate-500">Model</dt><dd>ibm/biomed.omics.bl.sm.ma-ted-458m</dd>
        <dt className="font-semibold text-slate-500">Pipeline mode</dt><dd>Deterministic fallback</dd>
        <dt className="font-semibold text-slate-500">Fallback status</dt><dd>Active for local tests</dd>
      </dl>
      <p className="mt-4 text-sm leading-6 text-slate-700">
        Latest interpretation: EGFR, KRAS, TP53, and BRCA pathway signals are routed through MAMMAL-driven biomedical interpretation, evidence matching, support scoring, risk flagging, and qualified human review.
      </p>
    </section>
  );
}
