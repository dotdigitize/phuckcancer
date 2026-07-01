import Header from './components/Header';
import SafetyNotice from './components/SafetyNotice';
import MetricCards from './components/MetricCards';
import GenomicAlterationMatrix from './components/GenomicAlterationMatrix';
import PathwayExplorer from './components/PathwayExplorer';
import MammalEnginePanel from './components/MammalEnginePanel';
import EvidenceAuditPanel from './components/EvidenceAuditPanel';
import LocalAssistantPanel from './components/LocalAssistantPanel';
import TrialSignalPanel from './components/TrialSignalPanel';
import ResistanceWatchPanel from './components/ResistanceWatchPanel';
import ExternalDataSourcesPanel from './components/ExternalDataSourcesPanel';
import ReportBuilder from './components/ReportBuilder';

export default function App() {
  return (
    <div>
      <Header />
      <main className="mx-auto max-w-7xl space-y-6 px-4 py-6 sm:px-6 lg:px-8">
        <section className="border-b border-slate-200 pb-6">
          <h1 className="text-4xl font-bold tracking-normal text-clinical-navy">PhuckCancer</h1>
          <p className="mt-3 max-w-4xl text-lg text-slate-700">
            Visualization, analysis, AI interpretation, evidence auditing, and human-reviewable reporting for cancer genomics and molecular evidence.
          </p>
          <p className="mt-3 max-w-4xl text-base text-slate-600">
            Built to help doctors, researchers, patients, and families understand cancer evidence faster, organize it better, and fight cancer with stronger information.
          </p>
        </section>
        <SafetyNotice />
        <MetricCards />
        <GenomicAlterationMatrix />
        <div className="grid gap-6 lg:grid-cols-2">
          <PathwayExplorer />
          <MammalEnginePanel />
        </div>
        <EvidenceAuditPanel />
        <LocalAssistantPanel />
        <div className="grid gap-6 lg:grid-cols-2">
          <TrialSignalPanel />
          <ResistanceWatchPanel />
        </div>
        <ExternalDataSourcesPanel />
        <ReportBuilder />
      </main>
    </div>
  );
}
