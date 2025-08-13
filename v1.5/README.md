# Central Query Brain (CQB)

**A modular AI reasoning engine with specialist-specific context awareness for precision multi-agent orchestration**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![vLLM](https://img.shields.io/badge/Powered%20by-vLLM-green.svg)](https://github.com/vllm-project/vllm)
[![University of Toronto](https://img.shields.io/badge/University%20of-Toronto-003F7F.svg)](https://www.utoronto.ca/)
[![Research](https://img.shields.io/badge/Type-Research-brightgreen.svg)](https://github.com)
[![RAO](https://img.shields.io/badge/Architecture-RAO-red.svg)](https://github.com)

## Overview
**v1.5 - Specialist-Specific Context Awareness**  

Central Query Brain (CQB) v1.5 introduces **Specialist-Specific Context Awareness** - a revolutionary advancement in Retrieval-Augmented Orchestration (RAO) where each AI agent receives **personalized, relevance-filtered context** based on their expertise. Instead of generic briefings, specialists now get precisely what they need to excel in their domain.

**🔥 KEY INNOVATION in v1.5**: **Specialist-Specific Context Summaries**
- Each agent receives **tailored briefings** filtered for their expertise
- **Relevance scoring** ensures specialists focus on their domain
- **Priority-based extraction filtering** - financial experts see budgets first, project managers see timelines first
- **Context personalization** at the individual agent level

**Additional v1.5 Improvements**:
- Streamlined execution with enhanced parsing reliability
- Increased token limits (4096) for comprehensive extractions
- Improved error recovery and fallback mechanisms

## 🧠 **The Specialist-Specific Context Revolution**

### **v1.4 vs v1.5: The Transformation**

#### **v1.4 - Generic Context (All Agents Get Same Info)**
```python
# Every agent receives identical context
all_agents.context = """
Working with business operations. 
Key concepts: budget, timeline, stakeholders, metrics.
"""
```

#### **v1.5 - Specialist-Specific Context (Personalized Briefings)**
```python
# Budget Analyst receives:
budget_analyst.context = """
SPECIALIZED CONTEXT FOR: Budget Analyst
Your Expertise Focus: ['financial_constraints', 'cost_optimization']

PRIORITY INSIGHTS FOR YOUR SPECIALTY:
CONSTRAINT (High Priority):
- NSF grant: $2.1M over 4 years (year 3 of funding)
- Equipment costs: $380K for sensors and computing
- Personnel: $1.2M for salaries and benefits

RESOURCE (Supporting Context):
- $450K for site visits and equipment
"""

# Project Manager receives:
project_manager.context = """
SPECIALIZED CONTEXT FOR: Project Manager
Your Expertise Focus: ['timeline_management', 'deliverable_tracking']

PRIORITY INSIGHTS FOR YOUR SPECIALTY:
CONSTRAINT (High Priority):
- Implementation window: 6 months
- Year 3 of 4-year grant cycle
- March 2025 submission deadline

STAKEHOLDER (Supporting Context):
- 8 PhD candidates requiring coordination
- 12 Master's students on timeline
"""

# Healthcare Specialist receives:
healthcare_specialist.context = """
SPECIALIZED CONTEXT FOR: Healthcare Market Analyst
Your Expertise Focus: ['market_opportunity', 'pivot_strategy']

PRIORITY INSIGHTS FOR YOUR SPECIALTY:
OBJECTIVE (High Priority):
- Pivot to healthcare vertical market
- 4 healthcare pilot customers (23% revenue)

METRICS (Supporting Context):
- Current healthcare segment growth: 23%
- HIPAA compliance work completed
"""
```

## 🎯 **How Specialist-Specific Context Works**

### **The Intelligence Pipeline**
```
Document Analysis
       ↓
Structured Extraction (constraints, metrics, objectives, stakeholders)
       ↓
🔥 SPECIALIST MAPPING (NEW in v1.5)
       ↓
For Each Agent:
  1. Identify expertise domain
  2. Map to priority extraction types
  3. Score relevance of each extraction
  4. Filter & prioritize by specialty
  5. Generate personalized briefing
       ↓
Context-Aware Specialist Team with Individualized Intelligence
```

### **Specialty-Extraction Mapping Examples**

| Specialist | Priority Extractions | Key Concepts | Focus Areas |
|------------|---------------------|--------------|-------------|
| **Venture Capitalist** | Constraints, Stakeholders | funding, runway, valuation, Series A | investor_relations, funding_timeline |
| **Project Manager** | Constraints, Objectives | timeline, milestone, deadline, implementation | project_constraints, deliverable_tracking |
| **Budget Analyst** | Constraints, Resources | budget, cost, expenses, capital | financial_constraints, cost_optimization |
| **Strategic Partnerships Manager** | Objectives, Constraints | partnership, integration, revenue, collaboration | partnership_opportunities, integration_challenges |
| **Healthcare Market Analyst** | Objectives, Stakeholders | healthcare, medical, pivot, vertical | market_opportunity, competitive_landscape |

## 📚 Version History

### v1.5 (CURRENT) - Specialist-Specific Context Awareness
- 🔥 **KEY INNOVATION**: Individual context personalization for each specialist
- 🔥 **NEW**: Relevance scoring and priority-based extraction filtering
- 🔥 **NEW**: Expertise-to-extraction mapping system
- 🔥 **NEW**: Dynamic context building based on agent specialty
- ✨ **Enhanced**: Streamlined execution with robust parsing
- ✨ **Enhanced**: Token management improvements (4096 limit)
- 🔧 **Maintained**: Full backwards compatibility with v1.4

### v1.4 - LangExtract Integration
- Integration of Google's LangExtract for structured extraction
- Universal extraction schemas for domain-agnostic operation
- Generic context summaries for all agents

### v1.3 - RAO Architecture
- Initial Retrieval-Augmented Orchestration implementation
- Context-aware agent generation from documents

## 🚀 Quick Start

### Configuration
```yaml
# config.yaml
conservative_model:
  max_tokens: 4096  # Required for complete extractions
  # ... other settings

rao_settings:
  enabled: true
  context_filename: 'cqb_framework_rao.txt'
  max_context_length: 2000
```

### Basic Usage
```python
from cqb_framework import initialize_cqb

# Initialize CQB v1.5
cqb = initialize_cqb()

# Generate specialists with personalized context
session_id = cqb.analyze_query_and_generate_agents(
    "How should we optimize our research budget allocation?",
    max_agents=6
)

# Each agent has specialty-specific context
agents = cqb.get_agents(session_id)
for agent in agents:
    print(f"🧠 {agent.specialty}")
    print(f"   Focus: {agent.spec.context_summary[:200]}...")
```

## 🧬 **Real-World Impact of Specialist Context**

### **Example: TechFlow AI Startup Crisis**

**Query**: "What should be our strategic priority?"

#### **Generic Context (v1.4) - All Agents See**:
> "Company has funding issues, technical debt, partnership opportunities..."

#### **Specialist Context (v1.5) - Each Expert Sees What Matters**:

**Venture Capitalist Sees**:
> "Series A at risk from Kleiner Perkins ($12M), current runway 5.8 months, burn rate $485K/month, need $200K MRR by Dec 2024 (currently $67K)"

**Microsoft Partnership Specialist Sees**:
> "Azure Cognitive Services integration opportunity, $2.8M guaranteed revenue over 18 months, white-label terms under discussion"

**Healthcare Market Analyst Sees**:
> "Healthcare vertical showing 23% of revenue, 4 pilot customers, HIPAA compliance completed, potential pivot opportunity"

### **The Result**: Dramatically improved response quality because each specialist works with their domain-relevant information!

## 📊 **Key Improvements in v1.5**

| Aspect | Generic Context (v1.4) | Specialist Context (v1.5) |
|--------|------------------------|---------------------------|
| **Context Distribution** | All agents get same summary | Each specialist gets filtered context |
| **Extraction Prioritization** | None | Based on specialist expertise |
| **Relevance Filtering** | None | Scored by concept matching |
| **Information Density** | Full context for everyone | Targeted insights per role |
| **Context Length** | Fixed for all | Varies by relevant content |

## 🏗️ Architecture Highlights

### **Core Innovation: Context Personalization Engine**

```python
# enhanced_rao_context_manager.py - The Magic Happens Here

def _build_agent_context_summary(self, extractions, query, 
                                domain_analysis, agent_specialty):
    """Build context summary tailored to specific agent specialty."""
    
    # Get specialty-specific focus areas
    specialty_focus = self._get_specialty_extraction_focus(agent_specialty)
    
    # Filter extractions by relevance to this specialty
    relevant_extractions = self._filter_extractions_for_specialty(
        extractions, specialty_focus
    )
    
    # Score relevance and prioritize
    for extraction in relevant_extractions:
        relevance_score = self._calculate_concept_relevance(
            extraction.text, specialty_focus['key_concepts']
        )
    
    # Build personalized briefing with priority insights first
    return personalized_context
```

## 🎯 Use Cases

### **Financial Analysis**
- Budget Analysts see financial constraints first
- CFOs see revenue metrics and burn rates prioritized
- Investors see valuation and growth metrics highlighted

### **Project Management**
- Project Managers see timelines and milestones first
- Implementation Specialists see technical constraints prioritized
- Coordinators see stakeholder dependencies highlighted

### **Healthcare Applications**
- Medical Specialists see clinical metrics first
- Healthcare Analysts see market opportunities prioritized
- Compliance Officers see regulatory requirements highlighted

## 📁 Project Structure

```
v1.5/
├── cqb_framework.py                  # Core framework with RAO
├── enhanced_rao_context_manager.py   # 🔥 Specialist context personalization
│   ├── _get_specialty_extraction_focus()     # Maps specialties to priorities
│   ├── _filter_extractions_for_specialty()   # Relevance filtering
│   ├── _calculate_concept_relevance()        # Scoring algorithm
│   └── _build_agent_context_summary()        # Personalized briefing generator
├── universal_extraction_schemas.py   # Domain patterns
├── vllm_langextract_adapter.py      # Model integration
└── config.yaml                      # Configuration (set max_tokens: 4096)
```

## 🤝 Contributing

Areas of interest for v1.5+:
- Additional specialty-to-extraction mappings
- Enhanced relevance scoring algorithms
- Cross-domain specialist coordination
- Multi-modal context personalization

## 📄 Citation

```bibtex
@software{CQB_v15,
  author = {[Your Name]},
  title = {CQB v1.5: Specialist-Specific Context Awareness for Multi-Agent Orchestration},
  year = {2025},
  version = {1.5},
  institution = {University of Toronto},
  note = {First implementation of personalized context briefings for AI specialists}
}
```

## 🙏 Acknowledgments

- Built on [vLLM](https://github.com/vllm-project/vllm) for efficient inference
- Integrates adapted components from [Google's LangExtract](https://github.com/google/langextract)
- University of Toronto for supporting this research

---

**🔥 v1.5: Every specialist gets exactly the context they need to excel**

**The first multi-agent system where each expert receives personalized, domain-relevant briefings**

**Version**: 1.5 | **Status**: Production Ready | **Last Updated**: 2025-01-08

---
