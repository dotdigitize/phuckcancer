export default function TrialSignalPanel() {
  return (
    <section className="panel">
      <h2 className="text-xl font-semibold text-clinical-navy">Clinical-Trial Signal Organizer</h2>
      <div className="mt-4 text-sm text-slate-700">
        <div className="font-semibold">Synthetic EGFR biomarker trial signal</div>
        <div className="mt-2">Biomarker: EGFR L858R</div>
        <div>Evidence status: Possible signal for review</div>
        <div>Missing information: trial protocol criteria, coordinator review</div>
        <div className="mt-3 text-clinical-amber font-semibold">Needs oncologist/research coordinator review</div>
      </div>
    </section>
  );
}
