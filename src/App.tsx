import { useEffect, useState } from 'react';
import { API_BASE_URL, type UserRole } from './api';
import Header from './components/Header';
import SafetyNotice from './components/SafetyNotice';
import MetricCards from './components/MetricCards';
import GenomicAlterationMatrix from './components/GenomicAlterationMatrix';
import PathwayExplorer from './components/PathwayExplorer';
import MammalEnginePanel from './components/MammalEnginePanel';
import MammalTaskWorkspace from './components/MammalTaskWorkspace';
import DrugEvidenceWorkspace from './components/DrugEvidenceWorkspace';
import EvidenceAuditPanel from './components/EvidenceAuditPanel';
import LocalAssistantPanel from './components/LocalAssistantPanel';
import TrialSignalPanel from './components/TrialSignalPanel';
import ResistanceWatchPanel from './components/ResistanceWatchPanel';
import ExternalDataSourcesPanel from './components/ExternalDataSourcesPanel';
import ReportBuilder from './components/ReportBuilder';
import UserRoleSelector from './components/UserRoleSelector';
import SetupStatusPanel from './components/SetupStatusPanel';

export default function App() {
  const [selectedRole, setSelectedRole] = useState<UserRole | ''>(() => (localStorage.getItem('phuckcancer.user_role') as UserRole | null) || '');
  const [systemStatus, setSystemStatus] = useState<any>(null);
  const [dataSources, setDataSources] = useState<any>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/system/status`).then((res) => res.json()).then(setSystemStatus).catch(() => setSystemStatus(null));
    fetch(`${API_BASE_URL}/api/data-sources`).then((res) => res.json()).then(setDataSources).catch(() => setDataSources(null));
  }, []);

  const updateRole = (role: UserRole) => {
    setSelectedRole(role);
    localStorage.setItem('phuckcancer.user_role', role);
  };

  return (
    <div>
      <Header />
      <main className="mx-auto max-w-7xl space-y-6 px-4 py-6 sm:px-6 lg:px-8">
        <section className="border-b border-slate-200 pb-6">
          <h1 className="text-4xl font-bold tracking-normal text-clinical-navy">PhuckCancer</h1>
          <p className="mt-3 max-w-4xl text-lg text-slate-700">
            Cancer genomics visualization, MAMMAL-powered biomedical interpretation, evidence auditing, and plain-English reports for doctors, researchers, patients, and families.
          </p>
        </section>
        <UserRoleSelector selectedRole={selectedRole} onRoleChange={updateRole} />
        <SafetyNotice />
        <SetupStatusPanel status={systemStatus} />
        <MetricCards />
        <GenomicAlterationMatrix />
        <div className="grid gap-6 lg:grid-cols-2">
          <PathwayExplorer />
          <MammalEnginePanel status={systemStatus} />
        </div>
        <DrugEvidenceWorkspace selectedRole={selectedRole} systemStatus={systemStatus} />
        <MammalTaskWorkspace selectedRole={selectedRole} />
        <EvidenceAuditPanel />
        <LocalAssistantPanel selectedRole={selectedRole} />
        <div className="grid gap-6 lg:grid-cols-2">
          <TrialSignalPanel />
          <ResistanceWatchPanel />
        </div>
        <ExternalDataSourcesPanel dataSources={dataSources} status={systemStatus} />
        <ReportBuilder selectedRole={selectedRole} />
      </main>
    </div>
  );
}
