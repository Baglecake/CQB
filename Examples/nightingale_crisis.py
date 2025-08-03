
# Nightingale Crisis Scenario
from cqb_framework import initialize_cqb
from collaboration_module import AgentCollaborationModule

print("🩺 Nightingale Crisis Analysis")
print("=" * 50)

# Initialize CQB and the collaboration module
cqb = initialize_cqb()
collab_module = AgentCollaborationModule(cqb)

# The crisis query
crisis_query = """
A leading hospital, 'St. Elara's Digital Health Institute,' uses a proprietary AI, 'Nightingale-7,' for real-time patient monitoring, diagnostics, and automated treatment adjustments in its advanced ICU.

The Crisis:
Over the past 72 hours, five patients in the Nightingale-7 ICU, who were admitted for unrelated conditions (e.g., post-op recovery, cardiac observation, diabetic ketoacidosis), have all developed a rapid-onset, unidentifiable syndrome. Symptoms include high fever, erratic blood pressure, vasculitis-like skin lesions, and acute respiratory distress. All standard infectious disease and pathogen screens have come back negative.

The Core Question:
Is this a novel, highly contagious pathogen that has breached hospital containment, an unknown environmental or toxicological factor within the ICU, OR is the Nightingale-7 AI itself, through a subtle emergent bias or a cascading feedback loop, causing or exacerbating this syndrome via its automated treatment adjustments?

The hospital's board of directors needs an immediate and comprehensive action plan. They need to simultaneously diagnose the root cause, mitigate the crisis for the affected patients, ensure the safety of other patients, and handle the potential ethical and PR fallout. Develop an integrated strategy.
"""

# Run the collaborative analysis
session_id = collab_module.collaborate_on_query(
    crisis_query,
    max_agents=8,      # A team of 8 seems appropriate
    collaboration_rounds=3 # 3 rounds for initial, refinement, and synthesis
)

# Get and print the final summary
summary = collab_module.get_collaboration_summary(session_id)
print(summary)

# Save the detailed JSON output
filename = collab_module.save_collaboration_json(session_id, "outputs/nightingale_crisis_analysis.json")
print(f"\n💾 Analysis saved to: {filename}")
