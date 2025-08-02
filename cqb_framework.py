# =============================================================================
# CQB Core - Dynamic Agent Generation Brain
# =============================================================================

import os
import time
import uuid
import yaml
import torch
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from vllm import LLM, SamplingParams

# =============================================================================
# CQB Model Manager
# =============================================================================

@dataclass
class CQBModelConfig:
    """CQB model configuration"""
    name: str
    model_path: str
    temperature: float
    top_p: float
    max_tokens: int
    max_model_len: int
    memory_fraction: float
    dtype: str = 'auto'
    quantization: Optional[str] = None
    enforce_eager: bool = True
    max_num_seqs: int = 2

class CQBModelManager:
    """Manages models for CQB"""
    
    def __init__(self):
        self.models: Dict[str, LLM] = {}
        self.sampling_params: Dict[str, SamplingParams] = {}
        self.model_configs: Dict[str, CQBModelConfig] = {}
        
    def load_config(self, config_path: str = 'config.yaml'):
        """Load model configurations"""
        try:
            with open(config_path, 'r') as file:
                config_data = yaml.safe_load(file)
            
            import inspect
            valid_fields = set(inspect.signature(CQBModelConfig.__init__).parameters.keys()) - {'self'}
            
            for model_id, config in config_data.items():
                if model_id in ['conservative_model', 'innovative_model']:
                    filtered_config = {k: v for k, v in config.items() if k in valid_fields}
                    self.model_configs[model_id] = CQBModelConfig(**filtered_config)
            
            print(f"✅ Loaded {len(self.model_configs)} model configurations")
            
        except Exception as e:
            print(f"⚠️ Config loading error: {e}, using defaults")
            self._create_default_configs()
    
    def _create_default_configs(self):
        """Create default model configurations"""
        self.model_configs = {
            'conservative_model': CQBModelConfig(
                name='Conservative-CQB',
                model_path='NousResearch/Nous-Hermes-2-Mistral-7B-DPO',
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024,
                max_model_len=2048,
                memory_fraction=0.4,
                max_num_seqs=2
            ),
            'innovative_model': CQBModelConfig(
                name='Innovative-CQB',
                model_path='NousResearch/Nous-Hermes-2-Mistral-7B-DPO',
                temperature=0.8,
                top_p=0.95,
                max_tokens=1024,
                max_model_len=2048,
                memory_fraction=0.4,
                max_num_seqs=2
            )
        }
    
    def load_model(self, model_id: str) -> bool:
        """Load a specific model"""
        if model_id in self.models:
            return True
        
        config = self.model_configs.get(model_id)
        if not config:
            print(f"❌ No config for {model_id}")
            return False
        
        print(f"📥 Loading {config.name}...")
        
        try:
            llm_args = {
                "model": config.model_path,
                "tensor_parallel_size": 1,
                "gpu_memory_utilization": config.memory_fraction,
                "max_model_len": config.max_model_len,
                "trust_remote_code": True,
                "dtype": config.dtype,
                "enforce_eager": config.enforce_eager,
                "max_num_seqs": config.max_num_seqs
            }
            
            if config.quantization:
                llm_args["quantization"] = config.quantization
            
            model = LLM(**llm_args)
            
            sampling_params = SamplingParams(
                temperature=config.temperature,
                top_p=config.top_p,
                max_tokens=config.max_tokens,
                stop=["</s>", "<|im_end|>"]
            )
            
            self.models[model_id] = model
            self.sampling_params[model_id] = sampling_params
            
            print(f"✅ {config.name} loaded")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load {config.name}: {e}")
            return False
    
    def generate_text(self, model_id: str, prompt: str, temperature: float = None) -> str:
        """Generate text using specified model"""
        if model_id not in self.models:
            if not self.load_model(model_id):
                raise ValueError(f"Model {model_id} not available")
        
        model = self.models[model_id]
        sampling_params = self.sampling_params[model_id]
        
        # Override temperature if specified
        if temperature is not None:
            sampling_params = SamplingParams(
                temperature=temperature,
                top_p=sampling_params.top_p,
                max_tokens=sampling_params.max_tokens,
                stop=sampling_params.stop
            )
        
        outputs = model.generate([prompt], sampling_params)
        return outputs[0].outputs[0].text.strip()

# =============================================================================
# CQB Agent
# =============================================================================

@dataclass
class CQBAgentSpec:
    """Specification for a CQB agent"""
    agent_id: str
    agent_type: str
    specialty: str
    model_assignment: str
    temperature: float
    persona: str

