import type { CancerContextRecord } from '../api';

type Props = {
  contexts: CancerContextRecord[];
  selectedContextIds: number[];
  onToggle: (id: number) => void;
};

export default function CancerContextPanel({ contexts, selectedContextIds, onToggle }: Props) {
  return (
    <section className="panel">
      <h3 className="text-lg font-semibold text-clinical-navy">Cancer Context Library</h3>
      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        {contexts.map((context) => (
          <label key={context.id} className="block border border-slate-200 bg-slate-50 p-3" style={{ borderRadius: 8 }}>
            <div className="flex items-start gap-3">
              <input type="checkbox" className="mt-1" checked={selectedContextIds.includes(context.id)} onChange={() => onToggle(context.id)} />
              <div>
                <strong className="text-clinical-navy">{context.cancer_type}</strong>
                <p className="mt-1 text-xs text-slate-600">Subtype: {context.subtype || 'not set'}</p>
                <p className="text-xs text-slate-600">Biomarker: {context.biomarker || 'not set'}</p>
                <p className="text-xs text-slate-600">Pathway: {context.pathway || 'not set'}</p>
              </div>
            </div>
          </label>
        ))}
      </div>
    </section>
  );
}
