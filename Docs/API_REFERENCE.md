# Central Query Brain - API Reference

Complete API documentation for the CQB system.

## Core Classes

### CentralQueryBrain

Main orchestrator class for the CQB system.

```python
class CentralQueryBrain:
    def __init__(self)
    def initialize_models(self, config_path: str = 'config.yaml') -> bool
    def analyze_query_and_generate_agents(self, query: str, max_agents: int = 8) -> str
    def get_agents(self, session_id: str) -> List[CQBAgent]
    def get_agent(self, session_id: str, agent_id: str) -> CQBAgent
    def get_session_info(self, session_id: str) -> Dict[str, Any]
    def list_active_sessions(self) -> List[str]
    def remove_session(self, session_id: str)
```

#### Methods

##### `initialize_models(config_path: str = 'config.yaml') -> bool`

Initialize the model system from configuration file.

**Parameters:**
- `config_path`: Path to YAML configuration file

**Returns:**
- `bool`: True if initialization successful

**Example:**
```python
cqb = CentralQueryBrain()
success = cqb.initialize_models('config.yaml')
if success:
    print("Models loaded successfully")
```

##### `analyze_query_and_generate_agents(query: str, max_agents: int = 8) -> str`

Analyze a query and generate appropriate expert agents.

**Parameters:**
- `query`: Input query/scenario text
- `max_agents`: Maximum number of agents to generate

**Returns:**
- `str`: Session ID for the generated agents

**Example:**
```python
session_id = cqb.analyze_query_and_generate_agents(
    "How can we improve team productivity?",
    max_agents=6
)
```

##### `get_agents(session_id: str) -> List[CQBAgent]`

Retrieve all agents for a session.

**Parameters:**
- `session_id`: Session identifier

**Returns:**
- `List[CQBAgent]`: List of agent objects

**Example:**
```python
agents = cqb.get_agents(session_id)
for agent in agents:
    print(f"{agent.agent_id}: {agent.specialty}")
```

---

### AgentCollaborationModule

Orchestrates multi-round collaboration between agents.

```python
class AgentCollaborationModule:
    def __init__(self, cqb_brain: CentralQueryBrain)
    def collaborate_on_query(self, query: str, max_agents: int = 6, collaboration_rounds: int = 3) -> str
    def get_collaboration_result(self, collab_session_id: str) -> Dict[str, Any]
    def get_collaboration_summary(self, collab_session_id: str) -> str
    def export_collaboration_json(self, collab_session_id: str) -> Dict[str, Any]
    def save_collaboration_json(self, collab_session_id: str, filename: str = None) -> str
```

#### Methods

##### `collaborate_on_query(query: str, max_agents: int = 6, collaboration_rounds: int = 3) -> str`

Run collaborative analysis on a query.

**Parameters:**
- `query`: Input query/scenario
- `max_agents`: Number of agents to generate
- `collaboration_rounds`: Number of collaboration rounds

**Returns:**
- `str`: Collaboration session ID

**Example:**
```python
collab_module = AgentCollaborationModule(cqb)
collab_session_id = collab_module.collaborate_on_query(
    "Develop a crisis management strategy",
    max_agents=8,
    collaboration_rounds=4
)
```

##### `export_collaboration_json(collab_session_id: str) -> Dict[str, Any]`

Export complete collaboration data as JSON.

**Parameters:**
- `collab_session_id`: Collaboration session identifier

**Returns:**
- `Dict[str, Any]`: Complete collaboration data

**Example:**
```python
json_data = collab_module.export_collaboration_json(collab_session_id)
print(f"Total responses: {json_data['metadata']['total_responses']}")
```

---

### CQBAgent

Individual agent that can generate responses.

```python
class CQBAgent:
    def __init__(self, spec: CQBAgentSpec, model_manager: CQBModelManager)
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str
    def get_agent_info(self) -> Dict[str, Any]
    
    # Properties
    @property
    def agent_id(self) -> str
    @property
    def agent_type(self) -> str
    @property
    def specialty(self) -> str
```

#### Methods

##### `generate_response(prompt: str, context: Dict[str, Any] = None) -> str`

Generate response to a prompt.

**Parameters:**
- `prompt`: Input prompt
- `context`: Optional context dictionary

**Returns:**
- `str`: Agent's response

**Example:**
```python
agent = agents[0]
response = agent.generate_response(
    "What are the key risks to consider?",
    context={'team_context': 'Previous discussion...'}
)
```

---

## Data Structures

### CQBAgentSpec

Specification for creating an agent.

```python
@dataclass
class CQBAgentSpec:
    agent_id: str
    agent_type: str  # "Conservative" or "Innovative"
    specialty: str
    model_assignment: str  # "conservative_model" or "innovative_model"
    temperature: float
    persona: str
```

### CollaborationRound

Results from a single collaboration round.

```python
@dataclass
class CollaborationRound:
    round_id: str
    round_type: str
    agent_responses: Dict[str, str]
    round_context: str = ""
    duration: float = 0.0
```

### CollaborationSession

Complete collaboration session data.

```python
@dataclass
class CollaborationSession:
    session_id: str
    query: str
    cqb_session_id: str
    agents_involved: List[str]
    rounds: List[CollaborationRound]
    final_synthesis: str = ""
    total_duration: float = 0.0
```

