# Why Agent Skills? - Part II

## Summary of the Slides

### What Are Agent Skills?

Agent Skills are a lightweight, open format for extending AI agent capabilities. A skill is a folder of organized files consisting of instructions, scripts, assets, and resources that agents can discover to perform specific tasks accurately.

### How We Used to Think About Agents

- Specialized agents: Research Agent, Coding Agent, Finance Agent, Marketing Agent
- Each with their own narrow focus, their own scaffolding, and specific tools

### The New Paradigm

- **General-purpose agents** use code as the universal interface
- Simple scaffolding: bash and filesystem
- But they need **context and domain expertise** to do the job reliably
- Skills provide procedural knowledge and company/team/user-specific context that agents can load on demand

### What Skills Enable

| Category | Examples |
|----------|----------|
| **Domain Expertise** | Brand guidelines and templates, legal review processes, data analysis methodologies |
| **Repeatable Workflows** | Weekly marketing campaign review, customer call prep workflow, quarterly business review |
| **New Capabilities** | Creating presentations, generating Excel sheets or PDF reports, building MCP servers |

### Without Skills

- Describe your instructions and requirements every time
- Bundle all your references and supporting files every time
- Manually ensure the workflow or outputs are always consistent

### Key Characteristics of Skills

1. **Portable:** You can reuse the same skill across different skills-compatible agents:
    - Claude Code
    - Claude.ai
    - Claude Agent SDK
    - Claude API

    Agent Skills are now an **open standard**, adopted by a growing number of agent products.

2. **Composable:** Skills can be combined to build complex workflows. For example:
    - **Company brand skill**: Provides brand guidelines (fonts, colors, logos)
    - **PowerPoint skill**: Creates slide decks
    - **BigQuery skill**: Provides marketing-related schema
    - **Marketing campaign analysis skill**: Analyzes marketing data

### How Do Skills Work? - Progressive Disclosure

Skills can contain a lot of information, and you may have hundreds of them. To protect the context window, skills are **progressively disclosed**:

| Layer | When Loaded |
|-------|-------------|
| **Metadata** (YAML frontmatter: name, description) | Always loaded |
| **Instructions** (main SKILL.md content) | Loaded when triggered |
| **Resources** (reference files, scripts) | Loaded as needed |

### Skill Structure Examples

According to the Agent Skills Specification:
- SKILL.md is required
- Optional directories: references, scripts, and assets

Since some skills were developed before Agent Skills became an open standard, you will see that some skills (like the PDF skill below) do not strictly follow the standard format.
```
analyzing-marketing-campaign/
├── SKILL.md
└── references/
    └── budget_reallocation_rules.md
```
```
pdf/
├── SKILL.md
├── forms.md
├── reference.md
└── scripts/
    ├── check_fillable_fields.py
    ├── convert_pdf_to_images.py
    ├── extract_form_field_info.py
    └── fill_pdf_form_with_annotations.py
```
```
designing-newsletters/
├── SKILL.md
├── references/
│   └── style-guide.md
└── assets/
    ├── header.png
    ├── icons/
    └── templates/
        ├── newsletter.html
        └── layout.docx
```

## References

- [What are Skills?](https://agentskills.io/what-are-skills)
- [How Skills Work](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)
- [Barry Zhang & Mahesh Murag Talk at the AI Engineer's Fair](https://www.youtube.com/watch?v=CEvIs9y1uog)