type Props = {
  comparisonName: string;
  taskTypes: string[];
  cellLineName: string;
  h5adFileRef: string;
  requirements: any;
  providerStatus: any;
  onNameChange: (value: string) => void;
  onTaskToggle: (taskType: string) => void;
  onCellLineChange: (value: string) => void;
  onH5adChange: (value: string) => void;
  onCreate: () => void;
  onRun: () => void;
};

const tasks = ['cell_line_drug_response', 'drug_target_interaction', 'drug_carcinogenicity', 'protein_protein_interaction'];

export default function DrugComparisonBuilder({ comparisonName, taskTypes, cellLineName, h5adFileRef, requirements, providerStatus, onNameChange, onTaskToggle, onCellLineChange, onH5adChange, onCreate, onRun }: Props) {
  const missing = requirements?.missing_structured_data || [];
  return (
    <section className="panel">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold text-clinical-navy">Build Comparison</h3>
          <p className="mt-1 text-sm text-slate-600">Prepare MAMMAL task batches across drugs, targets, and cancer contexts.</p>
        </div>
        <span className={`badge ${providerStatus?.mammal_available ? 'border-clinical-green text-clinical-green' : 'border-clinical-amber text-clinical-amber'}`}>MAMMAL {providerStatus?.mammal_available ? 'available' : 'not available'}</span>
      </div>
      <div className="mt-4 grid gap-3 md:grid-cols-2">
        <input className="border border-slate-300 p-2 text-sm" placeholder="Comparison name" value={comparisonName} onChange={(event) => onNameChange(event.target.value)} />
        <input className="border border-slate-300 p-2 text-sm" placeholder="Optional cell-line name" value={cellLineName} onChange={(event) => onCellLineChange(event.target.value)} />
        <input className="border border-slate-300 p-2 text-sm md:col-span-2" placeholder="Optional h5ad gene-expression file reference" value={h5adFileRef} onChange={(event) => onH5adChange(event.target.value)} />
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {tasks.map((task) => (
          <button key={task} className={`badge ${taskTypes.includes(task) ? 'border-clinical-blue bg-blue-50 text-clinical-blue' : 'border-slate-300 bg-white text-slate-700'}`} onClick={() => onTaskToggle(task)}>
            {task}
          </button>
        ))}
      </div>
      <div className="mt-4 flex flex-wrap gap-3">
        <button className="btn" onClick={onCreate}>Prepare comparison</button>
        <button className="btn" onClick={onRun}>Run comparison</button>
      </div>
      <div className="mt-5 border border-slate-200 bg-slate-50 p-4 text-sm" style={{ borderRadius: 8 }}>
        <strong className="text-clinical-navy">MAMMAL Requirements Panel</strong>
        {missing.length ? (
          <ul className="mt-3 space-y-2 text-clinical-amber">
            {missing.map((item: any, index: number) => (
              <li key={`${item.drug_id}-${item.target_id}-${item.task_type}-${index}`}>{item.drug_name || `Drug ${item.drug_id}`} / {item.target_name || 'no target'} / {item.task_type}: {(item.missing_fields || []).join(', ')}</li>
            ))}
          </ul>
        ) : (
          <p className="mt-3 text-slate-700">No missing structured data reported for the prepared comparison.</p>
        )}
      </div>
    </section>
  );
}
