# Cost and Context Optimization

When building complex software with autonomous agents, context windows can become polluted quickly, leading to degraded performance and massive API costs (if using cloud orchestrators like Gemini).

This integration leverages two unique workflows to ensure your Antigravity agent remains cheap to operate and highly focused.

## 1. Direct-to-File Code Generation (The `--code-only` flag)

Local inference speeds are heavily bottlenecked by output token generation. An LLM that spends 100 tokens writing "Here is the code you requested..." is wasting both time and context space.

The `coder` skills (`lm-studio-coder-12b`, `lm-studio-coder-26b`) enforce a strict system prompt requiring the model to output **only raw, executable code**. 

Furthermore, Antigravity executes the Python CLI wrapper, which writes the local model's output *directly to the target file on disk*.

**The Result:** The primary Antigravity agent never actually "reads" the generated code into its conversation history. It simply orchestrates the local model, verifying the result via terminal tests. This saves thousands of tokens per file modification.

## 2. The Diagnostic Funnel (The `@filename` syntax)

Imagine running a complex build pipeline that fails, producing a 3,000-line error log.

If you paste that error log directly into the Antigravity UI, those 3,000 lines become a permanent part of your chat history. Every subsequent question you ask the agent will re-process those 3,000 lines, polluting the context window and driving up costs.

The `chat` skills solve this using a **Diagnostic Funnel**.

The CLI wrapper supports inline file ingestion. If you prompt the local model with:
`--prompt "Why did the build fail? @/tmp/build.log"`

The Python script intercepts the `@` symbol, opens `/tmp/build.log`, and sends the massive file *directly to the local LM Studio model*.

**The Result:** The heavy lifting is done locally and for free. The local model processes the 3,000 lines and returns a concise, 2-sentence summary: *"The build failed because `npm install` wasn't run, missing the `lodash` dependency."*
Antigravity reads this tiny summary, keeping your main context window pristine.