class CQBAgent:
    """CQB Agent - persistent and reusable"""
    
    def __init__(self, spec: CQBAgentSpec, model_manager: CQBModelManager):
        self.spec = spec
        self.model_manager = model_manager
        self.conversation_history = []
        
    @property
    def agent_id(self) -> str:
        return self.spec.agent_id
    
    @property
    def agent_type(self) -> str:
        return self.spec.agent_type
    
    @property
    def specialty(self) -> str:
        return self.spec.specialty
    
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate response to prompt"""
        
        # Format prompt for this agent
        formatted_prompt = self._format_prompt(prompt, context)
        
        # Generate response
        response = self.model_manager.generate_text(
            self.spec.model_assignment,
            formatted_prompt,
            self.spec.temperature
        )
        
        # Track in history
        self.conversation_history.append({
            'prompt': prompt,
            'response': response,
            'timestamp': time.time(),
            'context_provided': context is not None
        })
        
        return response
    
    def _format_prompt(self, base_prompt: str, context: Dict[str, Any] = None) -> str:
        """Format prompt for this agent"""
        
        system_prompt = f"""You are {self.spec.agent_id}, {self.spec.persona}.

Specialty: {self.spec.specialty}
Agent Type: {self.spec.agent_type}

Provide expert analysis based on your specialty and perspective."""
        
        # Add context if provided
        if context and context.get('team_context'):
            system_prompt += f"\n\nTeam Context:\n{context['team_context']}"
        
        return f"""<|im_start|>system
{system_prompt}
<|im_end|>
<|im_start|>user
{base_prompt}
<|im_end|>
<|im_start|>assistant"""
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            'agent_id': self.spec.agent_id,
            'agent_type': self.spec.agent_type,
            'specialty': self.spec.specialty,
            'model_assignment': self.spec.model_assignment,
            'temperature': self.spec.temperature,
            'persona': self.spec.persona,
            'conversation_count': len(self.conversation_history)
        }

# =============================================================================
# Dynamic Agent Generation
# =============================================================================

class DynamicAgentGenerator:
    """Dynamically generates agents based on query analysis"""
    
    def __init__(self, model_manager: CQBModelManager):
        self.model_manager = model_manager
    
    def analyze_and_generate_agents(self, query: str, max_agents: int = 8) -> List[CQBAgent]:
        """Analyze query and generate appropriate agents"""
        
        print(f"🔍 Analyzing query to determine agent needs...")
        
        # Use model to analyze what agents are needed
        analysis_prompt = f"""Analyze this query and determine what types of expert agents would be most valuable for addressing it comprehensively.

Query: {query}

For this query, what specific types of expertise, perspectives, and specialists would be most helpful? Consider:
1. What fields of knowledge are relevant?
2. What different analytical approaches would be valuable?
3. What types of thinking (conservative/analytical vs innovative/creative) are needed?
4. What specific expert roles would contribute unique insights?

Provide a list of 6-8 specific expert types/specialties that would form an effective team for this query. Be specific about their expertise areas.

