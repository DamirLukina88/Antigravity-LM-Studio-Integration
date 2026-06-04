<p align="center">
  <img src="logo.png" alt="Antigravity LM Studio Logo" width="300"/>
</p>

# Antigravity LM Studio Integration

This repository provides a custom skill for Google Antigravity 2.0 that seamlessly integrates local LM Studio models (like Gemma, Llama 3, or DeepSeek) directly into your agent environment via the `http://localhost:1234/v1` API. 

It is designed for **maximum privacy and token efficiency**, allowing you to use Gemini for orchestration while offloading heavy code generation and sensitive reasoning to local models running on your own hardware.

## Features
- **Just-in-Time (JIT) Model Loading:** The plugin automatically detects which model is currently loaded in LM Studio and switches it if necessary (`lms unload --all` and `lms load <model>`), keeping your VRAM usage optimized.
- **Cost-Saving Workflows:** Includes a `--code-only` argument that forces local models to output raw, executable code directly to your project files, bypassing Antigravity's context window entirely.
- **Diagnostic Funneling:** Send massive error logs to your local models and have Antigravity read only the surgical fix, preventing context pollution.
- **Four Specialized Skills:** Includes pre-configured skills for both 12B and 26B parameter models, separated into "Coder" and "Chat" configurations.

---

## 1. Environment Setup

1. Ensure you have [LM Studio](https://lmstudio.ai/) installed.
2. Start the Local Server in LM Studio (make sure it's running on port `1234`).
3. Make sure the `lms` CLI tool is accessible in your terminal. You can test this by running `lms ps` in your terminal.

---

## 2. Install Dependencies

The integration uses the standard OpenAI SDK to connect to LM Studio's API, and the LM Studio CLI to manage VRAM.

```bash
pip install openai --break-system-packages
```

---

## 3. Deployment

Because Antigravity protects its system configuration folder, you must use an agent with `unsandboxed(bash)` permissions to deploy this plugin, or copy it manually.

**Manual Installation:**
Copy the `lm-studio-plugin` folder from this repository into your Antigravity plugins directory:

```bash
cp -r lm-studio-plugin ~/.gemini/config/plugins/
```

**Agent Installation (Direct from GitHub URL):**
You don't even need to clone this repo! Just ask your Antigravity agent:
> *"Please fetch the LM Studio integration from `https://github.com/DamirLukina88/Antigravity-LM-Studio-Integration.git` and install the `lm-studio-plugin` folder into your `~/.gemini/config/plugins/` directory."*

---

## 4. Documentation & Usage

For full details on how to utilize the specialized skills and the token optimization strategies, please see the [Wiki](wiki/LM-Studio-Integration-Wiki.md).
