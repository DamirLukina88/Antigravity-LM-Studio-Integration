---
name: lm-studio-chat-26b
description: >-
  Query local google/gemma-4-26b-a4b for reasoning, general chat, summarization, and log diagnosis. Automatically JIT loads the model if necessary.
---

# LM Studio Chat 26B Skill

## Overview
This skill allows agents to use the local `google/gemma-4-26b-a4b` model for complex text generation, reasoning, and summarizing large logs. It interacts with the local server running at `http://localhost:1234/v1`.

## Diagnostic Funneling Workflow
When you need to analyze a large error log, documentation file, or terminal output:
1. Save the target text to a file (e.g. `/tmp/error.log`).
2. Pass the file directly to the LM Studio script using `@filename` so it acts as the context.
3. Instruct the LM to output ONLY the specific diagnostic information (e.g., "Respond with only the line number and the fix"). 
4. Read the concise output. **Do not dump large logs into your own chat context!**

## How to Query
Use the provided `lm_studio_cli.py` script.

**Path:** `~/.gemini/config/plugins/lm-studio-plugin/scripts/lm_studio_cli.py`

**Arguments:**
- `--prompt` (required): The prompt or query for the model. Use `@filepath` to attach large texts/logs instead of pasting them in the prompt string.
- `--output` (required): The file path where the response will be saved.
- `--model` (MANDATORY): You must specify `--model google/gemma-4-26b-a4b`
- `--system` (optional): System prompt.
- `--temperature` (optional): Set generation temperature (default 0.7).

**Example Usage:**

Log Diagnosis (Diagnostic Funnel):
```bash
python3 ~/.gemini/config/plugins/lm-studio-plugin/scripts/lm_studio_cli.py query --model google/gemma-4-26b-a4b --prompt "Identify the root cause of the error in this log and provide a 1 sentence fix: @/tmp/server.log" --output /tmp/diagnosis.txt
```
