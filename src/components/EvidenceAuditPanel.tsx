export default function EvidenceAuditPanel() {
  return (
    <section className="panel">
      <h2 className="text-xl font-semibold text-clinical-navy">Evidence Audit Panel</h2>
      <div className="mt-4 overflow-x-auto">
        <table className="w-full min-w-[760px] text-sm">
          <thead><tr className="border-b bg-slate-50 text-left"><th className="p-3">Claim</th><th className="p-3">Evidence</th><th className="p-3">Support</th><th className="p-3">Risk flags</th><th className="p-3">Review</th></tr></thead>
          <tbody>
            <tr className="border-b"><td className="p-3">EGFR alteration suggests pathway signal</td><td className="p-3">Synthetic reference corpus</td><td className="p-3"><span className="badge border-clinical-green text-clinical-green">0.86</span></td><td className="p-3">needs_human_review</td><td className="p-3">Qualified review</td></tr>
            <tr className="border-b"><td className="p-3">Treatment certainty claim</td><td className="p-3">No matching source</td><td className="p-3"><span className="badge border-clinical-red text-clinical-red">0.15</span></td><td className="p-3">unsupported_treatment_claim</td><td className="p-3">Escalated</td></tr>
          </tbody>
        </table>
      </div>
    </section>
  );
}
