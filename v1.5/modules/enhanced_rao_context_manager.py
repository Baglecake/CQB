
# =============================================================================
# Enhanced RAO Context Manager - WITH ROBUST SANITIZER INTEGRATION
# =============================================================================

import os
import json
import time
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict

# LangExtract imports (adapted from provided files) 
from cqb.langextract.data import FormatType, Document, AnnotatedDocument
from cqb.langextract.prompting import QAPromptGenerator
from cqb.langextract.schema import GeminiSchema
from cqb.langextract import resolver

# Local imports
from vllm_langextract_adapter import VLLMLanguageModel
from universal_extraction_schemas import UniversalExtractionSchemas

# =============================================================================
# ROBUST JSON SANITIZATION PIPELINE
# =============================================================================

def robust_json_sanitizer(text: str) -> Optional[str]:
    """
    Robust JSON sanitization pipeline for LLM-generated content.
    
    Handles model contamination issues while maintaining generalizability.
    """
    if not text:
        return None
    
    print(f"🔧 Starting sanitization of {len(text)} chars")
    
    # Step 1: Extract fenced content or use full text
    json_content = extract_fenced_content_robust(text)
    print(f"   📄 Extracted content: {len(json_content)} chars")
    
    # Step 2: Structural repairs (order matters!)
    json_content = fix_broken_structure(json_content)
    print(f"   🏗️  Structure fixed: {len(json_content)} chars")
    
    # Step 3: Content sanitization
    json_content = sanitize_content(json_content)
    print(f"   🧼 Content sanitized: {len(json_content)} chars")
    
    # Step 4: Final JSON validation and repair
    json_content = final_json_repair(json_content)
    print(f"   ✅ Final repair: {len(json_content)} chars")
    
    return json_content

