export default function LocalAssistantPanel() {
  return (
    <section className="panel">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-xl font-semibold text-clinical-navy">Local Assistant</h2>
        <div className="inline-flex overflow-hidden border border-slate-300" style={{ borderRadius: 6 }}>
          <button className="bg-clinical-blue px-3 py-2 text-sm font-semibold text-white">Doctor / researcher</button>
          <button className="px-3 py-2 text-sm font-semibold text-slate-700">Patient / family</button>
        </div>
      </div>
      <p className="mt-4 text-sm leading-6 text-slate-700">
        Summarizes molecular evidence, explains mutation and pathway findings, identifies evidence gaps, and prepares questions for clinical review. It never diagnoses cancer, recommends treatment, predicts individual survival, replaces oncologists, or determines clinical-trial eligibility.
      </p>
      <div className="mt-4 border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700" style={{ borderRadius: 8 }}>
        Ask your oncologist about the EGFR, KRAS, TP53, and BRCA findings, what source evidence supports them, and what information may be missing.
      </div>
    </section>
  );
}
