import math
# from classes import CelestialBody
from vars import *
from random import randrange as rand



# CALCULATE GRAVITATIONAL FORCE
def gravitational_force(M, m, d):
	force = 0
	if d != 0:
		force = (G * M * m) / (d ** 2) # real-world
		# force = (G * M * m) / (d ** 1.9) # little bit less than real-world already has a HUGE impact
		# force = (G * M * m) / (d ** 2.1)

	if force > gravitational_force_limit:
		force = gravitational_force_limit

	# print(force)

	return force

#—————————————————————————————————————————————————————————————————————————————————————————————————


# DETECT MOUSE HOVER
# only detects hover over square hitbox, not circle
def mouse_hover( # not 3D
	mouseX, 
	mouseY, 
	body,
	camX: float = 0.0,
	camY: float = 0.0,
	zoom: float = 1.0
	):

	hover = False
	radius = (body.diameter / 2) / diameter_scale # scale in pixels...?

	if body.diameter < 5000: # make hitbox bigger if body too small
		radius = 5000 / 2000

	if mouseX >= (body.x - radius + camX) * zoom and mouseX <= (body.x + radius + camX) * zoom:
		if mouseY >= (body.y - radius + camY) * zoom and mouseY <= (body.y + radius + camY) * zoom:
			hover = True
	return hover

#—————————————————————————————————————————————————————————————————————————————————————————————————


# DETECT MOUSE CLICKS
def mouse_click(
	mouseX, 
	mouseY, 
	camX: float = 0.0,
	camY: float = 0.0
	):

	click = 0

	if mouseX >= button_rect[0] and mouseX <= button_rect[0] + button_rect[2]:
		if mouseY >= button_rect[1] and mouseY <= button_rect[1] + button_rect[3]:
			click = 1

	if mouseX >= button_plus_template_rect[0] and mouseX <= button_plus_template_rect[0] + button_plus_template_rect[2]:
		if mouseY >= button_plus_template_rect[1] and mouseY <= button_plus_template_rect[1] + button_plus_template_rect[3]:
			click = 2

	if mouseX >= button_minus_template_rect[0] and mouseX <= button_minus_template_rect[0] + button_minus_template_rect[2]:
		if mouseY >= button_minus_template_rect[1] and mouseY <= button_minus_template_rect[1] + button_minus_template_rect[3]:
			click = 3

	return click

#—————————————————————————————————————————————————————————————————————————————————————————————————


# RETURN RANDOM RGB COLOR
def random_color():
	color = tuple[int, int, int]
	R = rand(0, 255, 1)
	G = rand(0, 255, 1)
	B = rand(0, 255, 1)
	color = [R, G, B]

	return color

#—————————————————————————————————————————————————————————————————————————————————————————————————


# RETURN DISTANCE BETWEEN 2 BODIES, EXCLUDING Z AXIS
def distance(
	body1, 
	body2, 
	real_scale: bool = True
	): # in meters

	distanceX = body1.x - body2.x
	distanceY = body1.y - body2.y
	distance = math.sqrt(distanceX ** 2 + distanceY ** 2)
	if real_scale:
		distance *= scale
	return distance

#—————————————————————————————————————————————————————————————————————————————————————————————————


# RETURN DISTANCE BETWEEN 2 BODIES, INCLUDING Z AXIS
def threeD_distance(
	body1, 
	body2, 
	real_scale: bool = True
	):

	distanceX = body1.x - body2.x
	distanceY = body1.y - body2.y
	distanceZ = body1.z - body2.z
	distance = math.sqrt((distanceX ** 2) + (distanceY ** 2) + (distanceZ ** 2))
	if real_scale:
		distance *= scale
	return distance

#—————————————————————————————————————————————————————————————————————————————————————————————————


# RETURN VECTOR MODULE BASED ON COMPONENTS
def vector_module(x, y):
	module = math.sqrt((x ** 2) + (y ** 2))
	return module

#—————————————————————————————————————————————————————————————————————————————————————————————————


# RETURN VECTOR COMPONENTS IN X AND Y AXES
def vector_components(
	body, 
	vector: str = 'Velocity',
	scale: int = scale # not being used, implement later
	):

	x = 0.0
	y = 0.0

	mod = 0
	angle = 0

	if vector == 'Velocity':
		mod = body.velocityModule
		angle = body.velocityAngle

	elif vector == 'Acceleration':
		mod = body.accelerationModule
		angle = body.accelerationAngle

	x = (mod * math.cos(angle))
	y = (mod * math.sin(angle))

	return x, y

#—————————————————————————————————————————————————————————————————————————————————————————————————


