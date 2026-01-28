# Skills vs Tools, MCP, and Subagents

## Summary of the Slides

### Skills vs MCP

| Feature | MCP | Skills |
|--------|-----|--------|
| **Purpose** | Connects your agent to external systems and data (databases, APIs, services) | Teaches your agent what to do with that data |
| **Example** | MCP server connects to a database | Skill says "Compute metric X using columns A and B of this table" |

MCP provides *access*, Skills provide *expertise*.


### Skills vs Tools

| Feature | Tools | Skills |
|--------|-------|--------|
| **Purpose** | Provide agents with essential capabilities to accomplish tasks | Extend agent's capabilities with specialized knowledge |
| **Context** | Tool definitions (name, description, parameters) always live in the context window | Skills are loaded dynamically as needed |
| **Flexibility** | Fixed set of capabilities | Skills can include scripts as tools that are used when needed ("tools on demand") |



### Skills vs Subagents

| Feature | Subagents | Skills |
|--------|-----------|--------|
| **Purpose** | Have their own isolated context and tool permissions | Provide expertise knowledge to the main agent or any of its subagents |
| **Operation** | Agent delegates a task to the specialized subagent, which works independently (and maybe in parallel) and returns results | Skills inform how work should be done |
| **Example** | Code Reviewer subagent | Language- or framework-specific best practices skill |

Skills can enhance both the main agent AND its subagents with specialized knowledge.



### Putting Everything Together

**Example: Customer Insight Analyzer**

| Component | Role |
|-----------|------|
| **Skill** | A guide for how to categorize feedback and how to summarize findings |
| **MCP Server** | Google Drive MCP server accessing a Drive folder containing customer interview notes and survey responses|
| **Subagents** | Interview Analyzer, Survey Analyzer |





## References
* [Skills Explained](https://www.claude.com/blog/skills-explained)
* [Teach Claude your Way of Working using Skills](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills)