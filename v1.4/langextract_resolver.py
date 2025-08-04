# =============================================================================
# LangExtract Resolver - Content Extraction Utilities
# =============================================================================

import re
import json
import yaml
from typing import Optional, Dict, Any

# =============================================================================
# Content Extraction Functions
# =============================================================================

def extract_fenced_content(text: str, fence_type: str = "auto") -> Optional[str]:
    """Extract content from fenced code blocks (```json, ```yaml, etc.).
    
    Args:
        text: Text potentially containing fenced code blocks
        fence_type: Type of fence to look for ("json", "yaml", "auto")
        
    Returns:
        Extracted content or None if not found
    """
    if not text:
        return None
    
    # Patterns for different fence types
    if fence_type == "auto":
        # Try JSON first, then YAML
        patterns = [
            r'```(?:json)?\s*\n(.*?)\n```',
            r'```(?:yaml)?\s*\n(.*?)\n```',
            r'```\s*\n(.*?)\n```'  # Generic fence
        ]
    elif fence_type == "json":
        patterns = [r'```(?:json)?\s*\n(.*?)\n```']
    elif fence_type == "yaml":
        patterns = [r'```(?:yaml)?\s*\n(.*?)\n```']
    else:
        patterns = [r'```\s*\n(.*?)\n```']
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            content = match.group(1).strip()
            if content:
                return content
    
    return None

def clean_and_extract_json(text: str) -> Optional[Dict[Any, Any]]:
    """Clean text and attempt to extract valid JSON.
    
    Args:
        text: Text potentially containing JSON
        
    Returns:
        Parsed JSON dictionary or None
    """
    if not text:
        return None
    
    # First try to extract from fences
    fenced_content = extract_fenced_content(text, "json")
    if fenced_content:
        try:
            return json.loads(fenced_content)
        except json.JSONDecodeError:
            pass
    
    # Try to parse the entire text as JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON-like content in the text
    json_patterns = [
        r'\{.*\}',  # Simple braces
        r'\[.*\]'   # Array format
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
    
    return None

def clean_and_extract_yaml(text: str) -> Optional[Dict[Any, Any]]:
    """Clean text and attempt to extract valid YAML.
    
    Args:
        text: Text potentially containing YAML
        
    Returns:
        Parsed YAML dictionary or None
    """
    if not text:
        return None
    
    # First try to extract from fences
    fenced_content = extract_fenced_content(text, "yaml")
    if fenced_content:
        try:
            return yaml.safe_load(fenced_content)
        except yaml.YAMLError:
            pass
    
    # Try to parse the entire text as YAML
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError:
        pass
    
    return None

def extract_structured_content(text: str, format_preference: str = "json") -> Optional[Dict[Any, Any]]:
    """Extract structured content (JSON or YAML) with format preference.
    
    Args:
        text: Text containing structured data
        format_preference: Preferred format ("json" or "yaml")
        
    Returns:
        Parsed structured data or None
    """
    if format_preference == "json":
        # Try JSON first
        result = clean_and_extract_json(text)
        if result is not None:
            return result
        # Fallback to YAML
        return clean_and_extract_yaml(text)
    
    else:  # yaml preference
        # Try YAML first
        result = clean_and_extract_yaml(text)
        if result is not None:
            return result
        # Fallback to JSON
        return clean_and_extract_json(text)

# =============================================================================
# Response Validation Functions
# =============================================================================

def validate_extraction_response(response_data: Dict[Any, Any]) -> bool:
    """Validate that response data has expected extraction structure.
    
    Args:
        response_data: Parsed response data
        
    Returns:
        True if valid extraction format
    """
    if not isinstance(response_data, dict):
        return False
    
    # Check for extractions key
    if "extractions" not in response_data:
        return False
    
    extractions = response_data["extractions"]
    if not isinstance(extractions, list):
        return False
    
    # Validate extraction structure
    for extraction in extractions:
        if not isinstance(extraction, dict):
            return False
        
        # Should have at least one non-attributes field
        non_attr_fields = [k for k in extraction.keys() if not k.endswith("_attributes")]
        if not non_attr_fields:
            return False
    
    return True

def repair_common_json_issues(text: str) -> str:
    """Attempt to repair common JSON formatting issues.
    
    Args:
        text: Potentially malformed JSON text
        
    Returns:
        Repaired JSON text
    """
    # Remove common prefixes/suffixes
    text = text.strip()
    
    # Remove markdown formatting
    text = re.sub(r'^```(?:json)?\s*\n', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\n```\s*$', '', text)
    
    # Fix common trailing comma issues
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    
    # Fix missing quotes on keys (basic cases)
    text = re.sub(r'(\w+)(\s*:)', r'"\1"\2', text)
    
    return text

# =============================================================================
# Testing Functions
# =============================================================================

def test_resolver_functions():
    """Test the resolver functions with various inputs."""
    print("🧪 Testing LangExtract Resolver Functions...")
    
    # Test fenced content extraction
    test_text_json = '''
    Here's the analysis:
    
    ```json
    {
        "extractions": [
            {"constraint": "budget limit", "constraint_attributes": {"type": "financial"}}
        ]
    }
    ```
    
    That's the result.
    '''
    
    extracted = extract_fenced_content(test_text_json)
    print(f"✅ Fenced extraction: {len(extracted) if extracted else 0} chars")
    
    # Test JSON parsing
    parsed = clean_and_extract_json(test_text_json)
    print(f"✅ JSON parsing: {len(parsed) if parsed else 0} items")
    
    # Test validation
    if parsed:
        is_valid = validate_extraction_response(parsed)
        print(f"✅ Validation: {is_valid}")
    
    return True

if __name__ == "__main__":
    print("🔧 LangExtract Resolver Module")
    print("=" * 40)
    print("Utilities for extracting and parsing structured content")
    test_resolver_functions()
