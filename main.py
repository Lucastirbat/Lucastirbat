#!/usr/bin/env python3
"""
Godot Coding Agent CLI
A LangGraph-based AI assistant for creating Godot games
"""

import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

from godot_agent import GodotCodingAgent


console = Console()


def print_welcome():
    """Print welcome message"""
    welcome_text = """
# Godot Coding Agent

An AI-powered assistant for creating Godot games using LangGraph.

**Capabilities:**
- Plan and architect Godot game projects
- Write GDScript code
- Create project files and directory structures
- Follow Godot best practices
- Support for Godot 3.x and 4.x

**Example requests:**
- "Create a simple 2D platformer game"
- "Make a space shooter with enemies and scoring"
- "Create a main menu with play and quit buttons"
"""
    console.print(Panel(Markdown(welcome_text), title="Welcome", border_style="blue"))


def run_interactive_mode(agent: GodotCodingAgent):
    """Run the agent in interactive mode"""
    print_welcome()

    console.print("\n[bold green]Interactive mode started.[/bold green]")
    console.print("Type your game creation request or 'quit' to exit.\n")

    while True:
        try:
            # Get user input
            user_input = console.input("[bold cyan]You:[/bold cyan] ")

            if not user_input.strip():
                continue

            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("\n[bold yellow]Goodbye![/bold yellow]")
                break

            # Run agent
            console.print("\n[bold magenta]Agent:[/bold magenta] Thinking...\n")

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Processing...", total=None)

                try:
                    # Stream the agent's work
                    for state in agent.stream(user_input):
                        node_name = list(state.keys())[0]
                        progress.update(task, description=f"Running: {node_name}")

                    progress.update(task, description="Complete!")

                except Exception as e:
                    console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
                    continue

            # Get and display final result
            try:
                result = agent.run(user_input)
                console.print(f"\n[bold magenta]Agent:[/bold magenta]\n")
                console.print(Markdown(result))
            except Exception as e:
                console.print(f"\n[bold red]Error:[/bold red] {str(e)}")

            console.print("\n" + "─" * 80 + "\n")

        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]Interrupted. Goodbye![/bold yellow]")
            break
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")


def run_single_command(agent: GodotCodingAgent, command: str):
    """Run a single command and exit"""
    console.print(f"\n[bold cyan]Request:[/bold cyan] {command}\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing...", total=None)

        try:
            for state in agent.stream(command):
                node_name = list(state.keys())[0]
                progress.update(task, description=f"Running: {node_name}")

            progress.update(task, description="Complete!")

        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
            sys.exit(1)

    try:
        result = agent.run(command)
        console.print(f"\n[bold magenta]Result:[/bold magenta]\n")
        console.print(Markdown(result))
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Godot Coding Agent - AI-powered Godot game development assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Start interactive mode
  %(prog)s "Create a 2D platformer"          # Run single command
  %(prog)s --model openai --name gpt-4       # Use OpenAI GPT-4
        """
    )

    parser.add_argument(
        "command",
        nargs="?",
        help="Single command to execute (if not provided, starts interactive mode)"
    )

    parser.add_argument(
        "--model",
        choices=["anthropic", "openai"],
        default="anthropic",
        help="LLM provider to use (default: anthropic)"
    )

    parser.add_argument(
        "--name",
        default="claude-3-5-sonnet-20241022",
        help="Model name (default: claude-3-5-sonnet-20241022)"
    )

    parser.add_argument(
        "--workdir",
        type=Path,
        default=Path.cwd(),
        help="Working directory for the agent (default: current directory)"
    )

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Change to working directory
    if args.workdir:
        args.workdir.mkdir(parents=True, exist_ok=True)
        import os
        os.chdir(args.workdir)

    # Initialize agent
    try:
        agent = GodotCodingAgent(
            model_provider=args.model,
            model_name=args.name
        )
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        console.print("\n[yellow]Please set the required API key:[/yellow]")
        if args.model == "anthropic":
            console.print("  export ANTHROPIC_API_KEY='your-key-here'")
        else:
            console.print("  export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)

    # Run in appropriate mode
    if args.command:
        run_single_command(agent, args.command)
    else:
        run_interactive_mode(agent)


if __name__ == "__main__":
    main()
