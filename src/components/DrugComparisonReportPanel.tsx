import { type UserRole, roleLabels } from '../api';

type Props = {
  selectedRole: UserRole | '';
  explanation: any;
  report: any;
  onExplain: () => void;
  onReport: () => void;
  onExportJson: () => void;
  onExportMarkdown: () => void;
};

export default function DrugComparisonReportPanel({ selectedRole, explanation, report, onExplain, onReport, onExportJson, onExportMarkdown }: Props) {
  return (
    <section className="panel">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold text-clinical-navy">Role-Based Explanation and Report Builder</h3>
          <p className="mt-1 text-sm text-slate-600">Uses completed comparison results and evidence scores only.</p>
        </div>
        <span className="badge border-slate-300 text-slate-700">{selectedRole ? roleLabels[selectedRole] : 'Select a role above'}</span>
      </div>
      <div className="mt-4 flex flex-wrap gap-3">
        <button className="btn" onClick={onExplain}>Explain comparison</button>
        <button className="btn" onClick={onReport}>Generate comparison report</button>
        <button className="btn" onClick={onExportJson}>Export JSON</button>
        <button className="btn" onClick={onExportMarkdown}>Export Markdown</button>
      </div>
      {explanation ? <pre className="mt-4 max-h-64 overflow-auto border border-slate-200 bg-slate-50 p-3 text-xs">{JSON.stringify(explanation, null, 2)}</pre> : null}
      {report?.markdown ? <pre className="mt-4 max-h-64 overflow-auto border border-slate-200 bg-white p-3 text-xs">{report.markdown}</pre> : null}
    </section>
  );
}
