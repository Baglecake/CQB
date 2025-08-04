# =============================================================================
# Enhanced RAO Context Manager - Extraction-Augmented Orchestration
# =============================================================================

import os
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict

# LangExtract imports (adapted from provided files) 
from langextract.data import FormatType, Document, AnnotatedDocument
from langextract.prompting import QAPromptGenerator
from langextract.schema import GeminiSchema
from langextract import resolver

# Local imports
from vllm_langextract_adapter import VLLMLanguageModel
from universal_extraction_schemas import UniversalExtractionSchemas

# =============================================================================
# Enhanced RAO Context Manager with LangExtract Integration
# =============================================================================

class EnhancedRAOContextManager:
    """Enhanced RAO context manager using LangExtract for sophisticated document analysis.
    
    This replaces the basic keyword-based context analysis with structured extraction
    to enable more precise agent generation based on document content.
    """
    
    def __init__(self, cqb_model_manager, max_context_length: int = 2000):
        """Initialize the enhanced context manager.
        
        Args:
            cqb_model_manager: CQB model manager for vLLM inference
            max_context_length: Maximum context length for processing
        """
        self.max_context_length = max_context_length
        self.model_manager = cqb_model_manager
        self.context_file_cache = {}
        
        # Initialize LangExtract components
        self._initialize_extraction_engine()
        
        print("✅ Enhanced RAO Context Manager initialized with LangExtract")
    
    def _initialize_extraction_engine(self):
        """Initialize the LangExtract extraction engine."""
        try:
            # Create vLLM adapter
            self.vllm_language_model = VLLMLanguageModel(
                cqb_model_manager=self.model_manager,
                model_id="conservative_model",  # Use conservative model for extraction
                temperature=0.3  # Lower temperature for consistent extraction
            )
            
            # Get universal extraction template
            self.extraction_template = UniversalExtractionSchemas.create_extraction_template()
            
            # Create prompt generator
            self.prompt_generator = QAPromptGenerator(
                template=self.extraction_template,
                format_type=FormatType.JSON,
                fence_output=True  # Use fenced output for better parsing
            )
            
            # Get specialist mapping
            self.specialist_mapping = UniversalExtractionSchemas.get_specialist_mapping()
            
            print("✅ LangExtract extraction engine initialized")
            
        except Exception as e:
            print(f"❌ Failed to initialize extraction engine: {e}")
            raise
    
    def load_context_file(self, filename: str) -> Optional[str]:
        """Load context file content with caching.
        
        Args:
            filename: Path to context file
            
        Returns:
            File content or None if not found
        """
        try:
            if filename in self.context_file_cache:
                print(f"📋 Using cached context file: {filename}")
                return self.context_file_cache[filename]
            
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Cache the content
                self.context_file_cache[filename] = content
                
                print(f"✅ Loaded context file: {filename} ({len(content)} chars)")
                return content
            else:
                print(f"⚠️ Context file not found: {filename}")
                return None
                
        except Exception as e:
            print(f"❌ Error loading context file {filename}: {e}")
            return None
    
    def analyze_context_for_agent_generation(self, context_content: str, 
                                          query: str) -> Dict[str, Any]:
        """Analyze context content using LangExtract for agent generation.
        
        Args:
            context_content: Raw context document content
            query: Query that will be processed by agents
            
        Returns:
            Dictionary with agent generation parameters
        """
        if not context_content:
            return self._get_fallback_analysis(query)
        
        print("🔍 Running enhanced extraction analysis...")
        
        try:
            # Step 1: Extract structured information using LangExtract
            extraction_results = self._perform_extraction(context_content)
            
            # Step 2: Analyze extractions for domain and complexity
            domain_analysis = self._analyze_extraction_results(extraction_results)
            
            # Step 3: Generate specialist requirements
            specialist_requirements = self._generate_specialist_requirements(
                extraction_results, query, domain_analysis
            )
            
            # Step 4: Build context summary for agents
            context_summary = self._build_agent_context_summary(
                extraction_results, query, domain_analysis
            )
            
            return {
                "specialties_needed": specialist_requirements,
                "context_summary": context_summary,
                "domain_focus": domain_analysis["primary_domain"],
                "complexity_level": domain_analysis["complexity_level"],
                "key_concepts": domain_analysis["key_concepts"],
                "extraction_metadata": {
                    "total_extractions": len(extraction_results),
                    "extraction_categories": list(set(e.extraction_class for e in extraction_results)),
                    "extraction_method": "langextract_enhanced"
                }
            }
            
        except Exception as e:
            print(f"❌ Enhanced extraction failed: {e}")
            print("🔄 Falling back to basic analysis...")
            return self._get_fallback_analysis(query)
    
    def _perform_extraction(self, context_content: str) -> List[Any]:
        """Perform structured extraction using LangExtract.
        
        Args:
            context_content: Document content to extract from
            
        Returns:
            List of Extraction objects
        """
        print("🔍 Performing LangExtract structured extraction...")
        
        try:
            # Truncate content if too long
            if len(context_content) > self.max_context_length:
                context_content = context_content[:self.max_context_length] + "..."
                print(f"📝 Truncated context to {self.max_context_length} characters")
            
            # Generate extraction prompt
            extraction_prompt = self.prompt_generator.render(context_content)
            
            # Run extraction using vLLM adapter
            response = self.vllm_language_model.generate_single(
                extraction_prompt,
                temperature=0.3,
                max_output_tokens=1024
            )
            
            # Parse the structured response
            extraction_results = self._parse_extraction_response(response)
            
            print(f"✅ Extracted {len(extraction_results)} structured entities")
            return extraction_results
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return []
    
    def _parse_extraction_response(self, response: str) -> List[Any]:
        """Parse LangExtract response into structured extractions.
        
        Args:
            response: Raw model response
            
        Returns:
            List of extraction dictionaries
        """
        try:
            # Extract JSON from fenced code blocks if present
            extracted_content = resolver.extract_fenced_content(response)
            if extracted_content:
                response = extracted_content
            
            # Parse JSON response
            response_data = json.loads(response)
            
            # Extract the extractions list
            extractions = response_data.get("extractions", [])
            
            return extractions
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print(f"Raw response: {response[:200]}...")
            return []
        except Exception as e:
            print(f"❌ Response parsing failed: {e}")
            return []
    
    def _analyze_extraction_results(self, extractions: List[Dict]) -> Dict[str, Any]:
        """Analyze extraction results to determine domain and complexity.
        
        Args:
            extractions: List of extraction dictionaries
            
        Returns:
            Domain analysis results
        """
        # Count extraction types and analyze patterns
        category_counts = defaultdict(int)
        domain_indicators = defaultdict(int)
        complexity_signals = 0
        key_concepts = []
        
        for extraction in extractions:
            # Count extraction categories
            for key, value in extraction.items():
                if not key.endswith("_attributes"):
                    category_counts[key] += 1
                    
                    # Extract key concepts
                    if isinstance(value, str) and len(value) > 3:
                        key_concepts.append(value)
            
            # Analyze attributes for domain indicators
            for key, value in extraction.items():
                if key.endswith("_attributes") and isinstance(value, dict):
                    # Look for domain indicators in attributes
                    domain = value.get("domain", "")
                    if domain:
                        domain_indicators[domain] += 1
                    
                    # Check for complexity indicators
                    if any(indicator in str(value).lower() for indicator in 
                           ["complex", "critical", "advanced", "specialized"]):
                        complexity_signals += 1
        
        # Determine primary domain
        if domain_indicators:
            primary_domain = max(domain_indicators.items(), key=lambda x: x[1])[0]
        else:
            # Infer domain from extraction patterns
            if category_counts.get("metric", 0) > 2 and category_counts.get("constraint", 0) > 1:
                primary_domain = "business_operations"
            elif category_counts.get("stakeholder", 0) > 1:
                primary_domain = "organizational"
            else:
                primary_domain = "general"
        
        # Determine complexity level
        complexity_level = "high" if complexity_signals > 2 else "medium"
        
        return {
            "primary_domain": primary_domain,
            "complexity_level": complexity_level,
            "key_concepts": key_concepts[:15],  # Limit concepts
            "category_distribution": dict(category_counts),
            "domain_indicators": dict(domain_indicators)
        }
    
    def _generate_specialist_requirements(self, extractions: List[Dict], 
                                        query: str, domain_analysis: Dict) -> List[str]:
        """Generate specialist requirements based on extractions.
        
        Args:
            extractions: Extraction results
            query: Original query
            domain_analysis: Domain analysis results
            
        Returns:
            List of required specialist types
        """
        specialists_needed = set()
        
        # Analyze extractions for specialist needs
        for extraction in extractions:
            for key, value in extraction.items():
                if key.endswith("_attributes") and isinstance(value, dict):
                    # Map constraint types to specialists
                    constraint_type = value.get("type", "")
                    if constraint_type == "financial":
                        specialists_needed.add("Budget Analyst")
                        specialists_needed.add("Financial Planner")
                    elif constraint_type == "temporal":
                        specialists_needed.add("Project Manager")
                        specialists_needed.add("Implementation Specialist")
                    elif constraint_type == "regulatory":
                        specialists_needed.add("Compliance Officer")
                    elif constraint_type == "security":
                        specialists_needed.add("Security Specialist")
                    
                    # Map metric types to specialists
                    metric_category = value.get("metric_category", "")
                    if "performance" in metric_category:
                        specialists_needed.add("Performance Analyst")
                    elif "satisfaction" in metric_category:
                        specialists_needed.add("Customer Experience (CX) Strategist")
                    
                    # Map stakeholder types to specialists
                    stakeholder_category = value.get("stakeholder_category", "")
                    if "medical" in stakeholder_category:
                        specialists_needed.add("Medical Specialist")
                    elif "technical" in stakeholder_category:
                        specialists_needed.add("Technical Architect")
        
        # Add domain-specific specialists
        primary_domain = domain_analysis["primary_domain"]
        if primary_domain in self.specialist_mapping:
            specialists_needed.update(self.specialist_mapping[primary_domain][:3])
        
        # Always include general specialists for synthesis
        specialists_needed.add("Strategic Synthesizer")
        specialists_needed.add("Implementation Coordinator")
        
        return list(specialists_needed)[:8]  # Limit to 8 specialists
    
    def _build_agent_context_summary(self, extractions: List[Dict], 
                                   query: str, domain_analysis: Dict) -> str:
        """Build context summary for agent briefing.
        
        Args:
            extractions: Extraction results
            query: Original query
            domain_analysis: Domain analysis results
            
        Returns:
            Context summary string
        """
        summary_parts = [
            f"CONTEXT ANALYSIS FOR: {query}",
            f"Domain: {domain_analysis['primary_domain']}",
            f"Complexity: {domain_analysis['complexity_level']}",
            "",
            "KEY EXTRACTED INSIGHTS:"
        ]
        
        # Organize extractions by type
        extraction_by_type = defaultdict(list)
        for extraction in extractions:
            for key, value in extraction.items():
                if not key.endswith("_attributes") and isinstance(value, str):
                    extraction_by_type[key].append(value)
        
        # Add organized insights
        for extraction_type, values in extraction_by_type.items():
            if values:
                summary_parts.append(f"\n{extraction_type.upper()}:")
                for value in values[:3]:  # Limit to top 3 per type
                    summary_parts.append(f"- {value}")
        
        return "\n".join(summary_parts)
    
    def _get_fallback_analysis(self, query: str) -> Dict[str, Any]:
        """Provide fallback analysis when extraction fails.
        
        Args:
            query: Original query
            
        Returns:
            Basic analysis results
        """
        return {
            "specialties_needed": [
                "Strategic Analyst", "Process Expert", "Implementation Specialist"
            ],
            "context_summary": f"Basic analysis for: {query}",
            "domain_focus": "general",
            "complexity_level": "medium", 
            "key_concepts": ["analysis", "strategy", "implementation"],
            "extraction_metadata": {
                "extraction_method": "fallback_basic"
            }
        }

