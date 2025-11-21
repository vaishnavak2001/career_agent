from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.tools import job_tools, resume_tools, apply_tools
from app.config import settings

# 1. Define Tools
tools = [
    job_tools.scrape_jobs,
    job_tools.detect_scam,
    job_tools.parse_jd,
    job_tools.compute_match_score,
    resume_tools.rewrite_resume,
    resume_tools.add_projects_to_resume,
    resume_tools.generate_cover_letter,
    apply_tools.submit_application
]

# 2. Initialize LLM
# Fallback to a mock if no key provided, to prevent crash on startup
if settings.OPENAI_API_KEY:
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0, api_key=settings.OPENAI_API_KEY)
else:
    # This is just a placeholder to allow import; execution will fail if called without key
    print("WARNING: OPENAI_API_KEY not found. Agent will not function correctly.")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key="sk-mock")

# 3. Create Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an Autonomous Career Agent. Your goal is to find, analyze, and apply to jobs. "
               "Use the available tools to scrape jobs, detect scams, tailor resumes, and submit applications. "
               "Always check for scams before applying."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 4. Create Agent
agent = create_openai_tools_agent(llm, tools, prompt)

# 5. Create Executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def get_agent_executor():
    return agent_executor
