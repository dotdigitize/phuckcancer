INSERT INTO cancer_records (record_id, study, cancer_type, sample_group, human_review_status) VALUES
('synthetic-luad-cohort-001', 'Synthetic Lung Cancer Research Fixture', 'Lung adenocarcinoma', 'LUAD synthetic cohort A', 'needs_human_review'),
('synthetic-brca-cohort-001', 'Synthetic Breast Cancer Research Fixture', 'Breast cancer', 'BRCA synthetic cohort B', 'needs_human_review');

INSERT INTO genomic_alterations (record_id, gene, sample_id, cancer_type, alteration_type, variant, mutation_class, pathway) VALUES
('synthetic-luad-cohort-001', 'EGFR', 'SYN-LUAD-001', 'Lung adenocarcinoma', 'mutation', 'L858R', 'missense', 'EGFR signaling'),
('synthetic-luad-cohort-001', 'KRAS', 'SYN-LUAD-002', 'Lung adenocarcinoma', 'mutation', 'G12C', 'missense', 'MAPK pathway'),
('synthetic-brca-cohort-001', 'TP53', 'SYN-BRCA-001', 'Breast cancer', 'mutation', 'R175H', 'missense', 'Cell cycle regulation');

INSERT INTO molecular_evidence (evidence_id, gene, cancer_type, evidence_type, summary, source, confidence_note, support_status) VALUES
('ev-egfr-001', 'EGFR', 'Lung adenocarcinoma', 'mutation_pathway', 'EGFR pathway alteration is a molecular evidence record for research review.', 'Synthetic reference corpus', 'Synthetic research fixture; not patient data.', 'partially_supported'),
('ev-brca1-001', 'BRCA1', 'Breast cancer', 'dna_repair_signal', 'BRCA1 loss is tracked as a DNA repair pathway evidence signal.', 'Synthetic reference corpus', 'Synthetic research fixture; not patient data.', 'partially_supported');

INSERT INTO mammal_model_registry (
  task_type,
  provider,
  base_model_id,
  tokenizer_id,
  checkpoint_source,
  checkpoint_model_id,
  checkpoint_path,
  norm_y_mean,
  norm_y_std,
  official_example_script,
  hf_model_url,
  enabled,
  notes
) VALUES
('cell_line_drug_response', 'official_script', 'ibm/biomed.omics.bl.sm.ma-ted-458m', 'ibm/biomed.omics.bl.sm.ma-ted-458m', 'huggingface_or_local_path', NULL, NULL, NULL, NULL, 'mammal/examples/cell_line_drug_response/main_infer.py', 'https://huggingface.co/models?other=base_model:finetune:ibm-research/biomed.omics.bl.sm.ma-ted-458m&search=cell_line_drug_response', FALSE, 'Demo registry row. Configure a fine-tuned checkpoint path or Hugging Face checkpoint ID before running this downstream task.'),
('drug_target_interaction', 'official_script', 'ibm/biomed.omics.bl.sm.ma-ted-458m', 'ibm/biomed.omics.bl.sm.ma-ted-458m', 'huggingface_or_local_path', NULL, NULL, NULL, NULL, 'mammal/examples/dti_bindingdb_kd/main_infer.py', 'https://huggingface.co/models?other=base_model:finetune:ibm-research/biomed.omics.bl.sm.ma-ted-458m&search=drug_target_interaction', FALSE, 'Demo registry row. DTI requires a fine-tuned checkpoint, matching tokenizer, and norm_y_mean/norm_y_std.');