def extract_fenced_content_robust(text: str) -> str:
    """Extract JSON from fenced blocks with multiple fallback patterns."""
    
    # Pattern 1: Standard fenced blocks
    patterns = [
        r'```json\s*\n(.*?)\n```',
        r'```\s*\n(.*?)\n```',
        r'```json(.*?)```',
        r'```(.*?)```'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            content = match.group(1).strip()
            if content and ('{' in content or '[' in content):
                return content
    
    # Fallback: Extract everything between first { and last }
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
    
    return text

def fix_broken_structure(text: str) -> str:
    """Fix structural JSON issues before content sanitization."""
    
    print("   🔍 Detecting structural issues...")
    
    # Fix 1: Broken attribute keys (most common issue)
    text = re.sub(r'"(\w+)_<[^>]*>\s*\n', r'"\1_attributes": {\n', text)
    
    # Fix 2: Missing quotes around keys
    text = re.sub(r'\n\s*(\w+):', r'\n      "\1":', text)
    
    # Fix 3: Missing commas between objects
    text = re.sub(r'}\s*\n\s*{', '},\n    {', text)
    
    # Fix 4: Missing opening quotes on "attributes" key - NEW!
    text = re.sub(r'\s+attributes":', r'        "attributes":', text)
    
    # Fix 5: Orphaned lines that should be inside objects
    lines = text.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if this looks like a broken attribute object
        if ('"' in line and ':' not in line and 
            i > 0 and '"_attributes"' in fixed_lines[-1]):
            # This line should be part of the attributes object
            fixed_lines[-1] = fixed_lines[-1].rstrip() + ' {'
            fixed_lines.append(f'        {line.strip()},')
            
            # Add following lines until we complete the object
            j = i + 1
            while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith('"'):
                next_line = lines[j].strip()
                if ':' in next_line:
                    fixed_lines.append(f'        {next_line.rstrip(",")},')
                j += 1
            
            # Close the attributes object
            if fixed_lines[-1].endswith(','):
                fixed_lines[-1] = fixed_lines[-1].rstrip(',')
            fixed_lines.append('      }')
            
            i = j - 1
        else:
            fixed_lines.append(lines[i])
        
        i += 1
    
    text = '\n'.join(fixed_lines)
    
    return text

def sanitize_content(text: str) -> str:
    """Sanitize JSON content while preserving structure."""
    
    print("   🧹 Sanitizing content...")
    
    # Remove HTML tags entirely
    text = re.sub(r'<[^>]+>', '', text)
    
    # Fix unescaped quotes in values (generalized approach)
    # Find patterns like: "key": "value with "quotes" inside"
    def fix_quotes_in_values(match):
        key = match.group(1)
        value = match.group(2)
        # Escape internal quotes in the value
        fixed_value = value.replace('"', '\\"')
        return f'"{key}": "{fixed_value}"'
    
    # Apply quote fixing to string values
    text = re.sub(r'"([^"]+)":\s*"([^"]*"[^"]*)"(?=\s*[,}])', fix_quotes_in_values, text)
    
    # Remove control characters that break JSON
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', text)
    
    # Fix specific known problematic patterns
    text = text.replace('Data "quality"', 'Data quality')
    text = text.replace('"quality":', 'quality:')
    
    return text

def final_json_repair(text: str) -> str:
    """Final pass JSON repair with validation."""
    
    print("   🔧 Final JSON repair...")
    
    # Remove trailing commas
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    
    # Ensure proper spacing
    text = re.sub(r'\s*:\s*', ': ', text)
    text = re.sub(r'\s*,\s*(?=\s*["\d\{])', ', ', text)
    
    # Fix any remaining structure issues
    # Ensure all objects are properly closed
    open_braces = text.count('{')
    close_braces = text.count('}')
    
    if open_braces > close_braces:
        # Add missing closing braces
        text = text.rstrip() + '\n' + '  }' * (open_braces - close_braces)
    
    return text

# =============================================================================
# Enhanced RAO Context Manager with Robust Parsing
# =============================================================================

class EnhancedRAOContextManager:
    """Enhanced RAO context manager using LangExtract for sophisticated document analysis.
    
    NOW WITH ROBUST JSON SANITIZATION PIPELINE!
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
        
        print("✅ Enhanced RAO Context Manager initialized with LangExtract + Robust Sanitizer")
    
    def _initialize_extraction_engine(self):
        """Initialize the LangExtract extraction engine."""
        try:
            # Create vLLM adapter
            self.vllm_language_model = VLLMLanguageModel(
                cqb_model_manager=self.model_manager,
                model_id="conservative_model",
                temperature=0.3
            )
            
            # Get universal extraction template
            self.extraction_template = UniversalExtractionSchemas.create_extraction_template()
            
            # Create prompt generator
            self.prompt_generator = QAPromptGenerator(
                template=self.extraction_template,
                format_type=FormatType.JSON,
                fence_output=True
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
                    "extraction_categories": list(set(e.get('extraction_class', 'unknown') for e in extraction_results)),
                    "extraction_method": "langextract_enhanced_with_robust_sanitizer"
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
            
            # Run extraction with higher token limit
            response = self.vllm_language_model.generate_single(
                extraction_prompt,
                temperature=0.3,
                max_output_tokens=4096
            )
            
            # Parse the structured response using ROBUST SANITIZATION
            extraction_results = self._parse_extraction_response(response)
            
            print(f"✅ Extracted {len(extraction_results)} structured entities")
            return extraction_results
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return []
    
    def _parse_extraction_response(self, response: str) -> List[Any]:
        """
        Parse LangExtract response using ROBUST SANITIZATION PIPELINE.
        
        This replaces the old fragile parsing logic with comprehensive sanitization.
        """
        print("🧠 Using robust sanitization pipeline...")
        
        # Use robust sanitization
        sanitized_json = robust_json_sanitizer(response)
        
        if not sanitized_json:
            print("❌ Robust sanitization failed")
            return []
        
        try:
            data = json.loads(sanitized_json)
            extractions = data.get("extractions", [])
            converted = self._convert_extractions(extractions)
            print(f"✅ Robust sanitization successful: {len(converted)} extractions")
            return converted
            
        except json.JSONDecodeError as e:
            print(f"❌ Even robust sanitization failed: {e}")
            # Show problematic area for debugging
            snippet = sanitized_json[max(0, e.pos - 50): e.pos + 50]
            print(f"   Context around error: ...{snippet}...")
            print(f"   Full sanitized content:\n{sanitized_json}")
            return []

    def _convert_extractions(self, extractions):
        """Helper method to convert extractions to expected format."""
        converted = []
        for item in extractions:
            if isinstance(item, dict):
                extraction_class = None
                extraction_text = None
                attributes = {}
                
                for key, value in item.items():
                    if not key.endswith("_attributes"):
                        extraction_class = key
                        extraction_text = value
                    else:
                        attributes = value if isinstance(value, dict) else {}
                
                if extraction_class and extraction_text:
                    converted.append({
                        'extraction_class': extraction_class,
                        'extraction_text': extraction_text,
                        'attributes': attributes
                    })
        return converted

    def _get_specialty_extraction_focus(self, agent_specialty: str) -> Dict[str, Any]:
        """Map agent specialties to relevant extraction types and concepts."""
        
        specialty_mappings = {
            "Venture Capitalist": {
                "priority_types": ["constraint", "stakeholder"],
                "key_concepts": ["funding", "investor", "runway", "burn_rate", "Series A", "valuation", "Kleiner Perkins"],
                "focus_areas": ["financial_constraints", "investor_relations", "funding_timeline"]
            },
            
            "Healthcare Market Analyst": {
                "priority_types": ["objective", "stakeholder"],
                "key_concepts": ["healthcare", "market", "pivot", "vertical", "competition", "medical"],
                "focus_areas": ["market_opportunity", "competitive_landscape", "pivot_strategy"]
            },
            
            "Strategic Partnerships Manager": {
                "priority_types": ["objective", "constraint"],
                "key_concepts": ["partnership", "Microsoft", "revenue", "integration", "collaboration", "licensing"],
                "focus_areas": ["partnership_opportunities", "integration_challenges", "revenue_impact"]
            },
            
            "Microsoft Partnership Specialist": {
                "priority_types": ["objective", "resource"],
                "key_concepts": ["Microsoft", "partnership", "Azure", "integration", "licensing", "technology"],
                "focus_areas": ["Microsoft_ecosystem", "technical_integration", "partnership_terms"]
            },
            
            "Budget Analyst": {
                "priority_types": ["constraint", "resource"],
                "key_concepts": ["budget", "cost", "burn_rate", "capital", "expenses", "runway", "funding"],
                "focus_areas": ["financial_constraints", "cost_optimization", "resource_allocation"]
            },
            
            "Project Manager": {
                "priority_types": ["constraint", "objective"],
                "key_concepts": ["timeline", "milestone", "development", "implementation", "deadline", "product"],
                "focus_areas": ["project_constraints", "timeline_management", "deliverable_tracking"]
            },
            
            "Implementation Coordinator": {
                "priority_types": ["constraint", "resource"],
                "key_concepts": ["implementation", "coordination", "timeline", "resources", "deployment"],
                "focus_areas": ["implementation_planning", "resource_coordination", "execution_timeline"]
            }
        }
        
        # Default mapping for unknown specialties
        default_mapping = {
            "priority_types": ["constraint", "objective"],
            "key_concepts": [],
            "focus_areas": ["general_context"]
        }
        
        # Handle partial matches (e.g., "Climate Scientist specializing in agricultural impacts")
        for specialty_key in specialty_mappings.keys():
            if specialty_key.lower() in agent_specialty.lower():
                return specialty_mappings[specialty_key]
        
        return specialty_mappings.get(agent_specialty, default_mapping)

    def _filter_extractions_for_specialty(self, extractions: List[Dict], 
                                        specialty_focus: Dict) -> List[Dict]:
        """Filter extractions based on specialty relevance."""
        relevant = []
        
        for extraction in extractions:
            extraction_text = extraction.get('extraction_text', '').lower()
            extraction_class = extraction.get('extraction_class', '')
            
            # Check if extraction contains specialty-relevant concepts
            concept_matches = sum(1 for concept in specialty_focus['key_concepts'] 
                                if concept.lower() in extraction_text)
            
            # Include if it matches concepts OR is a priority type
            if (concept_matches > 0 or 
                extraction_class in specialty_focus['priority_types']):
                relevant.append(extraction)
        
        return relevant

    def _calculate_concept_relevance(self, text: str, key_concepts: List[str]) -> float:
        """Calculate how relevant text is to specialist's key concepts."""
        if not key_concepts:
            return 0.5  # Default relevance
        
        text_lower = text.lower()
        matches = sum(1 for concept in key_concepts if concept.lower() in text_lower)
        
        return min(matches / len(key_concepts), 1.0) if key_concepts else 0.5


    def _analyze_extraction_results(self, extractions: List[Dict]) -> Dict[str, Any]:
        """Analyze extraction results to determine domain and complexity."""
        # Count extraction types and analyze patterns
        category_counts = defaultdict(int)
        domain_indicators = defaultdict(int)
        complexity_signals = 0
        key_concepts = []
        
        for extraction in extractions:
            # Handle both dictionary and object formats
            if isinstance(extraction, dict):
                extraction_class = extraction.get('extraction_class', '')
                extraction_text = extraction.get('extraction_text', '')
                attributes = extraction.get('attributes', {})
            else:
                extraction_class = getattr(extraction, 'extraction_class', '')
                extraction_text = getattr(extraction, 'extraction_text', '')
                attributes = getattr(extraction, 'attributes', {})
            
            if extraction_class:
                category_counts[extraction_class] += 1
                
                # Extract key concepts from extraction text
                if extraction_text and len(extraction_text) > 3:
                    key_concepts.append(extraction_text)
            
            # Analyze attributes for domain indicators
            if isinstance(attributes, dict):
                domain = attributes.get("domain", "")
                if domain:
                    domain_indicators[domain] += 1
                
                # Check for complexity indicators
                attr_text = str(attributes).lower()
                if any(indicator in attr_text for indicator in 
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
            elif category_counts.get("objective", 0) > 2:
                primary_domain = "research_academic"
            else:
                primary_domain = "general"
        
        # Determine complexity level
        complexity_level = "high" if complexity_signals > 2 else "medium"
        
        return {
            "primary_domain": primary_domain,
            "complexity_level": complexity_level,
            "key_concepts": key_concepts[:15],
            "category_distribution": dict(category_counts),
            "domain_indicators": dict(domain_indicators)
        }
    
    def _generate_specialist_requirements(self, extractions: List[Dict], 
                                    query: str, domain_analysis: Dict) -> List[str]:
        """Generate specialist requirements based on extractions."""
        specialists_needed = set()
        
        # Analyze extractions for specialist needs
        for extraction in extractions:
            if isinstance(extraction, dict):
                extraction_class = extraction.get('extraction_class', '')
                attributes = extraction.get('attributes', {})
            else:
                extraction_class = getattr(extraction, 'extraction_class', '')
                attributes = getattr(extraction, 'attributes', {})
            
            # Map extraction types to specialists
            if extraction_class == 'constraint':
                constraint_type = attributes.get("type", "")
                if constraint_type == "financial":
                    specialists_needed.add("Budget Analyst")
                elif constraint_type == "temporal" or constraint_type == "data_quality":
                    specialists_needed.add("Project Manager")
                elif "methodological" in constraint_type:
                    specialists_needed.add("Research Methodologist")
                    
            elif extraction_class == 'stakeholder':
                stakeholder_category = attributes.get("stakeholder_category", "")
                if "research" in stakeholder_category:
                    specialists_needed.add("Research Coordinator")
                    
            elif extraction_class == 'objective':
                obj_category = attributes.get("objective_category", "")
                if "policy" in obj_category:
                    specialists_needed.add("Policy Analyst")
                elif "economic" in obj_category:
                    specialists_needed.add("Economic Impact Analyst")
        
        # Add domain-specific specialists
        primary_domain = domain_analysis["primary_domain"]
        if primary_domain in self.specialist_mapping:
            specialists_needed.update(self.specialist_mapping[primary_domain][:3])
        
        # Always include synthesis specialists
        specialists_needed.add("Strategic Synthesizer")
        specialists_needed.add("Implementation Coordinator")
        
        return list(specialists_needed)[:8]
    
    def _build_agent_context_summary(self, extractions: List[Dict], 
                               query: str, domain_analysis: Dict, 
                               agent_specialty: str = None) -> str:
        """Build context summary tailored to specific agent specialty."""
        
        if not agent_specialty:
            # Fallback to original behavior if no specialty provided
            return self._build_generic_context_summary(extractions, query, domain_analysis)
        
        # Get specialty-specific focus areas
        specialty_focus = self._get_specialty_extraction_focus(agent_specialty)
        
        # Filter extractions by relevance to this specialty
        relevant_extractions = self._filter_extractions_for_specialty(
            extractions, specialty_focus
        )
        
        # Build specialty-focused summary
        summary_parts = [
            f"SPECIALIZED CONTEXT FOR: {agent_specialty}",
            f"Query Analysis: {query}",
            f"Domain: {domain_analysis['primary_domain']}",
            f"Your Expertise Focus: {', '.join(specialty_focus['focus_areas'])}",
            "",
            "PRIORITY INSIGHTS FOR YOUR SPECIALTY:"
        ]
        
        # Group relevant extractions by type with relevance scoring
        specialty_extractions = defaultdict(list)
        for extraction in relevant_extractions:
            extraction_class = extraction.get('extraction_class', 'unknown')
            extraction_text = extraction.get('extraction_text', '')
            
            # Score relevance based on key concepts
            relevance_score = self._calculate_concept_relevance(
                extraction_text, specialty_focus['key_concepts']
            )
            
            if relevance_score > 0.2:  # Lower threshold for inclusion
                specialty_extractions[extraction_class].append({
                    'text': extraction_text,
                    'relevance': relevance_score
                })
        
        # Add high-priority extractions first
        for extraction_type in specialty_focus['priority_types']:
            if extraction_type in specialty_extractions:
                items = sorted(specialty_extractions[extraction_type], 
                            key=lambda x: x['relevance'], reverse=True)
                
                summary_parts.append(f"\n{extraction_type.upper()} (High Priority):")
                for item in items[:3]:  # Top 3 most relevant
                    summary_parts.append(f"- {item['text']}")
        
        # Add supporting context from other extraction types
        for extraction_type, items in specialty_extractions.items():
            if extraction_type not in specialty_focus['priority_types'] and items:
                items_sorted = sorted(items, key=lambda x: x['relevance'], reverse=True)
                summary_parts.append(f"\n{extraction_type.upper()} (Supporting Context):")
                for item in items_sorted[:2]:  # Top 2 supporting items
                    summary_parts.append(f"- {item['text']}")
        
        return "\n".join(summary_parts)

    def _build_generic_context_summary(self, extractions: List[Dict], 
                                    query: str, domain_analysis: Dict) -> str:
        """Build generic context summary (original v1.5 behavior)."""
        summary_parts = [
            f"CONTEXT ANALYSIS FOR: {query}",
            f"Domain: {domain_analysis['primary_domain']}",
            f"Complexity: {domain_analysis['complexity_level']}",
            "",
            "KEY EXTRACTED INSIGHTS:"
        ]
        
        # Organize extractions by type (original logic)
        extraction_by_type = defaultdict(list)
        for extraction in extractions:
            if isinstance(extraction, dict):
                extraction_class = extraction.get('extraction_class', 'unknown')
                extraction_text = extraction.get('extraction_text', '')
            else:
                extraction_class = getattr(extraction, 'extraction_class', 'unknown')
                extraction_text = getattr(extraction, 'extraction_text', '')
            
            if extraction_text and isinstance(extraction_text, str):
                extraction_by_type[extraction_class].append(extraction_text)
        
        # Add organized insights
        for extraction_type, values in extraction_by_type.items():
            if values:
                summary_parts.append(f"\n{extraction_type.upper()}:")
                for value in values[:3]:  # Limit to top 3 per type
                    summary_parts.append(f"- {value}")
        
        return "\n".join(summary_parts)
    
    def _get_fallback_analysis(self, query: str) -> Dict[str, Any]:
        """Provide fallback analysis when extraction fails."""
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
# Testing Integration
# =============================================================================

def test_enhanced_rao_context_manager_with_sanitizer(cqb_model_manager):
    """Test the enhanced RAO context manager with robust sanitizer.
    
    Args:
        cqb_model_manager: Initialized CQB model manager
        
    Returns:
        bool: True if test passes
    """
    print("🧪 Testing Enhanced RAO Context Manager with Robust Sanitizer...")
    
    try:
        # Initialize manager
        context_manager = EnhancedRAOContextManager(
            cqb_model_manager=cqb_model_manager,
            max_context_length=2000
        )
        
        # Test with your actual context file
        test_context = context_manager.load_context_file('cqb_framework_rao.txt')
        test_query = "What should be our strategic priorities for the final research phase?"
        
        # Run enhanced analysis with robust sanitizer
        analysis = context_manager.analyze_context_for_agent_generation(
            test_context, test_query
        )
        
        print(f"✅ Analysis Results with Robust Sanitizer:")
        print(f"   Domain: {analysis['domain_focus']}")
        print(f"   Complexity: {analysis['complexity_level']}")
        print(f"   Specialists: {len(analysis['specialties_needed'])}")
        print(f"   Method: {analysis.get('extraction_metadata', {}).get('extraction_method', 'unknown')}")
        print(f"   Extractions: {analysis.get('extraction_metadata', {}).get('total_extractions', 0)}")
        
        # Validate results
        assert analysis['specialties_needed'], "Should have specialist requirements"
        assert analysis['context_summary'], "Should have context summary"
        assert analysis['domain_focus'], "Should have domain focus"
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced context manager with sanitizer test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧠 Enhanced RAO Context Manager with Robust Sanitization")
    print("=" * 60)
    print("Extraction-Augmented Orchestration with comprehensive JSON repair")
    print("- Sophisticated document analysis")
    print("- Structured entity extraction") 
    print("- ROBUST sanitization pipeline")
    print("- Precise specialist selection")
