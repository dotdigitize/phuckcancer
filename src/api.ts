export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8717';

export type UserRole = 'patient_family' | 'doctor_tumor_board' | 'cancer_researcher' | 'data_engineer';

export const roleLabels: Record<UserRole, string> = {
  patient_family: 'Patient or family member',
  doctor_tumor_board: 'Doctor or tumor board reviewer',
  cancer_researcher: 'Cancer researcher',
  data_engineer: 'Data engineer or system administrator'
};
