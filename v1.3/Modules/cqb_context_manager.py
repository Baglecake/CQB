
# =============================================================================
# CQB Context Manager - RAO Implementation
# =============================================================================

import os
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

# =============================================================================
# RAO Context Management
# =============================================================================

@dataclass
class DocumentChunk:
    """Single chunk of document content"""
    content: str
    section_type: str
    relevance_score: float
    keywords_found: List[str]
    chunk_id: str
    is_high_value: bool = False

class RAOFilterType(Enum):
    """Types of context filtering for document analysis"""
    HIGH_RELEVANCE = "high_relevance"
    DOMAIN_SPECIFIC = "domain_specific"
    CONCEPTUAL_DENSITY = "conceptual_density"
    EXPERTISE_INDICATORS = "expertise_indicators"

class CQBContextManager:
    """RAO-specific context manager for document analysis and agent generation"""

    def __init__(self, max_context_length: int = 2000):
        self.max_context_length = max_context_length
        self.context_file_cache = {}
        
    def load_context_file(self, filename: str) -> Optional[str]:
        """Load context file content"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
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
        """Analyze context content to inform agent generation"""
        
        if not context_content:
            return {"specialties_needed": [], "context_summary": "", "domain_focus": "general"}
        
        print("🔍 Analyzing context for agent generation...")
        
        # 1. Chunk the document
        chunks = self._chunk_document(context_content)
        
        # 2. Analyze chunks for domain and expertise indicators
        domain_analysis = self._analyze_domain_indicators(chunks)
        
        # 3. Extract specialty requirements
        specialties_needed = self._extract_specialty_requirements(chunks, query)
        
        # 4. Build context summary for agent generation
        context_summary = self._build_agent_generation_context(chunks, query)
        
        return {
            "specialties_needed": specialties_needed,
            "context_summary": context_summary,
            "domain_focus": domain_analysis["primary_domain"],
            "complexity_level": domain_analysis["complexity_level"],
            "key_concepts": domain_analysis["key_concepts"]
        }
    
    def _chunk_document(self, content: str) -> List[DocumentChunk]:
        """Break document into analyzable chunks"""
        
        # Simple paragraph-based chunking
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        chunks = []
        for i, paragraph in enumerate(paragraphs):
            if len(paragraph) < 50:  # Skip very short paragraphs
                continue
                
            chunk = DocumentChunk(
                content=paragraph,
                section_type=self._identify_section_type(paragraph),
                relevance_score=self._calculate_relevance_score(paragraph),
                keywords_found=self._extract_keywords(paragraph),
                chunk_id=f"chunk_{i}",
                is_high_value=self._assess_chunk_value(paragraph)
            )
            chunks.append(chunk)
            
        return chunks[:20]  # Limit to prevent overwhelm
    
    def _identify_section_type(self, text: str) -> str:
        """Identify what type of section this chunk represents"""
        text_lower = text.lower()
        
        if any(indicator in text_lower for indicator in ['overview', 'introduction', 'summary']):
            return "overview"
        elif any(indicator in text_lower for indicator in ['method', 'approach', 'implementation']):
            return "methodology"
        elif any(indicator in text_lower for indicator in ['result', 'finding', 'outcome']):
            return "results"
        elif any(indicator in text_lower for indicator in ['conclusion', 'recommendation', 'suggest']):
            return "conclusions"
        elif any(indicator in text_lower for indicator in ['problem', 'challenge', 'issue']):
            return "problem_definition"
        else:
            return "content"
    
    def _calculate_relevance_score(self, text: str) -> float:
        """Calculate relevance score for a chunk"""
        text_lower = text.lower()
        
        # High-value indicators
        expertise_indicators = [
            'expert', 'specialist', 'analysis', 'evaluate', 'assess',
            'recommend', 'strategy', 'approach', 'methodology', 'framework'
        ]
        
        # Domain indicators  
        domain_indicators = [
            'medical', 'clinical', 'business', 'technical', 'legal',
            'scientific', 'research', 'academic', 'professional'
        ]
        
        # Complexity indicators
        complexity_indicators = [
            'complex', 'sophisticated', 'advanced', 'comprehensive',
            'multifaceted', 'interdisciplinary', 'systematic'
        ]
        
        score = 0.0
        score += len([i for i in expertise_indicators if i in text_lower]) * 0.3
        score += len([i for i in domain_indicators if i in text_lower]) * 0.2
        score += len([i for i in complexity_indicators if i in text_lower]) * 0.1
        
        # Length bonus for substantial content
        if 200 <= len(text) <= 800:
            score += 0.2
            
        return min(score, 1.0)  # Cap at 1.0
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text chunk"""
        text_lower = text.lower()
        
        # Domain-specific keyword sets
        keyword_sets = {
            'medical': ['diagnosis', 'treatment', 'patient', 'clinical', 'medical', 'healthcare'],
            'business': ['strategy', 'market', 'revenue', 'customer', 'business', 'operational'],
            'technical': ['system', 'architecture', 'implementation', 'technology', 'software'],
            'research': ['study', 'analysis', 'methodology', 'findings', 'research', 'academic'],
            'legal': ['compliance', 'regulation', 'legal', 'policy', 'governance', 'ethics']
        }
        
        found_keywords = []
        for domain, keywords in keyword_sets.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_keywords.append(f"{domain}:{keyword}")
                    
        return found_keywords[:10]  # Limit keywords
    
    def _assess_chunk_value(self, text: str) -> bool:
        """Assess if chunk is high-value for agent generation"""
        text_lower = text.lower()
        
        high_value_indicators = [
            'expertise', 'specialist', 'professional', 'expert',
            'recommend', 'strategy', 'approach', 'methodology',
            'critical', 'important', 'key', 'essential',
            'complex', 'challenging', 'sophisticated'
        ]
        
        indicator_count = sum(1 for indicator in high_value_indicators if indicator in text_lower)
        return indicator_count >= 3 or len(text) > 300
    
    def _analyze_domain_indicators(self, chunks: List[DocumentChunk]) -> Dict[str, Any]:
        """Analyze chunks to determine primary domain and complexity"""
        
        domain_scores = {}
        complexity_indicators = 0
        all_keywords = []
        
        for chunk in chunks:
            # Count domain keywords
            for keyword in chunk.keywords_found:
                domain = keyword.split(':')[0]
                domain_scores[domain] = domain_scores.get(domain, 0) + 1
                all_keywords.append(keyword.split(':')[1])
            
            # Count complexity indicators
            if 'complex' in chunk.content.lower() or chunk.is_high_value:
                complexity_indicators += 1
        
        # Determine primary domain
        primary_domain = max(domain_scores.items(), key=lambda x: x[1])[0] if domain_scores else "general"
        
        # Determine complexity level
        complexity_level = "high" if complexity_indicators > len(chunks) * 0.3 else "medium"
        
        return {
            "primary_domain": primary_domain,
            "complexity_level": complexity_level,
            "key_concepts": list(set(all_keywords))[:15]
        }
    
    def _extract_specialty_requirements(self, chunks: List[DocumentChunk], 
                                      query: str) -> List[str]:
        """Extract what types of specialists are needed based on context"""
        
        domain_specialty_map = {
            'medical': [
                'Medical Specialist', 'Clinical Researcher', 'Healthcare Analyst',
                'Diagnostic Expert', 'Treatment Coordinator'
            ],
            'business': [
                'Business Strategist', 'Market Analyst', 'Operations Expert',
                'Financial Advisor', 'Management Consultant'
            ],
            'technical': [
                'Technical Architect', 'Systems Analyst', 'Software Expert',
                'Implementation Specialist', 'Technology Consultant'
            ],
            'research': [
                'Research Analyst', 'Data Scientist', 'Academic Researcher',
                'Methodology Expert', 'Statistical Analyst'
            ],
            'legal': [
                'Legal Advisor', 'Compliance Expert', 'Policy Analyst',
                'Regulatory Specialist', 'Ethics Consultant'
            ]
        }
        
        # Analyze domain distribution
        domain_counts = {}
        for chunk in chunks:
            for keyword in chunk.keywords_found:
                domain = keyword.split(':')[0]
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        # Select specialists based on dominant domains
        needed_specialists = []
        
        # Add specialists from top domains
        sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)
        for domain, count in sorted_domains[:3]:  # Top 3 domains
            specialists = domain_specialty_map.get(domain, ['General Analyst'])
            needed_specialists.extend(specialists[:2])  # Take 2 per domain
        
        # Always add a synthesizer and coordinator
        needed_specialists.extend(['Strategic Synthesizer', 'Project Coordinator'])
        
        return needed_specialists[:8]  # Limit to reasonable number
    
    def _build_agent_generation_context(self, chunks: List[DocumentChunk], 
                                      query: str) -> str:
        """Build context summary for agent generation"""
        
        # Get highest value chunks
        high_value_chunks = [c for c in chunks if c.is_high_value][:5]
        
        context_parts = [
            f"CONTEXT ANALYSIS FOR: {query}\n",
            "KEY DOCUMENT INSIGHTS:"
        ]
        
        for chunk in high_value_chunks:
            # Truncate chunk content
            content = chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content
            context_parts.append(f"\n{chunk.section_type.upper()}: {content}")
        
        return "\n".join(context_parts)

