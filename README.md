# Central Query Brain (CQB)

**A modular AI reasoning engine for dynamic multi-agent collaboration and epistemic synthesis**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![vLLM](https://img.shields.io/badge/Powered%20by-vLLM-green.svg)](https://github.com/vllm-project/vllm)
[![University of Toronto](https://img.shields.io/badge/University%20of-Toronto-003F7F.svg)](https://www.utoronto.ca/)
[![Research](https://img.shields.io/badge/Type-Research-brightgreen.svg)](https://github.com)

## Overview
**v1.2 - Modular Reasoning Architecture**  

Central Query Brain (CQB) is a domain-agnostic AI orchestration system that dynamically generates expert agents and coordinates their reasoning through **pluggable modules**. Unlike fixed multi-agent systems, CQB analyzes any query, creates appropriate specialists on-demand, then facilitates structured deliberation through interchangeable reasoning modules.

**Key Innovation**: True epistemic labor division with **modular reasoning patterns** - the same dynamically-generated agents can engage in collaborative synthesis, adversarial debate, or any custom reasoning framework through plug-in modules.

### 🔌 **Modular Architecture**
CQB separates **agent generation** from **reasoning orchestration**, enabling:
- **Central Hub**: `cqb_framework.py` generates domain-appropriate experts for any query
- **Plug-in Modules**: Independent reasoning orchestrators that use the same agent pool
- **Flexible Deployment**: Switch between collaboration, debate, or custom reasoning patterns seamlessly

## 📚 Version History

### v1.2 (CURRENT) - Model License Integration
- ✨ **NEW**: Model licensing automation for citation compliance
- 🔧 **Enhanced**: Each module automatically exports license metadata in json files
- 🔧 **MAINTAINED**: All features of earlier versions

### v1.1 - Modular Reasoning Architecture
- ✨ **NEW**: Adversarial Debate Module for Red Team vs Blue Team analysis
- ✨ **NEW**: True plug-in architecture - modules are completely interchangeable
- ✨ **NEW**: Security audit capabilities with adversarial reasoning
- 🔧 **Enhanced**: Context window management for longer deliberations
- 🔧 **Enhanced**: JSON export with comprehensive debate transcripts
- 📖 **Added**: Multiple reasoning patterns demonstrated

### v1.0 - Foundation Release  
- 🚀 **Core**: Dynamic agent generation from query analysis
- 🚀 **Core**: Dual-model architecture (conservative/innovative agents)
- 🚀 **Core**: Collaborative reasoning with synthesis
- 🚀 **Core**: Domain-agnostic operation across multiple fields
- 🚀 **Core**: Rich JSON export with conversation transcripts

## 🧠 Core Features

- **Dynamic Agent Generation**: Analyzes queries to determine needed expertise and creates appropriate specialist agents
- **Dual-Model Architecture**: Conservative (analytical) and innovative (creative) agents using different model configurations  
- **🆕 Modular Reasoning Patterns**: Choose between collaborative synthesis, adversarial debate, or custom orchestration
- **🆕 Plug-in Architecture**: Independent modules that leverage the same agent generation service
- **Domain Agnostic**: Works across medical, business, technical, creative, security, and analytical domains
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

### 🔌 **Choose Your Reasoning Mode**

#### Collaborative Reasoning
```python
from cqb_framework import initialize_cqb
from collaboration_module import AgentCollaborationModule

# Initialize CQB
cqb = initialize_cqb()

# Plug in collaboration module
collab_module = AgentCollaborationModule(cqb)

# Run collaborative analysis
session_id = collab_module.collaborate_on_query(
    "How should we approach climate change mitigation in urban environments?",
    max_agents=6,
    collaboration_rounds=3
)

summary = collab_module.get_collaboration_summary(session_id)
print(summary)
```

#### 🆕 **Adversarial Debate Reasoning**
```python
from cqb_framework import initialize_cqb
from adversarial_debate_module import AdversarialDebateModule

# Initialize CQB  
cqb = initialize_cqb()

# Plug in adversarial debate module
debate_module = AdversarialDebateModule(cqb)

# Run adversarial analysis
session_id = debate_module.run_debate_on_query(
    "Should AI development be regulated by government agencies?",
    max_agents=7,
    debate_rounds=3,
    position_a="FOR government regulation",
    position_b="AGAINST government regulation"
)

summary = debate_module.get_debate_summary(session_id)
print(summary)
```

## 📁 Project Structure

```
central-query-brain/
├── README.md                         # This file
├── LICENSE                           # MIT License
├── requirements.txt                  # Python dependencies
v1.2/
│   ├── config.yaml                   # Model configurations
│   ├── cqb_framework.py              # 🧠 Core CQB agent generation engine
│   ├──collaboration_module.py        # 🤝 Collaborative reasoning orchestrator
│   ├── adversarial_debate_module.py  # ⚔️ Adversarial debate orchestrator
examples/                             # Example scenarios and use cases
│   ├── run_collaboration.py          # Collaborative reasoning examples
│   ├── run_debate.py                 # 🆕 Adversarial debate examples
│   ├── techflow_crisis.py            # AI startup crisis simulation
│   ├── medical_consultation.py       # Medical case analysis
│   ├── security_audit_debate.py      # 🆕 Red Team vs Blue Team security audit
│   └── climate_policy.py             # Policy analysis example
outputs/                              # Generated analysis results
│   └── sample_outputs/               # Example JSON outputs
docs/                                 # Documentation
│   ├── architecture.md               # System architecture details
│   ├── agent_types.md                # Agent specification guide
│   └── api_reference.md              # Complete API documentation

```

## 🎯 Reasoning Patterns & Examples

### 🤝 **Collaborative Reasoning**
*Agents work together, build on ideas, synthesize collective wisdom*

#### Crisis Management
```python
crisis_scenario = """
TechFlow AI startup faces simultaneous technical bias issues, 
regulatory scrutiny, funding challenges, and talent retention 
problems. Develop a comprehensive crisis response strategy.
"""

session_id = collab_module.collaborate_on_query(crisis_scenario)
```

**Generated Agents**: Crisis Management Expert, AI Ethics Specialist, Regulatory Compliance Advisor, Business Strategy Consultant, Talent Retention Specialist

#### Medical Case Analysis
```python
medical_case = """
45-year-old presents with acute chest pain, dyspnea, and 
diaphoresis. ECG shows ST elevation in inferior leads. 
Develop differential diagnosis and treatment approach.
"""

session_id = collab_module.collaborate_on_query(medical_case)
```

**Generated Agents**: Emergency Medicine Physician, Cardiologist, Internal Medicine Specialist, Critical Care Expert

### ⚔️ **Adversarial Debate Reasoning**
*Agents split into opposing teams, argue positions, compete through superior reasoning*

#### 🆕 **Security Audit (Red Team vs Blue Team)**
```python
security_audit = """
Conduct adversarial security audit of autonomous drone delivery network.
Identify critical vulnerabilities and evaluate proposed mitigations.
"""

session_id = debate_module.run_debate_on_query(
    security_audit,
    position_a="RED TEAM - Expose Vulnerabilities", 
    position_b="BLUE TEAM - Defend with Mitigations"
)
```

**Generated Teams**: 
- **Red Team**: Cybersecurity Analyst, Physical Security Expert, Social Engineering Specialist
- **Blue Team**: Security Architect, Risk Management Expert, Compliance Specialist  
- **Judge**: Security Auditor

#### Policy Analysis
```python
policy_debate = """
Should we prioritize Mars colonization or Earth climate solutions?
"""

session_id = debate_module.run_debate_on_query(
    policy_debate,
    position_a="FOR Mars colonization priority",
    position_b="FOR Earth climate priority"
)
```

**Generated Teams**:
- **Team A**: Aerospace Engineer, Planetary Scientist, Technology Futurist
- **Team B**: Climate Scientist, Environmental Policy Expert, Social Justice Advocate
- **Judge**: Strategic Policy Analyst

## 🏗️ Architecture

### 🧠 **Central Hub Design**
```
┌─────────────────────────────────────────────────────────┐
│                CQB Framework                            │
│  ┌─────────────────────────────────────────────────┐    │
│  │        Dynamic Agent Generation                 │    │
│  │  • Query Analysis                               │    │
│  │  • Specialist Selection                         │    │
│  │  • Dual-Model Assignment                        │    │
│  │  • Agent Pool Creation                          │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────┬───────────────────────────────────────┘
                  │ Agent Pool
      ┌───────────┴───────────┐
      │                       │
┌─────▼───────┐           ┌─────▼─────┐
│Collaboration│           │Adversarial│
│  Module     │           │  Debate   │
│             │           │  Module   │
│🤝 Synthesis │           │⚔️ Judgment │
└─────────────┘           └───────────┘
```

### Core Components

1. **🧠 CQB Framework** (`cqb_framework.py`)
   - Dynamic query analysis and agent specification
   - Dual-model management (conservative/innovative)
   - Agent generation and session management
   - **Serves as central hub for all reasoning modules**

2. **🤝 Collaboration Module** (`collaboration_module.py`)
   - Multi-round deliberation orchestration
   - Context building and collaborative synthesis
   - Consensus-driven reasoning patterns

3. **🆕 ⚔️ Adversarial Debate Module** (`adversarial_debate_module.py`)
   - Red Team vs Blue Team orchestration
   - Competitive reasoning with judge evaluation
   - Confrontational analysis patterns

### 🔌 **Plug-in Pattern**
Each module follows the same interface:
```python
# 1. Connect to CQB hub
module = ReasoningModule(cqb_brain)

# 2. Request agents for query  
session_id = cqb_brain.analyze_query_and_generate_agents(query)
agents = cqb_brain.get_agents(session_id)

# 3. Apply unique reasoning orchestration
result = module.orchestrate_reasoning(agents, query)
```

## 📊 Output Formats

### Collaborative Output
- **Query Analysis**: Domain classification, complexity assessment
- **Agent Details**: Specialties, reasoning styles, model assignments  
- **Round Transcripts**: Complete conversation history with context building
- **Synthesis Results**: Unified expert recommendations

### 🆕 **Adversarial Output**
- **Team Assignments**: Red Team vs Blue Team with judge
- **Debate Transcripts**: Attack/defense exchanges with escalation
- **Judge Evaluations**: Round-by-round assessment of arguments
- **Final Verdict**: Winning position with comprehensive reasoning

## 🔧 Configuration

### Model Configuration (`config.yaml`)

```yaml
conservative_model:
  name: 'Conservative-Model-Gemma-2-9B-AWQ'
  model_path: 'hugging-quants/gemma-2-9b-it-AWQ-INT4'
  temperature: 0.2
  top_p: 0.7
  max_tokens: 1536
  max_model_len: 8192  # Extended for longer deliberations

innovative_model:
  name: 'Innovative-Model-Qwen2.5-GPTQ'
  model_path: 'Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4'
  temperature: 0.8
  top_p: 0.95
  max_tokens: 1536
  max_model_len: 8192  # Extended for longer deliberations
```

## 🧪 Research Applications

CQB v1.1 enables research in:

- **🆕 Adversarial AI Systems**: Red Team vs Blue Team reasoning patterns
- **🆕 Modular Reasoning**: Comparison of collaborative vs competitive deliberation
- **Epistemic Modeling**: How knowledge emerges from different reasoning patterns
- **Multi-Agent Coordination**: Team dynamics in cooperative vs adversarial settings
- **Decision Support**: Expert system augmentation with flexible reasoning modes
- **🆕 Security Analysis**: AI-powered red team/blue team exercises
- **AI Safety**: Understanding emergent behaviors in different reasoning frameworks

## 🚀 **Getting Started Examples**

### Run Collaborative Analysis
```bash
python examples/clinical_ddx.py
```

### 🆕 **Run Adversarial Debate**
```bash
python examples/run_debate.py
```

### 🆕 **Run Security Audit**
```bash
python examples/security_audit_debate.py
```

## 🤝 Contributing

We welcome contributions! Areas of interest:

- **🆕 New reasoning modules** (consensus building, devil's advocate, etc.)
- **🆕 Domain-specific orchestration patterns**
- Enhanced evaluation metrics and benchmarks
- Integration with external knowledge sources
- Performance optimizations

See `CONTRIBUTING.md` for guidelines.

## 📋 License Compliance & Model Registry

CQB includes comprehensive license tracking to ensure compliance when using third-party AI models.

### 🔒 **Automatic License Compliance**

Every model used in CQB is automatically tracked for license compliance:

```python
# ✅ Automatic compliance checking at startup
cqb = initialize_cqb()
# Displays license status for all configured models

# ✅ All JSON exports include license manifest
json_data = collab_module.export_collaboration_json(session_id)
print(json_data['license_manifest'])
```

### 📋 **Model Registry Management**

Add new models to `licenses.yaml`:

```yaml
"organization/model-name":
  license: "License Name (e.g., Apache-2.0, MIT, Gemma Terms of Use)"
  repo: "https://huggingface.co/organization/model-name"
  description: "Human readable description"
  license_file: "filename.txt"  # Optional: local license file
```

### 🚨 **Compliance Warnings**

CQB will warn about unlicensed models but continue operation:

```
⚠️ Model 'new/model' not found in license registry!
🔧 Please add it to licenses.yaml before use
📥 Loading new-model... # Continues with warning
```

### 📁 **License File Organization**

```
central-query-brain/
├── licenses.yaml              # Model license registry
├── license_manager.py         # License compliance system
└── third_party_licenses/      # Full license texts
    ├── apache_2_0.txt
    ├── gemma_license.txt
    ├── mit_license.txt
    └── ...
```

### ⚖️ **Legal Compliance Notes**

- **Registry Requirement**: All models must be registered before use
- **Redistribution**: Users must comply with original model licenses
- **Commercial Use**: Review individual model licenses for commercial restrictions
- **Attribution**: Full license details included in all JSON exports

### 🔧 **For Developers**

```python
# Check specific model compliance
from license_manager import validate_model, get_license_info

is_compliant = validate_model("Qwen/Qwen3-8B")
license_info = get_license_info("Qwen/Qwen3-8B")

# Get complete session manifest
manifest = cqb.get_license_manifest()
```

The license system ensures full transparency and compliance while maintaining CQB's ease of use.

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
  title = {CQB: Central Query Brain - Modular AI Reasoning Engine},
  year = {2025},
  version = {1.1},
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

---
**Built for researchers, decision-makers, and AI developers who need sophisticated multi-agent reasoning capabilities.**

**🆕 v1.1: Now with modular reasoning patterns - collaborate or compete, your choice.**

**Made with ❤️ for democratizing AI access**

**Version**: v1.1 | **Last Updated**: 2025-08-02 |

---
