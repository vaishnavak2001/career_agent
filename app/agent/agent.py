from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.core.config import settings
from app.agent.tools import tools

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0,
    api_key=settings.OPENAI_API_KEY
)

# Define the agent prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an Autonomous AI Job Application Agent. Your goal is to help the user find and apply for jobs.\n"
            "You have access to tools for scraping jobs, detecting scams, parsing descriptions, and scoring matches.\n"
            "Always respect robots.txt and ethical guidelines.\n"
            "When asked to find jobs, use the scrape_jobs tool, then filter them using detect_scam and deduplicate_job.\n"
            "For each valid job, parse the JD and compute a match score."
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Create the agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Create the executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def get_agent_executor():
    return agent_executor
