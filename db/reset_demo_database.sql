DROP TABLE IF EXISTS human_reviews, reports, cbioportal_imports, external_data_sources, resistance_signals, trial_signals, risk_flags, evidence_matches, extracted_claims, mammal_interpretations, pathways, molecular_evidence, genomic_alterations, cancer_records;
SOURCE db/schema.sql;
SOURCE db/seed_cancer_demo.sql;
