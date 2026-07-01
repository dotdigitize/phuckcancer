const rows = [
  { pathway: 'EGFR signaling', gene: 'EGFR', a: 'mutation', b: 'none', c: 'none' },
  { pathway: 'MAPK pathway', gene: 'KRAS', a: 'none', b: 'mutation', c: 'none' },
  { pathway: 'DNA repair', gene: 'BRCA1', a: 'none', b: 'none', c: 'deletion' },
  { pathway: 'Cell cycle regulation', gene: 'TP53', a: 'mutation', b: 'none', c: 'none' }
];

const style: Record<string, string> = {
  mutation: 'bg-clinical-blue text-white',
  deletion: 'bg-clinical-red text-white',
  amplification: 'bg-clinical-amber text-white',
  expression: 'bg-clinical-green text-white',
  none: 'bg-slate-100 text-slate-500'
};

export default function GenomicAlterationMatrix() {
  return (
    <section className="panel overflow-x-auto">
      <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 className="text-xl font-semibold text-clinical-navy">Genomic Alteration Matrix</h2>
          <p className="text-sm text-slate-600">Gene rows across synthetic sample cohorts with pathway grouping.</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {Object.keys(style).filter(k => k !== 'none').map(k => <span className={`badge ${style[k]}`} key={k}>{k}</span>)}
        </div>
      </div>
      <table className="w-full min-w-[720px] border-collapse text-sm">
        <thead>
          <tr className="border-b bg-slate-50 text-left">
            <th className="p-3">Pathway</th><th className="p-3">Gene</th><th className="p-3">SYN-001</th><th className="p-3">SYN-002</th><th className="p-3">SYN-003</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(row => (
            <tr className="border-b" key={row.gene}>
              <td className="p-3 font-medium">{row.pathway}</td><td className="p-3 font-semibold">{row.gene}</td>
              {[row.a, row.b, row.c].map((v, i) => <td className="p-3" key={i}><span className={`badge ${style[v]}`}>{v}</span></td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
