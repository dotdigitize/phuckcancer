# Architecture

PhuckCancer is a FastAPI and React cancer evidence platform. MAMMAL is the required biomedical reasoning layer for cancer molecular interpretation, and the local LLM explains MAMMAL's structured output according to the selected user role.

Pipeline:

```text
Cancer genomics data / cBioPortal connector data / reports / molecular evidence
-> parser and normalizer
-> MAMMAL provider selection
-> local MAMMAL or MAMMAL API
-> MAMMAL-powered biomedical interpretation
-> claim extraction
-> evidence matching
-> support scoring
-> risk flagging
-> role-based local LLM explanation
-> doctor/family/research/system reports
```

Official MAMMAL task pipeline:

```text
Official MAMMAL repo / Hugging Face base model / fine-tuned checkpoints
-> PhuckCancer MAMMAL model registry
-> selected task runner
-> task-specific structured biological input
-> MAMMAL inference
-> normalized result
-> evidence audit
-> role-based local LLM explanation
-> MariaDB history and report export
```

The MAMMAL model registry stores the base model ID, tokenizer ID, official repository URL, checkpoint source, Hugging Face checkpoint link, local checkpoint path, provider mode, enablement state, and task-specific normalization values. This prevents PhuckCancer from treating the base pretrained model as a substitute for fine-tuned downstream checkpoints.

PhuckCancer uses MAMMAL in a cancer evidence workflow that is different from a normal chatbot. MAMMAL is not used to write friendly responses directly. It is used as the biomedical reasoning layer for molecular cancer evidence. The local LLM then explains MAMMAL's structured output according to the selected user role.

If the local MAMMAL package/model is unavailable and no MAMMAL API provider is configured, biomedical interpretation stops with a clear unavailable error. The application may still use JSON sample fixtures for layout, parser tests, cBioPortal normalization tests, and documentation examples.

Ollama and cBioPortal are optional. MariaDB/MySQL is the persistence layer when database mode is enabled.
