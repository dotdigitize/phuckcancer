import { useState } from 'react';
import { API_BASE_URL } from '../api';

type Props = { onResult: (result: any) => void };

export default function DrugTargetBindingPanel({ onResult }: Props) {
  const [form, setForm] = useState({ model_path: '', target_protein_sequence: '', drug_smiles: '', norm_y_mean: '', norm_y_std: '', target_name: '', drug_name: '' });
  const [status, setStatus] = useState('');
  const update = (key: string, value: string) => setForm((current) => ({ ...current, [key]: value }));
  const run = async () => {
    setStatus('running');
    const response = await fetch(`${API_BASE_URL}/api/mammal/tasks/drug_target_interaction`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, norm_y_mean: form.norm_y_mean ? Number(form.norm_y_mean) : null, norm_y_std: form.norm_y_std ? Number(form.norm_y_std) : null })
    });
    const result = await response.json();
    setStatus(response.ok ? 'complete' : result.error || 'error');
    onResult(result);
  };
  return (
    <div className="space-y-3">
      <div className="grid gap-3 md:grid-cols-2">
        <input className="border border-slate-300 p-2 text-sm" placeholder="MAMMAL DTI model path" value={form.model_path} onChange={(e) => update('model_path', e.target.value)} />
        <input className="border border-slate-300 p-2 text-sm" placeholder="Drug SMILES" value={form.drug_smiles} onChange={(e) => update('drug_smiles', e.target.value)} />
        <input className="border border-slate-300 p-2 text-sm" placeholder="norm_y_mean" value={form.norm_y_mean} onChange={(e) => update('norm_y_mean', e.target.value)} />
        <input className="border border-slate-300 p-2 text-sm" placeholder="norm_y_std" value={form.norm_y_std} onChange={(e) => update('norm_y_std', e.target.value)} />
        <input className="border border-slate-300 p-2 text-sm" placeholder="Target name optional" value={form.target_name} onChange={(e) => update('target_name', e.target.value)} />
        <input className="border border-slate-300 p-2 text-sm" placeholder="Drug name optional" value={form.drug_name} onChange={(e) => update('drug_name', e.target.value)} />
      </div>
      <textarea className="w-full border border-slate-300 p-2 text-sm" rows={4} placeholder="Target protein sequence" value={form.target_protein_sequence} onChange={(e) => update('target_protein_sequence', e.target.value)} />
      <button className="btn" onClick={run}>Run MAMMAL drug-target binding</button>
      {status ? <span className="badge border-slate-300 text-slate-700">{status}</span> : null}
    </div>
  );
}
