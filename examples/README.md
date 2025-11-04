# Godot Coding Agent Examples

This directory contains example scripts demonstrating different usage patterns for the Godot Coding Agent.

## Examples

### simple_usage.py

Basic usage examples:
- Creating a simple game with one command
- Streaming execution to see progress

Run it:
```bash
python examples/simple_usage.py
```

### advanced_usage.py

Advanced usage patterns:
- Using custom LLM configurations
- Creating games in specific directories
- Accessing full agent state
- Iterative game development

Run it:
```bash
python examples/advanced_usage.py
```

## Prerequisites

Before running the examples:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your API key in `.env`:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## What You'll Learn

- **simple_usage.py**: Quick start with the agent
- **advanced_usage.py**: Customization and advanced features

## Output

The examples will create Godot game files in the current directory or specified subdirectories. You can open these in the Godot Engine to test them.

## Tips

- Start with `simple_usage.py` to understand the basics
- Check `advanced_usage.py` for customization options
- Look at the main `README.md` for comprehensive documentation
- Modify the examples to create your own games!
