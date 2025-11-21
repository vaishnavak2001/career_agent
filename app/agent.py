"""Simple agent module without LangChain dependency."""
from typing import Dict, Any


def get_agent_executor():
    """
    Creates and returns a mock agent executor.
    
    Note: This is a simplified version that doesn't use LangChain.
    To use the full LLM-powered agent with LangChain:
    1. Install compatible LangChain version
    2. Set OPENAI_API_KEY in .env
    
    For now, use the individual API endpoints:
    - POST /jobs/scrape - Scrape jobs
    - GET /jobs - List jobs
    - POST /jobs/{id}/analyze - Analyze a job
    - POST /match-score - Calculate match score
    - POST /cover-letter/generate - Generate cover letter
    - GET /dashboard/stats - Get metrics
    """
    class MockAgentExecutor:
        def invoke(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
            instruction = input_dict.get("input", "")
            
            response = f"""Mock Agent Response
            
Received instruction: {instruction}

The autonomous agent is currently in mock mode. To enable full LLM-powered functionality:

1. Install compatible LangChain: pip install langchain==0.1.0 langchain-openai
2.  Add your OpenAI API key to .env: OPENAI_API_KEY=sk-...

Current Features Available (via REST API):
✅  Job Scraping: POST /jobs/scrape
✅ Job Listing: GET /jobs
✅ Job Analysis: POST /jobs/{{id}}/analyze
✅ Match Scoring: POST /match-score  
✅ Cover Letter Generation: POST /cover-letter/generate
✅ Project Search: POST /projects/search
✅ Dashboard Analytics: GET /dashboard/stats

Example workflow without agent:
1. Scrape jobs: POST /jobs/scrape
2. List jobs: GET /jobs
3. For each job:
   - Analyze: POST /jobs/{{id}}/analyze
   - Calculate match: POST /match-score
   - If match >= 70: POST /cover-letter/generate

All endpoints are fully functional and can be used independently!
"""
            
            return {"output": response}
    
    return MockAgentExecutor()
