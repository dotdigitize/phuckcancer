import { useState } from 'react';
import { API_BASE_URL } from '../api';

type Props = { onResult: (result: any) => void };

export default function CellLineDrugResponsePanel({ onResult }: Props) {
  const [form, setForm] = useState({ model_path: '', cell_line_name: '', cell_line_h5ad_file: '', drug_name: '', drug_smiles: '' });
  const [status, setStatus] = useState('');
  const update = (key: string, value: string) => setForm((current) => ({ ...current, [key]: value }));
  const run = async () => {
    setStatus('running');
    const response = await fetch(`${API_BASE_URL}/api/mammal/tasks/cell_line_drug_response`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    const result = await response.json();
    setStatus(response.ok ? 'complete' : result.error || 'error');
    onResult(result);
  };
  return (
    <div className="space-y-3">
      <div className="grid gap-3 md:grid-cols-2">
        <input className="border border-slate-300 p-2 text-sm" placeholder="MAMMAL model path" value={form.model_path} onChange={(e) => update('model_path', e.target.value)} />
        <input className="border border-slate-300 p-2 text-sm" placeholder="Cell line name" value={form.cell_line_name} onChange={(e) => update('cell_line_name', e.target.value)} />
        <input className="border border-slate-300 p-2 text-sm" placeholder="or h5ad file path/upload placeholder" value={form.cell_line_h5ad_file} onChange={(e) => update('cell_line_h5ad_file', e.target.value)} />
        <input className="border border-slate-300 p-2 text-sm" placeholder="Drug name" value={form.drug_name} onChange={(e) => update('drug_name', e.target.value)} />
      </div>
      <textarea className="w-full border border-slate-300 p-2 text-sm" rows={3} placeholder="Drug SMILES" value={form.drug_smiles} onChange={(e) => update('drug_smiles', e.target.value)} />
      <button className="btn" onClick={run}>Run MAMMAL cell-line drug response</button>
      {status ? <span className="badge border-slate-300 text-slate-700">{status}</span> : null}
    </div>
  );
}
