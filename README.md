# Central Query Brain (CQB)

**A modular AI reasoning engine for dynamic multi-agent collaboration and epistemic synthesis**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![vLLM](https://img.shields.io/badge/Powered%20by-vLLM-green.svg)](https://github.com/vllm-project/vllm)
[![University of Toronto](https://img.shields.io/badge/University%20of-Toronto-003F7F.svg)](https://www.utoronto.ca/)
[![Research](https://img.shields.io/badge/Type-Research-brightgreen.svg)](https://github.com)
[![EAO](https://img.shields.io/badge/Architecture-EAO-red.svg)](https://github.com)

## Overview
**v1.4 - Extraction-Augmented Orchestration (EAO) Architecture**  

Central Query Brain (CQB) implements **Extraction-Augmented Orchestration (EAO)** - a revolutionary AI architecture that uses sophisticated document analysis to dynamically build reasoning teams. Building on RAO, EAO integrates **Google's LangExtract** ([github.com/google/langextract](https://github.com/google/langextract)) for structured entity extraction, enabling precise context understanding that drives expert team assembly.

**🔥 NEW in v1.4**: **EAO Implementation** - Integration of Google's LangExtract for sophisticated structured extraction and context-aware agent generation

**Key Innovation**: **Extraction-Augmented Orchestration** - the system performs structured extraction on documents to identify constraints, metrics, stakeholders, and objectives, then generates specialist teams with precise contextual briefings.

### 🧠 **EAO vs RAO vs RAG - Evolutionary Comparison**

| Aspect | Traditional RAG | RAO (v1.3) | EAO (v1.4) |
|--------|-----------------|-------------|-------------|
| **Purpose of Retrieval** | Find facts to inform answer | Analyze context to determine expertise needed | Extract structured entities to drive team assembly |
| **Context Analysis** | Semantic search | Basic keyword matching | Sophisticated structured extraction |
| **Impact on AI** | Informs single agent response | Shapes reasoning team composition | Builds context-aware specialists with precise briefings |
| **User Insight** | Black box reasoning | Transparent specialist selection | Transparent extraction → specialist mapping |
| **Adaptability** | Static reasoning process | Dynamic team based on context | Dynamic team based on extracted entities |
| **Domain Transfer** | Limited | Basic domain detection | Sophisticated cross-domain adaptation |

### 🔌 **Enhanced Modular Architecture**
CQB v1.4 separates **extraction**, **agent generation**, and **reasoning orchestration**, enabling:
- **Central Hub**: `cqb_framework.py` generates context-aware experts for any query
- **EAO Context Manager**: `enhanced_rao_context_manager.py` performs structured extraction using LangExtract
- **Universal Schemas**: `universal_extraction_schemas.py` provides domain-agnostic extraction patterns
- **vLLM Integration**: `vllm_langextract_adapter.py` enables LangExtract to use existing models
- **Plug-in Modules**: Independent reasoning orchestrators that leverage context-aware agents
- **Flexible Deployment**: Switch between collaboration, debate, or custom reasoning patterns seamlessly

## 📚 Version History

### v1.4 (CURRENT) - Extraction-Augmented Orchestration (EAO) Implementation
- 🔥 **NEW**: Extraction-Augmented Orchestration (EAO) - Revolutionary advancement beyond RAO
- 🔥 **NEW**: LangExtract integration for sophisticated structured extraction
- 🔥 **NEW**: Universal extraction schemas for domain-agnostic operation
- 🔥 **NEW**: vLLM-LangExtract adapter for seamless model integration
- 🔥 **NEW**: Enhanced context manager with structured entity extraction
- 🔥 **NEW**: Proven domain adaptation (business → medical → research → technical)
- ✨ **Enhanced**: All modules now work with extraction-enhanced context-aware agents
- 🔧 **Maintained**: Full backwards compatibility with v1.3 RAO features

### v1.3 - RAO Architecture Implementation
- 🔥 **NEW**: Retrieval-Augmented Orchestration (RAO) - Novel implementation
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

- 🔥 **Extraction-Augmented Orchestration (EAO)**: Revolutionary implementation - sophisticated extraction drives reasoning teams
- 🔥 **Google LangExtract Integration**: Advanced structured extraction from documents using adapted LangExtract components
- 🔥 **Domain-Agnostic Adaptation**: Proven cross-domain functionality (business, medical, research, technical)
- 🔥 **Context-Aware Agent Generation**: Agents briefed with extracted constraints, metrics, stakeholders, objectives
- 🔥 **Universal Extraction Schemas**: Domain-agnostic patterns for constraints, metrics, stakeholders, objectives
- **Dynamic Agent Generation**: Analyzes queries to determine needed expertise and creates appropriate specialist agents
- **Dual-Model Architecture**: Conservative (analytical) and innovative (creative) agents using different model configurations  
- **🆕 Modular Reasoning Patterns**: Choose between collaborative synthesis, adversarial debate, or custom orchestration
- **🆕 Plug-in Architecture**: Independent modules that leverage the same agent generation service
- **Domain Agnostic**: Works across medical, business, technical, creative, security, research, and analytical domains
- **Rich Output**: JSON export with complete conversation transcripts, agent details, and performance metrics

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- CUDA-capable GPU (recommended)
- 16GB+ VRAM for dual model loading

### Installation

```bash
git clone https://github.com/Baglecake/central-query-brain.git
cd central-query-brain
pip install -r requirements.txt
pip install pydantic PyYAML  # Required for LangExtract integration

# Note: CQB includes adapted LangExtract components - no separate installation needed
# Original LangExtract: https://github.com/google/langextract
```

### 🔥 **EAO Extraction-Augmented Agent Generation**

#### Set Up Context File
```bash
# Create your context file (any domain works)
echo "Your domain-specific context content here..." > v1.4/cqb_framework_rao.txt
```

#### Enable EAO in Config
```yaml
# config.yaml
rao_settings:
  enabled: true
  context_filename: 'cqb_framework_rao.txt'
  max_context_length: 2000
  fallback_to_query_only: true
  use_enhanced_analysis: true  # NEW: Enable LangExtract integration
```

#### Extraction-Augmented Reasoning
```python
from cqb_framework import initialize_cqb
from collaboration_module import AgentCollaborationModule

# Initialize CQB with EAO
cqb = initialize_cqb()

# EAO automatically extracts structured entities and generates appropriate specialists
session_id = cqb.analyze_query_and_generate_agents(
    "Based on our situation, what strategy should we implement?",
    max_agents=6
)

# All agents are now context-aware with structured entity briefings
agents = cqb.get_agents(session_id)
for agent in agents:
    print(f"🧠 {agent.specialty}")
    print(f"   Context: {agent.spec.context_summary[:100]}...")
```

#### 🔌 **Use with Any Module**
```python
# Collaboration with extraction-enhanced context-aware agents
collab_module = AgentCollaborationModule(cqb)
collab_session = collab_module.collaborate_on_query(
    "Develop a comprehensive improvement strategy",
    max_agents=5,
    collaboration_rounds=3
)

# Adversarial debate with extraction-enhanced context-aware agents  
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
# Disable EAO for standard RAO operation
rao_settings:
  enabled: true
  use_enhanced_analysis: false  # Uses v1.3 RAO

# Disable RAO entirely for standard operation
rao_settings:
  enabled: false  # Works exactly like v1.2
```

## 📁 Project Structure

```
central-query-brain/
├── README.md                         # This file
├── LICENSE                           # MIT License
├── requirements.txt                  # Python dependencies
v1.4/                                 # 🔥 NEW: EAO Implementation
├── config.yaml                       # Enhanced with EAO settings
├── cqb_framework.py                  # 🧠 Enhanced with EAO support
├── enhanced_rao_context_manager.py   # 🔥 NEW: LangExtract-powered context analysis
├── vllm_langextract_adapter.py       # 🔥 NEW: vLLM-LangExtract bridge (adapted components)
├── universal_extraction_schemas.py   # 🔥 NEW: Domain-agnostic extraction patterns  
├── langextract_resolver.py           # 🔥 NEW: Content parsing utilities (adapted components)
├── collaboration_module.py           # 🤝 Enhanced with EAO context-aware agents
├── adversarial_debate_module.py      # ⚔️ Enhanced with EAO context-aware agents
├── licenses.yaml                     # Model license registry
├── license_manager.py                # License compliance system
├── cqb_framework_rao.txt             # Your context file
└── third_party_licenses/             # Full license texts
examples/                             # Example scenarios and use cases
├── eao_examples/                     # 🔥 NEW: EAO demonstration scripts
├── rao_examples/                     # RAO demonstration scripts
├── techflow_crisis.py                # AI startup crisis simulation
├── medical_consultation.py           # Medical case analysis
├── security_audit_debate.py          # Red Team vs Blue Team security audit
outputs/                              # Generated analysis results
│   └── sample_outputs/               # Example JSON outputs
docs/                                 # Documentation
│   ├── eao_architecture.md           # 🔥 NEW: EAO system documentation
│   ├── rao_architecture.md           # RAO system documentation
│   ├── architecture.md               # System architecture details
│   ├── agent_types.md                # Agent specification guide
│   └── api_reference.md              # Complete API documentation
```

## 🎯 EAO Examples & Use Cases

### 🔥 **Customer Service Operations (EAO)**
```python
# Context file contains operational details:
# - 25 representatives, 5,000+ monthly interactions
# - $2.1M budget, declining satisfaction scores
# - 48-hour response times, high turnover

query = "How should we improve our customer service operations?"

# EAO extracts structured entities and generates context-aware specialists:
# - Customer Experience (CX) Strategist 🧠
#   Context: "25-person team, 5,000+ interactions, $2.1M budget constraints"
# - Operations Efficiency Expert 🧠  
#   Context: "48-hour response time issue, 35% annual turnover"
# - Data Analyst specializing in Customer Service Metrics 🧠
#   Context: "Current satisfaction: 3.2/5.0, cost per resolution $450"
```

### 🔥 **Climate Research Strategy (EAO)**
```python  
# Context file contains research details:
# - Longitudinal study, 850K data points, 47 regions
# - 12% yield decline in drought areas, 18% with >2°C increases
# - $450K budget remaining, March 2025 deadline

query = "What should be our strategic priorities for the final research phase?"

# EAO extracts structured entities and generates context-aware specialists:
# - Climate Scientist specializing in agricultural impacts 🧠
#   Context: "12% yield decline drought data, 18% reduction >2°C threshold"
# - Agricultural Economist specializing in yield forecasting 🧠
#   Context: "$450K budget remaining, March 2025 deadline"
# - Research Analyst specializing in agricultural data analysis 🧠
#   Context: "850K data points, 47 regions, longitudinal study design"
```

### 🔥 **Medical Case Analysis (EAO)**
```python
# Context file contains clinical details:
# - 65-year-old patient, chest pain, elevated troponin
# - ST elevation ECG, blood pressure 180/95
# - Hospital protocols, door-to-balloon targets

query = "What's the optimal treatment approach for this patient?"

# EAO extracts structured entities and generates context-aware specialists:
# - Emergency Medicine Physician 🧠
#   Context: "ST elevation ECG, troponin 12.5 ng/mL, 65-year-old male"
# - Interventional Cardiologist 🧠
#   Context: "Door-to-balloon target <90 minutes, cath lab available"
# - Critical Care Specialist 🧠
#   Context: "BP 180/95, post-procedure monitoring requirements"
```

## 🧬 **EAO Architecture Deep Dive**

### **Extraction-Augmented Orchestration Pipeline**
```
📄 Context File → 🔍 LangExtract Analysis → 📊 Structured Entities → 🧠 Specialist Mapping → 🤖 Context-Aware Agents
     ↓                    ↓                        ↓                      ↓                     ↓
Domain-specific     Universal schema        Constraints, metrics,    Required expertise    Agents with detailed
   content           extraction            stakeholders, objectives   identification        contextual briefings
```

### **Enhanced Agent Briefing Process**
```python
# Standard Agent (v1.2)
agent.specialty = "Business Strategist"
agent.context_summary = ""  # No context

# RAO Agent (v1.3)  
agent.specialty = "Customer Experience (CX) Strategist"  # Context-driven
agent.context_summary = "Working with customer service operations."

# EAO Agent (v1.4)
agent.specialty = "Customer Experience (CX) Strategist"  # Extraction-driven
agent.context_summary = """Working with customer service operations. 
Key constraints: $2.1M annual budget, 6-month implementation window.
Metrics: 3.2/5.0 satisfaction, 48-hour response time, 35% turnover.
Stakeholders: 25 representatives, 5,000+ monthly customer interactions.
Objectives: Improve satisfaction to 4.0+, reduce costs by 20%."""
```

## 📊 EAO vs RAO vs Standard Comparison

### **Query**: "How should we improve our operations?"

**Standard CQB (v1.2) Generates**:
- Generic Business Strategist
- General Operations Expert  
- Standard Process Analyst

**RAO CQB (v1.3) with Context Generates**:
- Customer Experience (CX) Strategist 🧠
- Operations Efficiency Expert 🧠
- Data Analyst specializing in Customer Service Metrics 🧠

**EAO CQB (v1.4) with Extracted Entities Generates**:
- Customer Experience (CX) Strategist 🧠
- Operations Efficiency Expert specialized in service delivery 🧠
- Data Analyst specializing in Customer Service Metrics 🧠

**EAO Agent Response**:
> *"Given the extracted constraints of **$2.1M annual budget** and **6-month implementation window**, current metrics showing **3.2/5.0 satisfaction** and **48-hour response times**, and stakeholder context of **25 representatives handling 5,000+ monthly interactions**, I recommend a phased CRM implementation prioritizing automated response routing for routine inquiries, which should reduce response times to under 24 hours while staying within budget..."*

**The difference is transformational!** 🚀

## 🏗️ Architecture

### 🧠 **EAO-Enhanced CQB Design**
```
┌─────────────────────────────────────────────────────────┐
│                CQB Framework v1.4                       │
│  ┌─────────────────────────────────────────────────┐    │
│  │     EAO Extraction-Augmented Analysis           │    │
│  │  • LangExtract Integration                      │    │
│  │  • Universal Schema Processing                  │    │
│  │  • Structured Entity Extraction                 │    │
│  │  • Context-Aware Agent Generation               │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────┬───────────────────────────────────────┘
                  │ Extraction-Enhanced Agent Pool
      ┌───────────┴───────────┐
      │                       │
┌─────▼───────┐           ┌─────▼──────┐
│Collaboration│           │Adversarial │
│  Module     │           │  Debate    │
│             │           │  Module    │
│🤝 Enhanced  │           │⚔️ Enhanced  │
│with EAO     │           │with EAO    │
└─────────────┘           └────────────┘
```

### Core Components

1. **🧠 CQB Framework** (`cqb_framework.py`) - Enhanced with EAO
   - Extraction-augmented query analysis and agent specification
   - EAO integration with RAO backwards compatibility
   - LangExtract-powered domain-specific agent generation
   - **Serves as central hub for all reasoning modules**

2. **🔥 Enhanced RAO Context Manager** (`enhanced_rao_context_manager.py`) - NEW
   - LangExtract integration for sophisticated document analysis
   - Universal schema-based entity extraction
   - Structured context-aware agent specification enhancement
   - Smart constraint, metric, and stakeholder identification

3. **🔥 vLLM-LangExtract Adapter** (`vllm_langextract_adapter.py`) - NEW
   - Seamless integration allowing LangExtract to use existing vLLM models
   - Zero additional GPU memory overhead
   - Production-ready error handling and fallbacks

4. **🔥 Universal Extraction Schemas** (`universal_extraction_schemas.py`) - NEW
   - Domain-agnostic extraction patterns for any field
   - Constraint, metric, stakeholder, and objective identification
   - Cross-domain adaptation capabilities

5. **🤝 Collaboration Module** (`collaboration_module.py`) - Enhanced
   - Works seamlessly with extraction-enhanced context-aware agents
   - Enhanced collaboration with structured entity understanding
   - Context-informed synthesis based on extracted constraints

6. **⚔️ Adversarial Debate Module** (`adversarial_debate_module.py`) - Enhanced
   - Extraction-enhanced context-aware adversarial reasoning
   - Domain-specific debate frameworks with entity grounding
   - Enhanced judge evaluation with structured context

## 🧪 Research Applications

CQB v1.4 enables research in:

- **🔥 Extraction-Augmented Orchestration**: Revolutionary AI architecture for structured extraction-driven team assembly
- **🔥 Cross-Domain AI Adaptation**: How structured extraction enables seamless domain transfer
- **🔥 Context-Aware Multi-Agent Systems**: Impact of structured entity extraction on reasoning team composition
- **🔥 Transparent Knowledge Construction**: Making AI reasoning processes visible through extraction → specialist mapping
- **🔥 Universal Extraction Schemas**: Domain-agnostic patterns for organizational context understanding
- **Epistemic Modeling**: How knowledge emerges from different reasoning patterns enhanced with structured context
- **Multi-Agent Coordination**: Team dynamics in extraction-enhanced vs standard agents
- **Decision Support**: Expert system augmentation with structured context understanding
- **AI Safety**: Understanding emergent behaviors in extraction-informed reasoning frameworks

## 🚀 **Getting Started Examples**

### Run EAO Context Analysis
```bash
python examples/eao_examples/test_extraction_analysis.py
```

### Run Extraction-Augmented Collaboration
```bash
python examples/eao_examples/test_eao_collaboration.py
```

### Compare EAO vs RAO vs Standard
```bash
python examples/eao_examples/compare_eao_rao_standard.py
```

### Test Cross-Domain Adaptation
```bash
python examples/eao_examples/test_domain_adaptation.py
```

## 🤝 Contributing

We welcome contributions! Areas of interest:

- **🔥 Enhanced extraction schemas** (legal, creative, scientific, technical domains)
- **🔥 Advanced context analysis** (semantic similarity, vector embeddings, graph extraction)
- **🔥 New reasoning modules** (consensus building, devil's advocate, expert panels)
- **🔥 Domain-specific orchestration patterns** (medical rounds, research committees, technical reviews)
- **🔥 Cross-domain evaluation metrics** (adaptation quality, extraction accuracy)
- Enhanced evaluation metrics and benchmarks
- Integration with external knowledge sources
- Performance optimizations
- Multi-modal context support (documents, images, data)

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
- **Integrates Google's LangExtract** ([github.com/google/langextract](https://github.com/google/langextract)) for sophisticated structured extraction
  - Components adapted: inference patterns, data structures, prompting templates, and schema validation
  - Licensed under Apache 2.0 License
  - Special thanks to the Google Research team for developing this powerful extraction framework
- Inspired by research in collective intelligence and epistemic democracy
- Thanks to the open-source AI community for model development
- University of Toronto for supporting open research initiatives

## 📋 LangExtract Integration Details

CQB v1.4 adapts core components from Google's LangExtract to enable structured extraction with vLLM models:

### **Adapted Components:**
- **Inference Architecture**: Adapted `BaseLanguageModel` interface to work with vLLM
- **Data Structures**: Utilized `Extraction`, `ExampleData`, and schema classes
- **Prompting System**: Adapted few-shot prompting templates for entity extraction
- **Schema Validation**: Integrated structured output validation

### **CQB Innovations:**
- **vLLM Integration**: Custom adapter allowing LangExtract to use local vLLM models
- **Universal Schemas**: Domain-agnostic extraction patterns for organizational contexts
- **Agent Generation**: Novel application of extraction results to drive AI team assembly
- **Context-Aware Orchestration**: First implementation of extraction-driven reasoning team composition

### **License Compatibility:**
- LangExtract: Apache 2.0 License (compatible with CQB's MIT License)
- All adaptations maintain original license requirements
- Full attribution preserved in source code headers

## 📄 License & Attribution

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for complete details.

### **Citation Information**
```bibtex
@software{CQB,
  author = {Del Coburn},
  title = {CQB: Central Query Brain - EAO Architecture for Extraction-Augmented Multi-Agent Reasoning},
  year = {2025},
  version = {1.4},
  institution = {University of Toronto},
  url = {https://github.com/Baglecake/CQB},
  note = {First implementation of Extraction-Augmented Orchestration (EAO). Integrates Google's LangExtract.}
}

@software{LangExtract,
  author = {Google Research},
  title = {LangExtract: Structured Information Extraction with LLMs},
  year = {2025},
  url = {https://github.com/google/langextract},
  note = {Sophisticated structured extraction framework adapted in CQB v1.4}
}
```

---

## 👨‍💻 Author

**Del Coburn**  
University of Toronto  
📧 del.coburn@mail.utoronto.ca  

*For project-related questions, please use GitHub Issues or Discussions. For other inquiries, feel free to reach out via email.*

---
**🔥 World's first Extraction-Augmented Orchestration (EAO) implementation**

**Built for researchers, decision-makers, and AI developers who need sophisticated context-aware multi-agent reasoning capabilities.**

**🆕 v1.4: Revolutionary EAO architecture - structured extraction drives reasoning team assembly.**

**Made with ❤️ for democratizing AI understanding**

**Version**: v1.4 | **Last Updated**: 2025-08-04 |

---
