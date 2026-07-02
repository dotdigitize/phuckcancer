import DrugEvidenceScoreCard from './DrugEvidenceScoreCard';

type Props = { matrix: any };

export default function DrugComparisonMatrix({ matrix }: Props) {
  const firstScore = matrix?.rows?.[0]?.evidence_score;
  return (
    <section className="panel">
      <h3 className="text-lg font-semibold text-clinical-navy">Comparison Matrix</h3>
      <div className="mt-4 overflow-auto">
        <table className="min-w-full border-collapse text-left text-sm">
          <thead className="bg-slate-100 text-xs uppercase text-slate-600">
            <tr>
              {['Drug', 'Class', 'Target', 'Cancer context', 'Drug response signal', 'Binding signal', 'Carcinogenicity signal', 'Resistance notes', 'Evidence support score', 'Data completeness', 'Overall review priority', 'Missing data'].map((header) => (
                <th key={header} className="border border-slate-200 p-2">{header}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {(matrix?.rows || []).map((row: any, index: number) => (
              <tr key={`${row.drug_name}-${row.target}-${index}`} className="align-top">
                <td className="border border-slate-200 p-2 font-semibold text-clinical-navy">{row.drug_name}</td>
                <td className="border border-slate-200 p-2">{row.drug_class}</td>
                <td className="border border-slate-200 p-2">{row.target || 'not selected'}</td>
                <td className="border border-slate-200 p-2">{row.cancer_context || 'not selected'}</td>
                <td className="border border-slate-200 p-2">{row.cell_line_response_signal}</td>
                <td className="border border-slate-200 p-2">{row.drug_target_binding_signal}</td>
                <td className="border border-slate-200 p-2">{row.carcinogenicity_signal}</td>
                <td className="border border-slate-200 p-2">{row.resistance_notes}</td>
                <td className="border border-slate-200 p-2">{row.evidence_support_score ?? 'missing'}</td>
                <td className="border border-slate-200 p-2">{row.data_completeness_score}</td>
                <td className="border border-slate-200 p-2">{row.overall_review_priority}</td>
                <td className="border border-slate-200 p-2">{(row.missing_data || []).join(', ') || 'none'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-4">
        <DrugEvidenceScoreCard score={firstScore} />
      </div>
    </section>
  );
}
