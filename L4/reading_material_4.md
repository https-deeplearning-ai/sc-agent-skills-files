# Creating Custom Skills 

## Links to Custom Skills
- <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L4/custom_skills/analyzing-time-series/" target="_blank">analyzing time series</a>
- <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L4/custom_skills/generating-practice-questions/" target="_blank">generating practice questions</a>

## References
For a complete list of Skills creation best practices and specification, make sure to check out:
- <a href="https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices" target="_blank">Skill authoring best practices</a>
- <a href="https://agentskills.io/specification" target="_blank">Specification</a>
- <a href="https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf?hsLang=en" target="_blank">The Complete Guide
to Building Skills for Claude</a>

## How to Disable Plugins in Claude Code?

Plugins are designed to toggle on and off as needed. You can enable them when you need specific capabilities and disable them when you don't to reduce system prompt context and complexity. 

- Using the `/plugin` Command: navigate to `installed` tab, then select the plugin you want to disable.
- Using the command line:
`claude plugin disable <plugin-name>`


## Summary of the Slides

### SKILL.md File Structure

A skill file has two main parts:
1. **YAML Frontmatter** — Metadata at the top
2. **Body Content** — Markdown instructions below

### Frontmatter Required Fields

| Field | Constraints |
|-------|-------------|
| **name** | Max 64 chars; lowercase letters, numbers, and hyphens only; must not start/end with hyphens; must match parent directory name; recommended: gerund (verb+-ing) form |
| **description** | Max 1024 chars; non-empty; should describe what the skill does AND when to use it; include specific keywords to help agents identify relevant tasks |

### Frontmatter Optional Fields

| Field | Constraints |
|-------|-------------|
| **license** | License name or reference to a license file |
| **compatibility** | Max 500 chars; indicates environment requirements |
| **metadata** | Arbitrary key-value pairs (e.g., author, version) |
| **allowed-tools** | Space-delimited list of pre-approved tools (Experimental) |


### Body Content

**No format restrictions**, but here are some recommendations:

#### Recommended Sections
- Step-by-step instructions
- Input Format / Output Format / Examples
- Common edge cases

#### Practical Guidance
- Keep it **under 500 lines**
- Move detailed reference material to separate files (show basic content, link to advanced content)
- Keep references **one level deep** from SKILL.md (avoid nested file references)
- Be clear and concise, use consistent terminology
- Use forward slashes in file paths, even on Windows

#### Degrees of Freedom

| Level | Description |
|-------|-------------|
| **High freedom** | General text-based directions; multiple approaches are valid |
| **Medium freedom** | Instructions contain customizable pseudocode, code examples, or patterns; a preferred pattern exists but some variation is acceptable |
| **Low freedom** | Instructions refer to specific scripts; a specific sequence must be followed |

#### Complex Workflows
- Break complex operations into clear, sequential steps
- If workflows become large with many steps, consider pushing them into separate files

### Optional Directories

#### `/assets`
- **Templates:** document templates, configuration templates
- **Images:** diagrams, logos
- **Data files:** lookup tables, schemas

#### `/references`
- Contains additional documentation that agents can read when needed
- Keep individual reference files focused
- **Note:** For reference files longer than 100 lines, include a table of contents at the top so the agent can see the full scope

#### `/scripts`
- Clearly document dependencies
- Scripts should have clear documentation
- Error handling should be explicit and helpful
- **Note:** Make clear in your instructions whether Claude should execute the script or read it as reference


### Evaluation

#### Unit Tests

Define test cases with:
- **skills**: Which skills to test
- **queries**: Test prompts to run
- **files**: Input files to use
- **expected_behavior**: What success looks like

#### Example Test Case
```json
{
  "skills": ["generating-practice-questions"],
  "queries": [
    "Generate practice questions from this lecture note and save it to output.md",
    "Generate practice questions from this lecture note and save it to output.tex",
    "Generate practice questions from this lecture note and save it to output.pdf"
  ],
  "files": ["test-files/notes.pdf", "test-files/notes.tex", "test-files/notes.pdf"],
  "expected_behavior": [
    "Successfully reads and extracts the input file. For pdf input, uses pdfplumber.",
    "Successfully extracts all the learning objectives.",
    "Generates the 4 types of questions.",
    "Follows the guidelines for each question.",
    "Uses the output structure and the correct output templates.",
    "The latex output successfully compiles.",
    "Saves the generated questions to a file named output."
  ]
}
```
**Additional Evaluation Tips**:

- Get **human feedback**
- Test with **all the models** you plan to use
