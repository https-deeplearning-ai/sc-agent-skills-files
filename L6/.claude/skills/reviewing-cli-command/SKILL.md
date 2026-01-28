---
name: reviewing-cli-command
description: Provides checklist for reviewing Typer CLI command implementations. Covers structure, Annotated syntax, error handling, exit codes, display module usage, destructive action patterns, and help text conventions. Use when user asks to review/check/verify a CLI command, wants feedback on implementation, or asks if a command follows best practices.
---

# Reviewing CLI Commands

Checklist for reviewing Typer CLI command implementations.

## Review Process

1. Read the command file
2. Check each section below
3. Report findings using output format at bottom

## Structure

- [ ] File in `src/<cli_app>/commands/`
- [ ] Has `app = typer.Typer()` and `@app.command()`
- [ ] Command groups use `@app.command()` for each subcommand
- [ ] Registered in `commands/__init__.py` with `add_typer()`
- [ ] Single commands: `add_typer(app)` without name
- [ ] Command groups: `add_typer(app, name="group")`

## Arguments & Options

- [ ] Uses `Annotated` syntax
- [ ] Arguments for required positional input
- [ ] Options for optional named parameters
- [ ] Short flags where appropriate (`-f`, `-q`)
- [ ] Help text: lowercase, no period, brief

```python
# GOOD:
name: Annotated[str, typer.Argument(help="item name")]
force: Annotated[bool, typer.Option("--force", "-f", help="skip confirmation")] = False

# BAD:
name: str = typer.Argument(..., help="The name of the item.")
```

## Error Handling

- [ ] Validates input before processing
- [ ] Exit codes: 0=success, 1=error, 2=invalid input
- [ ] Errors via `display.error()`
- [ ] Uses `raise typer.Exit(code)` after errors
- [ ] Uses `raise typer.Abort()` for cancellation

```python
# GOOD:
if id < 1:
    display.error("ID must be positive")
    raise typer.Exit(EXIT_INVALID_INPUT)

# BAD:
if id < 1:
    print("Error: ID must be positive")
    return
```

## Output

- [ ] All output through `display` module
- [ ] No `print()`, `typer.echo()`, or `console.print()`

```python
# GOOD:
display.success(f"Added '{task.title}'")

# BAD:
print(f"Added '{task.title}'")
```

## Destructive Actions

- [ ] Has `--force` / `-f` flag
- [ ] `typer.confirm()` with `default=False`
- [ ] Shows "Cancelled" on abort

```python
# GOOD:
if not force:
    confirm = typer.confirm(f"Delete '{task.title}'?", default=False)
    if not confirm:
        display.info("Cancelled")
        raise typer.Abort()

# BAD: defaults to Yes
confirm = typer.confirm(f"Delete?", default=True)
```

## Help Text

- [ ] Docstring exists
- [ ] Imperative mood ("Add a task" not "Adds a task")
- [ ] First line < 60 characters

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `print()` | `display.success/error/warning/info()` |
| Wrong exit code | 0=success, 1=error, 2=invalid |
| Missing `--force` on delete | Add force option with default False |
| Confirmation defaults Yes | `default=False` in `typer.confirm()` |
| Old Typer syntax | `Annotated[type, typer.Argument()]` |
| Missing `app = typer.Typer()` | Each command file needs its own app |
| Not registered | `add_typer(app)` in `commands/__init__.py` |

## Review Output Format

```
## Review: <command_name>

[OK] Uses Annotated syntax
[OK] Has docstring in imperative mood
[X] Missing --force flag on destructive command
[X] Uses print() instead of display module
[!] Help text could be shorter

### Summary
<brief summary of issues found>

### Suggested Fixes
<code suggestions if needed>
```
