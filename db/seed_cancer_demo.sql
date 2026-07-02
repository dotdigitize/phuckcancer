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

INSERT INTO drug_library (
  drug_name,
  brand_names,
  drug_class,
  mechanism_summary,
  smiles,
  known_targets,
  cancer_contexts,
  resistance_notes,
  trial_notes,
  evidence_notes,
  source_label,
  synthetic_fixture
) VALUES
('Vemurafenib', JSON_ARRAY(), 'BRAF inhibitor', 'Synthetic fixture for BRAF pathway evidence organization. Add sourced SMILES before MAMMAL chemistry tasks.', NULL, JSON_ARRAY('BRAF'), JSON_ARRAY('Melanoma'), 'Synthetic fixture resistance note; replace with sourced evidence.', 'Synthetic fixture trial note; replace with sourced evidence.', 'Synthetic research fixture; no MAMMAL result is included.', 'Synthetic research fixture', TRUE),
('Osimertinib', JSON_ARRAY(), 'EGFR inhibitor', 'Synthetic fixture for EGFR pathway evidence organization. Add sourced SMILES before MAMMAL chemistry tasks.', NULL, JSON_ARRAY('EGFR'), JSON_ARRAY('Lung adenocarcinoma'), 'Synthetic fixture resistance note; replace with sourced evidence.', 'Synthetic fixture trial note; replace with sourced evidence.', 'Synthetic research fixture; no drug response score is included.', 'Synthetic research fixture', TRUE),
('Imatinib', JSON_ARRAY(), 'Tyrosine kinase inhibitor', 'Synthetic fixture for kinase target evidence organization. Add sourced SMILES before MAMMAL chemistry tasks.', NULL, JSON_ARRAY('ABL1', 'KIT', 'PDGFRA'), JSON_ARRAY('Leukemia', 'Gastrointestinal stromal tumor'), 'Synthetic fixture resistance note; replace with sourced evidence.', 'Synthetic fixture trial note; replace with sourced evidence.', 'Synthetic research fixture.', 'Synthetic research fixture', TRUE),
('Sotorasib', JSON_ARRAY(), 'KRAS G12C inhibitor', 'Synthetic fixture for KRAS pathway evidence organization. Add sourced SMILES before MAMMAL chemistry tasks.', NULL, JSON_ARRAY('KRAS'), JSON_ARRAY('Lung adenocarcinoma', 'Colorectal cancer'), 'Synthetic fixture resistance note; replace with sourced evidence.', 'Synthetic fixture trial note; replace with sourced evidence.', 'Synthetic research fixture.', 'Synthetic research fixture', TRUE),
('Trastuzumab style biologic', JSON_ARRAY(), 'HER2-directed biologic', 'Synthetic biologic-style fixture. No SMILES is supplied unless a valid structured representation is added.', NULL, JSON_ARRAY('ERBB2'), JSON_ARRAY('Breast cancer'), 'Synthetic fixture resistance note; replace with sourced evidence.', 'Synthetic fixture trial note; replace with sourced evidence.', 'Synthetic research fixture.', 'Synthetic research fixture', TRUE);

INSERT INTO drug_targets (
  target_name,
  gene_symbol,
  protein_name,
  protein_sequence,
  pathway,
  cancer_context,
  notes,
  source_label,
  synthetic_fixture
) VALUES
('EGFR', 'EGFR', 'Epidermal growth factor receptor', NULL, 'EGFR signaling', 'Lung adenocarcinoma', 'Synthetic fixture. Protein sequence intentionally omitted until supplied from a trusted source.', 'Synthetic research fixture', TRUE),
('BRAF', 'BRAF', 'B-Raf proto-oncogene serine/threonine-protein kinase', NULL, 'MAPK pathway', 'Melanoma', 'Synthetic fixture. Protein sequence intentionally omitted until supplied from a trusted source.', 'Synthetic research fixture', TRUE),
('KRAS', 'KRAS', 'KRAS proto-oncogene GTPase', NULL, 'MAPK pathway', 'Lung adenocarcinoma', 'Synthetic fixture. Protein sequence intentionally omitted until supplied from a trusted source.', 'Synthetic research fixture', TRUE),
('HER2/ERBB2', 'ERBB2', 'Receptor tyrosine-protein kinase erbB-2', NULL, 'ERBB signaling', 'Breast cancer', 'Synthetic fixture. Protein sequence intentionally omitted until supplied from a trusted source.', 'Synthetic research fixture', TRUE),
('ALK', 'ALK', 'ALK receptor tyrosine kinase', NULL, 'ALK signaling', 'Lung adenocarcinoma', 'Synthetic fixture. Protein sequence intentionally omitted until supplied from a trusted source.', 'Synthetic research fixture', TRUE);

INSERT INTO cancer_contexts (cancer_type, subtype, biomarker, pathway, notes, synthetic_fixture) VALUES
('Lung adenocarcinoma', 'Synthetic LUAD fixture', 'EGFR / KRAS / ALK review context', 'RTK / MAPK signaling', 'Synthetic research fixture; no patient data.', TRUE),
('Melanoma', 'Synthetic melanoma fixture', 'BRAF pathway review context', 'MAPK pathway', 'Synthetic research fixture; no patient data.', TRUE),
('Breast cancer', 'Synthetic breast cancer fixture', 'HER2/ERBB2 review context', 'ERBB signaling', 'Synthetic research fixture; no patient data.', TRUE),
('Colorectal cancer', 'Synthetic colorectal fixture', 'KRAS pathway review context', 'MAPK pathway', 'Synthetic research fixture; no patient data.', TRUE);