# RETURN INFO ABOUT BODY
def get_body_info(
	body, 
	info: int = -1
	):

	string = ''

	if info == 0:
		string = body.name
	elif info == 1:
		string = f'{body.mass:.1E} kg'
	elif info == 2:
		string = f'X{round(body.x)} Y{round(body.y)} Z{round(body.z)}'
	elif info == 3:
		velocityX = body.velocityModule * math.cos(body.velocityAngle)
		velocityY = body.velocityModule * math.sin(body.velocityAngle)
		string = f'vX{velocityX:.3f} vY{velocityY:.3f} vZ{body.velocityZ:.3f}'
		string =  f'vMod{body.velocityModule:.3f}   vAng{math.degrees(body.velocityAngle):.3f}°'
	elif info == 4:
		accelerationX = body.accelerationModule * math.cos(body.accelerationAngle)
		accelerationY = body.accelerationModule * math.sin(body.accelerationAngle)
		string = f'aX{accelerationX:.3f} aY{accelerationY:.3f} aZ{body.accelerationZ:.3f}'
		string = f'aMod{body.accelerationModule:.3f}   aAng{math.degrees(body.accelerationAngle):.3f}° aZ{body.accelerationZ:.3f}'
	elif info == 5:
		pass
	else:
		string = f'{body.name}\n X{body.x:.3f} Y{body.y:.3f}\n vX{body.velocityX} vY{body.velocityY}'
	return string

#—————————————————————————————————————————————————————————————————————————————————————————————————


# RETURN VELOCITY NEEDED TO STAY IN ORBIT
def orbital_velocity(M, d):
	velocity = 0
	if d != 0:
		velocity = (G * M / d) ** 0.5
	velocity /= 1000000 # 100 works better than 1000 even though it shouldn't
	return velocity

#—————————————————————————————————————————————————————————————————————————————————————————————————


# CHECK IF BODY IS ON SCREEN
def on_screen(body):
	to_return = False
	if body.x + (body.diameter / 2) / diameter_scale > 0 and body.x - (body.diameter / 2) / diameter_scale < screen_width:
		if body.y + (body.diameter / 2) / diameter_scale > 0 and body.y - (body.diameter / 2) / diameter_scale < screen_height - ui_height:
			to_return = True

	return to_return

#—————————————————————————————————————————————————————————————————————————————————————————————————


# RETURN VELOCITIES BASED ON ELASTIC COLLISION BETWEEN 2 BODIES
def elastic_collision(vA, mA, vB, mB):
	v1 = 0
	v2 = 0

	v1 = ((mA - mB) / (mA + mB)) * vA + ((2 * mB) / (mA + mB)) * vB
	v2 = ((2 * mA) / (mA + mB)) * vA + ((mB - mA) / (mA + mB)) * vB

	v1 *= elasticity
	v2 *= elasticity

	return v1, v2

#—————————————————————————————————————————————————————————————————————————————————————————————————


# LINEAR INTERPOLATION
def lerp(mini, maxi, val):
	x = ((maxi - mini) * val) + mini
	return x 

#—————————————————————————————————————————————————————————————————————————————————————————————————


# RETURN SIGN OF A NUMBER (+ OR -)
def sign(num):
	if num > 0:
		return 1
	elif num < 0:
		return -1
	else:
		return 0

#—————————————————————————————————————————————————————————————————————————————————————————————————


# GENERATE BACKGROUND STARS
def starry_background(
	number_stars: int = 100,
	layer_index: int = 0
	):

	layer_index += 6 # not an efficient solution
	stars = []
	for i in range(number_stars):
		rand_x = rand(boundary[0] * layer_index, boundary[1] * layer_index)
		rand_y = rand(boundary[2] * layer_index, boundary[3] * layer_index)
		rand_r = rand(1, 5)
		stars.append([rand_x, rand_y, rand_r])
		# layer_index += 1

	return stars


#—————————————————————————————————————————————————————————————————————————————————————————————————


# PRINT INFO
def debug_printer(strings: list = []):
	to_return = []
	for string in strings:
		to_return.append(str(string))
	print('   '.join(to_return))

#—————————————————————————————————————————————————————————————————————————————————————————————————


# DOT PRODUCT BETWEEN TWO VECTORS
def vectors_dot(body1, body2):
	x = body1.x * body2.x
	y = body1.y * body2.y
	z = body1.z * body2.z
	return x * y * z

#—————————————————————————————————————————————————————————————————————————————————————————————————


# CROSS PRODUCT BETWEEN TWO VECTORS
def vectors_cross(body1, body2):
	x = body1.y * body2.z - body1.z * body2.y
	y = body1.z * body2.x - body1.x * body2.z
	z = body1.x * body2.y - body1.y * body2.x
	return (x, y, z) # is this correct?

#—————————————————————————————————————————————————————————————————————————————————————————————————
#—————————————————————————————————————————————————————————————————————————————————————————————————

