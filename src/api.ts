export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8717';

export type UserRole = 'patient_family' | 'doctor_tumor_board' | 'cancer_researcher' | 'data_engineer';

export const roleLabels: Record<UserRole, string> = {
  patient_family: 'Patient or family member',
  doctor_tumor_board: 'Doctor or tumor board reviewer',
  cancer_researcher: 'Cancer researcher',
  data_engineer: 'Data engineer or system administrator'
};

export type DrugRecord = {
  id: number;
  drug_name: string;
  brand_names?: string[];
  drug_class?: string;
  mechanism_summary?: string;
  smiles?: string;
  known_targets?: string[];
  cancer_contexts?: string[];
  resistance_notes?: string;
  trial_notes?: string;
  evidence_notes?: string;
  source_label?: string;
  synthetic_fixture?: boolean;
};

export type DrugTargetRecord = {
  id: number;
  target_name: string;
  gene_symbol?: string;
  protein_name?: string;
  protein_sequence?: string;
  pathway?: string;
  cancer_context?: string;
  notes?: string;
  synthetic_fixture?: boolean;
};

export type CancerContextRecord = {
  id: number;
  cancer_type: string;
  subtype?: string;
  biomarker?: string;
  pathway?: string;
  notes?: string;
  synthetic_fixture?: boolean;
};
