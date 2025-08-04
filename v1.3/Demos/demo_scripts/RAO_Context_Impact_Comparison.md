```python

# =============================================================================
# RAO Context Impact Comparison - Same Agent Type, Different Context Awareness
# =============================================================================

print("⚔️ RAO CONTEXT IMPACT DEMONSTRATION")
print("=" * 60)

from cqb_framework import initialize_cqb
import time

# Test query for comparison
test_query = "What would be your top recommendation to improve our customer service operations?"

print(f"🎯 TEST QUERY: {test_query}")
print("\n" + "="*60)

# Test 1: RAO-Enhanced Agent
print("🧠 RAO-ENHANCED AGENT (Context-Aware)")
print("="*40)

cqb_rao = initialize_cqb('config.yaml')
if cqb_rao:
    session_rao = cqb_rao.analyze_query_and_generate_agents("Customer service improvement strategy", max_agents=1)
    agents_rao = cqb_rao.get_agents(session_rao)
    
    if agents_rao:
        rao_agent = agents_rao[0]
        print(f"Agent: {rao_agent.specialty} ({rao_agent.agent_type})")
        print(f"Context Summary: {rao_agent.spec.context_summary[:100]}...")
        print(f"\nRAO AGENT RESPONSE:")
        print("-" * 40)
        
        rao_response = rao_agent.generate_response(test_query)
        print(rao_response)
        
        print(f"\n" + "="*60)
        
        # Follow-up question to test context utilization
        print(f"🔍 CONTEXT-SPECIFIC FOLLOW-UP:")
        print("Query: How would you prioritize improvements given our $2.1M budget and 25-person team?")
        print("-" * 40)
        
        followup_response = rao_agent.generate_response(
            "How would you prioritize improvements given our $2.1M budget and 25-person team?"
        )
        print(followup_response)

print(f"\n" + "="*60)

# Test 2: Standard Agent (if we can create one without RAO context)
print("📝 SIMULATED STANDARD AGENT RESPONSE")
print("="*40)
print("(Simulating what a non-context-aware agent might say)")

# Let's manually create a non-context agent for comparison
from cqb_framework import CQBAgentSpec, CQBAgent

if cqb_rao:
    # Create a standard agent spec without context
    standard_spec = CQBAgentSpec(
        agent_id="Standard_BusinessStrategist_1",
        agent_type="Conservative",
        specialty="Business Strategist", 
        model_assignment="conservative_model",
        temperature=0.2,
        persona="Analytical and systematic Business Strategist",
        context_summary=""  # No context
    )
    
    standard_agent = CQBAgent(standard_spec, cqb_rao.model_manager)
    
    print(f"Agent: {standard_agent.specialty} ({standard_agent.agent_type})")
    print(f"Context Summary: None")
    print(f"\nSTANDARD AGENT RESPONSE:")
    print("-" * 40)
    
    standard_response = standard_agent.generate_response(test_query)
    print(standard_response)

print(f"\n" + "="*60)
print(f"📊 COMPARISON ANALYSIS:")
print("="*60)

print(f"Key Differences to Look For:")
print(f"✅ RAO Agent should mention specific metrics (5,000+ interactions, $450 per resolution)")
print(f"✅ RAO Agent should reference budget constraints ($2.1M)")
print(f"✅ RAO Agent should address team size issues (25 representatives)")
print(f"✅ RAO Agent should mention specific pain points (48-hour response time)")
print(f"✅ RAO Agent should provide context-specific recommendations")
print(f"")
print(f"❌ Standard Agent will give generic business advice")
print(f"❌ Standard Agent won't reference specific situation details")
print(f"❌ Standard Agent responses will be more theoretical")

print(f"\n✅ CONTEXT IMPACT DEMONSTRATION COMPLETE!")

```
