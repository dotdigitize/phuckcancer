import { useState } from 'react';
import { API_BASE_URL } from '../api';

type Props = { onResult: (result: any) => void };

export default function ProteinInteractionPanel({ onResult }: Props) {
  const [form, setForm] = useState({ protein_a_name: '', protein_a_sequence: '', protein_b_name: '', protein_b_sequence: '' });
  const [status, setStatus] = useState('');
  const run = async () => {
    setStatus('running');
    const response = await fetch(`${API_BASE_URL}/api/mammal/tasks/protein_protein_interaction`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) });
    const result = await response.json();
    setStatus(response.ok ? 'complete' : result.error || 'error');
    onResult(result);
  };
  return (
    <div className="space-y-3">
      <div className="grid gap-3 md:grid-cols-2">
        <input className="border border-slate-300 p-2 text-sm" placeholder="Protein A name" value={form.protein_a_name} onChange={(e) => setForm({ ...form, protein_a_name: e.target.value })} />
        <input className="border border-slate-300 p-2 text-sm" placeholder="Protein B name" value={form.protein_b_name} onChange={(e) => setForm({ ...form, protein_b_name: e.target.value })} />
        <textarea className="border border-slate-300 p-2 text-sm" rows={4} placeholder="Protein A sequence" value={form.protein_a_sequence} onChange={(e) => setForm({ ...form, protein_a_sequence: e.target.value })} />
        <textarea className="border border-slate-300 p-2 text-sm" rows={4} placeholder="Protein B sequence" value={form.protein_b_sequence} onChange={(e) => setForm({ ...form, protein_b_sequence: e.target.value })} />
      </div>
      <button className="btn" onClick={run}>Run MAMMAL protein-protein interaction</button>
      {status ? <span className="badge border-slate-300 text-slate-700">{status}</span> : null}
    </div>
  );
}
