import { roleLabels, type UserRole } from '../api';

const roles = Object.entries(roleLabels) as Array<[UserRole, string]>;

type Props = {
  selectedRole: UserRole | '';
  onRoleChange: (role: UserRole) => void;
};

export default function UserRoleSelector({ selectedRole, onRoleChange }: Props) {
  return (
    <section className="panel">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="text-xl font-semibold text-clinical-navy">Who is using PhuckCancer today?</h2>
          <p className="mt-2 text-sm text-slate-700">Choose your role so local LLM explanations use the right safety framing and technical depth.</p>
        </div>
        {selectedRole ? <span className="badge border-clinical-blue bg-blue-50 text-clinical-blue">Active: {roleLabels[selectedRole]}</span> : null}
      </div>
      <div className="mt-4 grid gap-3 md:grid-cols-4">
        {roles.map(([role, label]) => (
          <button
            key={role}
            type="button"
            onClick={() => onRoleChange(role)}
            className={`border px-3 py-3 text-left text-sm font-semibold ${selectedRole === role ? 'border-clinical-blue bg-blue-50 text-clinical-blue' : 'border-slate-200 bg-white text-slate-700 hover:border-clinical-blue'}`}
            style={{ borderRadius: 8 }}
          >
            {label}
          </button>
        ))}
      </div>
    </section>
  );
}
