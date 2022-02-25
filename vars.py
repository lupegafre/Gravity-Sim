scale = 1000000 # meters to 1 pixel
diameter_scale = scale / 1000 # just used for diameter, otherwise everything would be a single pixel

screen_width = 1400 # or 800
screen_height = 800

ui_height = 50

num = 1000
boundary = (-num, num, -num, num) # -x, +x, -y, +y

framerate = 144 # in Hz, can be higher than set value for some reason
timescale = 1 # sim speed is timescale / framerate
physics_step = 10 # 10 calculations per frame?

G = 6.67408 * (10 ** -11) # gravitational constant
gravitational_force_limit = 1 * (10 ** 23) # works pretty well
elasticity = 1 # planet "elasticity", for collisions

# BODY TRAILS
trail_length = 500
trail_radius = 4 # is this necessary?

# COMET TAIL
fadeaway = 0.95 # how quickly tail fades away
fadeaway_size = 1000
comet_tail_size = 100

vector_scale = 5

number_of_proc_gen_bodies = 0

collisions_for_destruction = 5 # if the same 2 bodies collide collisions_for_destruction times the lighter is absorbed

grid_width = 50 # this is wrong

# max min zoom should depend on boundary size
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

ui_background = (0, screen_height - ui_height, screen_width, screen_height - ui_height)
button_rect = (screen_width - 200, screen_height - 30, 30, 30)
button_plus_template_rect = ((screen_width / 2) - 10, 95, 30, 30)
button_minus_template_rect = ((screen_width / 2) + 150, 95, 30, 30)

# DEBUG
debug_velocity = 12.5