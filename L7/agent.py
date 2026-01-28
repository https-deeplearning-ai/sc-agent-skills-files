import asyncio
import os
from dotenv import load_dotenv
from claude_agent_sdk import ( 
    AgentDefinition, ClaudeSDKClient, ClaudeAgentOptions,AssistantMessage,
)
from utils import display_message

load_dotenv()
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")

PROMPTS_DIR = "prompts"

def load_prompt(filename: str) -> str:
    """Load a prompt from the prompts directory."""
    prompt_path = f"{PROMPTS_DIR}/{filename}"
    with open(prompt_path, "r") as f:
        return f.read().strip()

async def main():

    main_agent_prompt = load_prompt("main_agent.md")
    docs_researcher_prompt = load_prompt("docs_researcher.md")
    repo_analyzer_prompt = load_prompt("repo_analyzer.md")
    web_researcher_prompt = load_prompt("web_researcher.md")

    agents = {
        "docs_researcher" : AgentDefinition(
            description="Finds and extracts information from official documentation sources.",
            prompt = docs_researcher_prompt,
            tools = ["WebSearch", "WebFetch"],
            model = "sonnet"
        ),
        "repo_analyzer" : AgentDefinition(
            description="Analyzes code repositories for structure, examples, and implementation details.",
            prompt = repo_analyzer_prompt,
            tools = ["WebSearch","Bash"],
            model = "sonnet"
        ),
        "web_researcher" : AgentDefinition(
            description="Finds articles, videos, and community content.",
            prompt = web_researcher_prompt,
            tools = ["WebSearch", "WebFetch"],
            model = "sonnet"
        ),
    }


    # mcp, tools, subagents
    options = ClaudeAgentOptions(
        system_prompt=main_agent_prompt,
        setting_sources=["user", "project"],
        mcp_servers={
            "notion": {
                "command": "npx",
                "args": ["-y", "@notionhq/notion-mcp-server"],
                "env": {
                    "NOTION_TOKEN": NOTION_TOKEN,
                },
            }
        },
        allowed_tools=["Skill", "Task", "Write", "Bash", "WebSearch", "WebFetch", "mcp__notion__*"], # read-only tools like read, Grep, Glob are allowed by default
        model="sonnet",
        agents=agents
    )

    async with ClaudeSDKClient(options=options) as client:
        print("Starting conversation session.")
        print("Type 'exit' to quit\n") 
        # First question
        while True:
            user_input = input('\033[1m' + 'You' + '\033[0m'+': ')
            print('')
            if user_input.lower() == 'exit':
                break
            await client.query(user_input)
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    display_message(message)

asyncio.run(main())