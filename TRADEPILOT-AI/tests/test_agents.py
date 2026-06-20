def test_intent_agent():
    from agents.intent_agent import IntentAgent
    agent = IntentAgent()
    res = agent.process("test input")
    assert "Intent Agent" in res
