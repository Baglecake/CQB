# =============================================================================
# Agent Collaboration Module
# =============================================================================

import time
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

# =============================================================================
# Collaboration Module
# =============================================================================

@dataclass
class CollaborationRound:
    """Single round of collaboration"""
    round_id: str
    round_type: str
    agent_responses: Dict[str, str]
    round_context: str = ""
    duration: float = 0.0

@dataclass
class CollaborationSession:
    """Complete collaboration session"""
    session_id: str
    query: str
    cqb_session_id: str
    agents_involved: List[str]
    rounds: List[CollaborationRound]
    final_synthesis: str = ""
    total_duration: float = 0.0

class AgentCollaborationModule:
    """Module that orchestrates agent collaboration using CQB"""
    
    def __init__(self, cqb_brain):
        self.cqb_brain = cqb_brain
        self.active_collaborations: Dict[str, CollaborationSession] = {}
        
        print("🤝 Agent Collaboration Module initialized")
    
    def collaborate_on_query(self, query: str, max_agents: int = 6, 
                           collaboration_rounds: int = 3) -> str:
        """Run collaborative analysis on a query"""
        
        print(f"\n🤝 Starting Agent Collaboration")
        print("=" * 50)
        print(f"Query: {query[:100]}...")
        
        session_start = time.time()
        
        # 1. Get agents from CQB brain
        print(f"🧠 Requesting agents from CQB...")
        cqb_session_id = self.cqb_brain.analyze_query_and_generate_agents(query, max_agents)
        agents = self.cqb_brain.get_agents(cqb_session_id)
        
        print(f"✅ Received {len(agents)} agents from CQB")
        
        # 2. Create collaboration session
        collab_session_id = str(uuid.uuid4())
        session = CollaborationSession(
            session_id=collab_session_id,
            query=query,
            cqb_session_id=cqb_session_id,
            agents_involved=[agent.agent_id for agent in agents],
            rounds=[]
        )
        
        # 3. Run collaboration rounds
        for round_num in range(collaboration_rounds):
            round_result = self._run_collaboration_round(
                agents, query, round_num + 1, session.rounds
            )
            session.rounds.append(round_result)
        
        # 4. Generate final synthesis
        session.final_synthesis = self._synthesize_collaboration(agents, query, session.rounds)
        session.total_duration = time.time() - session_start
        
        # 5. Store session
        self.active_collaborations[collab_session_id] = session
        
        print(f"✅ Collaboration complete in {session.total_duration:.1f}s")
        print(f"📊 {len(session.rounds)} rounds, {len(agents)} agents")
        
        return collab_session_id
    
    def _run_collaboration_round(self, agents, query: str, round_num: int, 
                               previous_rounds: List[CollaborationRound]) -> CollaborationRound:
        """Run a single round of collaboration"""
        
        print(f"🔄 Round {round_num}: Agent Collaboration")
        
        round_start = time.time()
        round_id = str(uuid.uuid4())
        
        # Build context from previous rounds
        context = self._build_round_context(query, previous_rounds, round_num)
        
        # Get responses from all agents
        responses = {}
        for agent in agents:
            try:
                prompt = self._create_round_prompt(query, round_num, context)
                response = agent.generate_response(prompt, {'team_context': context})
                responses[agent.agent_id] = response
                print(f"   ✅ {agent.agent_id}: {len(response)} chars")
                
            except Exception as e:
                print(f"   ❌ {agent.agent_id}: {e}")
                responses[agent.agent_id] = f"Error: {str(e)}"
        
        round_duration = time.time() - round_start
        
        return CollaborationRound(
            round_id=round_id,
            round_type=f"collaboration_round_{round_num}",
            agent_responses=responses,
            round_context=context,
            duration=round_duration
        )
    
    def _build_round_context(self, query: str, previous_rounds: List[CollaborationRound], 
                           round_num: int) -> str:
        """Build context for current round - MEANINGFUL context for collaboration"""
        
        if round_num == 1:
            return f"Initial analysis of: {query}"
        
        context = f"Query: {query}\n\n"
        context += "Previous team discussion:\n"
        
        # Include key points from previous rounds - MEANINGFUL LENGTH
        for i, round_result in enumerate(previous_rounds[-2:], 1):  # Last 2 rounds
            context += f"\nRound {len(previous_rounds) - 2 + i} Key Points:\n"
            for agent_id, response in round_result.agent_responses.items():
                # Take first 300 characters - enough to be meaningful
                summary = response[:300] + "..." if len(response) > 300 else response
                context += f"- {agent_id}: {summary}\n"
        
        context += f"\nRound {round_num}: Build upon and refine the team's analysis."
        
        return context
    
    def _create_round_prompt(self, query: str, round_num: int, context: str) -> str:
        """Create prompt for collaboration round"""
        
        if round_num == 1:
            return f"""Query: {query}

Provide your initial expert analysis of this query. Focus on your area of specialty and provide specific insights, recommendations, or considerations that would be valuable for addressing this query comprehensively."""

        elif round_num == 2:
            return f"""Query: {query}

{context}

Based on the team discussion so far, provide your refined analysis. You may:
- Build upon points made by other team members
- Offer alternative perspectives or approaches
- Identify potential issues or gaps in the current analysis
- Suggest additional considerations or solutions

Focus on collaborative improvement of the team's understanding."""

        else:
            return f"""Query: {query}

{context}

For this final round, provide your conclusive analysis and recommendations. Consider the full team discussion and offer:
- Your final assessment or recommendations
- Key insights that should guide decision-making
- Any critical factors the team should prioritize
- Practical next steps or implementation considerations"""
    
    def _synthesize_collaboration(self, agents, query: str, 
                                rounds: List[CollaborationRound]) -> str:
        """Synthesize the collaboration - FIX: Don't include all full responses"""
        
        print(f"🔄 Synthesizing collaboration results...")
        
        # Use the first conservative agent for synthesis (more analytical)
        conservative_agents = [a for a in agents if a.agent_type == "Conservative"]
        synthesizer = conservative_agents[0] if conservative_agents else agents[0]
        
        # Build SMART synthesis context - extract key insights instead of dumping everything
        synthesis_context = f"Query: {query}\n\n"
        synthesis_context += "Team Collaboration Key Insights:\n"
        
        # For each round, extract the core points instead of full responses
        for i, round_result in enumerate(rounds, 1):
            synthesis_context += f"\nRound {i} Key Insights:\n"
            for agent_id, response in round_result.agent_responses.items():
                # Take meaningful excerpts - 200 chars should capture key points
                key_excerpt = response[:200] + "..." if len(response) > 200 else response
                synthesis_context += f"• {agent_id}: {key_excerpt}\n"
        
        synthesis_prompt = f"""{synthesis_context}

Based on this team collaboration, provide a comprehensive synthesized analysis that:

1. Integrates the key insights from all team members
2. Identifies the most important findings and recommendations  
3. Presents a coherent, actionable response to the original query
4. Provides clear next steps for implementation

Create a unified response that captures the collective expertise of the team."""
        
        synthesis = synthesizer.generate_response(synthesis_prompt)
        
        print(f"✅ Synthesis complete: {len(synthesis)} characters")
        
        return synthesis
    
    def get_collaboration_result(self, collab_session_id: str) -> Dict[str, Any]:
        """Get collaboration results"""
        session = self.active_collaborations.get(collab_session_id)
        if not session:
            raise ValueError(f"Collaboration session {collab_session_id} not found")
        
        return {
            'session_id': collab_session_id,
            'query': session.query,
            'agents_involved': session.agents_involved,
            'rounds_completed': len(session.rounds),
            'total_duration': session.total_duration,
            'final_synthesis': session.final_synthesis,
            'round_details': [
                {
                    'round_number': i + 1,
                    'round_type': round_result.round_type,
                    'duration': round_result.duration,
                    'agent_responses': round_result.agent_responses
                }
                for i, round_result in enumerate(session.rounds)
            ]
        }
    
    def get_collaboration_summary(self, collab_session_id: str) -> str:
        """Get formatted collaboration summary"""
        result = self.get_collaboration_result(collab_session_id)
        
        summary = f"""
🤝 AGENT COLLABORATION SUMMARY
==============================

Query: {result['query']}

Team Composition: {len(result['agents_involved'])} agents
Collaboration Duration: {result['total_duration']:.1f} seconds
Rounds Completed: {result['rounds_completed']}

Final Synthesis:
{result['final_synthesis']}

Agents Involved:
"""
        for agent_id in result['agents_involved']:
            summary += f"- {agent_id}\n"
        
        return summary
    
    def export_collaboration_json(self, collab_session_id: str) -> Dict[str, Any]:
        """Export collaboration results as JSON"""
        session = self.active_collaborations.get(collab_session_id)
        if not session:
            raise ValueError(f"Collaboration session {collab_session_id} not found")
        
        # Get CQB session info for agent details
        try:
            cqb_info = self.cqb_brain.get_session_info(session.cqb_session_id)
            agent_details = {agent['agent_id']: agent for agent in cqb_info['agents']}
        except:
            agent_details = {}
        
        return {
            'collaboration_session': {
                'session_id': collab_session_id,
                'query': session.query,
                'cqb_session_id': session.cqb_session_id,
                'total_duration_seconds': session.total_duration,
                'rounds_completed': len(session.rounds),
                'agents_involved': session.agents_involved
            },
            'agents': agent_details,
            'collaboration_rounds': [
                {
                    'round_number': i + 1,
                    'round_id': round_result.round_id,
                    'round_type': round_result.round_type,
                    'duration_seconds': round_result.duration,
                    'context_provided': round_result.round_context,
                    'agent_responses': round_result.agent_responses
                }
                for i, round_result in enumerate(session.rounds)
            ],
            'final_synthesis': session.final_synthesis,
            'metadata': {
                'export_timestamp': time.time(),
                'total_agents': len(session.agents_involved),
                'total_responses': sum(len(r.agent_responses) for r in session.rounds),
                'average_response_length': sum(
                    sum(len(resp) for resp in r.agent_responses.values()) 
                    for r in session.rounds
                ) / max(1, sum(len(r.agent_responses) for r in session.rounds))
            }
        }
    
    def save_collaboration_json(self, collab_session_id: str, filename: str = None) -> str:
        """Save collaboration results to JSON file"""
        import json
        
        if filename is None:
            filename = f"collaboration_{collab_session_id[:8]}.json"
        
        export_data = self.export_collaboration_json(collab_session_id)
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Collaboration exported to {filename}")
        return filename
    
    def list_active_collaborations(self) -> List[str]:
        """List active collaboration session IDs"""
        return list(self.active_collaborations.keys())

