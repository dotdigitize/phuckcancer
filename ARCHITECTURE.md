# Architecture

PhuckCancer is a local-first FastAPI and React cancer evidence platform.

Workflow:

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

MAMMAL is integrated through an adapter and pipeline layer with deterministic fallback behavior for tests and local development. Ollama and cBioPortal are optional and disabled by default.
