export default function Header() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div>
          <div className="text-xl font-bold text-clinical-navy">PhuckCancer</div>
          <div className="text-sm text-slate-600">MAMMAL-integrated cancer evidence system</div>
        </div>
        <nav className="hidden gap-5 text-sm font-semibold text-slate-700 md:flex">
          <span>Evidence</span>
          <span>Genomics</span>
          <span>Audits</span>
          <span>Reports</span>
        </nav>
      </div>
    </header>
  );
}
