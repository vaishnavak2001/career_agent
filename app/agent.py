# Temporary simplified agent (langchain dependencies being installed)
# This allows the server to start while we set up the full environment

class MockAgentExecutor:
    async def ainvoke(self, input_data):
        return {
            "output": "Agent functionality is currently being set up. Please install langchain dependencies to use the full agent features."
        }

def get_agent_executor():
    return MockAgentExecutor()