---

## Configuration

### Model Configuration

```yaml
conservative_model:
  name: str  # Model display name
  model_path: str  # Hugging Face model path
  quantization: str  # 'awq_marlin', 'gptq_marlin', or null
  dtype: str  # 'bfloat16', 'float16', 'auto'
  memory_fraction: float  # 0.1-0.9
  temperature: float  # Sampling temperature
  top_p: float  # Nucleus sampling parameter
  max_tokens: int  # Maximum generation tokens
  max_model_len: int  # Maximum model context length
  enforce_eager: bool  # Disable CUDA graphs
  max_num_seqs: int  # Maximum parallel sequences
```

---

## Utility Functions

### initialize_cqb(config_path: str = 'config.yaml') -> CentralQueryBrain

Convenience function to initialize CQB system.

**Example:**
```python
from cqb_framework import initialize_cqb
cqb = initialize_cqb()
```

---

## JSON Output Format

The `export_collaboration_json()` method returns data in this format:

```json
{
  "collaboration_session": {
    "session_id": "string",
    "query": "string", 
    "cqb_session_id": "string",
    "total_duration_seconds": float,
    "rounds_completed": int,
    "agents_involved": ["string"]
  },
  "agents": {
    "agent_id": {
      "agent_id": "string",
      "agent_type": "Conservative|Innovative",
      "specialty": "string",
      "model_assignment": "string",
      "temperature": float,
      "persona": "string"
    }
  },
  "collaboration_rounds": [
    {
      "round_number": int,
      "round_id": "string",
      "round_type": "string", 
      "duration_seconds": float,
      "context_provided": "string",
      "agent_responses": {
        "agent_id": "response_text"
      }
    }
  ],
  "final_synthesis": "string",
  "metadata": {
    "export_timestamp": float,
    "total_agents": int,
    "total_responses": int,
    "average_response_length": float
  }
}
```

---

## Error Handling

### Common Exceptions

#### `ValueError`
- Invalid session ID
- Invalid agent ID
- Missing configuration

#### `RuntimeError`
- Model initialization failure
- GPU memory issues

#### `FileNotFoundError`
- Missing configuration file
- Missing model files

### Example Error Handling

```python
try:
    cqb = initialize_cqb()
    session_id = cqb.analyze_query_and_generate_agents(query)
    agents = cqb.get_agents(session_id)
except ValueError as e:
    print(f"Configuration error: {e}")
except RuntimeError as e:
    print(f"System error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Performance Monitoring

### Session Metrics

Access performance data through the JSON export:

```python
json_data = collab_module.export_collaboration_json(session_id)

# Timing metrics
total_duration = json_data['collaboration_session']['total_duration_seconds']
avg_round_duration = sum(r['duration_seconds'] for r in json_data['collaboration_rounds']) / len(json_data['collaboration_rounds'])

# Response metrics  
total_responses = json_data['metadata']['total_responses']
avg_response_length = json_data['metadata']['average_response_length']

# Agent metrics
conservative_agents = [a for a in json_data['agents'].values() if a['agent_type'] == 'Conservative']
innovative_agents = [a for a in json_data['agents'].values() if a['agent_type'] == 'Innovative']
```

### Memory Usage

Monitor GPU memory during execution:

```python
import torch

def print_gpu_memory():
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1e9
        cached = torch.cuda.memory_reserved() / 1e9
        print(f"GPU Memory - Allocated: {allocated:.1f}GB, Cached: {cached:.1f}GB")

# Call before and after operations
print_gpu_memory()
session_id = cqb.analyze_query_and_generate_agents(query)
print_gpu_memory()
```

---

## Advanced Usage

### Custom Agent Creation

```python
from cqb_framework import CQBAgentSpec, CQBAgent

# Create custom agent specification
custom_spec = CQBAgentSpec(
    agent_id="Custom_Expert_1",
    agent_type="Conservative",
    specialty="Domain Expertise",
    model_assignment="conservative_model", 
    temperature=0.3,
    persona="Expert in domain-specific analysis"
)

# Create agent instance
custom_agent = CQBAgent(custom_spec, cqb.model_manager)
```

### Session Management

```python
# List all active sessions
active_sessions = cqb.list_active_sessions()

# Get detailed session information
for session_id in active_sessions:
    info = cqb.get_session_info(session_id)
    print(f"Session: {session_id}")
    print(f"  Query: {info['query'][:50]}...")
    print(f"  Agents: {info['agent_count']}")

# Clean up old sessions
for session_id in active_sessions[:-5]:  # Keep only last 5
    cqb.remove_session(session_id)
```

### Batch Processing

```python
# Process multiple queries
queries = [
    "Query 1...",
    "Query 2...", 
    "Query 3..."
]

results = []
for i, query in enumerate(queries):
    print(f"Processing query {i+1}/{len(queries)}")
    session_id = collab_module.collaborate_on_query(query)
    json_data = collab_module.export_collaboration_json(session_id)
    results.append(json_data)

# Analyze batch results
for i, result in enumerate(results):
    print(f"Query {i+1}: {result['metadata']['total_responses']} responses")
```
