# Usage Guide

This plugin introduces **Just-in-Time (JIT) Model Loading** and four specialized skills tailored for specific development tasks.

## Just-in-Time (JIT) Model Loading

LM Studio models require significant VRAM. Loading multiple massive models at the same time is usually impossible on consumer hardware.

To solve this, the core `lm_studio_cli.py` script acts as a smart traffic controller:
1. When you trigger a skill (e.g., `/lm-studio-coder-26b`), the script first runs `lms ps --json` to check what is currently loaded in memory.
2. If the `26b` model is already loaded, it proceeds immediately to query the API.
3. If a different model (e.g., the `12b` model) is loaded, the script gracefully unloads all models using `lms unload --all` to free up VRAM.
4. It then automatically loads the required model using `lms load <model_key> --yes` before executing your prompt.

This allows your agent to seamlessly switch between small, fast models and massive, high-accuracy models on-the-fly, without any manual intervention from you.

## The Specialized Skills

The plugin ships with four distinct skills, each mapped to a specific model and workflow strategy:

### 1. `lm-studio-coder-12b`
- **Model:** `google/gemma-4-12b` (or your preferred 12B equivalent)
- **Workflow:** **Code-Only**. This skill utilizes the `--code-only` flag.
- **Use Case:** Best for rapid code generation tasks where speed is critical. It strips all conversational markdown and outputs raw code directly to the destination file.

### 2. `lm-studio-chat-12b`
- **Model:** `google/gemma-4-12b`
- **Workflow:** **Diagnostic Funnel**. 
- **Use Case:** Best for general reasoning, log analysis, and architectural Q&A. You can pass large log files using the `@/path/to/file` syntax to keep the main agent context window clean.

### 3. `lm-studio-coder-26b`
- **Model:** `google/gemma-4-26b-a4b` (or your preferred 26B+ equivalent)
- **Workflow:** **Code-Only**. This skill utilizes the `--code-only` flag.
- **Use Case:** Best for complex refactoring, writing dense boilerplate, or solving complicated algorithmic tasks where a larger parameter count is required.

### 4. `lm-studio-chat-26b`
- **Model:** `google/gemma-4-26b-a4b`
- **Workflow:** **Diagnostic Funnel**. 
- **Use Case:** Best for deep debugging of massive, confusing error logs where a smaller model might hallucinate or miss the core issue.

## How to Trigger Skills

Simply ask your Antigravity agent to use the specific skill by name:
> *"Use the `/lm-studio-coder-26b` skill to rewrite `server.js` to use Fastify instead of Express."*

Or:
> *"Run the build script, and if it fails, send the log to `/lm-studio-chat-12b` to diagnose the error."*
