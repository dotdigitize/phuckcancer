type Props = {
  dataSources: any;
  status: any;
};

export default function ExternalDataSourcesPanel({ dataSources, status }: Props) {
  return (
    <section className="panel">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-xl font-semibold text-clinical-navy">External Cancer Data Sources</h2>
        <button className="btn">Import</button>
      </div>
      <div className="mt-4 grid gap-4 md:grid-cols-3">
        <div className="border border-slate-200 p-3" style={{ borderRadius: 8 }}><div className="font-semibold">Local sample fixtures</div><div className="text-sm text-slate-600">Enabled</div></div>
        <div className="border border-slate-200 p-3" style={{ borderRadius: 8 }}><div className="font-semibold">MariaDB database mode</div><div className="text-sm text-slate-600">{status?.database_enabled ? 'Configured' : 'Disabled'} / {status?.database_available ? 'available' : 'unavailable'}</div></div>
        <div className="border border-slate-200 p-3" style={{ borderRadius: 8 }}><div className="font-semibold">cBioPortal connector</div><div className="text-sm text-slate-600">{status?.cbioportal_connector_enabled ? 'Enabled' : 'Disabled'}</div></div>
      </div>
      <p className="mt-4 text-sm leading-6 text-slate-700">
        Configured API base URL: {dataSources?.configured_api_base_url || 'https://www.cbioportal.org/api'}. External data may require permission, institutional access, authentication, data-use agreements, privacy review, and local compliance. Imported records remain research/evidence input and still require MAMMAL-powered interpretation, evidence auditing, risk flagging, and qualified human review.
      </p>
      <div className="mt-3 text-sm text-slate-600">Available studies when enabled: {Array.isArray(dataSources?.available_studies) ? dataSources.available_studies.length : dataSources?.available_studies || 'shown after connector configuration'}. Last import summary: {dataSources?.last_import_summary || 'no external import has run'}.</div>
    </section>
  );
}
