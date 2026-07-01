# PhuckCancer

<img width="1536" height="1024" alt="jose perez phuck cancer research cure cancer" src="https://github.com/user-attachments/assets/7b4c17cb-3d4c-4c9c-a0ca-f57e7e907ece" />

PhuckCancer provides visualization, analysis, AI interpretation, evidence auditing, and human-reviewable reporting for large-scale cancer genomics, molecular evidence, mutation, pathway, treatment-response, and clinical-trial signal datasets.

It's really simple but powerful: 

Cancer data goes in.
MAMMAL compares it against its learned biological patterns.
MAMMAL outputs molecular interpretation.
PhuckCancer checks the evidence.
The local LLM explains it to humans.

Creator and author: Jose Perez. GitHub: dotdigitize. License: Apache License 2.0. Copyright 2026 Jose Perez.

PhuckCancer is the full cancer evidence platform. MAMMAL is the biomedical AI engine inside it. The local LLM is the plain-English assistant. The evidence portal is the interface doctors, researchers, patients, and families use. Optional external data connectors allow PhuckCancer to retrieve and normalize cancer genomics data from supported research portals and APIs.

## Core Mission

PhuckCancer exists to help doctors, researchers, patients, and families understand cancer evidence faster, organize it better, and fight cancer with stronger information.

The platform brings together cancer genomics data, molecular evidence, mutation and pathway analysis, a MAMMAL-powered biomedical AI engine, local LLM explanation, evidence auditing, optional external cancer genomics data retrieval, and human-reviewable reporting into one open-source cancer intelligence system.

PhuckCancer is not just a cancer data viewer and it is not just an AI chatbot. It is being built as a complete cancer research and evidence platform that can visualize cancer datasets, analyze molecular findings, route cancer evidence through MAMMAL-driven biomedical interpretation, explain complex medical language in plain English, flag unsupported claims, and produce reports that doctors, researchers, patients, and families can review together.

The goal is to make cancer information easier to see, easier to understand, easier to verify, and easier to act on with qualified medical professionals. Patients and families should not be lost inside confusing pathology reports, genomic test results, treatment notes, clinical-trial language, and scattered research data. Doctors and researchers should have better tools for reviewing cancer evidence, finding important signals, and explaining what matters.

## Who It Helps

- Doctors and tumor boards reviewing cancer evidence, molecular findings, and audit trails.
- Researchers organizing cancer research, tumor genomics, molecular evidence, clinical trial evidence, drug resistance, and precision oncology signals.
- Patients and families preparing better questions and family-friendly summaries for qualified medical review.

## Main Workflow

```text
Cancer genomics data, report text, molecular evidence, external connector data, or MAMMAL output
-> parser
-> cancer finding extraction
-> MAMMAL biomedical interpretation layer
-> claim extraction
-> evidence matching
-> support scoring
-> risk flagging
-> local LLM doctor or family explanation
-> human review status
-> Markdown/JSON report export
```

## Product Areas

PhuckCancer includes a cancer evidence portal, genomic alteration matrix, cancer pathway explorer, MAMMAL biomedical AI engine, local LLM patient and family assistant, evidence auditing, clinical-trial signal organizer, drug resistance signal watcher, optional cBioPortal data connector, and doctor/family report builder.

The MAMMAL research pipeline includes `app/mammal_engine.py`, `app/mammal_pipeline.py`, `app/mammal_importer.py`, `app/mammal_output_parser.py`, and `app/mammal_claim_extractor.py`. Tests pass without live MAMMAL installed by using deterministic fallback interpretation.

## How MAMMAL and the Local LLM Work Together

MAMMAL does not replace the normal local LLM. MAMMAL is the biomedical AI engine that reads cancer-related biological and molecular data. The local LLM is the explanation layer that turns the structured biomedical interpretation into language that doctors, researchers, patients, and families can understand.

The system is designed around this flow:

```text
Cancer data / molecular data
-> MAMMAL biomedical AI engine
-> structured biological interpretation
-> evidence audit and risk flagging
-> local LLM explanation
-> doctor report or family-friendly summary
```

MAMMAL is used to interpret biological meaning from data such as:

- Gene mutations such as TP53, KRAS, EGFR, BRAF, BRCA1, and BRCA2 alterations.
- Gene expression signals such as overexpression, underexpression, activation, or suppression.
- Pathway signals such as EGFR signaling, MAPK, PI3K/AKT, DNA repair, apoptosis, immune signaling, angiogenesis, and drug resistance pathways.
- Protein-related notes, molecular target information, and biological pathway evidence.
- Small molecule or drug-related evidence, including drug-target relationship notes when available.
- Cancer evidence notes from studies, reports, mutation records, pathway notes, resistance notes, and clinical-trial signal records.