# =============================================================================
# Usage and Testing
# =============================================================================

def test_collaboration_module(cqb_brain):
    """Test the collaboration module"""
    
    print("🧪 Testing Agent Collaboration Module")
    print("=" * 50)
    
    # Initialize collaboration module
    collab_module = AgentCollaborationModule(cqb_brain)
    
    # Test query - meaningful length for proper collaboration
    test_query = """
    Our company is experiencing declining employee engagement and increasing turnover. 
    We need to develop a comprehensive strategy to improve workplace satisfaction, 
    retain talent, and create a more positive company culture. What specific actions 
    should we take, and how should we prioritize and implement them?
    """
    
    # Run collaboration - restore meaningful settings
    collab_session_id = collab_module.collaborate_on_query(
        test_query, 
        max_agents=5, 
        collaboration_rounds=3
    )
    
    # Get results
    summary = collab_module.get_collaboration_summary(collab_session_id)
    print(summary)
    
    # Export to JSON
    json_filename = collab_module.save_collaboration_json(collab_session_id)
    
    # Also return the JSON data for viewing
    json_data = collab_module.export_collaboration_json(collab_session_id)
    
    return collab_module, collab_session_id, json_data

if __name__ == "__main__":
    print("🤝 Agent Collaboration Module")
    print("=" * 40)
    print("Usage:")
    print("  collab_module = AgentCollaborationModule(cqb_brain)")
    print("  session_id = collab_module.collaborate_on_query(query)")
    print("  summary = collab_module.get_collaboration_summary(session_id)")
    print("  json_data = collab_module.export_collaboration_json(session_id)")
    print("  filename = collab_module.save_collaboration_json(session_id)")
