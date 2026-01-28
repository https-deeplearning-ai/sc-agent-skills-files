# Skills with the Claude API

## Lesson Files

You can find the lesson's notebook and all the required input files [here](.).
To run the notebook, you need to create a `.env` file containing an Anthropic API key (no Claude subscription is required):

`ANTHROPIC_API_KEY="your-key"`

You can get a key from [Claude Developer Platform](https://platform.claude.com/dashboard). 

If you choose not to run the notebook, this [notebook](lesson_5.ipynb) displays the cell outputs (as shown in the video). And you can find the generated outputs [here](sample_outputs/).

## Notes
- Here's the [list of pre-installed libraries in the sandboxed environment](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#pre-installed-libraries)
- Streaming: The lesson's notebook does not implement streaming with the Messages API. So when you run the cells to get the response, you might need to wait for a few minutes. If you'd like to implement streaming, you can check the documentation [here](https://platform.claude.com/docs/en/build-with-claude/streaming).
- To see more examples of how to use Agent Skills with the API (like multi-turn conversation), make sure to check this [guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide).

## Additional References
- To learn more about the code execution tool, check [here](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)
- [Files API](https://platform.claude.com/docs/en/build-with-claude/files)
- [Claude Cookbook: Skills](https://github.com/anthropics/claude-cookbooks/tree/main/skills)