MAMMAL should return structured biomedical interpretation, not a final treatment decision. Example structured output may look like this:

```json
{
  "gene": "KRAS",
  "variant": "G12C",
  "cancer_type": "lung adenocarcinoma",
  "pathway": "MAPK signaling",
  "biological_signal": "KRAS G12C may activate downstream MAPK pathway signaling.",
  "evidence_strength": "moderate",
  "uncertainty": "Requires clinical and molecular review.",
  "possible_research_questions": [
    "Is this alteration linked to treatment resistance?",
    "Are there co-mutations affecting interpretation?",
    "Is there trial evidence involving this biomarker?"
  ],
  "risk_flags": [
    "Do not treat this as a treatment recommendation without oncologist review."
  ]
}
```

The local LLM then explains that structured interpretation in the right mode.

For a doctor or researcher, the local LLM may produce a concise medical-review summary:

```text
KRAS G12C is a molecular alteration that may activate MAPK pathway signaling. The available evidence should be reviewed in the context of cancer type, co-mutations, stage, treatment history, prior resistance, available clinical guidelines, and clinical-trial evidence. This finding should be interpreted by the oncology team or molecular tumor board before it affects care decisions.
```

For a patient or family member, the local LLM may produce a plain-English explanation:

```text
This report mentions a change in a gene called KRAS. KRAS helps control cell growth signals. Some KRAS changes can matter in cancer care, but this result does not automatically mean one specific treatment is right. A good question to ask the oncologist is: “Does this KRAS mutation affect treatment options, resistance, or clinical trials for this cancer type?”
```

In one sentence: MAMMAL interprets the biological meaning of cancer genes, mutations, proteins, molecules, expression signals, pathways, and drug/evidence relationships; then the local LLM explains that interpretation clearly for doctors, researchers, patients, and families.

## How It Helps Doctors

For doctors, oncologists, molecular tumor boards, and researchers, PhuckCancer is designed to reduce the time it takes to review complex cancer evidence. The system can organize cancer genomics records, route molecular findings through the MAMMAL biomedical AI engine, extract claims, compare those claims against evidence, flag uncertainty, and generate doctor-reviewable reports.

A doctor-facing workflow may look like this:

```text
Cancer genomic report or external dataset
-> mutation and pathway extraction
-> MAMMAL biomedical interpretation
-> evidence matching
-> risk and uncertainty flags
-> tumor board style report
-> qualified medical review
```

The doctor report can help highlight:

- Which genes, variants, biomarkers, or pathways appear important.
- Whether a molecular finding may be connected to treatment response, resistance, or clinical-trial evidence.
- Whether the evidence is supported, partially supported, unsupported, contradicted, or missing.
- Whether a claim uses unsafe language such as overconfident treatment language or diagnostic overreach.
- What information may be missing from the report.
- What should be reviewed by an oncologist, pathologist, genetic counselor, tumor board, or research coordinator.

The system should not tell a doctor what treatment to choose. It should help organize the evidence so a qualified medical team can make a better-informed decision.

## How It Helps Patients and Families

For patients and families, PhuckCancer is designed to make cancer documents less confusing. A family member may not understand terms such as mutation, biomarker, pathway, amplification, deletion, drug resistance, immunotherapy, targeted therapy, clinical trial, or molecular tumor board. The local LLM assistant can explain those terms in plain English and help the family prepare better questions for the doctor.

A patient/family workflow may look like this:

```text
Pathology report, genomic test, oncology note, or trial description
-> plain-English explanation
-> important genes and findings summary
-> missing information checklist
-> questions to ask the doctor
-> family-friendly summary for medical review
```

The assistant can help families ask questions such as:

- What type of cancer is this and what stage is it?
- Did the test find any mutations or biomarkers that matter?
- Are any of these findings connected to targeted therapy, immunotherapy, resistance, or clinical trials?
- Should we ask about a molecular tumor board review?
- Is more testing needed to confirm this finding?
- Are there co-mutations that change the meaning of this result?
- What does this report not tell us?
- What should we ask at the next oncology appointment?

The patient/family assistant should never say “take this treatment.” It should say “ask your oncologist about this finding” or “this may be worth discussing with your care team.”

## Example: Family Question, Doctor Review, and Possible Care Change

This example is not a treatment recommendation. It shows how PhuckCancer could help a family ask better questions and help a doctor review evidence more quickly.

A family member may ask PhuckCancer:

```text
My mother’s lung cancer report says KRAS G12C. What does this mean, and what should we ask the doctor?
```

