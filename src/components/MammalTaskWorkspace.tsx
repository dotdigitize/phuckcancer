import { useEffect, useState } from 'react';
import { API_BASE_URL, type UserRole } from '../api';
import CellLineDrugResponsePanel from './CellLineDrugResponsePanel';
import DrugCarcinogenicityPanel from './DrugCarcinogenicityPanel';
import DrugTargetBindingPanel from './DrugTargetBindingPanel';
import MammalModelRegistryPanel from './MammalModelRegistryPanel';
import ProteinInteractionPanel from './ProteinInteractionPanel';
import ProteinSolubilityPanel from './ProteinSolubilityPanel';

type Props = { selectedRole: UserRole | '' };

const tabs = [
  'Cancer Drug Response',
  'Drug Target Binding',
  'Drug Carcinogenicity',
  'Protein Interaction',
  'Protein Solubility',
  'TCR Epitope Binding',
  'MCP Server Tasks',
  'Model Registry'
];

export default function MammalTaskWorkspace({ selectedRole }: Props) {
  const [activeTab, setActiveTab] = useState(tabs[0]);
  const [taskInfo, setTaskInfo] = useState<any>(null);
  const [result, setResult] = useState<any>(null);
  const [explanation, setExplanation] = useState<any>(null);
  const [tcrForm, setTcrForm] = useState({ tcr_sequence: '', epitope_sequence: '', cancer_context: '' });

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/mammal/official-tasks`).then((res) => res.json()).then(setTaskInfo).catch(() => setTaskInfo(null));
  }, []);

  const runTcr = async () => {
    const response = await fetch(`${API_BASE_URL}/api/mammal/tasks/tcr_epitope_binding`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(tcrForm)
    });
    const body = await response.json();
    setResult(body);
  };

  const explain = async () => {
    if (!selectedRole || !result?.task_type) return;
    const response = await fetch(`${API_BASE_URL}/api/mammal/tasks/${result.task_type}/explain`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_role: selectedRole, task_result: result })
    });
    setExplanation(await response.json());
  };

  return (
    <section className="panel">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="text-xl font-semibold text-clinical-navy">Official MAMMAL Task Workspace</h2>
          <p className="mt-2 max-w-4xl text-sm leading-6 text-slate-700">
            MAMMAL needs structured biological inputs. PhuckCancer will not invent SMILES strings, protein sequences, gene-expression profiles, h5ad files, model checkpoints, or normalization values.
          </p>
        </div>
        <span className="badge border-slate-300 text-slate-700">{taskInfo?.tasks?.length || 0} official task types</span>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {tabs.map((tab) => (
          <button key={tab} className={`badge ${activeTab === tab ? 'border-clinical-blue bg-blue-50 text-clinical-blue' : 'border-slate-300 bg-white text-slate-700'}`} onClick={() => setActiveTab(tab)}>
            {tab}
          </button>
        ))}
      </div>
      <div className="mt-5">
        {activeTab === 'Cancer Drug Response' ? <CellLineDrugResponsePanel onResult={setResult} /> : null}
        {activeTab === 'Drug Target Binding' ? <DrugTargetBindingPanel onResult={setResult} /> : null}
        {activeTab === 'Drug Carcinogenicity' ? <DrugCarcinogenicityPanel onResult={setResult} /> : null}
        {activeTab === 'Protein Interaction' ? <ProteinInteractionPanel onResult={setResult} /> : null}
        {activeTab === 'Protein Solubility' ? <ProteinSolubilityPanel onResult={setResult} /> : null}
        {activeTab === 'TCR Epitope Binding' ? (
          <div className="space-y-3">
            <textarea className="w-full border border-slate-300 p-2 text-sm" rows={3} placeholder="TCR sequence" value={tcrForm.tcr_sequence} onChange={(e) => setTcrForm({ ...tcrForm, tcr_sequence: e.target.value })} />
            <textarea className="w-full border border-slate-300 p-2 text-sm" rows={3} placeholder="Epitope sequence" value={tcrForm.epitope_sequence} onChange={(e) => setTcrForm({ ...tcrForm, epitope_sequence: e.target.value })} />
            <input className="w-full border border-slate-300 p-2 text-sm" placeholder="Cancer context optional" value={tcrForm.cancer_context} onChange={(e) => setTcrForm({ ...tcrForm, cancer_context: e.target.value })} />
            <button className="btn" onClick={runTcr}>Run MAMMAL TCR-epitope binding</button>
          </div>
        ) : null}
        {activeTab === 'MCP Server Tasks' ? (
          <div className="space-y-3 text-sm text-slate-700">
            <p>MCP URL: {taskInfo ? 'configured by MAMMAL_MCP_BASE_URL' : 'waiting for backend'}</p>
            <p>MCP health: use the backend system status and task result panels after configuration.</p>
            <p>Enabled MCP tasks: protein-protein interaction, TCR epitope binding, and provider-exposed official tasks.</p>
          </div>
        ) : null}
        {activeTab === 'Model Registry' ? <MammalModelRegistryPanel /> : null}
      </div>
      {result ? (
        <div className="mt-5 border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700" style={{ borderRadius: 8 }}>
          <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
            <strong>Task result</strong>
            <button className="btn disabled:cursor-not-allowed disabled:border-slate-300 disabled:bg-slate-200 disabled:text-slate-500" disabled={!selectedRole || !result.task_type || !result.raw_mammal_output} onClick={explain}>
              Explain result for selected role
            </button>
          </div>
          <pre className="max-h-80 overflow-auto whitespace-pre-wrap text-xs">{JSON.stringify(result, null, 2)}</pre>
        </div>
      ) : null}
      {explanation ? (
        <div className="mt-4 border border-slate-200 bg-white p-4 text-sm text-slate-700" style={{ borderRadius: 8 }}>
          <strong>Local LLM explanation</strong>
          <pre className="mt-2 max-h-60 overflow-auto whitespace-pre-wrap text-xs">{JSON.stringify(explanation, null, 2)}</pre>
        </div>
      ) : null}
    </section>
  );
}
