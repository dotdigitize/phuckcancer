import type { DrugTargetRecord } from '../api';

type Props = {
  targets: DrugTargetRecord[];
  selectedTargetIds: number[];
  search: string;
  onSearch: (value: string) => void;
  onToggle: (id: number) => void;
};

export default function DrugTargetPanel({ targets, selectedTargetIds, search, onSearch, onToggle }: Props) {
  return (
    <section className="panel">
      <h3 className="text-lg font-semibold text-clinical-navy">Target Library</h3>
      <input className="mt-4 w-full border border-slate-300 p-2 text-sm" placeholder="Search targets, genes, pathways" value={search} onChange={(event) => onSearch(event.target.value)} />
      <div className="mt-4 max-h-80 space-y-3 overflow-auto">
        {targets.map((target) => (
          <label key={target.id} className="block border border-slate-200 bg-slate-50 p-3" style={{ borderRadius: 8 }}>
            <div className="flex items-start gap-3">
              <input type="checkbox" className="mt-1" checked={selectedTargetIds.includes(target.id)} onChange={() => onToggle(target.id)} />
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <strong className="text-clinical-navy">{target.target_name}</strong>
                  <span className="badge border-slate-300 bg-white text-slate-700">{target.gene_symbol || 'gene not set'}</span>
                  <span className={`badge ${target.protein_sequence ? 'border-clinical-green text-clinical-green' : 'border-clinical-amber text-clinical-amber'}`}>sequence {target.protein_sequence ? 'available' : 'missing'}</span>
                </div>
                <p className="mt-2 text-xs text-slate-600">Pathway: {target.pathway || 'not set'} · Context: {target.cancer_context || 'not set'}</p>
                <p className="mt-1 text-xs text-slate-600">{target.notes}</p>
              </div>
            </div>
          </label>
        ))}
      </div>
    </section>
  );
}
