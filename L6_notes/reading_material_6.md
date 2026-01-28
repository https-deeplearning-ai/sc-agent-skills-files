# Skills with Claude Code

## Lesson's Codebase and Files

Links to the lesson's files:
- [Codebase used in the lesson](../L6) 
- [Files of the lesson's skills](../L6/.claude/skills/)
- [Subagent Definitions](../L6/.claude/agents)
- [Prompts used in the conversation](prompts.md)
- [clear.py](clear.py)

When you run the application for the first time in the terminal:
- Start with `uv sync`
- Activate the virtual environment: `source .venv/bin/activate`
- Try the following commands:
   - `task –help`
   - `task add "write the final report" -p high -d 2025-01-15`
   - `task list`
   - `task done 1`
   - `task list -a`

This is a starter codebase for a todo CLI app. In the lesson, we demonstrated how to add edit and clear commands. You can also extend the app by adding delete and undo commands, or by changing the underlying logic for how tasks are stored and displayed.

## Claude Code

If this is your first time trying Claude Code, you can check out these courses:
- [Claude Code: A Highly Agentic Coding Assistant](https://www.deeplearning.ai/short-courses/claude-code-a-highly-agentic-coding-assistant/) 
- [Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action)

If you've completed any of these courses and would like to see an advanced course on Claude Code, please leave us feedback on what topics you'd like us to cover.

## Skills with Claude Code

In the lesson, you saw how to add skills at the project level. Here's a [list](https://code.claude.com/docs/en/skills#where-skills-live) of other locations where your skills can live.

### What additional fields can you add to the frontmatter?

In addition to `name` and `description`, you can add several other fields to your skills when working in Claude Code, such as `allowed-tools`, `model`, `disable-model-invocation`, `user-invocable`, `argument-hint`, `context`, and `agent`. Most of these fields were added after we filmed the course, which is why we didn't have the chance to cover them in the video. You can find a description of each field in the documentation [here](https://code.claude.com/docs/en/skills#frontmatter-reference).

### Skills Invocation in Claude Code

Any skill in Claude Code can be model-invoked (as demonstrated in this lesson) or user-invoked. For example, if you want to invoke the skill `adding-cli-command`, you can type `/adding-cli-command` and then describe what command to add. The fields `disable-model-invocation` and `user-invocable` allow you to further control this behavior, as explained [here](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill).

### Skills and Slash Commands Have Been Merged

Before Skills were introduced, Claude Code had a feature called slash commands. This feature allowed you to create custom commands by describing them in a markdown file saved in a `commands` folder under `.claude`.

As of January 23, custom slash commands have been merged into skills. This merger occurred because a file at `.claude/commands/review.md` and a skill at `.claude/skills/review/SKILL.md` both create the `/review` command and work the same way. However, skills offer additional optional features: a dedicated directory for supporting files that can be referenced in the `SKILL.md`, and frontmatter options to control whether you or Claude invokes them.

### Subagents and Skills

In the lesson, you saw how to create custom subagents. Claude Code also includes built-in subagents like `Explore`, `Plan`, and `General-Purpose` ([Built-in subagents](https://code.claude.com/docs/en/sub-agents#built-in-subagents)).

There are two approaches for using skills with subagents:

- **Approach 1**: Define a custom subagent that uses skills (as shown in the lesson)

    When you create a subagent, you can use the `skills` field to inject skill content into the subagent's context at startup. Since subagents don't inherit skills from the parent conversation, you must list the skills explicitly. The full content of the `SKILL.md` file is injected into the subagent's context when the subagent is invoked.

    Definition of the `code-reviewer` subagent:
    ```
    ---
    name: code-reviewer
    description: "Reviews code for quality, security, and convention compliance. Use when user asks to review, check, or verify code"
    tools: Bash, Glob, Grep, Read
    model: inherit
    color: purple
    skills: reviewing-cli-command
    ---
    ```

    In this case, the `reviewing-cli-command` skill is available to both your main agent and the subagent. The skill can be loaded into the context of the main agent when needed, or it can guide the `code-reviewer` subagent when the subagent is invoked.

    You can also list more than one skill for your `code-reviewer` subagent. For example, you can add another skill for reviewing CLI commands written in a different language or framework. You can also add a skill for reviewing SQL queries (if you want the app's tasks to be stored in a database instead of a local JSON file).

- **Approach 2**: Run skills in a subagent (not shown in the lesson)

    If you want a skill to always run in an isolated context, you need to use the field `context: fork` in the skill's frontmatter. When the skill runs, by default, the built-in `general-purpose` subagent receives the skill content as its prompt or task, runs as instructed by the skill in an isolated context, and then returns the results. If you want a specific subagent (built-in or custom) to be used with the skill, you need to specify the `agent` field in the skill's frontmatter.

    For example, here's a sample `SKILL.md` file:
    ```
    ---
    name: deep-research
    description: Research a topic thoroughly
    context: fork
    agent: Explore
    ---

    Research $ARGUMENTS thoroughly:

    1. Find relevant files using Glob and Grep
    2. Read and analyze the code
    3. Summarize findings with specific file references
    ```

    Reference: [Run Skills in a subagent](https://code.claude.com/docs/en/skills#run-skills-in-a-subagent)


## References

- For a more comprehensive guide on how to use Skills with Claude Code, please check out this [documentation](https://code.claude.com/docs/en/skills#run-skills-in-a-subagent).

- To learn more about subagents in Claude Code, check out this [guide](https://code.claude.com/docs/en/sub-agents).