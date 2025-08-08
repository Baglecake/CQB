# Test script to verify everything works
test_integration_script = '''
print("🧪 Testing Enhanced RAO Integration...")

try:
    # Import the enhanced CQB framework
    from cqb_framework import initialize_cqb

    print("✅ CQB framework imported successfully")

    # Initialize CQB
    cqb = initialize_cqb()

    if cqb:
        print("✅ Enhanced CQB initialized successfully")

        # Test agent generation with sample query
        test_query = "How can we improve our customer service operations based on the provided context?"

        session_id = cqb.analyze_query_and_generate_agents(test_query, max_agents=5)

        if session_id:
            print(f"✅ Agent generation successful: {session_id[:8]}...")

            # Get session info
            info = cqb.get_session_info(session_id)
            print(f"✅ RAO Enabled: {info.get('rao_enabled', False)}")
            print(f"✅ Agents Generated: {info['agent_count']}")

            # Get agents
            agents = cqb.get_agents(session_id)
            print("\\n🤖 Generated Agents:")
            for agent in agents:
                context_indicator = "🧠" if agent.spec.context_summary else ""
                print(f"   - {agent.specialty} {context_indicator}")

            print("\\n🎉 Integration test PASSED!")
            return True
        else:
            print("❌ Agent generation failed")
            return False
    else:
        print("❌ CQB initialization failed")
        return False

except Exception as e:
    print(f"❌ Integration test failed: {e}")
    import traceback
    traceback.print_exc()
    return False
'''

print("🚀 Ready to test! Run the next cell to test integration.")
