import { useState } from 'react';
import { API_BASE_URL } from '../api';

type Props = { onResult: (result: any) => void };

export default function DrugCarcinogenicityPanel({ onResult }: Props) {
  const [form, setForm] = useState({ model_path: '', drug_smiles: '', drug_name: '' });
  const [status, setStatus] = useState('');
  const run = async () => {
    setStatus('running');
    const response = await fetch(`${API_BASE_URL}/api/mammal/tasks/drug_carcinogenicity`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) });
    const result = await response.json();
    setStatus(response.ok ? 'complete' : result.error || 'error');
    onResult(result);
  };
  return (
    <div className="space-y-3">
      <div className="grid gap-3 md:grid-cols-2">
        <input className="border border-slate-300 p-2 text-sm" placeholder="Model path" value={form.model_path} onChange={(e) => setForm({ ...form, model_path: e.target.value })} />
        <input className="border border-slate-300 p-2 text-sm" placeholder="Drug name optional" value={form.drug_name} onChange={(e) => setForm({ ...form, drug_name: e.target.value })} />
      </div>
      <textarea className="w-full border border-slate-300 p-2 text-sm" rows={3} placeholder="Drug SMILES" value={form.drug_smiles} onChange={(e) => setForm({ ...form, drug_smiles: e.target.value })} />
      <button className="btn" onClick={run}>Run MAMMAL carcinogenicity task</button>
      {status ? <span className="badge border-slate-300 text-slate-700">{status}</span> : null}
    </div>
  );
}
