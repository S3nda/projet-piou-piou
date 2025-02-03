extends CharacterBody2D

## Spaceship Controller Script
# Controls movement, shooting, and destruction of the spaceship

### Objects ###
@export var bullet_scene: PackedScene = preload("res://objs/bullets/bullet_player.tscn")

### Spaceship Settings ###
@export var thrust: float = 400.0  # Acceleration force
@export var max_speed: float = 200.0  # Maximum movement speed
@export var friction: float = 300.0  # Friction when no input is given
@export var rotation_speed: float = 20.0  # Rotation speed toward the cursor
@export var lateral_speed: float = 50.0  # Strafing speed
@export var recoil_force: float = .1  # Recoil force when shooting

### Shooting Settings ###
@export var fire_rate: float = 0.5  # Time between shots
var can_shoot: bool = true  # Flag to prevent rapid firing

### Health ###
var is_alive: bool = true  # Indicates if the spaceship is alive

@onready var gun: Marker2D = $Gun  # Firing position
@onready var gundir: Marker2D = $GunDir  # Direction for shooting
@onready var animation_player: AnimatedSprite2D= $AnimationPlayer  # Animations

### Signals ###
signal player_destroyed  # Emitted when the player is destroyed

func _physics_process(delta: float) -> void:
	if not is_alive:
		return  # Prevent movement if destroyed

	_handle_rotation(delta)
	_handle_movement(delta)
	_handle_collision()
	
	# Handle shooting
	if Input.is_action_pressed("shoot") and can_shoot:
		shoot()

### Rotation ###
func _handle_rotation(delta: float) -> void:
	var mouse_position: Vector2 = get_global_mouse_position()
	var target_angle: float = (mouse_position - global_position).angle() + PI / 2
	rotation = lerp_angle(rotation, target_angle, rotation_speed * delta)

### Movement ###
func _handle_movement(delta: float) -> void:
	var input_direction: Vector2 = Vector2.ZERO
	
	if Input.is_action_pressed("up"):
		input_direction += -transform.y
		animation_player.play("move")
	if Input.is_action_pressed("down"):
		input_direction += transform.y
	if Input.is_action_pressed("left"):
		input_direction += -transform.x
	if Input.is_action_pressed("right"):
		input_direction += transform.x

	if input_direction.length() > 1:
		input_direction = input_direction.normalized()
	if input_direction.length() == 0:
		animation_player.play("idle")

	velocity += input_direction * thrust * delta
	
	# Limit max speed
	if velocity.length() > max_speed:
		velocity = velocity.normalized() * max_speed
	
	# Apply friction when not accelerating
	if input_direction == Vector2.ZERO:
		velocity = velocity.move_toward(Vector2.ZERO, friction * delta)
	
	move_and_slide()

### Collision Handling ###
func _handle_collision() -> void:
	var collision = move_and_collide(velocity * get_physics_process_delta_time())
	if collision:
		var collider = collision.get_collider()
		if collider and collider.is_in_group("enemy_bullets"):
			print("Hit by enemy bullet: ", collider.name)
			die()

### Shooting Function ###
func shoot() -> void:
	can_shoot = false  # Disable shooting temporarily
	
	# Create bullet instance
	var bullet = bullet_scene.instantiate()
	bullet.global_position = gun.global_position
	var bullet_direction: Vector2 = (gundir.global_position - gun.global_position).normalized()
	bullet.set_direction(bullet_direction)
	bullet.add_to_group("player_bullets")
	
	# Apply recoil
	velocity -= bullet_direction * recoil_force
	
	# Add bullet to scene
	get_parent().add_child(bullet)
	
	# Reactivate shooting after cooldown
	await get_tree().create_timer(fire_rate).timeout
	can_shoot = true

### Death Function ###
func die() -> void:
	is_alive = false  # Disable spaceship controls
	velocity = Vector2.ZERO  # Stop movement
	
	# Play explosion animation
	animation_player.play("explode")
	await animation_player.animation_finished
	queue_free()  # Remove the spaceship from the scene
	
	emit_signal("player_destroyed")  # Notify other objects
