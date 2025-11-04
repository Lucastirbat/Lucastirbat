"""
Prompts and knowledge for the Godot Coding Agent
"""

SYSTEM_PROMPT = """You are an expert Godot game development assistant with deep knowledge of:
- Godot Engine (versions 3.x and 4.x)
- GDScript programming language
- Game development patterns and best practices
- 2D and 3D game development
- Physics, animations, UI, and audio systems
- Scene management and node architecture

Your role is to help users create Godot games by:
1. Understanding their requirements and game concept
2. Planning the game architecture (scenes, scripts, nodes)
3. Writing clean, well-documented GDScript code
4. Creating necessary project files and directory structure
5. Following Godot best practices and conventions

When creating games:
- Always create a project.godot file first
- Organize code into logical scenes and scripts
- Use Godot's node system appropriately
- Add helpful comments in code
- Follow GDScript naming conventions (snake_case for variables/functions, PascalCase for classes)
- Include proper signal connections and scene setup

Available tools:
- read_file: Read file contents
- write_file: Write/create files
- list_files: List files in directory
- run_command: Execute shell commands
- create_directory: Create directories
- search_files: Search for patterns in files

Always think step-by-step and plan before executing."""


GODOT_KNOWLEDGE = """
# Godot Engine Quick Reference

## Project Structure
```
game_project/
├── project.godot          # Main project file
├── scenes/                # .tscn scene files
├── scripts/              # .gd script files
├── assets/               # Images, audio, etc.
│   ├── sprites/
│   ├── audio/
│   └── fonts/
└── export_presets.cfg    # Export settings
```

## Basic project.godot Template
```
config_version=5

[application]
config/name="GameName"
run/main_scene="res://scenes/main.tscn"
config/features=PackedStringArray("4.2")
config/icon="res://icon.svg"

[display]
window/size/viewport_width=1280
window/size/viewport_height=720

[rendering]
renderer/rendering_method="gl_compatibility"
```

## Common Node Types
- Node2D: Base for 2D nodes
- Sprite2D: Display 2D images
- AnimatedSprite2D: Animated sprites
- CharacterBody2D: 2D character with physics
- Area2D: Detect overlapping bodies
- CollisionShape2D: Define collision areas
- Camera2D: 2D camera
- Control: Base for UI elements
- Label, Button, TextureButton: UI components

## GDScript Basics
```gdscript
extends Node2D

# Signals
signal health_changed(new_health)

# Constants
const SPEED = 200.0

# Exported variables (visible in editor)
@export var max_health: int = 100

# Variables
var velocity = Vector2.ZERO
var current_health: int

# Built-in functions
func _ready():
    # Called when node enters scene tree
    current_health = max_health

func _process(delta):
    # Called every frame
    pass

func _physics_process(delta):
    # Called every physics frame (fixed timestep)
    pass

# Custom functions
func take_damage(amount: int) -> void:
    current_health -= amount
    health_changed.emit(current_health)
```

## Common Patterns

### Player Movement (2D)
```gdscript
extends CharacterBody2D

@export var speed = 300.0
@export var jump_velocity = -400.0

var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

func _physics_process(delta):
    # Gravity
    if not is_on_floor():
        velocity.y += gravity * delta

    # Jump
    if Input.is_action_just_pressed("ui_accept") and is_on_floor():
        velocity.y = jump_velocity

    # Horizontal movement
    var direction = Input.get_axis("ui_left", "ui_right")
    velocity.x = direction * speed

    move_and_slide()
```

### Scene Management
```gdscript
# Change scene
get_tree().change_scene_to_file("res://scenes/level2.tscn")

# Reload current scene
get_tree().reload_current_scene()

# Quit game
get_tree().quit()
```

### Signals
```gdscript
# Define signal
signal button_pressed(button_name: String)

# Emit signal
button_pressed.emit("start")

# Connect signal
some_node.button_pressed.connect(_on_button_pressed)

func _on_button_pressed(button_name: String):
    print("Button pressed: ", button_name)
```
"""


PLANNING_PROMPT = """Based on the user's request, create a detailed plan for the Godot game:

1. Game Concept: Briefly describe the game
2. Required Scenes: List main scenes needed (e.g., Main, Player, Enemy, UI)
3. Key Scripts: List main scripts and their responsibilities
4. Node Structure: Describe the node hierarchy for main scenes
5. Implementation Steps: Break down the work into steps

Be specific and actionable. Consider what files need to be created and in what order."""


GODOT_4_DIFFERENCES = """
# Godot 4.x vs 3.x Key Differences

1. Node Names: Sprite → Sprite2D, KinematicBody2D → CharacterBody2D
2. Signals: Use `signal_name.emit()` instead of `emit_signal()`
3. Export variables: Use `@export` annotation instead of `export` keyword
4. Random numbers: Use `randf()` and `randi()` (no RandomNumberGenerator needed for basic use)
5. Type hints encouraged: `var x: int = 5`
6. `_ready()` and other callbacks unchanged
7. `move_and_slide()` returns void, check velocity directly
"""
