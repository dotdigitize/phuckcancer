import { useState } from 'react';
import { API_BASE_URL } from '../api';

type Props = { onResult: (result: any) => void };

export default function ProteinSolubilityPanel({ onResult }: Props) {
  const [form, setForm] = useState({ model_path: '', protein_name: '', protein_sequence: '' });
  const [status, setStatus] = useState('');
  const run = async () => {
    setStatus('running');
    const response = await fetch(`${API_BASE_URL}/api/mammal/tasks/protein_solubility`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) });
    const result = await response.json();
    setStatus(response.ok ? 'complete' : result.error || 'error');
    onResult(result);
  };
  return (
    <div className="space-y-3">
      <div className="grid gap-3 md:grid-cols-2">
        <input className="border border-slate-300 p-2 text-sm" placeholder="Model path" value={form.model_path} onChange={(e) => setForm({ ...form, model_path: e.target.value })} />
        <input className="border border-slate-300 p-2 text-sm" placeholder="Protein name" value={form.protein_name} onChange={(e) => setForm({ ...form, protein_name: e.target.value })} />
      </div>
      <textarea className="w-full border border-slate-300 p-2 text-sm" rows={4} placeholder="Protein sequence" value={form.protein_sequence} onChange={(e) => setForm({ ...form, protein_sequence: e.target.value })} />
      <button className="btn" onClick={run}>Run MAMMAL protein solubility</button>
      {status ? <span className="badge border-slate-300 text-slate-700">{status}</span> : null}
    </div>
  );
}
