import { API_BASE_URL } from '../api';

type Props = {
  status: any;
};

function yesNo(value: boolean | undefined) {
  return value ? 'yes' : 'no';
}

export default function SetupStatusPanel({ status }: Props) {
  return (
    <section className="panel">
      <h2 className="text-xl font-semibold text-clinical-navy">Setup Status</h2>
      <dl className="mt-4 grid gap-3 text-sm md:grid-cols-2 lg:grid-cols-4">
        <div><dt className="font-semibold text-slate-500">Backend URL</dt><dd>{API_BASE_URL}</dd></div>
        <div><dt className="font-semibold text-slate-500">Frontend URL</dt><dd>http://localhost:{status?.frontend_port ?? 5179}</dd></div>
        <div><dt className="font-semibold text-slate-500">MariaDB configured</dt><dd>{yesNo(status?.database_enabled)}</dd></div>
        <div><dt className="font-semibold text-slate-500">MAMMAL configured</dt><dd>{yesNo(status?.mammal_provider === 'local' || status?.mammal_api_configured)}</dd></div>
        <div><dt className="font-semibold text-slate-500">MAMMAL available</dt><dd>{yesNo(status?.mammal_available)}</dd></div>
        <div><dt className="font-semibold text-slate-500">Ollama enabled</dt><dd>{yesNo(status?.local_llm_enabled)}</dd></div>
        <div><dt className="font-semibold text-slate-500">cBioPortal enabled</dt><dd>{yesNo(status?.cbioportal_connector_enabled)}</dd></div>
        <div><dt className="font-semibold text-slate-500">Database provider</dt><dd>{status?.database_provider ?? 'mariadb'}</dd></div>
      </dl>
    </section>
  );
}
