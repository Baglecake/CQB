# Central Query Brain (CQB)

**A modular AI reasoning engine for dynamic multi-agent collaboration and epistemic synthesis**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![vLLM](https://img.shields.io/badge/Powered%20by-vLLM-green.svg)](https://github.com/vllm-project/vllm)
[![University of Toronto](https://img.shields.io/badge/University%20of-Toronto-003F7F.svg)](https://www.utoronto.ca/)
[![Research](https://img.shields.io/badge/Type-Research-brightgreen.svg)](https://github.com)
[![RAO](https://img.shields.io/badge/Architecture-RAO-red.svg)](https://github.com)

## Overview
**v1.3 - Retrieval-Augmented Orchestration (RAO) Architecture**  

Central Query Brain (CQB) implements **Retrieval-Augmented Orchestration (RAO)** - a novel AI architecture that uses context to dynamically build reasoning teams rather than just inform responses. Unlike traditional RAG systems that retrieve information to enhance a single agent's answer, RAO retrieves and analyzes context to determine what kinds of experts are needed and generates a custom team of specialist agents.

**🔥 NEW in v1.3**: **RAO Implementation** - Context-aware agent generation with file-based knowledge integration

**Key Innovation**: True epistemic labor division with **context-driven team assembly** - the system analyzes your documents to build reasoning teams specifically suited to your domain and requirements.

### 🧠 **RAO vs RAG - Revolutionary Difference**

| Aspect | Traditional RAG | CQB's RAO |
|--------|-----------------|-----------|
| **Purpose of Retrieval** | Find facts to inform answer | Analyze context to determine expertise needed |
| **Impact on AI** | Informs single agent response | Shapes entire reasoning team composition |
| **User Insight** | Black box reasoning | Transparent specialist selection |
| **Adaptability** | Static reasoning process | Dynamic team based on context |

### 🔌 **Modular Architecture**
CQB separates **agent generation** from **reasoning orchestration**, enabling:
- **Central Hub**: `cqb_framework.py` generates context-aware experts for any query
- **RAO Context Manager**: `cqb_context_manager.py` analyzes documents to inform team composition
- **Plug-in Modules**: Independent reasoning orchestrators that leverage context-aware agents
- **Flexible Deployment**: Switch between collaboration, debate, or custom reasoning patterns seamlessly

## 📚 Version History

### v1.3 (CURRENT) - RAO Architecture Implementation
- 🔥 **NEW**: Retrieval-Augmented Orchestration (RAO) - world's first implementation
- 🔥 **NEW**: Context-aware agent generation from uploaded documents
- 🔥 **NEW**: File-based context system (`cqb_framework_rao.txt`)
- 🔥 **NEW**: Domain-specific specialist selection based on document analysis
- ✨ **Enhanced**: All existing modules now work with context-aware agents
- 🔧 **Maintained**: Full backwards compatibility with v1.2 features

### v1.2 - Model License Integration
- ✨ **NEW**: Model licensing automation for citation compliance
- 🔧 **Enhanced**: Each module automatically exports license metadata in json files
- 🔧 **MAINTAINED**: All features of earlier versions

### v1.1 - Modular Reasoning Architecture
- ✨ **NEW**: Adversarial Debate Module for Red Team vs Blue Team analysis
- ✨ **NEW**: True plug-in architecture - modules are completely interchangeable
- ✨ **NEW**: Security audit capabilities with adversarial reasoning
- 🔧 **Enhanced**: Context window management for longer deliberations
- 📖 **Added**: Multiple reasoning patterns demonstrated

### v1.0 - Foundation Release  
- 🚀 **Core**: Dynamic agent generation from query analysis
- 🚀 **Core**: Dual-model architecture (conservative/innovative agents)
- 🚀 **Core**: Collaborative reasoning with synthesis
- 🚀 **Core**: Domain-agnostic operation across multiple fields

## 🧠 Core Features

- 🔥 **Retrieval-Augmented Orchestration (RAO)**: Novel implementation - uses context to build reasoning teams
- 🔥 **Context-Aware Agent Generation**: Analyzes documents to determine needed expertise and creates appropriate specialists
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

### 🔥 **RAO Context-Aware Agent Generation**

#### Set Up Context File
```bash
# Create your context file (any domain works)
echo "Your domain-specific context content here..." > v1.3/cqb_framework_rao.txt
```

#### Enable RAO in Config
```yaml
# config.yaml
rao_settings:
  enabled: true
  context_filename: 'cqb_framework_rao.txt'
  max_context_length: 2000
  fallback_to_query_only: true
```

#### Context-Aware Reasoning
```python
from cqb_framework import initialize_cqb
from collaboration_module import AgentCollaborationModule

# Initialize CQB with RAO
cqb = initialize_cqb()

# RAO automatically analyzes your context file and generates appropriate specialists
session_id = cqb.analyze_query_and_generate_agents(
    "Based on our situation, what strategy should we implement?",
    max_agents=6
)

# All agents are now context-aware and domain-specific
agents = cqb.get_agents(session_id)
for agent in agents:
    print(f"🧠 {agent.specialty} - Context: {agent.spec.context_summary[:50]}...")
```

#### 🔌 **Use with Any Module**
```python
# Collaboration with context-aware agents
collab_module = AgentCollaborationModule(cqb)
collab_session = collab_module.collaborate_on_query(
    "Develop a comprehensive improvement strategy",
    max_agents=5,
    collaboration_rounds=3
)

# Adversarial debate with context-aware agents  
from adversarial_debate_module import AdversarialDebateModule
debate_module = AdversarialDebateModule(cqb)
debate_session = debate_module.run_debate_on_query(
    "Should we prioritize approach A or B?",
    max_agents=7,
    debate_rounds=3
)
```

### 🔄 **Backwards Compatibility**
```python
# Disable RAO for standard operation
rao_settings:
  enabled: false  # Works exactly like v1.2

# Or no context file = automatic fallback
# Missing cqb_framework_rao.txt = standard query-only agents
```

## 📁 Project Structure

```
central-query-brain/
├── README.md                         # This file
├── LICENSE                           # MIT License
├── requirements.txt                  # Python dependencies
v1.3/                                 # 🔥 NEW: RAO Implementation
├── config.yaml                       # Enhanced with RAO settings
├── cqb_framework.py                  # 🧠 Enhanced with RAO support
├── cqb_context_manager.py            # 🔥 NEW: RAO context analysis
├── collaboration_module.py           # 🤝 Enhanced with context-aware agents
├── adversarial_debate_module.py      # ⚔️ Enhanced with context-aware agents
├── licenses.yaml                     # Model license registry
├── license_manager.py                # License compliance system
├── cqb_framework_rao.txt             # 🔥 NEW: Your context file
└── third_party_licenses/             # Full license texts
examples/                             # Example scenarios and use cases
├── rao_examples/                     # 🔥 NEW: RAO demonstration scripts
├── techflow_crisis.py                # AI startup crisis simulation
├── medical_consultation.py           # Medical case analysis
├── security_audit_debate.py          # Red Team vs Blue Team security audit
outputs/                              # Generated analysis results
│   └── sample_outputs/               # Example JSON outputs
docs/                                 # Documentation
│   ├── rao_architecture.md           # 🔥 NEW: RAO system documentation
│   ├── architecture.md               # System architecture details
│   ├── agent_types.md                # Agent specification guide
│   └── api_reference.md              # Complete API documentation
```

## 🎯 RAO Examples & Use Cases

### 🔥 **Customer Service Operations (RAO)**
```python
# Context file: customer_service_context.txt contains:
# - 25 representatives, 5,000+ monthly interactions
# - $2.1M budget, declining satisfaction scores
# - 48-hour response times, high turnover

query = "How should we improve our customer service operations?"

# RAO generates context-aware specialists:
# - Customer Experience (CX) Strategist 🧠
# - Operations Efficiency Expert 🧠  
# - Data Analyst specializing in Customer Service Metrics 🧠
```

### 🔥 **Medical Case Analysis (RAO)**
```python  
# Context file: medical_case_context.txt contains:
# - Patient demographics, symptoms, test results
# - Hospital capabilities, resource constraints
# - Regulatory requirements, treatment protocols

query = "What's the differential diagnosis and treatment plan?"

# RAO generates context-aware specialists:
# - Emergency Medicine Physician 🧠
# - Cardiologist (based on symptoms) 🧠
# - Clinical Pharmacist (based on medications) 🧠
```

### 🔥 **Business Strategy (RAO)**
```python
# Context file: business_strategy_context.txt contains:
# - Market analysis, competitor landscape  
# - Financial constraints, growth targets
# - Regulatory environment, compliance requirements

query = "What's our optimal market entry strategy?"

# RAO generates context-aware specialists:
# - Market Entry Strategist 🧠
# - Regulatory Compliance Expert 🧠
# - Financial Risk Analyst 🧠
```

## 🧬 **RAO Architecture Deep Dive**

### **Context Analysis Pipeline**
```
📄 Context File → 🔍 Domain Analysis → 🧠 Specialist Selection → 🤖 Agent Generation
     ↓                    ↓                      ↓                    ↓
Domain-specific     Key concepts &        Required expertise    Context-aware agents
   content          terminology            identification        with background
```

### **Agent Enhancement Process**
```python
# Standard Agent (v1.2)
agent.specialty = "Business Strategist"
agent.context_summary = ""  # No context

# RAO Agent (v1.3)  
agent.specialty = "Customer Experience (CX) Strategist"  # Context-driven
agent.context_summary = "Working with customer service operations. Key challenges: 25-person team, 5,000+ interactions, $2.1M budget constraints."
```

### **Integration with Social Layers**
```python
# RAO + MVSU Social Layers
rao_config = {
    'context_file': 'medical_cases.txt',
    'social_layers': ['Layer_1_Synthesis', 'Layer_2_Ranking', 'Layer_3_Independent']
}
```

## 📊 RAO vs Standard Comparison

### **Query**: "How should we improve our operations?"

**Standard CQB (v1.2) Generates**:
- Generic Business Strategist
- General Operations Expert  
- Standard Process Analyst

**RAO CQB (v1.3) with Customer Service Context Generates**:
- Customer Experience (CX) Strategist 🧠
- Operations Efficiency Expert specialized in service delivery 🧠
- Data Analyst specializing in Customer Service Metrics 🧠

**RAO Agent Response**:
> *"Given your situation with **25 representatives, 5,000+ monthly interactions, and $2.1M budget**, I recommend implementing a CRM system to handle your interaction volume, with phased rollout to manage costs..."*

**Standard Agent Response**:
> *"To improve operations, consider streamlining processes, implementing better technology, and measuring performance metrics..."*

**The difference is transformational!** 🚀

## 🏗️ Architecture

### 🧠 **RAO-Enhanced CQB Design**
```
┌─────────────────────────────────────────────────────────┐
│                CQB Framework v1.3                       │
│  ┌─────────────────────────────────────────────────┐    │
│  │     RAO Context Analysis                        │    │
│  │  • Document Processing                          │    │
│  │  • Domain Identification                        │    │
│  │  • Specialist Requirements                      │    │
│  │  • Context-Aware Agent Generation               │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────┬───────────────────────────────────────┘
                  │ Context-Aware Agent Pool
      ┌───────────┴───────────┐
      │                       │
┌─────▼───────┐           ┌─────▼──────┐
│Collaboration│           │Adversarial │
│  Module     │           │  Debate    │
│             │           │  Module    │
│🤝 Enhanced  │           │⚔️ Enhanced  │
│with Context │           │with Context│
└─────────────┘           └────────────┘
```

### Core Components

1. **🧠 CQB Framework** (`cqb_framework.py`) - Enhanced with RAO
   - Context-aware query analysis and agent specification
   - RAO integration with backwards compatibility
   - Domain-specific agent generation
   - **Serves as central hub for all reasoning modules**

2. **🔥 CQB Context Manager** (`cqb_context_manager.py`) - NEW
   - Document analysis and domain identification
   - Specialist requirement extraction
   - Context-aware agent specification enhancement
   - Smart filtering and relevance scoring

3. **🤝 Collaboration Module** (`collaboration_module.py`) - Enhanced
   - Works seamlessly with context-aware agents
   - Enhanced collaboration with shared domain understanding
   - Context-informed synthesis

4. **🆕 ⚔️ Adversarial Debate Module** (`adversarial_debate_module.py`) - Enhanced
   - Context-aware adversarial reasoning
   - Domain-specific debate frameworks
   - Enhanced judge evaluation with context

## 🧪 Research Applications

CQB v1.3 enables research in:

- **🔥 Retrieval-Augmented Orchestration**: Novel AI architecture for context-driven team assembly
- **🔥 Context-Aware Multi-Agent Systems**: How document context shapes reasoning team composition
- **🔥 Transparent Knowledge Construction**: Making AI reasoning processes visible through specialist selection
- **Epistemic Modeling**: How knowledge emerges from different reasoning patterns
- **Multi-Agent Coordination**: Team dynamics in context-aware vs standard agents
- **Decision Support**: Expert system augmentation with flexible reasoning modes
- **AI Safety**: Understanding emergent behaviors in context-informed reasoning frameworks

## 🚀 **Getting Started Examples**

### Run RAO Context Analysis
```bash
python examples/rao_examples/test_context_analysis.py
```

### Run Context-Aware Collaboration
```bash
python examples/rao_examples/test_rao_collaboration.py
```

### Compare RAO vs Standard
```bash
python examples/rao_examples/compare_rao_standard.py
```

### 🆕 **Run Security Audit with Context**
```bash
python examples/security_audit_debate.py
```

## 🤝 Contributing

We welcome contributions! Areas of interest:

- **🔥 New context types and domains** (medical, legal, technical, creative)
- **🔥 Enhanced context analysis** (semantic similarity, vector embeddings)
- **🔥 New reasoning modules** (consensus building, devil's advocate, etc.)
- **🔥 Domain-specific orchestration patterns**
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
  title = {CQB: Central Query Brain - RAO Architecture for Context-Aware Multi-Agent Reasoning},
  year = {2025},
  version = {1.3},
  institution = {University of Toronto},
  url = {https://github.com/Baglecake/CQB},
  note = {First implementation of Retrieval-Augmented Orchestration (RAO)}
}
```

---

## 👨‍💻 Author

**Del Coburn**  
University of Toronto  
📧 del.coburn@mail.utoronto.ca  

*For project-related questions, please use GitHub Issues or Discussions. For other inquiries, feel free to reach out via email.*

---
**🔥 World's first Retrieval-Augmented Orchestration (RAO) implementation**

**Built for researchers, decision-makers, and AI developers who need sophisticated context-aware multi-agent reasoning capabilities.**

**🆕 v1.3: Revolutionary RAO architecture - context shapes reasoning teams, not just responses.**

**Made with ❤️ for democratizing AI understanding**

**Version**: v1.3 | **Last Updated**: 2025-08-04 |

---