# =============================================================================
# Testing and Integration
# =============================================================================

def test_enhanced_rao_context_manager(cqb_model_manager):
    """Test the enhanced RAO context manager.
    
    Args:
        cqb_model_manager: Initialized CQB model manager
        
    Returns:
        bool: True if test passes
    """
    print("🧪 Testing Enhanced RAO Context Manager...")
    
    try:
        # Initialize manager
        context_manager = EnhancedRAOContextManager(
            cqb_model_manager=cqb_model_manager,
            max_context_length=2000
        )
        
        # Test context
        test_context = """
        Customer Service Operations Analysis
        
        Our department handles 5,000+ customer interactions monthly with 25 representatives.
        Current satisfaction rating is 3.2/5.0 with 48-hour average response times.
        Budget is $2.1M annually. Implementation window is 6 months.
        Must comply with data privacy regulations.
        Target: Improve satisfaction to 4.0+ while reducing costs by 20%.
        """
        
        # Test query
        test_query = "How can we improve our customer service operations?"
        
        # Run enhanced analysis
        analysis = context_manager.analyze_context_for_agent_generation(
            test_context, test_query
        )
        
        print(f"✅ Analysis Results:")
        print(f"   Domain: {analysis['domain_focus']}")
        print(f"   Complexity: {analysis['complexity_level']}")
        print(f"   Specialists: {len(analysis['specialties_needed'])}")
        print(f"   Method: {analysis.get('extraction_metadata', {}).get('extraction_method', 'unknown')}")
        
        # Validate results
        assert analysis['specialties_needed'], "Should have specialist requirements"
        assert analysis['context_summary'], "Should have context summary"
        assert analysis['domain_focus'], "Should have domain focus"
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced context manager test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧠 Enhanced RAO Context Manager")
    print("=" * 50)
    print("Extraction-Augmented Orchestration using LangExtract")
    print("- Sophisticated document analysis")
    print("- Structured entity extraction") 
    print("- Precise specialist selection")
    print("- Domain-agnostic operation")
