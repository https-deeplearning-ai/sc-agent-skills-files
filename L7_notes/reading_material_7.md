# Skills with the Claude Agent SDK

## Lesson's Files

You can find all the files for L7 [here](../L7). Here are some highlighted files:
- [System prompts for the main agent and subagents](../L7/prompts)
- [Files for the `learning-a-tool` skill](../L7/.claude/skills/learning-a-tool/)
- [utils.py](../L7/utils.py) (message formatting)
- [agent.py](../L7/agent.py)
- [The learning guide generated during filming](reading_material_7.md)

To run the agent, follow the instructions in the [README file](../L7/README.md).

### Prompts Used in the Lesson

- `Help me get started with MinerU. Create a learning guide. Show me your plan first.`

    - **Note**: The agent might take around 15 minutes to finish. You can always update the skill's instructions and agent definitions if you want the research to be faster or the learning guide to be simpler. You can also try running the subagents with Haiku.

- For the MCP part (which you can skip if you wish):

    `Write ./learning-mineru/resources.md to the "Resources" subpage under Learning in Notion. The subpage already exists. Use rich formatting. For Notion MCP: You can use the full range of Notion block types for proper formatting.`
   
   In the Notion account we used in the lesson, we created a page called `Learning` and added a subpage called `Resources`.

## More Advanced Options

- [Advanced Permission Control](https://platform.claude.com/docs/en/agent-sdk/python#example-advanced-permission-control)
- [Building a Continuous Conversation Interface (interrupt, new conversation, exit)](https://platform.claude.com/docs/en/agent-sdk/python#building-a-continuous-conversation-interface)


## References

- [Claude Agent SDK Documentation](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Python Agent SDK](https://platform.claude.com/docs/en/agent-sdk/python)
- [Agent Skills in the SDK](https://platform.claude.com/docs/en/agent-sdk/skills)
- [Claude Agent SDK Demos](https://github.com/anthropics/claude-agent-sdk-demos)