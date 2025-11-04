"""
Godot Coding Agent using LangChain's Deep Agents framework
"""

import os
from typing import Optional
from deepagents import create_deep_agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from godot_agent.tools import get_godot_tools
from godot_agent.prompts import (
    SYSTEM_PROMPT,
    GODOT_KNOWLEDGE,
    GODOT_4_DIFFERENCES
)


class GodotCodingAgent:
    """
    Deep Agent specialized for Godot game development.

    This agent uses LangChain's Deep Agents framework which provides:
    - Automatic planning via built-in task breakdown tools
    - File system access for managing game project files
    - Sub-agent spawning for complex tasks
    - Persistent memory and context management

    Combined with Godot-specific tools and knowledge.
    """

    def __init__(
        self,
        model_provider: str = "anthropic",
        model_name: str = "claude-sonnet-4-5-20250929",
        custom_llm: Optional[object] = None
    ):
        """
        Initialize the Godot Coding Agent

        Args:
            model_provider: "anthropic" or "openai" (default: "anthropic")
            model_name: Name of the model to use (default: claude-sonnet-4-5-20250929)
            custom_llm: Optional custom LangChain LLM object
        """
        # Get Godot-specific tools
        self.godot_tools = get_godot_tools()

        # Initialize LLM
        if custom_llm:
            self.llm = custom_llm
        else:
            self.llm = self._initialize_llm(model_provider, model_name)

        # Create comprehensive system prompt
        self.system_prompt = self._build_system_prompt()

        # Create the deep agent
        # Deep agents automatically get:
        # - Planning tools (write_todos, update_todos)
        # - File system tools (read_file, write_file, edit_file, ls)
        # - Sub-agent spawning (task tool)
        self.agent = create_deep_agent(
            tools=self.godot_tools,
            system_prompt=self.system_prompt,
            model=self.llm
        )

    def _initialize_llm(self, provider: str, model_name: str):
        """Initialize LLM based on provider"""
        if provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY environment variable not set. "
                    "Set it with: export ANTHROPIC_API_KEY='your-key'"
                )
            return ChatAnthropic(
                model=model_name,
                api_key=api_key,
                temperature=0.1
            )
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY environment variable not set. "
                    "Set it with: export OPENAI_API_KEY='your-key'"
                )
            return ChatOpenAI(
                model=model_name,
                api_key=api_key,
                temperature=0.1
            )
        else:
            raise ValueError(f"Unknown model provider: {provider}. Use 'anthropic' or 'openai'")

    def _build_system_prompt(self) -> str:
        """Build comprehensive system prompt with Godot knowledge"""
        return f"""{SYSTEM_PROMPT}

# Godot Engine Knowledge Base

{GODOT_KNOWLEDGE}

{GODOT_4_DIFFERENCES}

# How to Use Your Tools

## Built-in Deep Agent Tools (Automatic)

You have access to these planning and file management tools:

1. **write_todos / update_todos**: Break down complex game creation tasks into steps
   - Use this to plan game architecture before coding
   - Track progress on multi-file projects

2. **read_file / write_file / edit_file**: Manage game project files
   - Use these to create and modify .gd scripts, .tscn scenes, project.godot
   - Files are in the local file system

3. **ls**: List directory contents
   - Check what files exist before creating new ones

4. **task**: Spawn sub-agents for complex sub-tasks
   - Example: "Create a complete health system" as a sub-task

## Godot-Specific Tools

1. **get_godot_code_snippet**: Get GDScript code examples for common patterns
   - player_movement_2d, health_system, signal_example, etc.

2. **create_godot_scene_template**: Get scene structure templates
   - 2d_character, 2d_level, ui_menu, enemy, projectile, etc.

3. **run_godot_command**: Run Godot commands (if Godot is installed)
   - Check version, export projects, etc.

# Workflow for Creating Games

1. **Understand Requirements**: Ask clarifying questions if needed
2. **Plan Architecture**: Use write_todos to break down the project
3. **Check Existing Files**: Use ls to see what's already there
4. **Get Templates/Snippets**: Use Godot-specific tools for guidance
5. **Create Files**: Start with project.godot, then scenes and scripts
6. **Write Code**: Create .gd scripts with proper structure
7. **Update Progress**: Use update_todos to track completion

# Best Practices

- Always create project.godot first for new projects
- Use res:// paths for internal Godot references
- Follow GDScript conventions (snake_case, proper exports)
- Add helpful comments in code
- Structure projects with scenes/ and scripts/ directories
- Test ideas with simple implementations first

Remember: You're a "deep agent" - you can plan complex tasks, manage files,
and spawn sub-agents. Use these capabilities to create complete, working games!
"""

    def invoke(self, user_message: str) -> dict:
        """
        Run the agent with a user message and return full state

        Args:
            user_message: The user's request

        Returns:
            Final state dictionary with messages and other data
        """
        return self.agent.invoke({
            "messages": [{"role": "user", "content": user_message}]
        })

    def run(self, user_message: str) -> str:
        """
        Run the agent with a user message and return just the final response

        Args:
            user_message: The user's request

        Returns:
            The agent's final response text
        """
        result = self.invoke(user_message)
        if result.get("messages"):
            last_message = result["messages"][-1]
            return last_message.content
        return "Task completed."

    def stream(self, user_message: str):
        """
        Run the agent with streaming output

        Args:
            user_message: The user's request

        Yields:
            State updates as they occur
        """
        for state in self.agent.stream({
            "messages": [{"role": "user", "content": user_message}]
        }):
            yield state
