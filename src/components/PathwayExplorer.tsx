const pathways = [
  ['EGFR signaling', 'EGFR', '0.74', 'Needs review'],
  ['MAPK pathway', 'KRAS', '0.74', 'Needs review'],
  ['DNA repair', 'BRCA1, BRCA2', '0.74', 'Needs review'],
  ['Cell cycle regulation', 'TP53', '0.74', 'Needs review']
];

export default function PathwayExplorer() {
  return (
    <section className="panel">
      <h2 className="text-xl font-semibold text-clinical-navy">Cancer Pathway Explorer</h2>
      <div className="mt-4 space-y-3">
        {pathways.map(([pathway, genes, score, review]) => (
          <div className="border border-slate-200 p-3" style={{ borderRadius: 8 }} key={pathway}>
            <div className="flex items-center justify-between gap-3">
              <div className="font-semibold">{pathway}</div>
              <span className="badge border-clinical-blue text-clinical-blue">support {score}</span>
            </div>
            <div className="mt-2 text-sm text-slate-600">Altered genes: {genes}</div>
            <div className="mt-1 text-sm text-slate-600">MAMMAL-driven interpretation requires evidence audit and qualified human review.</div>
            <div className="mt-2 text-xs font-semibold text-clinical-amber">{review}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
