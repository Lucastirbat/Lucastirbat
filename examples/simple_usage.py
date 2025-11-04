#!/usr/bin/env python3
"""
Simple usage example for the Godot Coding Agent

This demonstrates how to use the agent programmatically.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from godot_agent import GodotCodingAgent


def main():
    # Load environment variables
    load_dotenv()

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("Error: No API key found!")
        print("Set ANTHROPIC_API_KEY or OPENAI_API_KEY in your .env file")
        return

    # Initialize the agent
    print("Initializing Godot Coding Agent...")
    agent = GodotCodingAgent(
        model_provider="anthropic",
        model_name="claude-sonnet-4-5-20250929"
    )

    # Example 1: Simple game creation
    print("\n" + "="*80)
    print("Example 1: Creating a simple Pong game")
    print("="*80 + "\n")

    result = agent.run("""
    Create a simple Pong game with:
    - Two paddles (left and right)
    - A ball that bounces
    - Basic scoring
    - Reset when someone scores
    """)

    print("Result:")
    print(result)

    # Example 2: Streaming execution
    print("\n" + "="*80)
    print("Example 2: Streaming execution (shows progress)")
    print("="*80 + "\n")

    for state in agent.stream("Create a player character that can jump"):
        node_name = list(state.keys())[0]
        print(f"→ Executing: {node_name}")

    print("\nDone!")


if __name__ == "__main__":
    main()
