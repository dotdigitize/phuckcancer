type Props = { score?: any };

export default function DrugEvidenceScoreCard({ score }: Props) {
  if (!score) {
    return null;
  }
  return (
    <div className="border border-slate-200 bg-white p-4" style={{ borderRadius: 8 }}>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <strong className="text-clinical-navy">Evidence Score Card</strong>
        <span className={`badge ${score.overall_review_priority === 'insufficient_data' ? 'border-clinical-amber text-clinical-amber' : 'border-clinical-blue text-clinical-blue'}`}>{score.overall_review_priority}</span>
      </div>
      <div className="mt-3 grid gap-3 text-sm sm:grid-cols-3">
        <p>Response: <strong>{score.response_signal_score ?? 'missing'}</strong></p>
        <p>Binding: <strong>{score.binding_signal_score ?? 'missing'}</strong></p>
        <p>Evidence: <strong>{score.evidence_support_score ?? 'missing'}</strong></p>
        <p>Completeness: <strong>{score.data_completeness_score}</strong></p>
        <p>Uncertainty: <strong>{score.uncertainty_score}</strong></p>
        <p>Resistance flag: <strong>{score.resistance_flag ? 'yes' : 'no'}</strong></p>
      </div>
      <p className="mt-3 text-sm text-slate-700">{score.explanation_summary}</p>
    </div>
  );
}
