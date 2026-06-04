# Installation Guide

Setting up the LM Studio Integration requires configuring LM Studio and copying the plugin files to your Antigravity configuration directory.

## 1. LM Studio Configuration

1. Download and install [LM Studio](https://lmstudio.ai/).
2. Open LM Studio and navigate to the **Local Server** tab (the `<->` icon).
3. Start the server. Ensure the port is set to `1234`.
4. Ensure the `lms` CLI tool is accessible. Open your terminal and run:
   ```bash
   lms status
   ```
   If this command is not found, you may need to add LM Studio's CLI tools to your system `PATH`.

## 2. Python Dependencies

The integration relies on the official `openai` Python package to communicate with the LM Studio API endpoint.

```bash
pip install openai --break-system-packages
```

## 3. Plugin Deployment

Antigravity stores its plugins in a hidden system configuration folder at `~/.gemini/config/plugins/`.

To install the plugin, simply copy the `lm-studio-plugin` directory from this repository to that location.

### Manual Copy
```bash
cp -r lm-studio-plugin ~/.gemini/config/plugins/
```

### Agent Installation
If you prefer, you can ask your agent to do it for you, provided it has unsandboxed permissions:
> *"Please copy the `lm-studio-plugin` folder from this project into your `~/.gemini/config/plugins/` directory."*

Once the folder is copied, Antigravity will automatically detect and load the new skills. You can verify this by asking the agent to list its available skills.
