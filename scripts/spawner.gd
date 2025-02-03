extends Node2D

@onready var enemy_scene: PackedScene = preload("res://objs/enemy.tscn")  # Assign the enemy scene in the inspector
@onready var player: Node2D = $"../Spaceship"  # Reference to the player
@export var spawn_margin: int = 30  # Distance outside the screen for spawning
@export var enemies_per_wave: int = 5  # Number of enemies per wave
@export var wave_interval: float = 10  # Time between waves (in seconds)

var screen_size: Vector2  # Stores screen dimensions

func _ready():
	screen_size = get_viewport_rect().size
	start_wave_timer()

func start_wave_timer():
	# Starts the recurring wave timer
	var wave_timer = Timer.new()
	wave_timer.wait_time = wave_interval
	wave_timer.autostart = true
	wave_timer.timeout.connect(spawn_wave)
	add_child(wave_timer)

func spawn_wave():
	for i in range(enemies_per_wave):
		spawn_enemy()

func spawn_enemy():
	if not enemy_scene or not player:
		return

	var enemy = enemy_scene.instantiate() as CharacterBody2D
	enemy.global_position = get_spawn_position()
	enemy.target = player  # Assign the player as the enemy's target

	get_parent().add_child(enemy)  # Add enemy to the scene

func get_spawn_position() -> Vector2:
	# Randomly chooses a spawn point outside the 1920x1080 screen
	var side = randi_range(0, 3)  # 0: Top, 1: Bottom, 2: Left, 3: Right
	var x: float
	var y: float

	match side:
		0:  # Top
			x = randf_range(-spawn_margin, screen_size.x + spawn_margin)
			y = -spawn_margin
		1:  # Bottom
			x = randf_range(-spawn_margin, screen_size.x + spawn_margin)
			y = screen_size.y + spawn_margin
		2:  # Left
			x = -spawn_margin
			y = randf_range(-spawn_margin, screen_size.y + spawn_margin)
		3:  # Right
			x = screen_size.x + spawn_margin
			y = randf_range(-spawn_margin, screen_size.y + spawn_margin)

	return Vector2(x, y)
