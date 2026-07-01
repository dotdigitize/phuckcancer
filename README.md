# PhuckCancer

![PhuckCancer banner placeholder](docs/banner-placeholder.png)

PhuckCancer provides visualization, analysis, AI interpretation, evidence auditing, and human-reviewable reporting for large-scale cancer genomics, molecular evidence, mutation, pathway, treatment-response, and clinical-trial signal datasets.

Creator and author: Jose Perez. GitHub: dotdigitize. License: Apache License 2.0. Copyright 2026 Jose Perez.

PhuckCancer is the full cancer evidence platform. MAMMAL is the biomedical AI engine inside it. The local LLM is the plain-English assistant. The evidence portal is the interface doctors, researchers, patients, and families use. Optional external data connectors allow PhuckCancer to retrieve and normalize cancer genomics data from supported research portals and APIs.

## Core Mission

PhuckCancer exists to help doctors, researchers, patients, and families understand cancer evidence faster, organize it better, and fight cancer with stronger information.

The platform brings together cancer genomics data, molecular evidence, mutation and pathway analysis, a MAMMAL-powered biomedical AI engine, local LLM explanation, evidence auditing, optional external cancer genomics data retrieval, and human-reviewable reporting into one open-source cancer intelligence system.

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
-> human review status
-> Markdown/JSON report export
```

## Product Areas

PhuckCancer includes a cancer evidence portal, genomic alteration matrix, cancer pathway explorer, MAMMAL biomedical AI engine, local LLM patient and family assistant, evidence auditing, clinical-trial signal organizer, drug resistance signal watcher, optional cBioPortal data connector, and doctor/family report builder.

The MAMMAL research pipeline includes `app/mammal_engine.py`, `app/mammal_pipeline.py`, `app/mammal_importer.py`, `app/mammal_output_parser.py`, and `app/mammal_claim_extractor.py`. Tests pass without live MAMMAL installed by using deterministic fallback interpretation.

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
