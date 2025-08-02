# Central Query Brain (CQB)

**A modular AI reasoning engine for dynamic multi-agent collaboration and epistemic synthesis**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![vLLM](https://img.shields.io/badge/Powered%20by-vLLM-green.svg)](https://github.com/vllm-project/vllm)
[![University of Toronto](https://img.shields.io/badge/University%20of-Toronto-003F7F.svg)](https://www.utoronto.ca/)
[![Research](https://img.shields.io/badge/Type-Research-brightgreen.svg)](https://github.com)

## Overview
**v1.0**  

Central Query Brain (CQB) is a domain-agnostic AI orchestration system that dynamically generates expert agents and coordinates their collaborative reasoning. Unlike fixed multi-agent systems, CQB analyzes any query and creates appropriate specialists on-demand, then facilitates structured deliberation to produce synthesized insights.

**Key Innovation**: True epistemic labor division - agents with different reasoning styles (conservative vs innovative) and specialties collaborate through multiple rounds of structured discourse.

## 🧠 Core Features

- **Dynamic Agent Generation**: Analyzes queries to determine needed expertise and creates appropriate specialist agents
- **Dual-Model Architecture**: Conservative (analytical) and innovative (creative) agents using different model configurations  
- **Structured Collaboration**: Multi-round deliberation with context building and synthesis
- **Domain Agnostic**: Works across medical, business, technical, creative, and analytical domains
- **Modular Design**: Independent modules can plug into the CQB agent generation service
- **Rich Output**: JSON export with complete conversation transcripts, agent details, and performance metrics

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- CUDA-capable GPU (recommended)
- 16GB+ VRAM for dual model loading

### Installation

```bash
git clone https://github.com/yourusername/central-query-brain.git
cd central-query-brain
pip install -r requirements.txt
```

### Basic Usage

```python
from cqb_framework import initialize_cqb
from collaboration_module import AgentCollaborationModule

# Initialize CQB
cqb = initialize_cqb()

# Create collaboration module
collab_module = AgentCollaborationModule(cqb)

# Run analysis on any query
session_id = collab_module.collaborate_on_query(
    "How should we approach climate change mitigation in urban environments?",
    max_agents=6,
    collaboration_rounds=3
)

# Get results
summary = collab_module.get_collaboration_summary(session_id)
print(summary)

# Export detailed JSON
json_data = collab_module.export_collaboration_json(session_id)
```

## 📁 Project Structure

```
central-query-brain/
├── README.md                    # This file
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── config.yaml                  # Model configurations
├── cqb_framework.py            # Core CQB agent generation engine
├── collaboration_module.py     # Multi-round collaboration orchestrator
├── examples/                   # Example scenarios and use cases
│   ├── techflow_crisis.py     # AI startup crisis simulation
│   ├── medical_consultation.py # Medical case analysis
│   ├── business_strategy.py   # Strategic planning scenario
│   └── climate_policy.py      # Policy analysis example
├── outputs/                    # Generated collaboration results
│   └── sample_outputs/        # Example JSON outputs
├── docs/                       # Documentation
│   ├── architecture.md        # System architecture details
│   ├── agent_types.md         # Agent specification guide
│   └── api_reference.md       # Complete API documentation
└── tests/                      # Test suite
    ├── test_cqb_core.py       # Core functionality tests
    └── test_collaboration.py  # Collaboration module tests
```

## 🎯 Example Scenarios

### 1. Crisis Management
```python
crisis_scenario = """
TechFlow AI startup faces simultaneous technical bias issues, 
regulatory scrutiny, funding challenges, and talent retention 
problems. Develop a comprehensive crisis response strategy.
"""

session_id = collab_module.collaborate_on_query(crisis_scenario)
```

**Generated Agents**: Crisis Management Expert, AI Ethics Specialist, Regulatory Compliance Advisor, Business Strategy Consultant, Talent Retention Specialist, Technical Risk Analyst

### 2. Medical Case Analysis
```python
medical_case = """
45-year-old presents with acute chest pain, dyspnea, and 
diaphoresis. ECG shows ST elevation in inferior leads. 
Develop differential diagnosis and treatment approach.
"""

session_id = collab_module.collaborate_on_query(medical_case)
```

**Generated Agents**: Emergency Medicine Physician, Cardiologist, Internal Medicine Specialist, Critical Care Expert, Diagnostic Imaging Specialist

### 3. Strategic Planning
```python
strategy_query = """
Mid-size manufacturing company considering digital transformation. 
Evaluate approaches, risks, and implementation roadmap for 
Industry 4.0 adoption while maintaining operational continuity.
"""

session_id = collab_module.collaborate_on_query(strategy_query)
```

**Generated Agents**: Digital Transformation Consultant, Operations Analyst, Technology Architect, Change Management Expert, Financial Risk Assessor

## 🏗️ Architecture

### Core Components

1. **CQB Framework** (`cqb_framework.py`)
   - Dynamic query analysis and agent specification
   - Dual-model management (conservative/innovative)
   - Agent generation and persistence
   - Session management

2. **Collaboration Module** (`collaboration_module.py`)
   - Multi-round deliberation orchestration
   - Context building and synthesis
   - JSON export and result formatting

3. **Agent System**
   - Conservative agents: Analytical, systematic, evidence-based
   - Innovative agents: Creative, forward-thinking, exploratory
   - Persistent conversation history and learning

### Collaboration Flow

```
Query → Analysis → Agent Generation → Round 1 (Initial) → Round 2 (Refinement) → Round 3 (Synthesis) → Final Output
```

Each round builds context from previous discussions, enabling true collaborative reasoning.

## 📊 Output Format

CQB generates comprehensive JSON outputs containing:

- **Query Analysis**: Domain classification, complexity assessment
- **Agent Details**: Specialties, reasoning styles, model assignments
- **Round Transcripts**: Complete conversation history with timestamps
- **Synthesis Results**: Unified expert recommendations
- **Performance Metrics**: Response times, participation rates, quality scores

## 🔧 Configuration

### Model Configuration (`config.yaml`)

```yaml
conservative_model:
  name: 'Conservative-Model-Gemma-2-9B-AWQ'
  model_path: 'hugging-quants/gemma-2-9b-it-AWQ-INT4'
  temperature: 0.2
  top_p: 0.7
  max_tokens: 1536

innovative_model:
  name: 'Innovative-Model-Qwen2.5-GPTQ'
  model_path: 'Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4'
  temperature: 0.8
  top_p: 0.95
  max_tokens: 1536
```

### Custom Agent Types

Extend the system by defining custom agent specifications:

```python
custom_spec = CQBAgentSpec(
    agent_id="Domain_Expert_1",
    agent_type="Conservative",
    specialty="Your Specialty",
    model_assignment="conservative_model",
    temperature=0.3,
    persona="Expert description"
)
```

## 🧪 Research Applications

CQB is designed for research in:

- **Epistemic Modeling**: How knowledge emerges from collaborative reasoning
- **Multi-Agent Systems**: Coordination and synthesis in AI teams
- **Decision Support**: Expert system augmentation for complex problems
- **Cognitive Simulation**: Modeling human expert collaboration
- **AI Safety**: Understanding emergent behaviors in AI teams

## 🤝 Contributing

We welcome contributions! Areas of interest:

- New collaboration patterns and social layers
- Domain-specific agent templates
- Evaluation metrics and benchmarks
- Integration with external knowledge sources
- Performance optimizations

See `CONTRIBUTING.md` for guidelines.

## 🙏 Acknowledgments

- Built on [vLLM](https://github.com/vllm-project/vllm) for efficient LLM inference
- Inspired by research in collective intelligence and epistemic democracy
- Thanks to the open-source AI community for model development
- University of Toronto for supporting open research initiatives


## 📄 License & Attribution

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for complete details.

### **Citation Information**
```bibtex
@software{CQB,
  author = {Del Coburn},
  title = {Émile-1: Personal Local AI Assistant},
  year = {2025},
  institution = {University of Toronto},
  url = {https://github.com/Baglecake/CQB}
}
```

---

## 👨‍💻 Author

**Del Coburn**  
University of Toronto  
📧 del.coburn@mail.utoronto.ca  

*For project-related questions, please use GitHub Issues or Discussions. For other inquiries, feel free to reach out via email.*

### **Acknowledgments**
- The open-source AI community for inspiration and foundational models
- University of Toronto for supporting open research initiatives

---

**Made with ❤️ for democratizing AI access**

**Built for researchers, decision-makers, and AI developers who need sophisticated multi-agent reasoning capabilities.**

**Version**: v1.0 | **Last Updated**: 2025-07-29 | **Compatibility**: Ollama 0.1+, Streamlit 1.28+

---
