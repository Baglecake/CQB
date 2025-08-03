
# Clinical Differential Diagnosis Scenario (Extended DDx)
from cqb_framework import initialize_cqb
from collaboration_module import AgentCollaborationModule

print("🩺 Clinical Differential Diagnosis Team Consultation (Extended DDx)")
print("=" * 60)

# Initialize CQB and the collaboration module
cqb = initialize_cqb()
collab_module = AgentCollaborationModule(cqb)

# The structured query for the clinical case
ddx_query = """
**Case Presentation:**

An 81-year-old man is brought to the clinic by his son to be evaluated for memory issues. The patient's son says he has difficulty remembering recent events and names. He says the patient's symptoms have progressively worsened over the last several years but became acutely worse just recently. Also, yesterday, the patient complained that he could not see out of his right eye, but today he can. When asked about these concerns, the patient seems to have no insight into the problem and reports feeling well. His medical history is significant for diabetes mellitus type 2 and hypertension. He had a left basal ganglia hemorrhage 12 years ago and a right middle cerebral artery infarction 4 years ago. Current medications are amlodipine, aspirin, clopidogrel, metformin, sitagliptin, and valsartan. He lives with his son and can feed himself and change his clothes. There is no history of urinary or fecal incontinence. His vitals include: blood pressure 137/82 mm Hg, pulse 78/min, respiratory rate 16/min, temperature 37.0 °C (98.6 °F). On physical examination, the patient is alert and oriented. He is unable to perform simple arithmetic calculations and the mini-mental status exam is inconclusive. He can write his name and comprehend written instructions. Muscle strength is 4/5 on the right side. The tone is also slightly reduced on the right side with exaggerated reflexes. His gait is hemiparetic.

---

**Core Task for the Diagnostic Team:**

Based on the provided clinical case, please collaborate to produce a comprehensive differential diagnosis. Your final synthesized report should address the following points:

1.  A primary, most likely diagnosis with detailed reasoning, referencing specific findings from the patient's history and physical exam.
2.  A list of up to 7 other important differential diagnoses that must be considered.
3.  For each differential, provide a brief rationale for why it is on the list and what makes it less likely than the primary diagnosis.
4.  Recommendations for the next steps in management, including specific diagnostic tests (e.g., imaging, labs) to confirm the diagnosis and rule out others.
5.  A brief summary of how each specialist's perspective (e.g., Neurology, Geriatrics, Neuroradiology) contributes to the overall picture.
"""

# Run the collaborative analysis
session_id = collab_module.collaborate_on_query(
    ddx_query,
    max_agents=5,
    collaboration_rounds=3 
)

# Get and print the final summary
summary = collab_module.get_collaboration_summary(session_id)
print(summary)

# Save the detailed JSON output
filename = collab_module.save_collaboration_json(session_id, "outputs/clinical_ddx_extended_analysis.json")
print(f"\n💾 Analysis saved to: {filename}")
