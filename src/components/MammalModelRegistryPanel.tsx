import { useEffect, useState } from 'react';
import { API_BASE_URL } from '../api';

export default function MammalModelRegistryPanel() {
  const [registry, setRegistry] = useState<any>(null);
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/mammal/model-registry`).then((res) => res.json()).then(setRegistry).catch(() => setRegistry(null));
  }, []);
  const models = registry?.models || [];
  return (
    <div className="space-y-4">
      <div className="border border-amber-200 bg-amber-50 p-3 text-sm text-amber-900" style={{ borderRadius: 8 }}>
        Some MAMMAL downstream tasks require fine-tuned checkpoints and matching tokenizers. The base MAMMAL model alone may not be sufficient for every task.
      </div>
      <div className="grid gap-3 text-sm text-slate-700 md:grid-cols-2">
        <div><span className="font-semibold text-slate-500">Base model ID:</span> {registry?.base_model_id || 'not configured'}</div>
        <div><span className="font-semibold text-slate-500">Tokenizer ID:</span> {registry?.base_tokenizer_id || 'not configured'}</div>
        <div>
          <span className="font-semibold text-slate-500">Official repository URL:</span>{' '}
          {registry?.official_repo_url ? <a className="text-clinical-blue underline" href={registry.official_repo_url} target="_blank" rel="noreferrer">{registry.official_repo_url}</a> : 'not configured'}
        </div>
        <div>
          <span className="font-semibold text-slate-500">Fine-tuned checkpoint source:</span>{' '}
          {registry?.hf_finetuned_models_url ? <a className="text-clinical-blue underline" href={registry.hf_finetuned_models_url} target="_blank" rel="noreferrer">Hugging Face checkpoint index</a> : 'not configured'}
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[1180px] text-left text-sm">
          <thead className="border-b border-slate-200 text-xs uppercase text-slate-500">
            <tr>
              <th className="py-2 pr-3">Task type</th>
              <th className="py-2 pr-3">Provider</th>
              <th className="py-2 pr-3">Base model ID</th>
              <th className="py-2 pr-3">Tokenizer ID</th>
              <th className="py-2 pr-3">Checkpoint source</th>
              <th className="py-2 pr-3">HF model/checkpoint link</th>
              <th className="py-2 pr-3">Local checkpoint path</th>
              <th className="py-2 pr-3">norm_y_mean</th>
              <th className="py-2 pr-3">norm_y_std</th>
              <th className="py-2 pr-3">Enabled</th>
            </tr>
          </thead>
          <tbody>
            {models.map((model: any) => (
              <tr key={`${model.task_type}-${model.provider}`} className="border-b border-slate-100 align-top">
                <td className="py-2 pr-3 font-semibold text-clinical-navy">{model.task_type}</td>
                <td className="py-2 pr-3">{model.provider}</td>
                <td className="py-2 pr-3">{model.base_model_id || 'not configured'}</td>
                <td className="py-2 pr-3">{model.tokenizer_id || 'not configured'}</td>
                <td className="py-2 pr-3">{model.checkpoint_source || 'not configured'}</td>
                <td className="py-2 pr-3">
                  {model.hf_model_url ? <a className="text-clinical-blue underline" href={model.hf_model_url} target="_blank" rel="noreferrer">{model.checkpoint_model_id || 'Hugging Face link'}</a> : 'not configured'}
                </td>
                <td className="py-2 pr-3">{model.checkpoint_path || model.model_path || 'not configured'}</td>
                <td className="py-2 pr-3">{model.norm_y_mean ?? 'not required/configured'}</td>
                <td className="py-2 pr-3">{model.norm_y_std ?? 'not required/configured'}</td>
                <td className="py-2 pr-3">{model.enabled ? 'yes' : 'no'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
