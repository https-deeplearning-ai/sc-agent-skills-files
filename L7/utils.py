from claude_agent_sdk import ( AssistantMessage, TextBlock, ToolUseBlock,
)

def truncate(value, max_length=200):
    """Truncate a value for display."""
    text = str(value)
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def format_input(input_dict, max_length=200):
    """Format tool input for readable display."""
    if not input_dict:
        return "{}"
    parts = []
    for key, value in input_dict.items():
        val_str = str(value)
        if len(val_str) > 50:
            val_str = val_str[:50] + "..."
        parts.append(f"{key}={val_str}")
    result = ", ".join(parts)
    return truncate(result, max_length)

# Track subagent names by their tool_use_id
subagent_registry = {}

def display_message(message: AssistantMessage):
    # Determine source agent
    parent_id = getattr(message, 'parent_tool_use_id', None)
    if parent_id:
        subagent_name = subagent_registry.get(parent_id, 'unknown')
        agent_label = f"\033[35m[Subagent {subagent_name}]\033[0m"
    else:
        agent_label = "\033[36m[Main]\033[0m"

    for block in message.content:
        if isinstance(block, ToolUseBlock):
            if block.name == 'Task':
                subagent_type = block.input.get('subagent_type', 'unknown')
                description = block.input.get('description', '')
                # Register this subagent with its tool_use_id
                tool_id = getattr(block, 'id', None)
                if tool_id:
                    subagent_registry[tool_id] = subagent_type
                print(f"{agent_label} 🚀 Spawning subagent: \033[1m{subagent_type}\033[0m")
                if description:
                    print(f"   Description: {description}")
            else:
                tool_id = getattr(block, 'id', 'unknown')[:8]
                print(f"{agent_label} 🔧 \033[1m{block.name}\033[0m (id: {tool_id})")
                print(f"   Input: {format_input(block.input)}")

        elif isinstance(block, TextBlock):
            print(f"\033[1mClaude\033[0m: {block.text}\n")