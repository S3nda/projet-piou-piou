extends Control


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.


func resume():
	get_tree().paused = false

func pause():
	get_tree().paused = true
	
func testESC():
	if Input.is_action_just_pressed("escape") and get_tree().paused == false:
		pause()
	elif Input.is_action_just_pressed("escape") and get_tree().paused:
		resume()
		
func _on_resume_pressed():
	resume()
	
func on_restart_pressed():
	get_tree().reload_current_scene()
	
func _on_quit_pressed():
	get_tree().quit()
	
func _process(delta):
	testESC()
	
