```python
# =============================================================================
# RAO Collaboration Showcase - See How Context-Aware Agents Collaborate
# =============================================================================

print("🤝 RAO COLLABORATION SHOWCASE")
print("=" * 60)

from cqb_framework import initialize_cqb
from collaboration_module import AgentCollaborationModule

# Initialize CQB and collaboration module
cqb = initialize_cqb('config.yaml')

if cqb:
    collab_module = AgentCollaborationModule(cqb)
    
    # Query that should leverage customer service context
    collaboration_query = """
    Given our customer service challenges (declining satisfaction, high costs, 
    staffing issues), develop a comprehensive 6-month improvement plan that 
    addresses our most critical needs while staying within budget constraints.
    """
    
    print(f"🎯 COLLABORATION QUERY:")
    print(f"{collaboration_query.strip()}")
    print("\n" + "="*60)
    
    # Run short collaboration to see interactions
    print(f"🚀 Starting RAO-Enhanced Agent Collaboration...")
    
    # Use fewer agents and rounds to see detailed interactions
    collab_session_id = collab_module.collaborate_on_query(
        collaboration_query,
        max_agents=3,  # Smaller team for detailed view
        collaboration_rounds=2  # Just 2 rounds to see interaction
    )
    
    # Get the full collaboration results
    collab_results = collab_module.get_collaboration_result(collab_session_id)
    
    print(f"\n" + "="*60)
    print(f"👥 COLLABORATION TEAM:")
    print("="*60)
    
    for agent_id in collab_results['agents_involved']:
        print(f"🤖 {agent_id}")
    
    print(f"\n" + "="*60)
    print(f"🎭 ROUND-BY-ROUND INTERACTIONS:")
    print("="*60)
    
    # Show each round in detail
    for round_info in collab_results['round_details']:
        round_num = round_info['round_number']
        print(f"\n🔄 ROUND {round_num}: {round_info['round_type'].upper()}")
        print("-" * 50)
        
        for agent_id, response in round_info['agent_responses'].items():
            print(f"\n🎭 {agent_id}:")
            print(f"{'─' * 30}")
            print(f"{response}")
            print(f"{'─' * 30}")
    
    print(f"\n" + "="*60)
    print(f"🎯 FINAL TEAM SYNTHESIS:")
    print("="*60)
    print(f"{collab_results['final_synthesis']}")
    
    print(f"\n" + "="*60)
    print(f"📊 COLLABORATION METRICS:")
    print("-" * 30)
    print(f"Duration: {collab_results['total_duration']:.1f} seconds")
    print(f"Rounds: {collab_results['rounds_completed']}")
    print(f"Team Size: {len(collab_results['agents_involved'])}")
    print(f"Total Responses: {sum(len(r['agent_responses']) for r in collab_results['round_details'])}")
    
    print(f"\n✅ RAO COLLABORATION SHOWCASE COMPLETE!")
    
else:
    print("❌ CQB initialization failed")
```
