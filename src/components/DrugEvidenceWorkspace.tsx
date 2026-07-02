import { useEffect, useState } from 'react';
import { API_BASE_URL, type CancerContextRecord, type DrugRecord, type DrugTargetRecord, type UserRole } from '../api';
import CancerContextPanel from './CancerContextPanel';
import DrugComparisonBuilder from './DrugComparisonBuilder';
import DrugComparisonMatrix from './DrugComparisonMatrix';
import DrugComparisonReportPanel from './DrugComparisonReportPanel';
import DrugLibraryPanel from './DrugLibraryPanel';
import DrugTargetPanel from './DrugTargetPanel';

type Props = { selectedRole: UserRole | ''; systemStatus: any };

const toggleValue = <T,>(values: T[], value: T) => (values.includes(value) ? values.filter((item) => item !== value) : [...values, value]);

export default function DrugEvidenceWorkspace({ selectedRole, systemStatus }: Props) {
  const [drugs, setDrugs] = useState<DrugRecord[]>([]);
  const [targets, setTargets] = useState<DrugTargetRecord[]>([]);
  const [contexts, setContexts] = useState<CancerContextRecord[]>([]);
  const [drugSearch, setDrugSearch] = useState('');
  const [targetSearch, setTargetSearch] = useState('');
  const [selectedDrugIds, setSelectedDrugIds] = useState<number[]>([]);
  const [selectedTargetIds, setSelectedTargetIds] = useState<number[]>([]);
  const [selectedContextIds, setSelectedContextIds] = useState<number[]>([]);
  const [comparisonName, setComparisonName] = useState('BRAF drug comparison');
  const [taskTypes, setTaskTypes] = useState<string[]>(['drug_target_interaction']);
  const [cellLineName, setCellLineName] = useState('');
  const [h5adFileRef, setH5adFileRef] = useState('');
  const [comparisonId, setComparisonId] = useState<number | null>(null);
  const [requirements, setRequirements] = useState<any>(null);
  const [matrix, setMatrix] = useState<any>(null);
  const [explanation, setExplanation] = useState<any>(null);
  const [report, setReport] = useState<any>(null);

  const load = () => {
    fetch(`${API_BASE_URL}/api/drugs?search=${encodeURIComponent(drugSearch)}`).then((res) => res.json()).then((body) => setDrugs(body.drugs || [])).catch(() => setDrugs([]));
    fetch(`${API_BASE_URL}/api/drug-targets?search=${encodeURIComponent(targetSearch)}`).then((res) => res.json()).then((body) => setTargets(body.targets || [])).catch(() => setTargets([]));
    fetch(`${API_BASE_URL}/api/cancer-contexts`).then((res) => res.json()).then((body) => setContexts(body.contexts || [])).catch(() => setContexts([]));
  };

  useEffect(load, [drugSearch, targetSearch]);

  const createComparison = async () => {
    const response = await fetch(`${API_BASE_URL}/api/drug-comparisons`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        comparison_name: comparisonName,
        drug_ids: selectedDrugIds,
        target_ids: selectedTargetIds,
        cancer_context_ids: selectedContextIds,
        task_types: taskTypes,
        cell_line_names: cellLineName ? [cellLineName] : [],
        h5ad_file_refs: h5adFileRef ? [h5adFileRef] : []
      })
    });
    const body = await response.json();
    setComparisonId(body.comparison?.comparison_id || null);
    setRequirements(body.requirements || body);
    if (body.comparison?.comparison_id) {
      const matrixResponse = await fetch(`${API_BASE_URL}/api/drug-comparisons/${body.comparison.comparison_id}/matrix`);
      setMatrix(await matrixResponse.json());
    }
  };

  const runComparison = async () => {
    const id = comparisonId;
    if (!id) {
      await createComparison();
      return;
    }
    const response = await fetch(`${API_BASE_URL}/api/drug-comparisons/${id}/run`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) });
    const body = await response.json();
    if (body.missing_structured_data) {
      setRequirements(body);
    }
    const matrixResponse = await fetch(`${API_BASE_URL}/api/drug-comparisons/${id}/matrix`);
    setMatrix(await matrixResponse.json());
  };

  const explain = async () => {
    if (!comparisonId) return;
    const response = await fetch(`${API_BASE_URL}/api/drug-comparisons/${comparisonId}/explain`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_role: selectedRole })
    });
    setExplanation(await response.json());
  };

  const generateReport = async () => {
    if (!comparisonId) return;
    const response = await fetch(`${API_BASE_URL}/api/drug-comparisons/${comparisonId}/report`, { method: 'POST' });
    setReport(await response.json());
  };

  const exportJson = () => {
    const data = JSON.stringify(matrix || {}, null, 2);
    window.open(`data:application/json;charset=utf-8,${encodeURIComponent(data)}`);
  };

  const exportMarkdown = () => {
    const data = report?.markdown || '# Drug Evidence Comparison\n\nGenerate a report first.\n';
    window.open(`data:text/markdown;charset=utf-8,${encodeURIComponent(data)}`);
  };

  return (
    <section className="space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h2 className="text-2xl font-bold text-clinical-navy">Drug Evidence Workspace</h2>
        <p className="mt-2 max-w-5xl text-sm leading-6 text-slate-700">
          Compare cancer drugs across molecular targets, cancer contexts, MAMMAL task outputs, resistance notes, clinical-trial notes, and evidence organization scores.
        </p>
      </div>
      <div className="grid gap-6 xl:grid-cols-2">
        <DrugLibraryPanel drugs={drugs} selectedDrugIds={selectedDrugIds} search={drugSearch} onSearch={setDrugSearch} onToggle={(id) => setSelectedDrugIds(toggleValue(selectedDrugIds, id))} onRefresh={load} />
        <DrugTargetPanel targets={targets} selectedTargetIds={selectedTargetIds} search={targetSearch} onSearch={setTargetSearch} onToggle={(id) => setSelectedTargetIds(toggleValue(selectedTargetIds, id))} />
      </div>
      <CancerContextPanel contexts={contexts} selectedContextIds={selectedContextIds} onToggle={(id) => setSelectedContextIds(toggleValue(selectedContextIds, id))} />
      <DrugComparisonBuilder comparisonName={comparisonName} taskTypes={taskTypes} cellLineName={cellLineName} h5adFileRef={h5adFileRef} requirements={requirements} providerStatus={systemStatus} onNameChange={setComparisonName} onTaskToggle={(task) => setTaskTypes(toggleValue(taskTypes, task))} onCellLineChange={setCellLineName} onH5adChange={setH5adFileRef} onCreate={createComparison} onRun={runComparison} />
      <DrugComparisonMatrix matrix={matrix} />
      <DrugComparisonReportPanel selectedRole={selectedRole} explanation={explanation} report={report} onExplain={explain} onReport={generateReport} onExportJson={exportJson} onExportMarkdown={exportMarkdown} />
    </section>
  );
}
