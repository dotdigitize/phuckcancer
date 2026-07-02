import { useEffect, useState } from 'react';
import { API_BASE_URL } from '../api';

export default function MammalModelRegistryPanel() {
  const [registry, setRegistry] = useState<any>(null);
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/mammal/model-registry`).then((res) => res.json()).then(setRegistry).catch(() => setRegistry(null));
  }, []);
  const models = registry?.models || [];
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[720px] text-left text-sm">
        <thead className="border-b border-slate-200 text-xs uppercase text-slate-500">
          <tr>
            <th className="py-2 pr-3">Task</th>
            <th className="py-2 pr-3">Provider</th>
            <th className="py-2 pr-3">Model path</th>
            <th className="py-2 pr-3">norm_y_mean</th>
            <th className="py-2 pr-3">norm_y_std</th>
            <th className="py-2 pr-3">Enabled</th>
          </tr>
        </thead>
        <tbody>
          {models.map((model: any) => (
            <tr key={`${model.task_type}-${model.provider}`} className="border-b border-slate-100">
              <td className="py-2 pr-3 font-semibold text-clinical-navy">{model.task_type}</td>
              <td className="py-2 pr-3">{model.provider}</td>
              <td className="py-2 pr-3">{model.model_path || 'not configured'}</td>
              <td className="py-2 pr-3">{model.norm_y_mean ?? 'not configured'}</td>
              <td className="py-2 pr-3">{model.norm_y_std ?? 'not configured'}</td>
              <td className="py-2 pr-3">{model.enabled ? 'yes' : 'no'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