PhuckCancer may explain:

```text
KRAS is a gene involved in cell growth signaling. G12C is a specific KRAS alteration. Some KRAS alterations can matter in cancer care, but the meaning depends on the exact cancer type, stage, full molecular report, prior treatment history, co-mutations, and available clinical evidence. Ask the oncologist whether this KRAS G12C finding changes treatment options, clinical-trial options, or resistance review for this cancer type.
```

The family may then ask the oncologist:

```text
Does this KRAS G12C mutation change treatment options, clinical-trial options, or resistance concerns for this cancer type? Should this case be reviewed by a molecular tumor board?
```

A doctor might answer:

```text
This is an important molecular finding. We need to review it in the context of the full diagnosis, stage, prior treatments, co-mutations, pathology, performance status, and current clinical guidelines. We may order confirmatory testing, review the full genomic panel, check for other biomarkers, discuss this at a molecular tumor board, or consider whether targeted therapy, immunotherapy, chemotherapy, radiation, surgery, or a clinical trial is appropriate.
```

Depending on the cancer type, the full medical history, the full biomarker profile, and the doctor’s judgment, this kind of evidence review might lead to a care change such as:

- Ordering additional molecular testing.
- Confirming a biomarker or mutation with another test.
- Referring the case to a molecular tumor board.
- Reviewing targeted therapy options.
- Reviewing immunotherapy relevance.
- Reviewing clinical-trial options.
- Checking for drug resistance signals.
- Changing the treatment plan when the evidence supports a different approach.
- Monitoring response more closely.

In some real-world cancer cases, identifying an actionable biomarker and matching it with the right medically approved therapy or clinical-trial strategy can lead to a strong response, long-term disease control, or remission. PhuckCancer does not promise remission and does not decide treatment. Its goal is to help important evidence get noticed, explained, audited, and discussed with the qualified medical team that can make real treatment decisions.

## Example: Doctor and Family Report Output

PhuckCancer can generate two different summaries from the same evidence.

Doctor/research report:

```text
Finding: KRAS G12C alteration detected.
Biological context: KRAS signaling is associated with downstream MAPK pathway activation.
Evidence status: Needs qualified review with cancer type, stage, co-mutations, prior treatment history, and clinical evidence.
Risk flags: Do not treat as a standalone treatment recommendation.
Recommended review: Oncology team, molecular tumor board, and clinical-trial evidence review if appropriate.
```

Family-friendly summary:

```text
The report mentions a change in a gene called KRAS. This may matter because KRAS is involved in cancer cell growth signals. This does not automatically mean one treatment is right, but it is important enough to ask the doctor about. Ask whether this finding affects treatment options, clinical-trial options, or whether the case should be reviewed by a molecular tumor board.
```

The same system can produce both outputs while keeping a clear safety boundary: the doctor reviews the evidence and makes medical decisions; the family gets help understanding what to ask.

## Optional cBioPortal Data Connector

PhuckCancer can optionally connect to a public, institutional, or self-hosted cBioPortal API instance as an external cancer genomics data source.

This connector is used only for data retrieval and normalization. PhuckCancer remains its own cancer evidence platform, with its own MAMMAL-powered biomedical AI engine, local LLM assistant, evidence auditing workflow, risk flagging, and doctor/family report builder.

The default public API base URL is:

```text
https://www.cbioportal.org/api
```

Self-hosted or institutional instances can be configured with:

```env
ENABLE_CBIOPORTAL_CONNECTOR=true
CBIOPORTAL_BASE_URL=http://localhost:8080/api
CBIOPORTAL_AUTH_TOKEN=
```

When enabled, PhuckCancer can retrieve cancer studies, cancer types, sample lists, molecular profiles, mutation records, and available clinical data from a cBioPortal API instance, normalize the records into the PhuckCancer data model, and route the findings into the MAMMAL-powered biomedical interpretation and evidence audit pipeline.

This connector is optional. Local development, tests, sample fixtures, and core PhuckCancer workflows must work without cBioPortal, internet access, authentication, MariaDB, MAMMAL, or Ollama.

Security and privacy requirements:

- Never commit API tokens.
- Store tokens only through environment variables.
- Do not log full tokens.
- Do not import real patient-identifiable data into sample fixtures.
- Follow institutional data access, data-use agreements, privacy rules, and local compliance.
- Treat external data as research/evidence input, not as a medical decision by itself.
- Any imported record must still go through MAMMAL-powered interpretation, evidence auditing, risk flagging, and qualified human review.

## MAMMAL Install

MAMMAL stands for Molecular Aligned Multi-Modal Architecture and Language.

