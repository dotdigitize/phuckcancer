import { API_BASE_URL, type UserRole } from '../api';

type Props = {
  selectedRole: UserRole | '';
};

export default function ReportBuilder({ selectedRole }: Props) {
  const buildReport = async (reportType: 'doctor' | 'family' | 'json') => {
    await fetch(`${API_BASE_URL}/api/reports/build`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ report_type: reportType, user_role: selectedRole || undefined })
    });
  };

  return (
    <section className="panel">
      <h2 className="text-xl font-semibold text-clinical-navy">Report Builder</h2>
      <p className="mt-2 text-sm text-slate-700">Generate doctor-reviewable reports, family-friendly summaries, missing information checklists, risk and uncertainty notes, and human review reminders.</p>
      <div className="mt-4 flex flex-wrap gap-3">
        <button className="btn" onClick={() => buildReport('doctor')}>Generate doctor report</button>
        <button className="btn" onClick={() => buildReport('family')}>Generate family summary</button>
        <button className="btn" onClick={() => buildReport('json')}>Export JSON</button>
      </div>
      <p className="mt-4 text-sm text-slate-600">Reports are for education, research support, evidence organization, and qualified human review.</p>
    </section>
  );
}
