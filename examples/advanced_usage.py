#!/usr/bin/env python3
"""
Advanced usage example for the Godot Coding Agent

Demonstrates more complex scenarios and customization.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from godot_agent import GodotCodingAgent
from langchain_anthropic import ChatAnthropic


def example_with_custom_llm():
    """Example: Using a custom LLM configuration"""
    print("Example: Using custom LLM configuration")
    print("-" * 80)

    # Create a custom LLM with specific settings
    custom_llm = ChatAnthropic(
        model="claude-3-opus-20240229",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        temperature=0.3,  # Higher temperature for more creativity
        max_tokens=4096
    )

    # Initialize agent with custom LLM
    agent = GodotCodingAgent(custom_llm=custom_llm)

    result = agent.run("Create a creative boss battle system")
    print(result)
    print()


def example_with_working_directory():
    """Example: Creating game in specific directory"""
    print("Example: Creating game in specific directory")
    print("-" * 80)

    # Create working directory
    game_dir = Path("./my_awesome_game")
    game_dir.mkdir(exist_ok=True)

    # Change to that directory
    original_dir = os.getcwd()
    os.chdir(game_dir)

    try:
        agent = GodotCodingAgent()
        result = agent.run("""
        Create a complete game project structure:
        - project.godot file
        - scenes/ directory with main.tscn
        - scripts/ directory with player.gd
        - assets/ directory structure
        """)
        print(result)
    finally:
        # Change back to original directory
        os.chdir(original_dir)

    print(f"Game created in: {game_dir.absolute()}")
    print()


def example_full_state_access():
    """Example: Accessing full agent state"""
    print("Example: Accessing full agent state")
    print("-" * 80)

    agent = GodotCodingAgent()

    # Use invoke() to get full state
    result = agent.invoke("Create a health bar UI")

    # Access different parts of the state
    print(f"Total messages: {len(result['messages'])}")
    print(f"Final message: {result['messages'][-1].content[:200]}...")

    # Check if any todos were created
    if 'todos' in result:
        print(f"Todos created: {result['todos']}")

    print()


def example_iterative_development():
    """Example: Iterative game development"""
    print("Example: Iterative game development")
    print("-" * 80)

    agent = GodotCodingAgent()

    # Step 1: Create base game
    print("\nStep 1: Creating base game...")
    agent.run("Create a simple player controller for a platformer")

    # Step 2: Add features
    print("\nStep 2: Adding features...")
    agent.run("Add double jump ability to the player")

    # Step 3: Add enemies
    print("\nStep 3: Adding enemies...")
    agent.run("Create an enemy that patrols and damages the player")

    print("\nIterative development complete!")
    print()


def main():
    # Load environment variables
    load_dotenv()

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found in environment")
        print("Please set it in your .env file")
        return

    print("\n" + "="*80)
    print("Godot Coding Agent - Advanced Usage Examples")
    print("="*80 + "\n")

    # Run examples
    try:
        example_with_custom_llm()
        example_with_working_directory()
        example_full_state_access()
        example_iterative_development()
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "="*80)
    print("All examples completed!")
    print("="*80)


if __name__ == "__main__":
    main()
