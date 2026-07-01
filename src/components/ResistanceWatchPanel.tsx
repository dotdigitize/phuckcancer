export default function ResistanceWatchPanel() {
  return (
    <section className="panel">
      <h2 className="text-xl font-semibold text-clinical-navy">Drug Resistance Signal Watch</h2>
      <div className="mt-4 text-sm text-slate-700">
        <div className="font-semibold">KRAS/MAPK pathway</div>
        <div className="mt-2">Cancer type: Lung adenocarcinoma</div>
        <div>Treatment category: targeted therapy class</div>
        <div>Support status: needs_human_review</div>
        <div className="mt-3 text-slate-600">MAMMAL-driven interpretation: resistance-associated signal requires source evidence auditing and qualified human review.</div>
      </div>
    </section>
  );
}
