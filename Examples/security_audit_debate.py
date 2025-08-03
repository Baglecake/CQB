# Red Team / Blue Team Security Audit using Adversarial Debate
from cqb_framework import initialize_cqb
from adversarial_debate_module import AdversarialDebateModule

print("🛡️ Red Team vs Blue Team Security Audit - Adversarial Analysis")
print("=" * 70)

# Initialize CQB and the adversarial debate module  
cqb = initialize_cqb()
debate_module = AdversarialDebateModule(cqb)

# The security audit query - perfectly suited for adversarial debate
security_audit_query = """
The city of Metropolis is proposing a new, fully autonomous drone delivery network 
called 'SkyNet Logistics'. The system features:

TECHNICAL ARCHITECTURE:
- Central AI dispatcher managing all flight paths and deliveries
- Hybrid communication: public 5G networks + proprietary mesh networks
- Real-time weather integration and dynamic routing
- Automated drone maintenance scheduling and fault detection
- Integration with city traffic management and emergency services

OPERATIONAL SCOPE:
- 500+ drones operating simultaneously across the city
- Delivery of medical supplies, food, packages, and emergency equipment
- 24/7 operation with priority lanes for emergency services
- Coverage of 95% of the metropolitan area including high-rise buildings
- Expected 50,000+ deliveries daily at full capacity

SECURITY CONCERNS:
- Massive attack surface with hundreds of connected devices
- Critical infrastructure implications for emergency services
- Privacy concerns with citywide surveillance capabilities
- Potential for weaponization or terrorist exploitation
- Economic disruption potential if system compromised

AUDIT OBJECTIVE:
Conduct a comprehensive adversarial security assessment to determine if this 
system can be safely deployed. Identify critical vulnerabilities and evaluate 
whether proposed mitigations are sufficient for public safety.

The city council needs a definitive recommendation on whether to approve, 
modify, or reject this proposal based on security analysis.
"""

# Run adversarial security audit
print("🚨 Initiating Red Team vs Blue Team Security Analysis...")
print("Red Team: Find vulnerabilities and attack vectors")
print("Blue Team: Propose defenses and mitigations")
print()

session_id = debate_module.run_debate_on_query(
    security_audit_query,
    max_agents=7,  # 3 Red Team, 3 Blue Team, 1 Security Judge
    debate_rounds=4,  # Extended rounds for thorough analysis
    position_a="RED TEAM - Expose Critical Vulnerabilities", 
    position_b="BLUE TEAM - Defend with Robust Mitigations"
)

# Get the comprehensive security assessment
summary = debate_module.get_debate_summary(session_id)
print(summary)

# Save the detailed adversarial analysis
filename = debate_module.save_debate_json(session_id, "outputs/red_blue_security_audit.json")
print(f"\n💾 Security audit saved to: {filename}")

# Export additional analysis
json_data = debate_module.export_debate_json(session_id)

print(f"\n🔍 SECURITY AUDIT METRICS")
print("=" * 40)
print(f"Total Security Experts: {json_data['metadata']['total_agents']}")
print(f"Total Attack/Defense Exchanges: {json_data['metadata']['total_responses']}")
print(f"Audit Duration: {json_data['debate_session']['total_duration_seconds']:.1f} seconds")

print(f"\n⚔️ TEAM BREAKDOWN")
print("=" * 40)
for agent_id, agent_info in json_data['agents'].items():
    team = "RED TEAM" if agent_info['agent_id'] in json_data['debate_session']['team_a_agents'] else \
           "BLUE TEAM" if agent_info['agent_id'] in json_data['debate_session']['team_b_agents'] else \
           "SECURITY JUDGE"
    print(f"• {agent_info['specialty']} ({team})")
    print(f"  Agent Type: {agent_info['agent_type']}")
    print(f"  Model: {agent_info['model_assignment']}")
    print()

print("✅ Adversarial security audit complete!")
print("📊 Check the JSON file for complete attack vectors, defense strategies, and final verdict.")
