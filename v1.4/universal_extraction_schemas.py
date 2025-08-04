# =============================================================================
# Universal Extraction Schemas for Domain-Agnostic Context Analysis
# =============================================================================

from typing import List, Dict, Any
from dataclasses import dataclass

# LangExtract imports (adapted from provided files)
from langextract.data import ExampleData, Extraction
from langextract.prompting import PromptTemplateStructured

# =============================================================================
# Universal Extraction Schema Definition
# =============================================================================

class UniversalExtractionSchemas:
    """Domain-agnostic extraction schemas for context analysis.
    
    These schemas are designed to work across medical, business, technical,
    legal, and other domains by focusing on universal organizational elements.
    """
    
    @staticmethod
    def get_context_analysis_description() -> str:
        """Get the prompt description for context analysis extraction."""
        return """
Extract structured information from this document to understand the organizational context and requirements.

Focus on identifying:
1. CONSTRAINTS: Budget limits, time constraints, resource limitations, regulatory requirements
2. METRICS: Performance indicators, measurements, targets, current status
3. STAKEHOLDERS: Roles, teams, departments, external parties involved
4. OBJECTIVES: Goals, targets, desired outcomes, success criteria
5. DOMAIN_INDICATORS: Field-specific terminology, processes, standards
6. RESOURCES: Tools, systems, capabilities, infrastructure

Extract information exactly as it appears in the text. Do not infer or add information not explicitly stated.
Provide meaningful attributes to add context for specialist selection.
"""

    @staticmethod
    def get_universal_examples() -> List[ExampleData]:
        """Get universal extraction examples that work across domains."""
        
        return [
            # Business/Operations Example
            ExampleData(
                text="""Department budget is $2.1M annually with 25 full-time representatives. 
Current customer satisfaction rating is 3.2/5.0, with average response time of 48 hours. 
Target is to improve satisfaction to 4.0+ while reducing costs by 20%. 
Implementation window is 6 months. Must comply with data privacy regulations.""",
                extractions=[
                    Extraction(
                        extraction_class="constraint",
                        extraction_text="budget is $2.1M annually",
                        attributes={
                            "type": "financial",
                            "amount": "2100000",
                            "frequency": "annual",
                            "constraint_category": "budget_limit"
                        }
                    ),
                    Extraction(
                        extraction_class="constraint",
                        extraction_text="Implementation window is 6 months",
                        attributes={
                            "type": "temporal",
                            "duration": "6_months",
                            "constraint_category": "time_limit"
                        }
                    ),
                    Extraction(
                        extraction_class="constraint",
                        extraction_text="Must comply with data privacy regulations",
                        attributes={
                            "type": "regulatory",
                            "domain": "data_privacy",
                            "constraint_category": "compliance"
                        }
                    ),
                    Extraction(
                        extraction_class="metric",
                        extraction_text="customer satisfaction rating is 3.2/5.0",
                        attributes={
                            "type": "performance",
                            "current_value": "3.2",
                            "scale": "5.0",
                            "metric_category": "satisfaction"
                        }
                    ),
                    Extraction(
                        extraction_class="metric",
                        extraction_text="average response time of 48 hours",
                        attributes={
                            "type": "operational",
                            "current_value": "48",
                            "unit": "hours",
                            "metric_category": "response_time"
                        }
                    ),
                    Extraction(
                        extraction_class="stakeholder",
                        extraction_text="25 full-time representatives",
                        attributes={
                            "role": "customer_service_rep",
                            "count": "25",
                            "employment_type": "full_time",
                            "stakeholder_category": "internal_team"
                        }
                    ),
                    Extraction(
                        extraction_class="objective",
                        extraction_text="improve satisfaction to 4.0+",
                        attributes={
                            "type": "performance_improvement",
                            "target_value": "4.0+",
                            "metric": "satisfaction",
                            "objective_category": "quality_improvement"
                        }
                    ),
                    Extraction(
                        extraction_class="objective",
                        extraction_text="reducing costs by 20%",
                        attributes={
                            "type": "cost_reduction",
                            "target_percentage": "20",
                            "objective_category": "efficiency_improvement"
                        }
                    )
                ]
            ),
            
            # Medical/Healthcare Example
            ExampleData(
                text="""Patient presents with chest pain, elevated troponin levels at 0.8 ng/mL. 
ECG shows ST elevation in leads II, III, aVF. Blood pressure 150/90, heart rate 102 bpm.
Cardiologist consultation required within 30 minutes. Hospital policy requires dual antiplatelet therapy.
Family history of coronary artery disease.""",
                extractions=[
                    Extraction(
                        extraction_class="metric",
                        extraction_text="troponin levels at 0.8 ng/mL",
                        attributes={
                            "type": "laboratory",
                            "biomarker": "troponin",
                            "value": "0.8",
                            "unit": "ng/mL",
                            "metric_category": "cardiac_biomarker"
                        }
                    ),
                    Extraction(
                        extraction_class="metric",
                        extraction_text="Blood pressure 150/90",
                        attributes={
                            "type": "vital_sign",
                            "systolic": "150",
                            "diastolic": "90",
                            "metric_category": "blood_pressure"
                        }
                    ),
                    Extraction(
                        extraction_class="constraint",
                        extraction_text="Cardiologist consultation required within 30 minutes",
                        attributes={
                            "type": "temporal",
                            "timeframe": "30_minutes",
                            "requirement": "specialist_consultation",
                            "constraint_category": "time_critical"
                        }
                    ),
                    Extraction(
                        extraction_class="constraint",
                        extraction_text="Hospital policy requires dual antiplatelet therapy",
                        attributes={
                            "type": "clinical_protocol",
                            "treatment": "dual_antiplatelet_therapy",
                            "constraint_category": "treatment_protocol"
                        }
                    ),
                    Extraction(
                        extraction_class="stakeholder",
                        extraction_text="Cardiologist",
                        attributes={
                            "role": "specialist_physician",
                            "specialty": "cardiology",
                            "stakeholder_category": "medical_specialist"
                        }
                    ),
                    Extraction(
                        extraction_class="domain_indicator",
                        extraction_text="ST elevation in leads II, III, aVF",
                        attributes={
                            "domain": "cardiology",
                            "test_type": "ECG",
                            "finding": "ST_elevation",
                            "leads": "inferior",
                            "domain_category": "diagnostic_finding"
                        }
                    )
                ]
            ),
            
            # Technical/Engineering Example
            ExampleData(
                text="""System requires 99.9% uptime with maximum latency of 100ms. 
Current architecture uses microservices with Kubernetes orchestration.
Database handles 10,000 transactions per second. Security team mandates OAuth 2.0 authentication.
DevOps engineer needs access to production logs. Budget allocated for cloud infrastructure is $50K monthly.""",
                extractions=[
                    Extraction(
                        extraction_class="constraint",
                        extraction_text="requires 99.9% uptime",
                        attributes={
                            "type": "performance",
                            "sla": "99.9",
                            "metric": "uptime",
                            "constraint_category": "availability_requirement"
                        }
                    ),
                    Extraction(
                        extraction_class="constraint",
                        extraction_text="maximum latency of 100ms",
                        attributes={
                            "type": "performance",
                            "max_value": "100",
                            "unit": "milliseconds",
                            "constraint_category": "latency_requirement"
                        }
                    ),
                    Extraction(
                        extraction_class="constraint",
                        extraction_text="Security team mandates OAuth 2.0 authentication",
                        attributes={
                            "type": "security",
                            "protocol": "OAuth_2.0",
                            "requirement": "authentication",
                            "constraint_category": "security_requirement"
                        }
                    ),
                    Extraction(
                        extraction_class="resource",
                        extraction_text="microservices with Kubernetes orchestration",
                        attributes={
                            "architecture": "microservices",
                            "orchestration": "kubernetes",
                            "resource_category": "infrastructure"
                        }
                    ),
                    Extraction(
                        extraction_class="metric",
                        extraction_text="Database handles 10,000 transactions per second",
                        attributes={
                            "type": "throughput",
                            "value": "10000",
                            "unit": "transactions_per_second",
                            "metric_category": "database_performance"
                        }
                    ),
                    Extraction(
                        extraction_class="stakeholder",
                        extraction_text="DevOps engineer",
                        attributes={
                            "role": "devops_engineer",
                            "responsibilities": "production_monitoring",
                            "stakeholder_category": "technical_team"
                        }
                    ),
                    Extraction(
                        extraction_class="constraint",
                        extraction_text="Budget allocated for cloud infrastructure is $50K monthly",
                        attributes={
                            "type": "financial",
                            "amount": "50000",
                            "frequency": "monthly",
                            "allocation": "cloud_infrastructure",
                            "constraint_category": "infrastructure_budget"
                        }
                    )
                ]
            )
        ]
    
    @staticmethod
    def create_extraction_template() -> PromptTemplateStructured:
        """Create the complete extraction template for context analysis."""
        
        return PromptTemplateStructured(
            description=UniversalExtractionSchemas.get_context_analysis_description(),
            examples=UniversalExtractionSchemas.get_universal_examples()
        )
    
    @staticmethod
    def get_specialist_mapping() -> Dict[str, List[str]]:
        """Get mapping from extracted elements to specialist types."""
        
        return {
            # Financial constraints suggest need for financial specialists
            "financial_constraint": [
                "Budget Analyst", "Financial Planner", "Cost Optimization Expert"
            ],
            
            # Temporal constraints suggest project management
            "temporal_constraint": [
                "Project Manager", "Implementation Specialist", "Timeline Coordinator"
            ],
            
            # Regulatory constraints suggest compliance experts
            "regulatory_constraint": [
                "Compliance Officer", "Regulatory Specialist", "Legal Advisor"
            ],
            
            # Performance metrics suggest operational experts
            "performance_metric": [
                "Performance Analyst", "Operations Manager", "Quality Assurance Specialist"
            ],
            
            # Medical domain indicators
            "medical_domain": [
                "Medical Specialist", "Clinical Researcher", "Healthcare Analyst"
            ],
            
            # Technical domain indicators
            "technical_domain": [
                "Technical Architect", "Systems Engineer", "DevOps Specialist"
            ],
            
            # Customer service indicators
            "customer_service_domain": [
                "Customer Experience (CX) Strategist", "Service Operations Expert", "Customer Success Manager"
            ],
            
            # Default specialists for complex scenarios
            "general": [
                "Strategic Analyst", "Process Improvement Expert", "Change Management Specialist"
            ]
        }

# =============================================================================
# Testing and Validation
# =============================================================================

def test_extraction_schemas():
    """Test the universal extraction schemas."""
    
    print("🧪 Testing Universal Extraction Schemas...")
    
    try:
        # Test template creation
        template = UniversalExtractionSchemas.create_extraction_template()
        print(f"✅ Template created with {len(template.examples)} examples")
        
        # Test specialist mapping
        mapping = UniversalExtractionSchemas.get_specialist_mapping()
        print(f"✅ Specialist mapping has {len(mapping)} categories")
        
        # Validate examples
        for i, example in enumerate(template.examples):
            print(f"✅ Example {i+1}: {len(example.extractions)} extractions")
            
            # Check extraction categories
            categories = set(e.extraction_class for e in example.extractions)
            print(f"   Categories: {', '.join(categories)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        return False

if __name__ == "__main__":
    print("📋 Universal Extraction Schemas")
    print("=" * 50)
    print("Domain-agnostic schemas for context analysis across:")
    print("- Business/Operations")
    print("- Medical/Healthcare") 
    print("- Technical/Engineering")
    print("- And other domains...")
    
    test_extraction_schemas()
