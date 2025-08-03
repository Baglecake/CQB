
#!/usr/bin/env python3
"""
TechFlow Crisis Scenario - Example CQB Usage
============================================

This example demonstrates CQB's ability to handle complex, multi-faceted
crisis scenarios requiring diverse expertise and collaborative reasoning.

The scenario involves an AI startup facing simultaneous technical, business,
regulatory, and organizational challenges.
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cqb_framework import initialize_cqb
from collaboration_module import AgentCollaborationModule


def run_techflow_crisis_analysis():
    """Run the TechFlow crisis analysis scenario"""
    
    print("🎭 TechFlow AI Startup Crisis Analysis")
    print("=" * 60)
    print("Multi-agent collaborative reasoning for complex crisis management")
    print()
    
    # Define the crisis scenario
    crisis_scenario = """
    TechFlow, a 50-person AI startup, is facing a critical multi-dimensional crisis:

    TECHNICAL CRISIS:
    - ML models showing algorithmic bias in loan approval recommendations
    - Potential fair lending law violations discovered in recent audit
    - Engineering team split: retrain from scratch vs. patch existing system
    - Head of AI Ethics resigned citing bias concerns, damaging internal morale

    BUSINESS CRISIS:
    - Major competitor announced similar product with $100M funding
    - Only 6 months of runway remaining
    - Series A negotiations have stalled due to technical issues
    - Biggest client (40% revenue) threatening cancellation within 60 days

    REGULATORY CRISIS:
    - CFPB inquiry letter about algorithmic decision-making processes
    - 30-day deadline for comprehensive documentation response
    - Potential investigation could impact future funding and partnerships

    ORGANIZATIONAL CRISIS:
    - Three key engineers considering resignation following ethics head departure
    - Team morale at all-time low due to uncertainty and ethical concerns
    - Leadership credibility questioned internally

    STRATEGIC QUESTION:
    The CEO needs an integrated crisis response strategy addressing:
    1. Technical approach to bias remediation
    2. Business continuity and funding strategy  
    3. Regulatory compliance and communication
    4. Talent retention and organizational recovery
    5. Client relationship management and damage control

    What should be the comprehensive crisis response plan with specific actions,
    timelines, resource allocation, and risk mitigation strategies?
    """
    
    # Initialize CQB system
    print("🧠 Initializing Central Query Brain...")
    cqb = initialize_cqb()
    
    if not cqb:
        print("❌ Failed to initialize CQB. Check your configuration.")
        return None
    
    # Initialize collaboration module
    collab_module = AgentCollaborationModule(cqb)
    
    # Run collaborative analysis
    print("🤝 Starting multi-agent crisis analysis...")
    print("Expected agents: Crisis Management, AI Ethics, Regulatory, Business Strategy, etc.")
    print()
    
    session_id = collab_module.collaborate_on_query(
        crisis_scenario,
        max_agents=8,  # Large team for comprehensive crisis response
        collaboration_rounds=4  # Extended deliberation for complex scenario
    )
    
    # Generate outputs
    print("\n📊 Generating Analysis Results...")
    
    # Get summary
    summary = collab_module.get_collaboration_summary(session_id)
    
    # Export detailed JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"outputs/techflow_crisis_{timestamp}.json"
    
    # Ensure outputs directory exists
    os.makedirs("outputs", exist_ok=True)
    
    collab_module.save_collaboration_json(session_id, json_filename)
    json_data = collab_module.export_collaboration_json(session_id)
    
    # Display key results
    print("\n" + "="*60)
    print("🎯 CRISIS ANALYSIS SUMMARY")
    print("="*60)
    print(summary)
    
    print("\n" + "="*60)
    print("📈 COLLABORATION METRICS")
    print("="*60)
    print(f"Total Agents: {json_data['metadata']['total_agents']}")
    print(f"Total Responses: {json_data['metadata']['total_responses']}")
    print(f"Average Response Length: {json_data['metadata']['average_response_length']:.0f} chars")
    print(f"Total Duration: {json_data['collaboration_session']['total_duration_seconds']:.1f} seconds")
    
    print("\n" + "="*60)
    print("🤖 AGENT BREAKDOWN")
    print("="*60)
    for agent_id, agent_info in json_data['agents'].items():
        print(f"• {agent_id}")
        print(f"  Specialty: {agent_info['specialty']}")
        print(f"  Type: {agent_info['agent_type']}")
        print(f"  Model: {agent_info['model_assignment']}")
        print()
    
    print(f"💾 Detailed results saved to: {json_filename}")
    
    return {
        'session_id': session_id,
        'json_data': json_data,
        'filename': json_filename,
        'summary': summary
    }


def analyze_agent_performance(json_data):
    """Analyze the performance and patterns of different agent types"""
    
    print("\n" + "="*60)
    print("🔬 AGENT PERFORMANCE ANALYSIS")
    print("="*60)
    
    conservative_responses = []
    innovative_responses = []
    
    # Categorize responses by agent type
    for round_data in json_data['collaboration_rounds']:
        for agent_id, response in round_data['agent_responses'].items():
            if agent_id in json_data['agents']:
                agent_type = json_data['agents'][agent_id]['agent_type']
                response_length = len(response)
                
                if agent_type == 'Conservative':
                    conservative_responses.append(response_length)
                elif agent_type == 'Innovative':
                    innovative_responses.append(response_length)
    
    # Calculate statistics
    if conservative_responses:
        print(f"Conservative Agents:")
        print(f"  Average Response Length: {sum(conservative_responses)/len(conservative_responses):.0f} chars")
        print(f"  Total Responses: {len(conservative_responses)}")
    
    if innovative_responses:
        print(f"Innovative Agents:")
        print(f"  Average Response Length: {sum(innovative_responses)/len(innovative_responses):.0f} chars")
        print(f"  Total Responses: {len(innovative_responses)}")
    
    # Analyze round progression
    print(f"\nRound Progression:")
    for i, round_data in enumerate(json_data['collaboration_rounds'], 1):
        print(f"  Round {i}: {len(round_data['agent_responses'])} responses, "
              f"{round_data['duration_seconds']:.1f}s duration")


if __name__ == "__main__":
    print("🚀 Central Query Brain - TechFlow Crisis Example")
    print("This example demonstrates multi-agent crisis management analysis")
    print()
    
    try:
        # Run the crisis analysis
        results = run_techflow_crisis_analysis()
        
        if results:
            # Perform additional analysis
            analyze_agent_performance(results['json_data'])
            
            print("\n✅ Crisis analysis complete!")
            print(f"📁 Results available in: {results['filename']}")
            
        else:
            print("❌ Analysis failed. Please check your setup.")
            
    except KeyboardInterrupt:
        print("\n⚠️ Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
