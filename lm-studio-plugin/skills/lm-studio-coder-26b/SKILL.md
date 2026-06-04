---
name: lm-studio-coder-26b
description: >-
  Query local google/gemma-4-26b-a4b for code generation tasks. Enforces writing directly to files. Automatically JIT loads the model if necessary.
---

# LM Studio Coder 26B Skill

## Overview
This skill allows agents to use the local `google/gemma-4-26b-a4b` model for complex code generation, refactoring, and code analysis. It interacts with the local server running at `http://localhost:1234/v1`.

## Cost and Token Saving Workflows (MANDATORY)
When using this skill to generate or refactor code, you MUST optimize for context efficiency:
- **Direct-to-File:** Use the `--code-only` flag and specify the target file as the `--output`. **DO NOT** read the resulting file back into your own context unless validation fails. The script automatically strips markdown formatting.
- **Provide Context Efficiently:** When modifying an existing file, use `@filename` to pass it directly to the model as part of the prompt without polluting your own chat context.

## How to Query
Use the provided `lm_studio_cli.py` script.

**Path:** `~/.gemini/config/plugins/lm-studio-plugin/scripts/lm_studio_cli.py`

**Arguments:**
- `--prompt` (required): The instruction for the model. Use `@file.txt` to include a file's content.
- `--output` (required): The file path where the generated code should be saved.
- `--model` (MANDATORY): You must specify `--model google/gemma-4-26b-a4b`
- `--code-only` (required for code generation): Strips markdown blocks to output raw text.
- `--system` (optional): System prompt for the generation task.

**Example Usage:**

Generate a Python script directly to a file:
```bash
python3 ~/.gemini/config/plugins/lm-studio-plugin/scripts/lm_studio_cli.py query --model google/gemma-4-26b-a4b --code-only --prompt "Write a Python script to parse JSON." --output src/parser.py
```
