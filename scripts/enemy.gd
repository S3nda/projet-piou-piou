## Enemy.gd - AI-controlled enemy spaceship
## ------------------------------------------------------------
## This script defines an enemy spaceship that moves towards a player,
## stops at a specified distance, and periodically fires projectiles.
## It also handles collisions with player bullets.
## ------------------------------------------------------------

class_name Enemy extends CharacterBody2D

## Exported properties (configurable in the Godot editor)
@export var target: Node2D  ## Reference to the player spaceship
@export var acceleration: float = 10.0  ## Gradual acceleration
@export var max_speed: float = 200.0  ## Maximum movement speed
@export var rotation_speed: float = 5.0  ## Speed of gradual rotation
@export var stop_distance: float = 500.0  ## Distance at which the enemy stops moving
@export var fire_rate: float = 1.5  ## Time between each shot (in seconds)
@export var recoil_force: float = 0  ## Knockback applied after shooting

## Bullet configuration
var Bullet: PackedScene = preload("res://objs/bullets/bullet_enemy.tscn")
var can_shoot: bool = true  ## Controls firing cooldown

## Node references
@onready var gun: Marker2D = $Gun  ## Position where bullets spawn
@onready var gundir: Marker2D = $GunDir  ## Direction the bullets should follow

## Called every physics frame to update movement and check collisions
func _physics_process(delta: float) -> void:
	if not target:
		return

	# Calculate direction and distance to the target
	var direction_to_target: Vector2 = (target.global_position - global_position).normalized()
	var distance_to_target: float = global_position.distance_to(target.global_position)

	# Rotate smoothly towards the target
	var target_angle: float = direction_to_target.angle() + PI / 2
	rotation = lerp_angle(rotation, target_angle, rotation_speed * delta)

	# Move towards the target unless within stop distance
	if distance_to_target > stop_distance:
		velocity = velocity.lerp(direction_to_target * max_speed, acceleration * delta)
	else:
		velocity = velocity.move_toward(Vector2.ZERO, acceleration * delta)  # Gradual slowdown

	# Handle movement and collisions
	var collision := move_and_collide(velocity * delta)
	if collision:
		_handle_collision(collision)

	# Shoot at the player if within range
	if can_shoot and distance_to_target <= stop_distance:
		shoot()

## Handles collision events
func _handle_collision(collision: KinematicCollision2D) -> void:
	var collider: Object = collision.get_collider()
	if collider and collider.is_in_group("player_bullets"):
		print("Hit by player bullet: ", collider.name)
		collider.queue_free()
		die()

## Handles the enemy shooting logic
func shoot() -> void:
	can_shoot = false  # Prevent consecutive shots before cooldown

	# Instantiate and configure the bullet
	var bullet: Node2D = Bullet.instantiate()
	bullet.global_position = gun.global_position  # Set starting position
	var bullet_direction: Vector2 = (gundir.global_position - gun.global_position).normalized()
	bullet.set_direction(bullet_direction)
	bullet.add_to_group("enemy_bullets")  # Add to collision group

	# Apply recoil effect to the enemy
	velocity -= bullet_direction * recoil_force

	# Add bullet to the scene
	get_parent().add_child(bullet)

	# Start cooldown timer
	await get_tree().create_timer(fire_rate).timeout
	can_shoot = true

## Handles the destruction of the enemy
func die() -> void:
	queue_free()  # Remove the enemy from the scene
