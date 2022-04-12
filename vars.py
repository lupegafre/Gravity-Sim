scale = 1000000 # MAIN SCALE, meters to 1 pixel
diameter_scale = scale / 1000 # SCALE FOR BODY DIAMETER

screen_width = 1400
screen_height = 800

ui_height = 50 # SIZE OF THE UI TAB

num = 1500 # SIZE OF THE UNIVERSE
boundary = (-num, num, -num, num, -num, num) # -x, +x, -y, +y, -z, +z

framerate = 144 # in Hz, can be higher than set value for some reason
timescale = 1 # SIMULATION SPEED
physics_step = 10 # PHYSICS CALCULATIONS PER FRAME

G = 6.67408 * (10 ** -11) # GRAVITATIONAL CONSTANT
gravitational_force_limit = 1 * (10 ** 23) # GRAVITATIONAL FORCE LIMIT, to avoid weird behaviour when close
elasticity = 1 # BODY "ELASTICITY" FOR COLLISIONS

# BODY TRAILS
trail_length = 500

# COMET TAIL
fadeaway = 0.95 # how quickly tail fades away
fadeaway_size = 1000
comet_tail_size = 100

vector_scale = 5 # SCALE OF VELOCITY AND ACCELERATION VECTORS

number_of_proc_gen_bodies = 0 # NUMBER OF RANDOM BODIES

collisions_for_destruction = 5 # BODY WILL BE DESTROYED IF IT COLLIDES THIS MANY TIMES IN A ROW

grid_width = 50

max_zoom = 10
min_zoom = 0.001

# COLORS
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
yellow = [255, 255, 0]
gray = [121, 121, 121]
light_gray = [175, 175, 175]
white = [255, 255, 255]

# BUTTON RECTS
ui_background = (0, screen_height - ui_height, screen_width, screen_height - ui_height)
button_rect = (screen_width - 200, screen_height - 30, 30, 30)
button_plus_template_rect = ((screen_width / 2) - 10, 95, 30, 30)
button_minus_template_rect = ((screen_width / 2) + 150, 95, 30, 30)

# DEBUG
debug_velocity = 12.5