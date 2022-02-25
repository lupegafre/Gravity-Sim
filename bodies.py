from vars import *
from classes import *

import random



# store all bodies more like sun
sun = [
	'Sun', 
	1988500, 
	1390000, 
	0, 
	0, 
	0, 
	0, 
	0,
	0,
	yellow
	]

mercury = [
	'Mercury', 
	0.330, 
	4879, 
	-57000, 
	0, 
	0, 
	0, 
	0, 
	0,
	red
	]

venus = [
	'Venus', 
	0.33, 
	4879, 
	0, 
	-108000, 
	0, 
	0, 
	0, 
	0, 
	green
	]

earth = [
	'Earth', 
	5.9724, 
	12756, 
	0, 
	0, 
	0, 
	0, 
	0,
	0,
	blue
	]
earth2 = [
	'Earth2', 
	5.9724, 
	12756, 
	200, 
	0, 
	0, 
	0,
	0,
	0, 
	blue
	]
earth3 = [
	'Earth3', 
	5.9724, 
	12756, 
	-200, 
	0, 
	0, 
	0,
	0,
	0, 
	blue
	]

moon = [
	'Moon', 
	0.07346, 
	13475, 
	300, 
	0, 
	0, 
	0, 
	1.167,
	0,
	white
	]
moon2 = [
	'Moon2', 
	0.07346, 
	13475, 
	-300, 
	0, 
	0, 
	0, 
	-1.167,
	0,
	white
	]
moon3 = [
	'Moon3', 
	0.07346, 
	13475, 
	0, 
	-300, 
	0, 
	1.167, 
	0,
	0,
	white
	]
moon4 = [
	'Moon4', 
	0.07346, 
	13475, 
	0, 
	300, 
	0, 
	-1.167, 
	0,
	0,
	white
	]

moon5 = [
	'Moon5', 
	0.07346, 
	3475, 
	-600, 
	0, 
	0, 
	0, 
	-5,
	0,
	white
	]
moon6 = [
	'Moon6', 
	0.07346, 
	3475, 
	600, 
	0, 
	0, 
	0,
	5,
	0, 
	white
	]

# "3D" moons
moon7 = [
	'Moon7', 
	0.07346, 
	25475, 
	800, 
	0, 
	0, 
	0, 
	debug_velocity,
	0,
	green
	]
moon8 = [
	'Moon8', 
	0.07346, 
	25475, 
	-800, 
	0, 
	0, 
	0,
	-debug_velocity,
	0, 
	white
	]

moon9 = [
	'Moon9', 
	0.07346, 
	25475, 
	0, 
	0, 
	600, 
	0, 
	-20.5,
	0,
	red
	]
moon10 = [
	'Moon10', 
	0.07346, 
	25475, 
	0, 
	0, 
	-600, 
	0, 
	20.5,
	0,
	yellow
	]

moon11 = [
	'Moon11', 
	0.07346, 
	25475, 
	0, 
	0, 
	-800, 
	debug_velocity, 
	0,
	0,
	red
	]
moon12 = [
	'Moon12', 
	0.07346, 
	25475, 
	0, 
	0, 
	800, 
	-debug_velocity,
	0,
	0, 
	light_gray
	]

mars = [
	'Mars', 
	0.642, 
	6792, 
	0, 
	-228000, 
	0, 
	0, 
	0,
	0,
	red
	]

jupiter = [
	'Jupiter', 
	1898, 
	142984, 
	0, 
	-779000, 
	0, 
	0, 
	0,
	0,
	blue
	]
jupiter2 = [
	'Jupiter', 
	1898, 
	142984, 
	0, 
	0, 
	0, 
	0, 
	0,
	0,
	blue
	]
jupiter3 = [
	'Jupiter', 
	1898, 
	142984, 
	0, 
	0, 
	0, 
	0, 
	0,
	0,
	blue
	]

saturn = [
	'Saturn', 
	568, 
	12536, 
	25000, 
	0, 
	0, 
	0, 
	0,
	0,
	gray
	]
uranus = [
	'Uranus', 
	86.8, 
	51118, 
	50000, 
	100, 
	0, 
	0,
	0,
	0, 
	green
	]
neptune = [
	'Neptune', 
	102, 
	49528, 
	-70000, 
	0, 
	0, 
	0, 
	0,
	0,
	blue
	]
pluto = [
	'Pluto', 
	0.013, 
	2376, 
	52222, 
	522222, 
	0, 
	0,
	0,
	0, 
	blue]

comet = [
	'Comet', 
	0.043, 
	15000, 
	0, 
	400, 
	0, 
	1.5, 
	0,
	0,
	white]

rocket = [
	'Rocket', 
	0.0001, 
	2000, 
	100, 
	100, 
	0, 
	0, 
	0,
	0,
	blue]

test_body = [
	'Test body', 
	2000, 
	20000, 
	0, 
	0, 
	0, 
	0, 
	0,
	0,
	red
	]
test_body2 = [
	'Test body2', 
	2000, 
	20000, 
	200, 
	200, 
	0, 
	0, 
	0,
	0,
	red
	]
test_body3 = [
	'Test body3', 
	2000, 
	20000, 
	-2800, 
	0, 
	0, 
	-5, 
	-5,
	0,
	red
	]

black_hole = [
	'Supermassive Black Hole', 
	800000, 
	2000, 
	0, 
	0, 
	0, 
	0, 
	0,
	0,
	gray
	]

earth_tim = [
	'Earth', 
	5.9724, 
	12756, 
	0, 
	-150000, 
	30, 
	0, 
	0,
	0,
	blue
	]

moons = [earth, moon, moon2, moon3, moon4]
earths = [earth2, earth3, moon, moon2, moon3, moon4]
solar_system = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]
test_system = [earth, moon, moon3, jupiter, saturn, mercury]
test_system_2 = [moon, moon2, moon3, moon4, black_hole]
test_system_3 = [jupiter2, moon5, moon6]
test_system_4 = [jupiter3, moon7, moon8, moon9, moon10] # original is [jupiter3, moon7, moon8, moon9, moon10]
test_system_5 = [jupiter3, moon11, moon12] # , moon11, moon12
test_system_5 = [jupiter3, moon7, moon8,moon11, moon12]

tim = [sun, earth_tim, mars, venus, mercury]

def proc_gen_body( 
	i: int = 0, 
	exclusion_list_x: list = [0],
	exclusion_list_y: list = [0],
	exclusion_list_d: list = [0]
	):
	name = f'Unidentified{i + 1}'
	mass = random.triangular(0.01,2000)
	diameter = random.randrange(1000, 55000)
	vX = random.triangular(-5, 5, 0)
	vY = random.triangular(-5, 5, 0)

	# not taking diameter into consideration, only exact coords
	x = random.randrange(boundary[0], boundary[1])
	y = random.randrange(boundary[2], boundary[3])

	color = random_color()
	is_comet = bool(random.getrandbits(1))

	return name, mass, diameter, vX, vY, x, y, color, is_comet