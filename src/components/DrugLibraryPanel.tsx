import type { DrugRecord } from '../api';

type Props = {
  drugs: DrugRecord[];
  selectedDrugIds: number[];
  search: string;
  onSearch: (value: string) => void;
  onToggle: (id: number) => void;
  onRefresh: () => void;
};

export default function DrugLibraryPanel({ drugs, selectedDrugIds, search, onSearch, onToggle, onRefresh }: Props) {
  return (
    <section className="panel">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold text-clinical-navy">Drug Library</h3>
          <p className="mt-1 text-sm text-slate-600">Search and select drugs for evidence comparison.</p>
        </div>
        <button className="btn" onClick={onRefresh}>Refresh</button>
      </div>
      <input className="mt-4 w-full border border-slate-300 p-2 text-sm" placeholder="Search drugs, targets, notes" value={search} onChange={(event) => onSearch(event.target.value)} />
      <div className="mt-4 max-h-96 space-y-3 overflow-auto">
        {drugs.map((drug) => (
          <label key={drug.id} className="block border border-slate-200 bg-slate-50 p-3" style={{ borderRadius: 8 }}>
            <div className="flex items-start gap-3">
              <input type="checkbox" className="mt-1" checked={selectedDrugIds.includes(drug.id)} onChange={() => onToggle(drug.id)} />
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <strong className="text-clinical-navy">{drug.drug_name}</strong>
                  <span className="badge border-slate-300 bg-white text-slate-700">{drug.drug_class || 'class not set'}</span>
                  <span className={`badge ${drug.smiles ? 'border-clinical-green text-clinical-green' : 'border-clinical-amber text-clinical-amber'}`}>SMILES {drug.smiles ? 'available' : 'missing'}</span>
                </div>
                <p className="mt-2 text-sm text-slate-700">{drug.mechanism_summary}</p>
                <p className="mt-2 text-xs text-slate-600">Targets: {(drug.known_targets || []).join(', ') || 'none listed'}</p>
                <p className="text-xs text-slate-600">Cancer contexts: {(drug.cancer_contexts || []).join(', ') || 'none listed'}</p>
                <p className="mt-2 text-xs text-slate-600">Resistance: {drug.resistance_notes || 'none'}</p>
                <p className="text-xs text-slate-600">Trials: {drug.trial_notes || 'none'}</p>
              </div>
            </div>
          </label>
        ))}
      </div>
    </section>
  );
}
