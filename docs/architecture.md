# architecture.md

# VELIX Architecture

```
User

↓

Speech Recognition

↓

Router

├──────── NLP Matcher

│           │

│           ├── High Confidence → Skills

│           │

│           └── Low Confidence

↓

Brain (Ollama)

├── Prompt Builder

├── Context Manager

├── Parser

└── Memory Detector

↓

Memory Manager

├── Short-Term

├── Long-Term

└── Semantic Memory (Future)

↓

Executor

↓

Voice Output
```

---

## Modules

### Core

Controls the entire assistant lifecycle.

### Brain

Handles AI reasoning and response generation.

### Memory

Stores user preferences, habits, and context.

### NLP

Detects intents using lightweight matching.

### Skills

Executes commands and automations.

### Voice

Handles speech recognition and speech synthesis.

### Vision (Future)

Image understanding and object detection.

### UI

Dashboard and terminal interface.

### Logs

Stores execution and debugging information.
