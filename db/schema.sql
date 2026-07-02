CREATE TABLE IF NOT EXISTS cancer_records (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  record_id VARCHAR(128) NOT NULL UNIQUE,
  study VARCHAR(255) NOT NULL,
  cancer_type VARCHAR(255) NOT NULL,
  sample_group VARCHAR(255) NOT NULL,
  human_review_status VARCHAR(64) NOT NULL DEFAULT 'needs_human_review',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS genomic_alterations (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  record_id VARCHAR(128) NOT NULL,
  gene VARCHAR(64) NOT NULL,
  sample_id VARCHAR(128) NOT NULL,
  cancer_type VARCHAR(255) NOT NULL,
  alteration_type VARCHAR(64) NOT NULL,
  variant VARCHAR(128),
  mutation_class VARCHAR(128),
  copy_number_alteration VARCHAR(128),
  expression_signal VARCHAR(128),
  pathway VARCHAR(255),
  INDEX idx_gene (gene),
  INDEX idx_record_id (record_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS molecular_evidence (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  evidence_id VARCHAR(128) NOT NULL UNIQUE,
  gene VARCHAR(64) NOT NULL,
  cancer_type VARCHAR(255) NOT NULL,
  evidence_type VARCHAR(128) NOT NULL,
  summary TEXT NOT NULL,
  source VARCHAR(255) NOT NULL,
  confidence_note TEXT,
  support_status VARCHAR(64) NOT NULL DEFAULT 'needs_human_review',
  INDEX idx_evidence_gene (gene)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS pathways (id BIGINT PRIMARY KEY AUTO_INCREMENT, pathway VARCHAR(255) NOT NULL, category VARCHAR(255), evidence_notes TEXT) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS mammal_interpretations (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  interpretation_id VARCHAR(128) NOT NULL,
  provider VARCHAR(32) NOT NULL,
  model_name VARCHAR(255),
  biological_interpretation LONGTEXT,
  molecular_signal TEXT,
  pathway_context TEXT,
  evidence_strength TEXT,
  uncertainty TEXT,
  review_questions JSON,
  raw_mammal_output JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_mammal_provider (provider)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS mammal_model_registry (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  task_type VARCHAR(128) NOT NULL,
  provider VARCHAR(32) NOT NULL,
  base_model_id VARCHAR(255),
  tokenizer_id VARCHAR(255),
  checkpoint_source VARCHAR(128),
  checkpoint_model_id VARCHAR(255),
  checkpoint_path VARCHAR(1000),
  norm_y_mean DOUBLE,
  norm_y_std DOUBLE,
  official_example_script VARCHAR(1000),
  hf_model_url VARCHAR(1000),
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_mammal_model_registry_task (task_type),
  INDEX idx_mammal_model_registry_provider (provider)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS mammal_task_runs (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  task_type VARCHAR(128) NOT NULL,
  provider VARCHAR(32) NOT NULL,
  status VARCHAR(64) NOT NULL,
  model_registry_id BIGINT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_mammal_task_runs_task (task_type),
  INDEX idx_mammal_task_runs_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS mammal_task_inputs (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  task_run_id BIGINT NOT NULL,
  input_json JSON NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_mammal_task_inputs_run (task_run_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS mammal_task_outputs (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  task_run_id BIGINT NOT NULL,
  output_json JSON NOT NULL,
  raw_mammal_output JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_mammal_task_outputs_run (task_run_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS mammal_task_errors (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  task_run_id BIGINT,
  error_code VARCHAR(128) NOT NULL,
  message TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_mammal_task_errors_code (error_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS mammal_uploaded_files (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  task_type VARCHAR(128),
  original_filename VARCHAR(500),
  stored_path VARCHAR(1000) NOT NULL,
  content_type VARCHAR(255),
  file_size_bytes BIGINT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_mammal_uploaded_files_task (task_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS extracted_claims (id BIGINT PRIMARY KEY AUTO_INCREMENT, claim_id VARCHAR(128), claim_text TEXT NOT NULL, gene VARCHAR(64), pathway VARCHAR(255), source VARCHAR(255)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS evidence_matches (id BIGINT PRIMARY KEY AUTO_INCREMENT, claim_id VARCHAR(128), evidence_id VARCHAR(128), support_status VARCHAR(64), support_score DECIMAL(5,2), rationale TEXT) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS risk_flags (id BIGINT PRIMARY KEY AUTO_INCREMENT, flag VARCHAR(128) NOT NULL, claim_id VARCHAR(128), note TEXT) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS trial_signals (id BIGINT PRIMARY KEY AUTO_INCREMENT, title VARCHAR(255), biomarker VARCHAR(255), cancer_type VARCHAR(255), evidence_status VARCHAR(128), human_review_status VARCHAR(128)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS resistance_signals (id BIGINT PRIMARY KEY AUTO_INCREMENT, cancer_type VARCHAR(255), treatment_category VARCHAR(255), gene_pathway VARCHAR(255), signal TEXT, support_status VARCHAR(128)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS external_data_sources (id BIGINT PRIMARY KEY AUTO_INCREMENT, source_name VARCHAR(255), enabled BOOLEAN, base_url VARCHAR(500), compliance_note TEXT) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS cbioportal_imports (id BIGINT PRIMARY KEY AUTO_INCREMENT, base_url VARCHAR(500), study_id VARCHAR(255), sample_list_id VARCHAR(255), molecular_profile_id VARCHAR(255), import_status VARCHAR(128), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS reports (id BIGINT PRIMARY KEY AUTO_INCREMENT, report_type VARCHAR(128), path VARCHAR(500), review_status VARCHAR(128), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS human_reviews (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_type VARCHAR(128), subject_id VARCHAR(128), review_status VARCHAR(128), reviewer_note TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS assistant_sessions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_role VARCHAR(64) NOT NULL,
  model_name VARCHAR(255),
  source_type VARCHAR(128),
  safety_constraints JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_assistant_user_role (user_role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS user_role_preferences (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  preference_key VARCHAR(128) NOT NULL UNIQUE,
  user_role VARCHAR(64) NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_role_preference (user_role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS drug_library (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  drug_name VARCHAR(255) NOT NULL,
  brand_names JSON,
  drug_class VARCHAR(255),
  mechanism_summary TEXT,
  smiles TEXT,
  known_targets JSON,
  cancer_contexts JSON,
  resistance_notes TEXT,
  trial_notes TEXT,
  evidence_notes TEXT,
  source_label VARCHAR(500) NOT NULL,
  source_url VARCHAR(1000),
  synthetic_fixture BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_drug_library_name (drug_name),
  INDEX idx_drug_library_class (drug_class),
  INDEX idx_drug_library_fixture (synthetic_fixture)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS drug_targets (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  target_name VARCHAR(255) NOT NULL,
  gene_symbol VARCHAR(128),
  protein_name VARCHAR(500),
  protein_sequence LONGTEXT,
  pathway VARCHAR(255),
  cancer_context VARCHAR(255),
  notes TEXT,
  source_label VARCHAR(500) NOT NULL,
  synthetic_fixture BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_drug_targets_name (target_name),
  INDEX idx_drug_targets_gene (gene_symbol),
  INDEX idx_drug_targets_pathway (pathway),
  INDEX idx_drug_targets_fixture (synthetic_fixture)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS cancer_contexts (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  cancer_type VARCHAR(255) NOT NULL,
  subtype VARCHAR(255),
  biomarker VARCHAR(255),
  pathway VARCHAR(255),
  notes TEXT,
  synthetic_fixture BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_cancer_context_type (cancer_type),
  INDEX idx_cancer_context_biomarker (biomarker),
  INDEX idx_cancer_context_pathway (pathway),
  INDEX idx_cancer_context_fixture (synthetic_fixture)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS drug_target_links (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  drug_id BIGINT NOT NULL,
  target_id BIGINT NOT NULL,
  relationship_label VARCHAR(255),
  source_label VARCHAR(500),
  synthetic_fixture BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_drug_target_link (drug_id, target_id),
  CONSTRAINT fk_drug_target_links_drug FOREIGN KEY (drug_id) REFERENCES drug_library(id) ON DELETE CASCADE,
  CONSTRAINT fk_drug_target_links_target FOREIGN KEY (target_id) REFERENCES drug_targets(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS drug_cancer_context_links (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  drug_id BIGINT NOT NULL,
  cancer_context_id BIGINT NOT NULL,
  relationship_label VARCHAR(255),
  source_label VARCHAR(500),
  synthetic_fixture BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_drug_context_link (drug_id, cancer_context_id),
  CONSTRAINT fk_drug_context_links_drug FOREIGN KEY (drug_id) REFERENCES drug_library(id) ON DELETE CASCADE,
  CONSTRAINT fk_drug_context_links_context FOREIGN KEY (cancer_context_id) REFERENCES cancer_contexts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS drug_resistance_notes (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  drug_id BIGINT NOT NULL,
  cancer_context_id BIGINT,
  note_text TEXT NOT NULL,
  source_label VARCHAR(500) NOT NULL,
  synthetic_fixture BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_drug_resistance_drug (drug_id),
  CONSTRAINT fk_drug_resistance_drug FOREIGN KEY (drug_id) REFERENCES drug_library(id) ON DELETE CASCADE,
  CONSTRAINT fk_drug_resistance_context FOREIGN KEY (cancer_context_id) REFERENCES cancer_contexts(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS drug_trial_notes (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  drug_id BIGINT NOT NULL,
  cancer_context_id BIGINT,
  note_text TEXT NOT NULL,
  source_label VARCHAR(500) NOT NULL,
  source_url VARCHAR(1000),
  synthetic_fixture BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_drug_trial_drug (drug_id),
  CONSTRAINT fk_drug_trial_drug FOREIGN KEY (drug_id) REFERENCES drug_library(id) ON DELETE CASCADE,
  CONSTRAINT fk_drug_trial_context FOREIGN KEY (cancer_context_id) REFERENCES cancer_contexts(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS drug_comparison_runs (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  comparison_name VARCHAR(255) NOT NULL,
  task_types JSON NOT NULL,
  cell_line_names JSON,
  h5ad_file_refs JSON,
  status VARCHAR(64) NOT NULL DEFAULT 'prepared',
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_drug_comparison_status (status),
  INDEX idx_drug_comparison_name (comparison_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS drug_comparison_items (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  comparison_id BIGINT NOT NULL,
  drug_id BIGINT NOT NULL,
  target_id BIGINT,
  cancer_context_id BIGINT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_drug_comparison_items_comparison (comparison_id),
  CONSTRAINT fk_drug_comparison_items_run FOREIGN KEY (comparison_id) REFERENCES drug_comparison_runs(id) ON DELETE CASCADE,
  CONSTRAINT fk_drug_comparison_items_drug FOREIGN KEY (drug_id) REFERENCES drug_library(id) ON DELETE CASCADE,
  CONSTRAINT fk_drug_comparison_items_target FOREIGN KEY (target_id) REFERENCES drug_targets(id) ON DELETE SET NULL,
  CONSTRAINT fk_drug_comparison_items_context FOREIGN KEY (cancer_context_id) REFERENCES cancer_contexts(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS drug_comparison_results (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  comparison_id BIGINT NOT NULL,
  item_id BIGINT,
  task_type VARCHAR(128) NOT NULL,
  status VARCHAR(64) NOT NULL,
  mammal_task_run_id BIGINT,
  result_json JSON,
  missing_structured_data JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_drug_comparison_results_comparison (comparison_id),
  INDEX idx_drug_comparison_results_task (task_type),
  CONSTRAINT fk_drug_comparison_results_run FOREIGN KEY (comparison_id) REFERENCES drug_comparison_runs(id) ON DELETE CASCADE,
  CONSTRAINT fk_drug_comparison_results_item FOREIGN KEY (item_id) REFERENCES drug_comparison_items(id) ON DELETE SET NULL,
  CONSTRAINT fk_drug_comparison_results_mammal_run FOREIGN KEY (mammal_task_run_id) REFERENCES mammal_task_runs(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS drug_evidence_scores (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  comparison_id BIGINT NOT NULL,
  item_id BIGINT,
  response_signal_score DECIMAL(6,3),
  binding_signal_score DECIMAL(6,3),
  carcinogenicity_flag BOOLEAN NOT NULL DEFAULT FALSE,
  resistance_flag BOOLEAN NOT NULL DEFAULT FALSE,
  evidence_support_score DECIMAL(6,3),
  data_completeness_score DECIMAL(6,3) NOT NULL DEFAULT 0,
  uncertainty_score DECIMAL(6,3) NOT NULL DEFAULT 1,
  overall_review_priority VARCHAR(64) NOT NULL,
  explanation_summary TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_drug_scores_comparison (comparison_id),
  INDEX idx_drug_scores_priority (overall_review_priority),
  CONSTRAINT fk_drug_scores_run FOREIGN KEY (comparison_id) REFERENCES drug_comparison_runs(id) ON DELETE CASCADE,
  CONSTRAINT fk_drug_scores_item FOREIGN KEY (item_id) REFERENCES drug_comparison_items(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS drug_comparison_reports (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  comparison_id BIGINT NOT NULL,
  report_type VARCHAR(128) NOT NULL,
  report_markdown LONGTEXT,
  report_json JSON,
  output_path VARCHAR(1000),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_drug_reports_comparison (comparison_id),
  CONSTRAINT fk_drug_reports_run FOREIGN KEY (comparison_id) REFERENCES drug_comparison_runs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
