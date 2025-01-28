extends CharacterBody2D

### objects imports ###
var Bullet: PackedScene = preload("res://objs/Bullet.tscn")

### constants ###
@export var thrust = 1000  # The force applied when accelerating
@export var max_speed = 100  # Maximum speed the ship can reach
@export var friction = 200  # Friction applied when no input is given
@export var dash_force = 400  # Force applied during a dash
@export var dash_duration = 0.05  # Duration of the dash in seconds
@export var rotation_speed = 20  # Controls how fast the ship rotates instantly

@onready var gun = $Gun
@onready var gundir = $GunDir

signal player_fired_bullet(bullet, position, direction)

### Variables ###
var dash_timer = 0.0

### Main movement function ###
func _physics_process(delta):

	var mouse_position = get_global_mouse_position()
	rotation = (mouse_position - global_position).angle() + PI / 2
	
	var input_direction = Vector2.ZERO
	if Input.is_action_pressed("up"):
		input_direction = -transform.y  # Forward thrust
	if Input.is_action_pressed("down"):
		input_direction = transform.y  # Backward thrust
	
	if dash_timer <= 0.0:  # Only allow dashing if the dash cooldown has ended
		if Input.is_action_just_pressed("left"):
			velocity += -transform.x * dash_force  # Dash to the left
			dash_timer = dash_duration
		elif Input.is_action_just_pressed("right"):
			velocity += transform.x * dash_force  # Dash to the right
			dash_timer = dash_duration


	velocity += input_direction * thrust * delta
	
	if velocity.length() > max_speed:
		velocity = velocity.normalized() * max_speed
	
	if input_direction == Vector2.ZERO and dash_timer <= 0.0:
		velocity = velocity.move_toward(Vector2.ZERO, friction * delta)

	if dash_timer > 0.0:
		dash_timer -= delta
	
	# Move the ship
	move_and_slide()

### Shooting function ###
func shoot():
	var bullet = Bullet.instantiate()
	var direction = (gundir.global_position - gun.global_position).normalized()
	emit_signal("player_fired_bullet", bullet, gun.global_position, direction)

### Input handler ###
func _unhandled_input(event):
	if event.is_action_released("shoot"):
		shoot()
