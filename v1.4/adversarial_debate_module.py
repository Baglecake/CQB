
# =============================================================================
# Adversarial Debate Module - Confrontational Agent Reasoning
# =============================================================================

import time
import uuid
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

# =============================================================================
# Adversarial Debate Classes
# =============================================================================

@dataclass
class DebateRound:
    """Single round of adversarial debate"""
    round_id: str
    round_type: str
    team_a_responses: Dict[str, str]
    team_b_responses: Dict[str, str]
    judge_evaluation: str = ""
    round_context: str = ""
    duration: float = 0.0

@dataclass
class DebateSession:
    """Complete adversarial debate session"""
    session_id: str
    query: str
    cqb_session_id: str
    team_a_agents: List[str]
    team_b_agents: List[str]
    judge_agent: str
    rounds: List[DebateRound]
    final_verdict: str = ""
    total_duration: float = 0.0

class AdversarialDebateModule:
    """Module that orchestrates adversarial debates using CQB agents"""

    def __init__(self, cqb_brain):
        self.cqb_brain = cqb_brain
        self.active_debates: Dict[str, DebateSession] = {}

        print("⚔️ Adversarial Debate Module initialized")

    def run_debate_on_query(self, query: str, max_agents: int = 7,
                           debate_rounds: int = 3, position_a: str = "FOR",
                           position_b: str = "AGAINST") -> str:
        """Run adversarial debate on a query"""

        print(f"\n⚔️ Starting Adversarial Debate")
        print("=" * 50)
        print(f"Query: {query[:100]}...")
        print(f"Positions: {position_a} vs {position_b}")

        session_start = time.time()

        # 1. Get agents from CQB brain
        print(f"🧠 Requesting agents from CQB...")
        cqb_session_id = self.cqb_brain.analyze_query_and_generate_agents(query, max_agents)
        agents = self.cqb_brain.get_agents(cqb_session_id)

        print(f"✅ Received {len(agents)} agents from CQB")

        # 2. Split agents into opposing teams + judge
        team_a, team_b, judge = self._assign_debate_teams(agents, position_a, position_b)

        # 3. Create debate session
        debate_session_id = str(uuid.uuid4())
        session = DebateSession(
            session_id=debate_session_id,
            query=query,
            cqb_session_id=cqb_session_id,
            team_a_agents=[agent.agent_id for agent in team_a],
            team_b_agents=[agent.agent_id for agent in team_b],
            judge_agent=judge.agent_id,
            rounds=[]
        )

        # 4. Run debate rounds
        for round_num in range(debate_rounds):
            round_result = self._run_debate_round(
                team_a, team_b, judge, query, round_num + 1,
                session.rounds, position_a, position_b
            )
            session.rounds.append(round_result)

        # 5. Generate final verdict
        session.final_verdict = self._generate_final_verdict(
            judge, query, session.rounds, position_a, position_b
        )
        session.total_duration = time.time() - session_start

        # 6. Store session
        self.active_debates[debate_session_id] = session

        print(f"✅ Debate complete in {session.total_duration:.1f}s")
        print(f"📊 {len(session.rounds)} rounds, Teams: {len(team_a)} vs {len(team_b)}")

        return debate_session_id

    def _assign_debate_teams(self, agents, position_a: str, position_b: str) -> Tuple[List, List, Any]:
        """Assign agents to opposing teams and select judge"""

        print(f"⚔️ Assigning agents to debate teams...")

        # Last agent becomes the judge (preferably conservative for impartiality)
        conservative_agents = [a for a in agents if a.agent_type == "Conservative"]
        if conservative_agents:
            judge = conservative_agents[-1]
            remaining_agents = [a for a in agents if a != judge]
        else:
            judge = agents[-1]
            remaining_agents = agents[:-1]

        # Split remaining agents into two teams
        mid_point = len(remaining_agents) // 2
        team_a = remaining_agents[:mid_point]
        team_b = remaining_agents[mid_point:]

        print(f"   Team {position_a}: {[a.agent_id for a in team_a]}")
        print(f"   Team {position_b}: {[a.agent_id for a in team_b]}")
        print(f"   Judge: {judge.agent_id}")

        return team_a, team_b, judge

    def _run_debate_round(self, team_a, team_b, judge, query: str, round_num: int,
                         previous_rounds: List[DebateRound], position_a: str,
                         position_b: str) -> DebateRound:
        """Run a single round of adversarial debate"""

        print(f"⚔️ Round {round_num}: Adversarial Debate")

        round_start = time.time()
        round_id = str(uuid.uuid4())

        # Build context from previous rounds
        context = self._build_debate_context(query, previous_rounds, round_num)

        # Get arguments from Team A (FOR position)
        print(f"   📢 Team {position_a} arguments...")
        team_a_responses = {}
        for agent in team_a:
            try:
                prompt = self._create_debate_prompt(
                    query, round_num, context, position_a, "team_a"
                )
                response = agent.generate_response(prompt)
                team_a_responses[agent.agent_id] = response
                print(f"      ✅ {agent.agent_id}: {len(response)} chars")
            except Exception as e:
                print(f"      ❌ {agent.agent_id}: {e}")
                team_a_responses[agent.agent_id] = f"Error: {str(e)}"

        # Get counter-arguments from Team B (AGAINST position)
        print(f"   📢 Team {position_b} counter-arguments...")
        team_b_responses = {}
        for agent in team_b:
            try:
                prompt = self._create_debate_prompt(
                    query, round_num, context, position_b, "team_b", team_a_responses
                )
                response = agent.generate_response(prompt)
                team_b_responses[agent.agent_id] = response
                print(f"      ✅ {agent.agent_id}: {len(response)} chars")
            except Exception as e:
                print(f"      ❌ {agent.agent_id}: {e}")
                team_b_responses[agent.agent_id] = f"Error: {str(e)}"

        # Judge evaluates the round
        print(f"   ⚖️ Judge evaluation...")
        try:
            judge_prompt = self._create_judge_prompt(
                query, round_num, team_a_responses, team_b_responses, position_a, position_b
            )
            judge_evaluation = judge.generate_response(judge_prompt)
            print(f"      ✅ Judge: {len(judge_evaluation)} chars")
        except Exception as e:
            print(f"      ❌ Judge: {e}")
            judge_evaluation = f"Evaluation error: {str(e)}"

        round_duration = time.time() - round_start

        return DebateRound(
            round_id=round_id,
            round_type=f"debate_round_{round_num}",
            team_a_responses=team_a_responses,
            team_b_responses=team_b_responses,
            judge_evaluation=judge_evaluation,
            round_context=context,
            duration=round_duration
        )

    def _build_debate_context(self, query: str, previous_rounds: List[DebateRound],
                             round_num: int) -> str:
        """Build context for current debate round"""

        if round_num == 1:
            return f"Initial debate on: {query}"

        context = f"Query: {query}\n\n"
        context += "Previous debate rounds:\n"

        # Include key points from previous rounds
        for i, round_result in enumerate(previous_rounds[-2:], 1):
            context += f"\nRound {len(previous_rounds) - 2 + i} Summary:\n"

            # Summarize key arguments from each team
            if round_result.team_a_responses:
                context += "Team A arguments: "
                for agent_id, response in round_result.team_a_responses.items():
                    summary = response[:150] + "..." if len(response) > 150 else response
                    context += f"{summary} "
                context += "\n"

            if round_result.team_b_responses:
                context += "Team B arguments: "
                for agent_id, response in round_result.team_b_responses.items():
                    summary = response[:150] + "..." if len(response) > 150 else response
                    context += f"{summary} "
                context += "\n"

            # Include judge's evaluation
            if round_result.judge_evaluation:
                judge_summary = round_result.judge_evaluation[:200] + "..." if len(round_result.judge_evaluation) > 200 else round_result.judge_evaluation
                context += f"Judge evaluation: {judge_summary}\n"

        context += f"\nRound {round_num}: Continue the adversarial debate with stronger arguments."

        return context

    def _create_debate_prompt(self, query: str, round_num: int, context: str,
                             position: str, team: str, opponent_responses: Dict = None) -> str:
        """Create prompt for debate round"""

        if round_num == 1 and team == "team_a":
            return f"""You are participating in an adversarial debate. Your position is {position} the following query:

Query: {query}

Your role: Argue forcefully {position} this position. Present your strongest arguments, evidence, and reasoning. Be confrontational and challenge any weaknesses you anticipate in the opposing position.

Provide compelling arguments that support your {position} stance."""

        elif round_num == 1 and team == "team_b":
            return f"""You are participating in an adversarial debate. Your position is {position} the following query:

Query: {query}

{context}

Your role: Argue forcefully {position} this position. You have seen the opposing team's arguments. Counter their points directly, expose weaknesses in their reasoning, and present stronger arguments for your {position} stance.

Provide compelling counter-arguments and challenge the opposing position."""

        else:
            opponent_context = ""
            if opponent_responses:
                opponent_context = "\n\nOpposing team's latest arguments:\n"
                for agent_id, response in opponent_responses.items():
                    excerpt = response[:200] + "..." if len(response) > 200 else response
                    opponent_context += f"- {excerpt}\n"

            return f"""You are in Round {round_num} of an adversarial debate. Your position is {position}.

Query: {query}

{context}

{opponent_context}

Your role: Continue arguing forcefully {position} this position. Address the opposing team's arguments directly, expose any flaws in their reasoning, and strengthen your own position with new evidence or perspectives.

Be confrontational and challenge their assumptions."""

    def _create_judge_prompt(self, query: str, round_num: int, team_a_responses: Dict,
                            team_b_responses: Dict, position_a: str, position_b: str) -> str:
        """Create prompt for judge evaluation"""

        # Compile all arguments for the judge
        arguments_summary = f"""Round {round_num} Arguments:

Team {position_a} Arguments:
"""
        for agent_id, response in team_a_responses.items():
            arguments_summary += f"- {agent_id}: {response}\n\n"

        arguments_summary += f"""Team {position_b} Arguments:
"""
        for agent_id, response in team_b_responses.items():
            arguments_summary += f"- {agent_id}: {response}\n\n"

        return f"""You are the impartial judge in an adversarial debate about:

Query: {query}

{arguments_summary}

As the judge, evaluate this round of debate by:

1. Assessing the strength of each team's arguments
2. Identifying which team presented more compelling evidence
3. Noting any logical fallacies or weak reasoning
4. Determining which team was more persuasive in this round
5. Providing constructive feedback for both teams

Be objective and critical in your analysis. Point out both strengths and weaknesses in each team's performance."""

    def _generate_final_verdict(self, judge, query: str, rounds: List[DebateRound],
                               position_a: str, position_b: str) -> str:
        """Generate final verdict after all debate rounds"""

        print(f"⚖️ Generating final verdict...")

        # Compile all rounds for final judgment
        full_debate_summary = f"Complete Debate Summary for: {query}\n\n"

        for i, round_result in enumerate(rounds, 1):
            full_debate_summary += f"=== Round {i} ===\n"

            full_debate_summary += f"Team {position_a} Arguments:\n"
            for agent_id, response in round_result.team_a_responses.items():
                summary = response[:300] + "..." if len(response) > 300 else response
                full_debate_summary += f"- {summary}\n"

            full_debate_summary += f"\nTeam {position_b} Arguments:\n"
            for agent_id, response in round_result.team_b_responses.items():
                summary = response[:300] + "..." if len(response) > 300 else response
                full_debate_summary += f"- {summary}\n"

            full_debate_summary += f"\nRound {i} Evaluation: {round_result.judge_evaluation}\n\n"

        verdict_prompt = f"""{full_debate_summary}

As the final judge, provide your comprehensive verdict on this adversarial debate:

1. Declare the winning position ({position_a} or {position_b}) and explain why
2. Summarize the strongest arguments from each side
3. Identify key turning points in the debate
4. Provide an overall assessment of the quality of reasoning
5. Offer final insights on the query based on the complete debate

Your verdict should be thorough, balanced, and decisive."""

        verdict = judge.generate_response(verdict_prompt)

        print(f"✅ Final verdict complete: {len(verdict)} characters")

        return verdict

    def get_debate_summary(self, debate_session_id: str) -> str:
        """Get formatted debate summary"""
        session = self.active_debates.get(debate_session_id)
        if not session:
            raise ValueError(f"Debate session {debate_session_id} not found")

        summary = f"""
⚔️ ADVERSARIAL DEBATE SUMMARY
=============================

Query: {session.query}

Team Composition:
- Team A: {len(session.team_a_agents)} agents
- Team B: {len(session.team_b_agents)} agents
- Judge: {session.judge_agent}

Debate Duration: {session.total_duration:.1f} seconds
Rounds Completed: {len(session.rounds)}

Final Verdict:
{session.final_verdict}

Participants:
Team A: {', '.join(session.team_a_agents)}
Team B: {', '.join(session.team_b_agents)}
Judge: {session.judge_agent}
"""
        return summary

    def export_debate_json(self, debate_session_id: str) -> Dict[str, Any]:
        """Export debate results as JSON with license compliance"""
        session = self.active_debates.get(debate_session_id)
        if not session:
            raise ValueError(f"Debate session {debate_session_id} not found")

        # Get CQB session info for agent details AND license manifest
        try:
            cqb_info = self.cqb_brain.get_session_info(session.cqb_session_id)
            agent_details = {agent['agent_id']: agent for agent in cqb_info['agents']}
            license_manifest = cqb_info.get('license_manifest', {})
        except:
            agent_details = {}
            license_manifest = {}

        # ADD the license_manifest and compliance_info sections:
        return {
            'debate_session': {
                'session_id': debate_session_id,
                'query': session.query,
                'cqb_session_id': session.cqb_session_id,
                'total_duration_seconds': session.total_duration,
                'rounds_completed': len(session.rounds),
                'team_a_agents': session.team_a_agents,
                'team_b_agents': session.team_b_agents,
                'judge_agent': session.judge_agent
            },
            'agents': agent_details,
            'debate_rounds': [
                {
                    'round_number': i + 1,
                    'round_id': round_result.round_id,
                    'round_type': round_result.round_type,
                    'duration_seconds': round_result.duration,
                    'context_provided': round_result.round_context[:500] + "..." if len(round_result.round_context) > 500 else round_result.round_context,
                    'team_a_responses': round_result.team_a_responses,
                    'team_b_responses': round_result.team_b_responses,
                    'judge_evaluation': round_result.judge_evaluation
                }
                for i, round_result in enumerate(session.rounds)
            ],
            'final_verdict': session.final_verdict,
            'metadata': {
                'export_timestamp': time.time(),
                'total_agents': len(session.team_a_agents) + len(session.team_b_agents) + 1,
                'total_responses': sum(
                    len(r.team_a_responses) + len(r.team_b_responses) + 1 
                    for r in session.rounds
                ),
                'debate_format': 'adversarial',
                'reasoning_type': 'adversarial'
            },
            
            'license_manifest': license_manifest,
            'compliance_info': {
                'models_compliant': license_manifest.get('license_compliance', False),
                'registry_version': license_manifest.get('registry_version', 'unknown'),
                'compliance_note': 'Users must comply with model licenses when redistributing outputs'
            }
        }
        
    def save_debate_json(self, debate_session_id: str, filename: str = None) -> str:
        """Save debate results to JSON file"""
        import json

        if filename is None:
            filename = f"debate_{debate_session_id[:8]}.json"

        export_data = self.export_debate_json(debate_session_id)

        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Debate exported to {filename}")
        return filename

# =============================================================================
# Usage Example
# =============================================================================

def test_adversarial_debate():
    """Test the adversarial debate module"""
    from cqb_framework import initialize_cqb

    print("🧪 Testing Adversarial Debate Module")
    print("=" * 50)

    # Initialize CQB and debate module
    cqb = initialize_cqb()
    if not cqb:
        print("❌ Failed to initialize CQB")
        return

    debate_module = AdversarialDebateModule(cqb)

    # Test query - something debatable
    test_query = """
    Should artificial intelligence development be regulated by government agencies,
    or should the tech industry remain self-regulated to foster innovation?
    """

    # Run debate
    debate_session_id = debate_module.run_debate_on_query(
        test_query,
        max_agents=7,
        debate_rounds=3,
        position_a="FOR government regulation",
        position_b="AGAINST government regulation"
    )

    # Get results
    summary = debate_module.get_debate_summary(debate_session_id)
    print(summary)

    # Save results
    filename = debate_module.save_debate_json(debate_session_id)

    return debate_module, debate_session_id

if __name__ == "__main__":
    test_adversarial_debate()
