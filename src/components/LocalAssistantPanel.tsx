import { API_BASE_URL, roleLabels, type UserRole } from '../api';

type Props = {
  selectedRole: UserRole | '';
};

const tabs: Array<[UserRole, string]> = [
  ['patient_family', 'Patient/family explanation'],
  ['doctor_tumor_board', 'Doctor/tumor board explanation'],
  ['cancer_researcher', 'Research explanation'],
  ['data_engineer', 'System/data explanation']
];

export default function LocalAssistantPanel({ selectedRole }: Props) {
  const explain = async () => {
    if (!selectedRole) return;
    await fetch(`${API_BASE_URL}/api/assistant/explain`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_role: selectedRole,
        source_text: 'Explain the current MAMMAL interpretation, evidence audit, risk flags, and review questions.',
        risk_flags: ['needs_human_review'],
        safety_constraints: ['qualified_human_review_required']
      })
    });
  };

  return (
    <section className="panel">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-xl font-semibold text-clinical-navy">Local LLM Assistant</h2>
        <span className="badge border-slate-300 text-slate-700">Active role: {selectedRole ? roleLabels[selectedRole] : 'none selected'}</span>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {tabs.map(([role, label]) => (
          <span key={role} className={`badge ${selectedRole === role ? 'border-clinical-blue bg-blue-50 text-clinical-blue' : 'border-slate-200 text-slate-600'}`}>
            {label}
          </span>
        ))}
      </div>
      <p className="mt-4 text-sm leading-6 text-slate-700">
        The local LLM explains MAMMAL's structured biomedical interpretation, evidence audit output, source notes, uncertainty, and risk flags. It does not replace MAMMAL and does not make medical decisions.
      </p>
      <div className="mt-4 border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700" style={{ borderRadius: 8 }}>
        {selectedRole ? 'Ready to format the explanation for the selected role.' : 'Choose a user type so PhuckCancer can format the explanation safely.'}
      </div>
      <button className="btn mt-4 disabled:cursor-not-allowed disabled:border-slate-300 disabled:bg-slate-200 disabled:text-slate-500" disabled={!selectedRole} onClick={explain}>
        Explain
      </button>
    </section>
  );
}
