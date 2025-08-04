```python

# =============================================================================
# RAO Agent Interaction Deep Dive - See What Agents Actually Say
# =============================================================================

print("🎭 RAO AGENT INTERACTION DEEP DIVE")
print("=" * 60)

from cqb_framework import initialize_cqb

# Initialize RAO-enabled CQB
cqb = initialize_cqb('config.yaml')

if cqb:
    # Test query that should benefit from customer service context
    test_query = """
    We're facing declining customer satisfaction and rising operational costs. 
    What are the most critical issues we should address first, and what 
    specific actions would you recommend?
    """
    
    print(f"🔍 Query: {test_query.strip()}")
    print("\n" + "="*60)
    
    # Generate RAO agents
    session_id = cqb.analyze_query_and_generate_agents(test_query, max_agents=4)
    agents = cqb.get_agents(session_id)
    
    print(f"🤖 AGENT TEAM ASSEMBLED:")
    for i, agent in enumerate(agents, 1):
        context_note = "🧠 Context-Aware" if agent.spec.context_summary else "📝 Standard"
        print(f"   {i}. {agent.specialty} ({agent.agent_type}) {context_note}")
    
    print(f"\n" + "="*60)
    print(f"🎯 CONTEXT BACKGROUND (What agents know):")
    print("-" * 40)
    if agents and agents[0].spec.context_summary:
        print(f"Context Summary: {agents[0].spec.context_summary}")
    else:
        print("No context summary available")
    
    print(f"\n" + "="*60)
    print(f"💬 AGENT RESPONSES TO QUERY:")
    print("="*60)
    
    # Get responses from each agent
    for i, agent in enumerate(agents, 1):
        print(f"\n🎭 AGENT {i}: {agent.agent_id}")
        print(f"   Specialty: {agent.specialty}")
        print(f"   Type: {agent.agent_type}")
        print(f"   Context-Aware: {'Yes' if agent.spec.context_summary else 'No'}")
        print("-" * 50)
        
        try:
            # Ask agent for their perspective
            response = agent.generate_response(
                "Based on your expertise, what are the 3 most critical issues to address first, "
                "and what specific actions would you recommend? Be concrete and actionable."
            )
            
            print(f"RESPONSE:")
            print(f"{response}")
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Error getting response from {agent.agent_id}: {e}")
            print("-" * 50)
    
    print(f"\n" + "="*60)
    print(f"🧠 CONTEXT-INFORMED REASONING ANALYSIS:")
    print("="*60)
    
    # Analyze how context influenced responses
    context_agents = [a for a in agents if a.spec.context_summary]
    standard_agents = [a for a in agents if not a.spec.context_summary]
    
    print(f"Context-Aware Agents: {len(context_agents)}")
    print(f"Standard Agents: {len(standard_agents)}")
    
    # Show one detailed comparison if we have different types
    if context_agents:
        print(f"\n🎯 DETAILED CONTEXT UTILIZATION:")
        print("-" * 40)
        
        context_agent = context_agents[0]
        print(f"Agent: {context_agent.specialty}")
        print(f"Context Background: {context_agent.spec.context_summary}")
        
        # Ask a specific follow-up about the context
        follow_up = context_agent.generate_response(
            "Looking at our specific situation with 25 representatives, 5,000+ monthly interactions, "
            "and a $2.1M budget, what would be your most cost-effective recommendation?"
        )
        
        print(f"\nContext-Specific Follow-up Response:")
        print(f"{follow_up}")
    
    print(f"\n" + "="*60)
    print(f"✅ INTERACTION DEEP DIVE COMPLETE!")
    
else:
    print("❌ CQB initialization failed")

```
