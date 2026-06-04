#!/usr/bin/env python3
import argparse
import sys
import os
import re
import json
import subprocess
from openai import OpenAI

def strip_markdown_blocks(text):
    """Strip markdown code blocks from the response."""
    pattern = r"^```[a-zA-Z]*\n(.*?)```$"
    match = re.search(pattern, text, flags=re.DOTALL | re.MULTILINE)
    if match:
        return match.group(1).strip() + "\n"
    return text

def ensure_model_loaded(model_name):
    """Ensure the target model is loaded. If not, unload all and load the new one."""
    if model_name == "local-model":
        return # Skip JIT loading if no specific model requested

    try:
        # Check currently loaded models
        result = subprocess.run(["lms", "ps", "--json"], capture_output=True, text=True, check=True)
        loaded_models = json.loads(result.stdout)
        
        # Check if our model is already running
        for model in loaded_models:
            if model.get("modelKey") == model_name:
                return # Already loaded
                
        # If we reach here, the model is not loaded. Unload everything else first.
        print(f"Model '{model_name}' not loaded. Performing Just-in-Time loading...", file=sys.stderr)
        if len(loaded_models) > 0:
            print("Unloading existing models...", file=sys.stderr)
            subprocess.run(["lms", "unload", "--all"], check=True)
            
        print(f"Loading model '{model_name}'...", file=sys.stderr)
        subprocess.run(["lms", "load", model_name, "--yes"], check=True)
        print("Model loaded successfully.", file=sys.stderr)
        
    except Exception as e:
        print(f"Failed during JIT model loading: {e}", file=sys.stderr)
        sys.exit(1)

def query_lm_studio(args):
    # Perform JIT model load if a specific model is required
    ensure_model_loaded(args.model)

    try:
        client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}", file=sys.stderr)
        sys.exit(1)

    messages = []
    
    system_prompt = args.system
    if args.code_only:
        code_enforcer = "You must output ONLY raw, valid code. Do not include any explanations, introductory text, or concluding remarks. Do not wrap the code in markdown blocks unless absolutely necessary, but prioritize raw text."
        if system_prompt:
            system_prompt = f"{system_prompt}\n\n{code_enforcer}"
        else:
            system_prompt = code_enforcer

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    prompt_text = args.prompt
    if prompt_text.startswith("@") and os.path.isfile(prompt_text[1:]):
        with open(prompt_text[1:], "r", encoding="utf-8") as f:
            prompt_text = f.read()

    messages.append({"role": "user", "content": prompt_text})

    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=args.temperature,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print(f"Error querying LM Studio API: {e}", file=sys.stderr)
        sys.exit(1)
        
    if args.code_only:
        reply = strip_markdown_blocks(reply.strip())
        
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(reply)
    print(f"Success! Response written to: {args.output}")

def main():
    parser = argparse.ArgumentParser(description="Query local LM Studio API.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("--prompt", required=True, help="Text prompt or @filepath")
    query_parser.add_argument("--output", required=True, help="Output file path")
    query_parser.add_argument("--model", default="local-model", help="Model name key (e.g. google/gemma-4-12b)")
    query_parser.add_argument("--system", help="Optional system prompt")
    query_parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for generation")
    query_parser.add_argument("--code-only", action="store_true", help="Force output to be raw code, stripping markdown blocks.")
    
    args = parser.parse_args()
    if args.command == "query":
        query_lm_studio(args)

if __name__ == "__main__":
    main()
