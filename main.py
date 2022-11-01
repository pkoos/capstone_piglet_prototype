import pyglet
"""
	moving right == subtract one from x
	as you move right, everything else moves left
"""

"""
	moving left == add one to x
	as you move left, everything else moves right
"""

current_x = 0
current_y = 0

winsize_x = 960
winsize_y = 540

window_center_width = winsize_x // 2
window_center_height = winsize_y // 2

border_x_slow = winsize_x // 4
border_x_fast = winsize_x // 8 + border_x_slow

border_y_slow = winsize_y // 4
border_y_fast = winsize_y // 8 + border_y_slow

h_movement = 0
v_movement = 0

fast_movement = 6
slow_movement = 3

def main():
	window = pyglet.window.Window(width = winsize_x, height = winsize_y)

	lbl_title = pyglet.text.Label("Hello World", font_name="Times New Roman",
														font_size=36, x = window.width // 2, y = window.height // 2,
														anchor_x = "center", anchor_y = "center")
	
	lbl_win_height = pyglet.text.Label(f"window height: {window.height}",
														 font_size = 20, x = 50, y = 100)
	
	lbl_win_width = pyglet.text.Label(f"window width: {window.width}",
														font_size = 20, x = 50, y = 75)
	
	lbl_x_pos = pyglet.text.Label(f"Mouse X Position: {current_x}", font_size = 16,
														 x = 25, y = 470, anchor_x = "left")
	
	lbl_y_pos = pyglet.text.Label(f"Mouse Y Position: {current_y}", font_size = 16,
														 x = 25, y = 450, anchor_x = "left")
	
	lbl_x_title_pos = pyglet.text.Label(f"Title X Position: {lbl_title.x}", font_size = 16,
														 x = 25, y = 430, anchor_x = "left")
	
	lbl_y_title_pos = pyglet.text.Label(f"Title Y Position: {lbl_title.y}", font_size = 16,
														 x = 25, y = 410, anchor_x = "left")

	lbl_h_zone = pyglet.text.Label("Horizontal Zone", font_size = 16, x = 75, y = 25, anchor_x = "left")
	
	lbl_v_zone = pyglet.text.Label("Vertical Zone", font_size = 16, x = 75, y = 50, anchor_x = "left")

	border_slow = pyglet.shapes.Rectangle(
		window_center_width - border_x_slow, 
		window_center_height - border_y_slow, 
		2 * border_x_slow, 
		2 * border_y_slow,
		color = (75, 75, 75, 75)
	)

	border_fast = pyglet.shapes.Rectangle(
		window_center_width - border_x_fast, 
		window_center_height - border_y_fast, 
		2 * border_x_fast, 
		2 * border_y_fast,
		color = (125, 125, 125, 125)
	)

	ui_elements = [ lbl_title, lbl_win_height, lbl_win_width, lbl_x_pos, 
									lbl_y_pos, lbl_h_zone, lbl_v_zone, lbl_x_title_pos, 
									lbl_y_title_pos, border_slow, border_fast ]


	@window.event
	def on_draw():
		window.clear()
		
		print(f"h_movement: {h_movement} v_movement: {v_movement}")
		print(f"current_x: {current_x} current_y: {current_y}")
		print(f"lbl_title.x: {lbl_title.x} lbl_title.y: {lbl_title.y}")
		print(f"title height: {lbl_title.content_height} title width: {lbl_title.content_width}")

		if not moving_past_horizontal_edge(lbl_title.x, h_movement):
			lbl_title.x += h_movement
		
		if not moving_past_vertical_edge(lbl_title.y, v_movement):
			lbl_title.y += v_movement
		
		lbl_x_title_pos.text = f"Title X position: {lbl_title.x}"
		lbl_y_title_pos.text = f"Title Y position: {lbl_title.y}"

		for element in ui_elements:
			element.draw()
	
	@window.event
	def on_mouse_motion(x, y, dx, dy):
		global current_x
		current_x = x
		global current_y
		current_y = y

		lbl_x_pos.text = f"Mouse X Position: {x}"
		lbl_y_pos.text = f"Mouse Y Position: {y}"
		
		h_zone = horizontal_zone(x)
		v_zone = vertical_zone(y)
		lbl_h_zone.text = f"Horizontal zone: {h_zone}"
		lbl_v_zone.text = f"Vertical zone: {v_zone}"

		global h_movement
		h_movement = horizontal_movement(h_zone)
		global v_movement
		v_movement = vertical_movement(v_zone)


	@window.event
	def on_mouse_leave(x, y):
		global h_movement
		h_movement = 0
		global v_movement
		v_movement = 0

	pyglet.app.run()

def moving_past_horizontal_edge(x, h_movement):
	return at_left_edge_moving_left(x, h_movement) or at_right_edge_moving_right(x, h_movement)

def moving_past_vertical_edge(y, v_movement):
	return at_bottom_edge_moving_down(y, v_movement) or at_top_edge_moving_up(y, v_movement)

def at_left_edge_moving_left(x, h_movement):
	return x < 150 and h_movement < 0

def at_right_edge_moving_right(x, h_movement):
	return x > (winsize_x - 150) and h_movement > 0

def at_bottom_edge_moving_down(y, v_movement):
	return y < 25 and v_movement < 0

def at_top_edge_moving_up(y, v_movement):
	return y > (winsize_y - 25) and v_movement > 0

def vertical_movement(zone_string):
	match zone_string:
			case "fast bottom":
				v_movement = fast_movement
			case "fast top":
				v_movement = -fast_movement
			case "slow bottom":
				v_movement = slow_movement
			case "slow top":
				v_movement = -slow_movement
			case "top":
				v_movement = 0
			case "bottom":
				v_movement = 0
			case _:
				v_movement = 0
	
	return v_movement

def horizontal_movement(zone_string):
	match zone_string:
			case "fast left":
				h_movement = fast_movement
			case "fast right":
				h_movement = -fast_movement
			case "slow left":
				h_movement = slow_movement
			case "slow right":
				h_movement = -slow_movement
			case "left":
				h_movement = 0
			case "right":
				h_movement = 0
			case _:
				h_movement = 0
	
	return h_movement

def horizontal_zone(x):

	if x < (window_center_width - border_x_fast):
		zone_speed = "fast"
	elif x < (window_center_width - border_x_slow):
		zone_speed = "slow"
	elif x < (window_center_width + border_x_slow):
		zone_speed = ""
	elif x < (window_center_width + border_x_fast):
		zone_speed = "slow"
	else:
		zone_speed = "fast"
	
	screen_side = "left" if x < window_center_width else "right"

	return f"{zone_speed} {screen_side}"

def vertical_zone(y):
	if y < (window_center_height - border_y_fast):
		zone_speed = "fast"
	elif y < (window_center_height - border_y_slow):
		zone_speed = "slow"
	elif y < (window_center_height + border_y_slow):
		zone_speed = ""
	elif y < (window_center_height + border_y_fast):
		zone_speed = "slow"
	else:
		zone_speed = "fast"
	
	screen_side = "bottom" if y < window_center_height else "top"

	return f"{zone_speed} {screen_side}"

if __name__ == "__main__":
	main()