<img width="1547" height="1067" alt="mammal" src="https://github.com/user-attachments/assets/e51377d9-be9b-4449-b562-7541cd61a8e2" />

Official code: https://github.com/BiomedSciAI/biomed-multi-alignment

Hugging Face model: https://huggingface.co/ibm-research/biomed.omics.bl.sm.ma-ted-458m

Paper: https://arxiv.org/abs/2410.22367

```bash
pip install biomed-multi-alignment[examples]
```

Alternative source install:

```bash
git clone https://github.com/BiomedSciAI/biomed-multi-alignment.git
pip install -e ./biomed-multi-alignment[examples]
```

Documentation-only loading example:

```python
from mammal.model import Mammal

model = Mammal.from_pretrained("ibm/biomed.omics.bl.sm.ma-ted-458m")
model.eval()
```

If that import path changes upstream, confirm the latest official usage from the MAMMAL repository. The application itself runs tests without live MAMMAL.

## Medical Safety Notice

PhuckCancer is not a medical device, not a diagnostic system, and not a treatment recommendation engine.

It does not diagnose cancer, prescribe treatment, predict individual outcomes, determine clinical-trial eligibility, replace oncologists, replace molecular tumor boards, replace pathologists, replace genetic counselors, or replace licensed clinical judgment.

All outputs are for education, research support, evidence organization, and qualified human review.

Patients and families should use PhuckCancer to understand information and prepare better questions, not to make medical decisions without a qualified doctor.

## Local Development Setup

Backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m pytest
uvicorn app.main:app --reload
```

Frontend:

```bash
npm install
npm run build
npm run dev
```

Ollama optional:

```bash
ollama pull gemma4:e4b
```

MariaDB optional:

```bash
sudo apt install mariadb-server mariadb-client
mysql -u root -p
```

```sql
CREATE DATABASE phuckcancer_demo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'phuckcancer_user'@'localhost' IDENTIFIED BY 'change_this_password';
GRANT ALL PRIVILEGES ON phuckcancer_demo.* TO 'phuckcancer_user'@'localhost';
FLUSH PRIVILEGES;
```

```bash
mysql -u phuckcancer_user -p phuckcancer_demo < db/schema.sql
mysql -u phuckcancer_user -p phuckcancer_demo < db/seed_cancer_demo.sql
```

## API Overview

Core endpoints include `/health`, `/api/system/status`, `/api/sample/overview`, `/api/data-sources`, `/api/cancer-records`, `/api/genomics/matrix`, `/api/pathways`, `/api/mammal/interpret`, `/api/evidence/audit`, `/api/assistant/explain`, `/api/reports/build`, and optional `/api/cbioportal/*` endpoints.

## Future Vision: AGI-Assisted Cancer Research System

The long-term goal of PhuckCancer is to become a self-expanding open-source cancer research and AGI-assisted evidence system that helps doctors, researchers, patients, and families fight cancer with better information, faster review, and stronger evidence organization.

PhuckCancer is being designed as more than a static cancer information portal. The future vision is to incorporate advanced AI and AGI-style systems that can continuously organize cancer research, compare molecular findings, review clinical evidence, analyze cancer genomics datasets, track treatment-resistance signals, explain complex reports, and help human experts identify important research directions faster.

The goal is not to replace doctors, oncologists, researchers, molecular tumor boards, pathologists, genetic counselors, or licensed medical judgment. The goal is to build an open-source cancer intelligence system that helps qualified humans see more, miss less, understand faster, and make better-informed decisions.

Future AGI-assisted capabilities may include:

- Self-expanding cancer research knowledge maps
- Automated review of new cancer genomics studies
- MAMMAL-powered biomedical interpretation workflows
- Local LLM assistants for doctors, researchers, patients, and families
- Molecular evidence comparison across cancer types
- Drug-resistance signal monitoring
- Clinical-trial evidence organization
- Plain-English explanations of cancer reports
- Question builders for oncology appointments
- Research hypothesis generation for human review
- Evidence grading and uncertainty tracking
- Open-source collaboration tools for cancer research communities
- Optional external cancer data connector expansion
- Multi-agent research review workflows
- Automated evidence-change tracking
- Human-reviewed cancer knowledge graph expansion

The mission is to build a complete open-source cancer research and AI evidence platform that helps people beat the odds against cancer by making cancer data easier to understand, easier to audit, easier to connect, and harder to ignore.

## Project Structure

Backend code lives in `app/`, React code in `src/`, MariaDB scripts in `db/`, deterministic fixtures in `sample_data/`, and tests in `tests/`.

## License

Apache License 2.0.

## Attribution

See `ATTRIBUTION.md`.