# =============================================================================
# Testing Function
# =============================================================================

def test_rao_context_manager():
    """Test the RAO context manager"""
    
    # Create test context content
    test_context = """
    Medical Case Analysis Framework
    
    This document outlines a comprehensive approach to medical diagnosis using AI specialists.
    The methodology involves multiple expert perspectives to ensure accurate diagnosis.
    
    Key Components:
    - Specialist expertise in cardiology, pulmonology, and emergency medicine
    - Systematic evaluation of symptoms and test results
    - Collaborative decision-making process
    
    Implementation Strategy:
    The approach requires careful coordination between different medical specialists.
    Each expert contributes their unique perspective based on their specialty knowledge.
    
    Critical Considerations:
    Patient safety must be the top priority in all diagnostic decisions.
    Complex cases may require additional subspecialist consultation.
    """
    
    # Test the context manager
    context_manager = CQBContextManager()
    
    analysis = context_manager.analyze_context_for_agent_generation(
        test_context, 
        "Analyze chest pain in 45-year-old patient"
    )
    
    print("🧪 Testing RAO Context Manager")
    print("=" * 50)
    print(f"Domain Focus: {analysis['domain_focus']}")
    print(f"Complexity: {analysis['complexity_level']}")
    print(f"Specialists Needed: {analysis['specialties_needed']}")
    print(f"Key Concepts: {analysis['key_concepts']}")
    print("\nContext Summary:")
    print(analysis['context_summary'])
    
    return analysis

if __name__ == "__main__":
    test_rao_context_manager()
