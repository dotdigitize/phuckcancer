const metrics = [
  ['Cancer records loaded', '2'],
  ['Molecular evidence items', '4'],
  ['MAMMAL interpretations', '2'],
  ['Evidence audits', '1'],
  ['Risk flags', '3'],
  ['Reports generated', '0'],
  ['External connector status', 'Disabled']
];

export default function MetricCards() {
  return (
    <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {metrics.map(([label, value]) => (
        <div className="panel" key={label}>
          <div className="text-sm font-semibold text-slate-500">{label}</div>
          <div className="mt-2 text-2xl font-bold text-clinical-navy">{value}</div>
        </div>
      ))}
    </section>
  );
}
