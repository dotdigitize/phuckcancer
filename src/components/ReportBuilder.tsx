export default function ReportBuilder() {
  return (
    <section className="panel">
      <h2 className="text-xl font-semibold text-clinical-navy">Report Builder</h2>
      <p className="mt-2 text-sm text-slate-700">Generate doctor-reviewable reports, family-friendly summaries, missing information checklists, risk and uncertainty notes, and human review reminders.</p>
      <div className="mt-4 flex flex-wrap gap-3">
        <button className="btn">Generate doctor report</button>
        <button className="btn">Generate family summary</button>
        <button className="btn">Export JSON</button>
      </div>
      <p className="mt-4 text-sm text-slate-600">Reports are for education, research support, evidence organization, and qualified human review.</p>
    </section>
  );
}
