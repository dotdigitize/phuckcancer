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
CREATE TABLE IF NOT EXISTS mammal_interpretations (id BIGINT PRIMARY KEY AUTO_INCREMENT, interpretation_id VARCHAR(128) NOT NULL, model_name VARCHAR(255), fallback_used BOOLEAN NOT NULL DEFAULT TRUE, interpretation LONGTEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS extracted_claims (id BIGINT PRIMARY KEY AUTO_INCREMENT, claim_id VARCHAR(128), claim_text TEXT NOT NULL, gene VARCHAR(64), pathway VARCHAR(255), source VARCHAR(255)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS evidence_matches (id BIGINT PRIMARY KEY AUTO_INCREMENT, claim_id VARCHAR(128), evidence_id VARCHAR(128), support_status VARCHAR(64), support_score DECIMAL(5,2), rationale TEXT) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS risk_flags (id BIGINT PRIMARY KEY AUTO_INCREMENT, flag VARCHAR(128) NOT NULL, claim_id VARCHAR(128), note TEXT) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS trial_signals (id BIGINT PRIMARY KEY AUTO_INCREMENT, title VARCHAR(255), biomarker VARCHAR(255), cancer_type VARCHAR(255), evidence_status VARCHAR(128), human_review_status VARCHAR(128)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS resistance_signals (id BIGINT PRIMARY KEY AUTO_INCREMENT, cancer_type VARCHAR(255), treatment_category VARCHAR(255), gene_pathway VARCHAR(255), signal TEXT, support_status VARCHAR(128)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS external_data_sources (id BIGINT PRIMARY KEY AUTO_INCREMENT, source_name VARCHAR(255), enabled BOOLEAN, base_url VARCHAR(500), compliance_note TEXT) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS cbioportal_imports (id BIGINT PRIMARY KEY AUTO_INCREMENT, base_url VARCHAR(500), study_id VARCHAR(255), sample_list_id VARCHAR(255), molecular_profile_id VARCHAR(255), import_status VARCHAR(128), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS reports (id BIGINT PRIMARY KEY AUTO_INCREMENT, report_type VARCHAR(128), path VARCHAR(500), review_status VARCHAR(128), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS human_reviews (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_type VARCHAR(128), subject_id VARCHAR(128), review_status VARCHAR(128), reviewer_note TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
