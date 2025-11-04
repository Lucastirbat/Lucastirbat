"""
Godot Coding Agent - A Deep Agent for creating Godot games

Built on LangChain's Deep Agents framework with Godot-specific tools and knowledge.
"""

from godot_agent.agent import GodotCodingAgent
from godot_agent.tools import get_godot_tools

__version__ = "0.1.0"
__all__ = ["GodotCodingAgent", "get_godot_tools"]