Format your response as a simple list of expert types, one per line."""
        
        # Use conservative model for analysis
        analysis = self.model_manager.generate_text('conservative_model', analysis_prompt, temperature=0.3)
        
        print(f"✅ Query analysis complete")
        
        # Extract agent specifications from analysis
        agent_specs = self._extract_agent_specs(analysis, max_agents)
        
        # Generate agents
        agents = []
        for spec in agent_specs:
            agent = CQBAgent(spec, self.model_manager)
            agents.append(agent)
        
        print(f"✅ Generated {len(agents)} agents:")
        for agent in agents:
            print(f"   - {agent.agent_id} ({agent.specialty})")
        
        return agents
    
    def _extract_agent_specs(self, analysis: str, max_agents: int) -> List[CQBAgentSpec]:
        """Extract agent specifications from analysis"""
        
        # Parse the analysis to extract expert types
        lines = analysis.strip().split('\n')
        expert_types = []
        
        for line in lines:
            line = line.strip()
            # Skip empty lines and headers
            if not line or line.lower().startswith(('here', 'for this', 'the following', 'based on')):
                continue
            
            # Remove numbering, bullets, etc.
            import re
            cleaned = re.sub(r'^\d+[\.\)\-\s]*', '', line)
            cleaned = re.sub(r'^[-•*]\s*', '', cleaned)
            cleaned = cleaned.strip()
            
            if len(cleaned) > 5 and ':' not in cleaned[:20]:  # Avoid explanatory text
                expert_types.append(cleaned)
        
        # Ensure we have enough expert types
        if len(expert_types) < max_agents:
            # Add some general experts if needed
            general_experts = [
                "Systems Analyst", "Strategic Thinker", "Risk Assessor", 
                "Innovation Specialist", "Quality Reviewer", "Process Expert"
            ]
            expert_types.extend(general_experts)
        
        # Take first max_agents experts
        selected_experts = expert_types[:max_agents]
        
        # Create agent specifications
        agent_specs = []
        conservative_count = max_agents // 2
        
        for i, expert_type in enumerate(selected_experts):
            is_conservative = i < conservative_count
            
            spec = CQBAgentSpec(
                agent_id=f"{'Conservative' if is_conservative else 'Innovative'}_{expert_type.replace(' ', '')}_{i+1}",
                agent_type="Conservative" if is_conservative else "Innovative",
                specialty=expert_type,
                model_assignment="conservative_model" if is_conservative else "innovative_model",
                temperature=0.1 + (i * 0.05) if is_conservative else 0.7 + (i * 0.05),
                persona=f"{'Analytical and systematic' if is_conservative else 'Creative and forward-thinking'} {expert_type}"
            )
            
            agent_specs.append(spec)
        
        return agent_specs

# =============================================================================
# Central Query Brain - Simple Agent Generation Service
# =============================================================================

class CentralQueryBrain:
    """Simple brain that generates agents for any query"""
    
    def __init__(self):
        self.model_manager = CQBModelManager()
        self.agent_generator = DynamicAgentGenerator(self.model_manager)
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
        print("🧠 CQB Dynamic Agent Generation Brain initialized")
    
    def initialize_models(self, config_path: str = 'config.yaml') -> bool:
        """Initialize model system"""
        print("🚀 Initializing CQB models...")
        
        self.model_manager.load_config(config_path)
        
        # Load both models
        success = True
        for model_id in ['conservative_model', 'innovative_model']:
            if not self.model_manager.load_model(model_id):
                success = False
        
        if success:
            print("✅ CQB models ready")
        else:
            print("❌ Model initialization failed")
        
        return success
    
    def analyze_query_and_generate_agents(self, query: str, max_agents: int = 8) -> str:
        """Analyze query and generate appropriate agents"""
        
        print(f"\n🧠 CQB Processing Query")
        print("=" * 40)
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Generate agents dynamically
        agents = self.agent_generator.analyze_and_generate_agents(query, max_agents)
        
        # Store session
        self.active_sessions[session_id] = {
            'query': query,
            'agents': {agent.agent_id: agent for agent in agents},
            'agent_list': agents,
            'created_at': time.time()
        }
        
        print(f"✅ Session {session_id[:8]}... created with {len(agents)} agents")
        
        return session_id
    
    def get_agents(self, session_id: str) -> List[CQBAgent]:
        """Get agents for a session"""
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        return session['agent_list']
    
    def get_agent(self, session_id: str, agent_id: str) -> CQBAgent:
        """Get specific agent from session"""
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        agent = session['agents'].get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found in session")
        
        return agent
    
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get session information"""
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        return {
            'session_id': session_id,
            'query': session['query'],
            'agent_count': len(session['agent_list']),
            'agents': [agent.get_agent_info() for agent in session['agent_list']],
            'created_at': session['created_at']
        }
    
    def list_active_sessions(self) -> List[str]:
        """List active session IDs"""
        return list(self.active_sessions.keys())
    
    def remove_session(self, session_id: str):
        """Remove session and clean up"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            print(f"🗑️ Session {session_id[:8]}... removed")

# =============================================================================
# Usage and Testing
# =============================================================================

def initialize_cqb(config_path: str = 'config.yaml') -> CentralQueryBrain:
    """Initialize CQB brain"""
    cqb = CentralQueryBrain()
    
    if not cqb.initialize_models(config_path):
        return None
    
    return cqb

def test_cqb_brain(cqb: CentralQueryBrain):
    """Test CQB brain with any query"""
    
    test_query = """
    How can we improve customer satisfaction while reducing operational costs
    in our customer service department?
    """
    
    # Generate agents for query
    session_id = cqb.analyze_query_and_generate_agents(test_query, max_agents=6)
    
    # Get session info
    info = cqb.get_session_info(session_id)
    
    print(f"\n📊 Test Results:")
    print(f"   Session: {session_id[:8]}...")
    print(f"   Agents: {info['agent_count']}")
    print(f"   Query: {info['query'][:50]}...")
    
    # Test agent usage
    agents = cqb.get_agents(session_id)
    test_response = agents[0].generate_response("What are the key factors to consider?")
    print(f"   Sample response: {len(test_response)} characters")
    
    return session_id

if __name__ == "__main__":
    print("🧠 CQB Dynamic Agent Generation Brain")
    print("=" * 50)
    print("Usage:")
    print("  cqb = initialize_cqb()")
    print("  session_id = cqb.analyze_query_and_generate_agents(query)")
    print("  agents = cqb.get_agents(session_id)")
    print("  # Use agents in your modules")
