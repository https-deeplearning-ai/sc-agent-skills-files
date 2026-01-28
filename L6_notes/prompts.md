# Prompts

- Add a new CLI  edit command to allow users edit the title or priority of the task. For example: edit task 3 --title "New title". If users do not provide any options, then do not edit anything and exit with a message "no edits were done, specify title or priority". If edits are done, display the table of tasks. Make sure to follow the conventions for creating a new CLI command.

- Use the code-reviewer subagent to review the @edit.py command

- Use the test-generator-runner subagent to generate tests for the @edit.py command

- Use the code-reviewer subagent to review the @clear.py command. Fix any issues and then use the test-generator-runner subagent to generate tests for the @clear.py command. 