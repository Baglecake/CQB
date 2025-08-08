# Test the integration
try:
    from cqb_framework import initialize_cqb

    cqb = initialize_cqb()

    if cqb:
        print("✅ Enhanced CQB initialized successfully")

        # Test with a query
        session_id = cqb.analyze_query_and_generate_agents(
            "How can we improve customer service operations?",
            max_agents=5
        )

        if session_id:
            agents = cqb.get_agents(session_id)
            print(f"✅ Generated {len(agents)} agents:")
            for agent in agents:
                context_flag = "🧠" if agent.spec.context_summary else ""
                print(f"   - {agent.specialty} {context_flag}")
            print("\n🎉 SUCCESS! Enhanced RAO is working!")
        else:
            print("❌ Agent generation failed")
    else:
        print("❌ CQB initialization failed")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
