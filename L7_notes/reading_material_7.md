# Skills with the Claude Agent SDK

## Lesson Files

You can find all the files for L7 <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7" target="_blank">here</a>, with a few variations from what's shown in the video:
- Used `haiku` as the model for each subagent
- Specified the exact list of MCP tools to use

Here are some key files to explore:
- <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7/prompts" target="_blank">System prompts for the main agent and subagents</a>
- <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7/.claude/skills/learning-a-tool/" target="_blank">Files for the `learning-a-tool` skill</a>
- <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7/utils.py" target="_blank">utils.py</a> (message formatting)
- <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7/agent.py" target="_blank">agent.py</a>
- <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7_notes/learning-mineru/" target="_blank">The learning guide generated during filming</a>

To run the agent, follow the instructions in the <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7/README.md" target="_blank">README file</a>. You'll need an Anthropic API key (no subscription required).

**About costs:** Running the agent with the same requests costs approximately &#36;3.43 in API credits if you use `haiku` as the subagent model (and using `sonnet` with the main agent), or &#36;6.35 if you use `sonnet` with the subagents.

### Prompts Used in the Lesson

**Step 1:** Start the research process
```
Help me get started with MinerU. Create a learning guide. Show me your plan first.
```

**Note:** The agent might take around 15 minutes to complete. You can always update the skill's instructions and agent definitions if you want faster research or a simpler learning guide.

**Step 2:** Review and approve the plan

You can agree with the plan or provide your feedback and suggestions.

**Step 3 (Optional):** Export to Notion

If you'd like to try the MCP integration with Notion:
```
Write ./learning-mineru/resources.md to the "Resources" subpage under Learning in Notion. The subpage already exists. Use rich formatting. For Notion MCP: You can use the full range of Notion block types for proper formatting.
```

**Note:** In the Notion account used in the lesson, we created a page called `Learning` with a subpage called `Resources`.

## More Advanced Options

- <a href="https://platform.claude.com/docs/en/agent-sdk/python#example-advanced-permission-control" target="_blank">Advanced Permission Control</a>
- <a href="https://platform.claude.com/docs/en/agent-sdk/python#building-a-continuous-conversation-interface" target="_blank">Building a Continuous Conversation Interface</a> (interrupt, new conversation, exit)

## References

- <a href="https://platform.claude.com/docs/en/agent-sdk/overview" target="_blank">Claude Agent SDK Documentation</a>
- <a href="https://platform.claude.com/docs/en/agent-sdk/python" target="_blank">Python Agent SDK</a>
- <a href="https://platform.claude.com/docs/en/agent-sdk/skills" target="_blank">Agent Skills in the SDK</a>
- <a href="https://github.com/anthropics/claude-agent-sdk-demos" target="_blank">Claude Agent SDK Demos</a>