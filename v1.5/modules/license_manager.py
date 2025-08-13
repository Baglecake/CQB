# =============================================================================
# License Manager - Model License Tracking for CQB
# =============================================================================

import yaml
import os
import hashlib
from typing import Dict, Optional, Any
from datetime import datetime

class LicenseManager:
    """Manages model licenses and compliance tracking"""
    
    def __init__(self, registry_path: str = 'licenses.yaml'):
        self.registry_path = registry_path
        self.license_registry = {}
        self.load_registry()
    
    def load_registry(self):
        """Load the license registry from YAML file"""
        try:
            with open(self.registry_path, 'r') as file:
                self.license_registry = yaml.safe_load(file) or {}
            print(f"✅ Loaded license registry with {len(self.license_registry)} models")
        except FileNotFoundError:
            print(f"⚠️ License registry not found at {self.registry_path}")
            print("📝 Creating empty registry - please add your models!")
            self.license_registry = {}
            self._create_empty_registry()
        except Exception as e:
            print(f"❌ Error loading license registry: {e}")
            self.license_registry = {}
    
    def _create_empty_registry(self):
        """Create an empty registry file as template"""
        template = """# CQB Model License Registry
# Add any model you use to this registry with its license info

# Example:
# "organization/model-name":
#   license: "Apache-2.0"
#   repo: "https://huggingface.co/organization/model-name"
#   description: "Human readable description"
#   license_file: "filename.txt"  # Optional
"""
        try:
            with open(self.registry_path, 'w') as file:
                file.write(template)
            print(f"📝 Created template registry at {self.registry_path}")
        except Exception as e:
            print(f"❌ Could not create registry template: {e}")
    
    def get_model_license_info(self, model_path: str) -> Dict[str, Any]:
        """Get license information for a model"""
        
        # Check if model is in registry
        if model_path in self.license_registry:
            license_info = self.license_registry[model_path].copy()
            
            # Add computed fields
            license_info['model_path'] = model_path
            license_info['registry_status'] = 'registered'
            license_info['compliance_check'] = datetime.now().isoformat()
            
            return license_info
        else:
            # Model not in registry - return warning info
            return {
                'model_path': model_path,
                'license': 'UNKNOWN - NOT IN REGISTRY',
                'repo': 'Unknown',
                'description': 'Model not found in license registry',
                'registry_status': 'unregistered',
                'compliance_check': datetime.now().isoformat(),
                'warning': 'This model is not in the license registry. Please add it to ensure compliance.'
            }
    
    def validate_model_compliance(self, model_path: str) -> bool:
        """Check if a model is properly licensed"""
        if model_path not in self.license_registry:
            print(f"⚠️ Model '{model_path}' not found in license registry!")
            print(f"🔧 Please add it to {self.registry_path} before use")
            return False
        
        license_info = self.license_registry[model_path]
        if not license_info.get('license') or license_info['license'] == 'UNKNOWN':
            print(f"⚠️ Model '{model_path}' has unknown license!")
            return False
        
        print(f"✅ Model '{model_path}' license: {license_info['license']}")
        return True
    
    def get_all_used_models_manifest(self, model_configs: Dict) -> Dict[str, Any]:
        """Generate manifest of all models used in a session"""
        manifest = {
            'models_used': {},
            'license_compliance': True,
            'registry_version': self._get_registry_hash(),
            'generated_at': datetime.now().isoformat()
        }
        
        for model_id, config in model_configs.items():
            model_path = config.model_path if hasattr(config, 'model_path') else str(config)
            license_info = self.get_model_license_info(model_path)
            
            manifest['models_used'][model_id] = license_info
            
            # Check compliance
            if license_info.get('registry_status') != 'registered':
                manifest['license_compliance'] = False
        
        return manifest
    
    def _get_registry_hash(self) -> str:
        """Get hash of registry file for version tracking"""
        try:
            with open(self.registry_path, 'rb') as file:
                content = file.read()
                return hashlib.md5(content).hexdigest()[:8]
        except:
            return "unknown"
    
    def print_startup_banner(self, model_configs: Dict):
        """Print license compliance banner at startup"""
        print("\n" + "="*60)
        print("📋 CQB LICENSE COMPLIANCE CHECK")
        print("="*60)
        
        all_compliant = True
        
        for model_id, config in model_configs.items():
            model_path = config.model_path if hasattr(config, 'model_path') else str(config)
            license_info = self.get_model_license_info(model_path)
            
            status = "✅" if license_info.get('registry_status') == 'registered' else "⚠️"
            print(f"{status} {model_id}: {license_info.get('license', 'UNKNOWN')}")
            
            if license_info.get('registry_status') != 'registered':
                all_compliant = False
        
        if all_compliant:
            print("✅ All models properly licensed")
        else:
            print("⚠️ Some models need license registry entries")
            print(f"🔧 Update {self.registry_path} to ensure compliance")
        
        print("📄 See third_party_licenses/ for full license texts")
        print("="*60 + "\n")

# =============================================================================
# Global License Manager Instance
# =============================================================================

# Create a global instance that can be imported
license_manager = LicenseManager()

def get_license_info(model_path: str) -> Dict[str, Any]:
    """Convenience function to get license info"""
    return license_manager.get_model_license_info(model_path)

def validate_model(model_path: str) -> bool:
    """Convenience function to validate model compliance"""
    return license_manager.validate_model_compliance(model_path)

def get_models_manifest(model_configs: Dict) -> Dict[str, Any]:
    """Convenience function to get models manifest"""
    return license_manager.get_all_used_models_manifest(model_configs)

# =============================================================================
# Usage Example
# =============================================================================

if __name__ == "__main__":
    # Test the license manager
    print("🧪 Testing License Manager")
    print("=" * 40)
    
    # Test with some example models
    test_models = [
        "Qwen/Qwen3-8B",
        "hugging-quants/gemma-2-9b-it-AWQ-INT4", 
        "some/unknown-model"
    ]
    
    for model in test_models:
        print(f"\nTesting: {model}")
        info = get_license_info(model)
        print(f"  License: {info.get('license')}")
        print(f"  Status: {info.get('registry_status')}")
        
        is_valid = validate_model(model)
        print(f"  Valid: {is_valid}")
