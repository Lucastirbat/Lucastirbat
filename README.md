# Godot Coding Agent 🎮

An AI-powered coding assistant specialized in creating Godot games, built on LangChain's **Deep Agents** framework.

## Overview

This agent is inspired by applications like Claude Code, Deep Research, and Manus. It uses the "deep agent" pattern with:

- **Automatic Planning**: Built-in task breakdown and progress tracking
- **File System Access**: Create and manage entire game projects
- **Sub-Agent Spawning**: Delegate complex subtasks to specialized agents
- **Godot Expertise**: Deep knowledge of GDScript, scenes, and game development patterns

## Features

- Create complete Godot game projects from natural language descriptions
- Generate GDScript code following best practices
- Provide scene structure templates for common game elements
- Support for both Godot 3.x and 4.x
- Interactive CLI with streaming output
- Extensible tool system

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Lucastirbat/Lucastirbat.git
cd Lucastirbat
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up your API key:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY or OPENAI_API_KEY
```

## Quick Start

### Interactive Mode

Run the agent in interactive mode for a conversational experience:

```bash
python main.py
```

Then try requests like:
- "Create a simple 2D platformer game"
- "Make a space shooter with enemies and scoring"
- "Create a main menu with play and quit buttons"

### Single Command Mode

Execute a single command and exit:

```bash
python main.py "Create a simple Pong game"
```

### Custom Model

Use a different model or provider:

```bash
# Use OpenAI GPT-4
python main.py --model openai --name gpt-4

# Use a specific Anthropic model
python main.py --model anthropic --name claude-3-opus-20240229
```

### Custom Working Directory

Generate the game in a specific directory:

```bash
python main.py --workdir ./my_game "Create a platformer"
```

## Programmatic Usage

You can also use the agent directly in your Python code:

```python
from godot_agent import GodotCodingAgent

# Initialize the agent
agent = GodotCodingAgent(
    model_provider="anthropic",
    model_name="claude-sonnet-4-5-20250929"
)

# Simple usage - get final result
result = agent.run("Create a simple 2D platformer")
print(result)

# Advanced usage - stream the execution
for state in agent.stream("Create a space shooter"):
    print(f"Step: {list(state.keys())[0]}")

# Full state access
result = agent.invoke("Create a menu system")
print(result["messages"][-1].content)
```

## How It Works

This agent uses LangChain's **Deep Agents** framework, which implements four key components:

### 1. Detailed System Prompt
Comprehensive instructions with Godot-specific knowledge, best practices, and examples.

### 2. Planning Tool
Built-in `write_todos` and `update_todos` tools for breaking down complex game projects into manageable steps.

### 3. Sub-Agents
Ability to spawn specialized agents for complex subtasks using the `task` tool.

### 4. File System Access
Built-in tools for file operations:
- `read_file`: Read existing files
- `write_file`: Create new files
- `edit_file`: Modify existing files
- `ls`: List directory contents

Plus Godot-specific tools:
- `get_godot_code_snippet`: Get GDScript code examples
- `create_godot_scene_template`: Get scene structure templates
- `run_godot_command`: Execute Godot CLI commands

## Architecture

```
godot_agent/
├── __init__.py          # Package initialization
├── agent.py             # Main GodotCodingAgent class using Deep Agents
├── tools.py             # Godot-specific tools
└── prompts.py           # System prompts and knowledge base

main.py                  # CLI interface with Rich formatting
requirements.txt         # Python dependencies
```

## Example Projects

### 2D Platformer

```bash
python main.py "Create a 2D platformer with:
- A player character that can move left, right, and jump
- Platforms to jump on
- Enemies that patrol back and forth
- A goal to reach to win the level"
```

### Space Shooter

```bash
python main.py "Create a space shooter game with:
- Player spaceship at the bottom
- Enemies spawning from the top
- Player can shoot projectiles
- Score tracking
- Game over when player is hit"
```

### Menu System

```bash
python main.py "Create a game menu with:
- Main menu scene with Play and Quit buttons
- Settings menu with volume slider
- Proper scene transitions"
```

## Deep Agents Framework

This project uses LangChain's `deepagents` package, which provides:

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    tools=[...],           # Your custom tools
    system_prompt="...",   # Detailed instructions
    model=llm              # LangChain LLM
)
```

The framework automatically provides:
- Task planning and tracking
- File system operations
- Sub-agent spawning
- Memory management

Learn more: [LangChain Deep Agents Blog Post](https://blog.langchain.com/deep-agents/)

## Requirements

- Python 3.10+
- Anthropic or OpenAI API key
- Dependencies listed in `requirements.txt`

## Contributing

Contributions are welcome! Areas for improvement:

- Additional Godot code snippets and templates
- More game genre templates
- Better scene file generation (currently text descriptions)
- Integration with Godot's command-line tools
- Visual scene editor integration
- Asset management tools

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built on [LangChain](https://github.com/langchain-ai/langchain) and [LangGraph](https://github.com/langchain-ai/langgraph)
- Uses the [Deep Agents](https://github.com/langchain-ai/deepagents) framework
- Inspired by Claude Code, Deep Research, and Manus

## Resources

- [Godot Engine Documentation](https://docs.godotengine.org/)
- [GDScript Style Guide](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html)
- [LangChain Documentation](https://docs.langchain.com/)
- [Deep Agents Overview](https://docs.langchain.com/oss/python/deepagents/overview)

---

![My GitHub Metrics](github-metrics.svg)
