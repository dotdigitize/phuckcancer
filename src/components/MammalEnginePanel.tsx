type Props = {
  status: any;
};

export default function MammalEnginePanel({ status }: Props) {
  const mammal = status?.mammal || {};
  const available = Boolean(status?.mammal_available);
  const provider = status?.mammal_provider || mammal.provider || 'local';
  return (
    <section className="panel">
      <h2 className="text-xl font-semibold text-clinical-navy">MAMMAL Biomedical AI Engine</h2>
      <dl className="mt-4 grid grid-cols-2 gap-3 text-sm">
        <dt className="font-semibold text-slate-500">Required</dt><dd>yes</dd>
        <dt className="font-semibold text-slate-500">Provider</dt><dd>{provider}</dd>
        <dt className="font-semibold text-slate-500">Available</dt><dd>{available ? 'yes' : 'no'}</dd>
        <dt className="font-semibold text-slate-500">Model</dt><dd>{status?.mammal_model_name || mammal.model_name || 'ibm/biomed.omics.bl.sm.ma-ted-458m'}</dd>
        <dt className="font-semibold text-slate-500">Device</dt><dd>{status?.mammal_device || mammal.device || 'auto'}</dd>
        <dt className="font-semibold text-slate-500">API configured</dt><dd>{status?.mammal_api_configured ? 'yes' : 'no'}</dd>
        <dt className="font-semibold text-slate-500">Last status check</dt><dd>{status ? 'current page load' : 'waiting for backend'}</dd>
      </dl>
      {!available ? (
        <div className="mt-4 border border-clinical-amber bg-amber-50 p-3 text-sm font-semibold text-clinical-amber" style={{ borderRadius: 8 }}>
          MAMMAL is required for biomedical interpretation. Configure local MAMMAL or a MAMMAL API provider before running cancer evidence analysis.
        </div>
      ) : null}
      <p className="mt-4 text-sm leading-6 text-slate-700">
        PhuckCancer applies MAMMAL in a cancer evidence workflow, then audits support, uncertainty, risk flags, and review questions for qualified human review.
      </p>
    </section>
  );
}
