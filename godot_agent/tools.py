"""
Godot-specific tools for the Deep Agent
"""

import subprocess
from typing import Literal
from langchain.tools import tool


@tool
def run_godot_command(command: str, working_dir: str = ".") -> str:
    """
    Execute a Godot-related shell command (e.g., running Godot editor or exporting project).

    Args:
        command: Command to execute (e.g., 'godot --version', 'godot --headless --path . --export-debug Linux')
        working_dir: Directory to run the command in

    Returns:
        Command output or error message
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Exit code: {result.returncode}")

        return "\n".join(output) if output else "Command executed successfully (no output)"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"


@tool
def create_godot_scene_template(
    scene_type: Literal["2d_character", "2d_level", "ui_menu", "3d_character", "enemy", "projectile"]
) -> str:
    """
    Generate a template for common Godot scene structures.

    Args:
        scene_type: Type of scene template to generate

    Returns:
        Scene template structure description
    """
    templates = {
        "2d_character": """
2D Character Scene Structure:
Root: CharacterBody2D
├── Sprite2D (for character graphics)
├── CollisionShape2D (for physics)
├── AnimationPlayer (for animations)
└── Camera2D (optional, for following character)

Attach a script to CharacterBody2D for movement and game logic.
""",
        "2d_level": """
2D Level Scene Structure:
Root: Node2D
├── TileMap (for level geometry)
├── Player (instance of player scene)
├── Enemies (Node2D container)
│   ├── Enemy1
│   └── Enemy2
├── Collectibles (Node2D container)
└── Camera2D (follows player)

Add background, lighting, and parallax nodes as needed.
""",
        "ui_menu": """
UI Menu Scene Structure:
Root: Control (or Panel/MarginContainer)
├── VBoxContainer (for vertical layout)
│   ├── Label (title)
│   ├── Button (Play)
│   ├── Button (Settings)
│   ├── Button (Quit)
└── Background (TextureRect or ColorRect)

Attach script to Root for button signal connections.
""",
        "3d_character": """
3D Character Scene Structure:
Root: CharacterBody3D
├── MeshInstance3D (character model)
├── CollisionShape3D (physics)
├── AnimationPlayer (animations)
├── Camera3D (optional)
└── RayCast3D (for ground detection)

Attach script for 3D movement and controls.
""",
        "enemy": """
Enemy Scene Structure:
Root: CharacterBody2D (or Area2D)
├── Sprite2D (or AnimatedSprite2D)
├── CollisionShape2D
├── DetectionArea (Area2D for player detection)
│   └── CollisionShape2D
└── NavigationAgent2D (for pathfinding)

Script handles AI behavior, health, and damage.
""",
        "projectile": """
Projectile Scene Structure:
Root: Area2D (or CharacterBody2D)
├── Sprite2D
├── CollisionShape2D
└── VisibleOnScreenNotifier2D (for cleanup)

Script handles movement and collision detection.
"""
    }

    return templates.get(scene_type, "Unknown scene type")


@tool
def get_godot_code_snippet(
    snippet_type: Literal[
        "player_movement_2d",
        "player_movement_3d",
        "jump_physics",
        "health_system",
        "signal_example",
        "scene_change",
        "button_handler",
        "timer_usage",
        "collision_detection",
        "animation_control"
    ]
) -> str:
    """
    Get GDScript code snippets for common game mechanics.

    Args:
        snippet_type: Type of code snippet to retrieve

    Returns:
        GDScript code example
    """
    snippets = {
        "player_movement_2d": """
# 2D Player Movement (Top-down or Platformer)
extends CharacterBody2D

@export var speed: float = 300.0
@export var jump_velocity: float = -400.0

var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

func _physics_process(delta):
    # Add gravity (for platformer)
    if not is_on_floor():
        velocity.y += gravity * delta

    # Handle jump
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    # Get input direction
    var direction = Input.get_axis("move_left", "move_right")

    # Apply movement
    if direction:
        velocity.x = direction * speed
    else:
        velocity.x = move_toward(velocity.x, 0, speed)

    move_and_slide()
""",
        "player_movement_3d": """
# 3D Player Movement
extends CharacterBody3D

@export var speed: float = 5.0
@export var jump_velocity: float = 4.5

var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

func _physics_process(delta):
    # Add gravity
    if not is_on_floor():
        velocity.y -= gravity * delta

    # Handle jump
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    # Get input direction
    var input_dir = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

    # Apply movement
    if direction:
        velocity.x = direction.x * speed
        velocity.z = direction.z * speed
    else:
        velocity.x = move_toward(velocity.x, 0, speed)
        velocity.z = move_toward(velocity.z, 0, speed)

    move_and_slide()
""",
        "health_system": """
# Health System
extends Node

signal health_changed(new_health)
signal died()

@export var max_health: int = 100
var current_health: int

func _ready():
    current_health = max_health

func take_damage(amount: int) -> void:
    current_health = max(0, current_health - amount)
    health_changed.emit(current_health)

    if current_health == 0:
        died.emit()

func heal(amount: int) -> void:
    current_health = min(max_health, current_health + amount)
    health_changed.emit(current_health)

func get_health_percentage() -> float:
    return float(current_health) / float(max_health)
""",
        "signal_example": """
# Signal Example
extends Node

# Define custom signals
signal button_pressed(button_name: String)
signal game_started()
signal score_updated(new_score: int)

func _ready():
    # Connect signals
    button_pressed.connect(_on_button_pressed)

func _on_button_pressed(button_name: String):
    print("Button pressed: ", button_name)
    if button_name == "start":
        game_started.emit()

# Emit signals
func some_function():
    button_pressed.emit("start")
    score_updated.emit(100)
""",
        "scene_change": """
# Scene Management
extends Node

func change_scene(scene_path: String) -> void:
    get_tree().change_scene_to_file(scene_path)

func reload_scene() -> void:
    get_tree().reload_current_scene()

func quit_game() -> void:
    get_tree().quit()

# Example usage:
# change_scene("res://scenes/level_2.tscn")
""",
        "button_handler": """
# Button Handler
extends Button

func _ready():
    pressed.connect(_on_button_pressed)

func _on_button_pressed():
    print("Button pressed!")
    # Your button logic here
    get_tree().change_scene_to_file("res://scenes/game.tscn")
""",
        "timer_usage": """
# Timer Usage
extends Node

@onready var timer = $Timer

func _ready():
    # Configure timer
    timer.wait_time = 2.0
    timer.one_shot = false
    timer.timeout.connect(_on_timer_timeout)
    timer.start()

func _on_timer_timeout():
    print("Timer expired!")
    # Your timer logic here
""",
        "collision_detection": """
# Collision Detection (Area2D)
extends Area2D

func _ready():
    body_entered.connect(_on_body_entered)
    body_exited.connect(_on_body_exited)

func _on_body_entered(body: Node2D):
    if body.is_in_group("player"):
        print("Player entered!")
        # Handle collision

func _on_body_exited(body: Node2D):
    if body.is_in_group("player"):
        print("Player exited!")
""",
        "animation_control": """
# Animation Control
extends Node2D

@onready var animation_player = $AnimationPlayer

func _ready():
    animation_player.play("idle")

func play_animation(anim_name: String):
    if animation_player.has_animation(anim_name):
        animation_player.play(anim_name)

func _on_animation_finished(anim_name: String):
    if anim_name == "attack":
        animation_player.play("idle")
"""
    }

    return snippets.get(snippet_type, "Unknown snippet type")


def get_godot_tools():
    """Return list of Godot-specific tools"""
    return [
        run_godot_command,
        create_godot_scene_template,
        get_godot_code_snippet,
    ]
