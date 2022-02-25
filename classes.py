from vars import *
from functions import *



class CelestialBody:
	def __init__(self,  # use *args or 
		name: str,
		mass: float = 0.0,  # in 10^24 kg
		diameter: float = 0.0,
		x: float = 0.0,
		y: float = 0.0,
		z: float = 0.0,
		velocityX: float = 0,
		velocityY: float = 0,
		velocityZ: float = 0,
		color: tuple = [255, 255, 255],
		is_comet: bool = False,
		*args
		):

		self.name = name
		self.mass = mass * (10 ** 24)
		self.diameter = diameter

		self.accelerationModule = vector_module(0, 0)
		self.accelerationAngle = math.atan2(0, 0)
		self.accelerationZ = 0.0

		self.velocityX = velocityX
		self.velocityY = velocityY
		self.velocityZ = velocityZ

		self.velocityModule = vector_module(velocityX, velocityY)
		self.velocityAngle = math.atan2(velocityY, velocityX)
		self.originalVelocityModule = self.velocityModule
		self.originalVelocityAngle = self.velocityAngle

		self.x = x
		self.y = y
		self.z = z

		self.originalPosX = x
		self.originalPosY = y
		self.originalPosZ = z

		self.color = color

		self.circleOfInfluence = []

		self.forceSummationX = 0
		self.forceSummationY = 0
		self.forceSummationZ = 0

		self.is_comet = is_comet

		self.previous_positions = []
		self.comet_trail_positions = []

		if self.is_comet:
			self.comet_trail_positions = []
			for i in range(comet_tail_size):
				self.comet_trail_positions.append((0, 0))

		self.has_gravity = True
		self.can_move = True
		self.influenced_by_gravity = True
		self.has_propulsion = False # for vehicles and stuff
		self.has_reaction_wheels = False

		self.propulsion_force = 0
		self.reaction_wheels_force = 0

		self.collisions_in_period = []

		self.destructible = True

		self.debug_verbose = False

	# LIST OF BODIES' GRAVITIES THAT INFLUENCE SELF
	def set_circle_of_influence(self, bodies: list = []):
		for body in bodies:
			self.circleOfInfluence.append(body)
		self.circleOfInfluence = list(set(self.circleOfInfluence)) # uniques only

	def update_acceleration(self):
		if self.influenced_by_gravity:
			for body in self.circleOfInfluence:
				d = threeD_distance(body, self)
				gravitationalForce = gravitational_force(self.mass, body.mass, d)

				angle = math.atan2((body.y - self.y), (body.x - self.x)) # atan2 is from -pi to pi (360°)

				self.forceSummationX += gravitationalForce * math.cos(angle)
				self.forceSummationY += gravitationalForce * math.sin(angle)

				angleZ = math.atan2((body.y - self.y), (body.z - self.z)) # falsch?
				self.forceSummationZ += gravitationalForce * math.cos(angleZ)

		else:
			self.forceSummationX = 0
			self.forceSummationY = 0
			self.forceSummationZ = 0

		accelerationX = self.forceSummationX / self.mass
		accelerationY = self.forceSummationY / self.mass	
		self.accelerationZ = self.forceSummationZ / self.mass

		if self.debug_verbose:
			print(f'accelX{accelerationX:3f} accelY{accelerationY:3f} accelZ{self.accelerationZ:3f}')					

		self.accelerationModule = vector_module(accelerationX, accelerationY)
		self.accelerationAngle = math.atan2(accelerationY, accelerationX)

		self.forceSummationX = 0
		self.forceSummationY = 0
		self.forceSummationZ = 0

	def update_velocity(self,  # is this necessary?
		current_timescale, 
		current_framerate: float = framerate
		):

		if self.can_move:
			# try to do this without getting vector components
			accelerationX = self.accelerationModule * math.cos(self.accelerationAngle)
			accelerationY = self.accelerationModule * math.sin(self.accelerationAngle)
			velocityX = self.velocityModule * math.cos(self.velocityAngle) + accelerationX * (current_timescale / current_framerate)
			velocityY = self.velocityModule * math.sin(self.velocityAngle) + accelerationY * (current_timescale / current_framerate)
			self.velocityZ = self.velocityZ + self.accelerationZ * (current_timescale / current_framerate)

			self.velocityModule = vector_module(velocityX, velocityY)
			self.velocityAngle = math.atan2(velocityY, velocityX)

			if self.debug_verbose:
				print(f'velX{velocityX:3f} velY{velocityY:3f} velZ{self.velocityZ:3f}')	

		else:
			self.velocityModule = 0
			self.velocityAngle = 0
			self.velocityZ = 0

	def update_position(self, 
		current_timescale, 
		current_framerate: float = framerate
		):

		if self.can_move:
			accelerationX = self.accelerationModule * math.cos(self.accelerationAngle)
			accelerationY = self.accelerationModule * math.sin(self.accelerationAngle)
			self.x = self.x + self.velocityModule * math.cos(self.velocityAngle) * (current_timescale / current_framerate) + (accelerationX * (current_timescale / current_framerate) ** 2) / 2
			self.y = self.y + self.velocityModule * math.sin(self.velocityAngle) * (current_timescale / current_framerate) + (accelerationY * (current_timescale / current_framerate) ** 2) / 2		
			self.z = self.z + self.velocityZ * (current_timescale / current_framerate) + (self.accelerationZ * (current_timescale / current_framerate) ** 2) / 2		

			if self.debug_verbose:
				print(f'X{self.x:3f} Y{self.y:3f} Z{self.z:3f}')		

			# COMET TAIL
			if self.is_comet:
				for i in range(len(self.comet_trail_positions) - 1, -1, -1): 
					if i == 0:
						self.comet_trail_positions[i] = (self.x, self.y, self.z)
					else:
						self.comet_trail_positions[i] = self.comet_trail_positions[i - 1]

			# BODY TRAIL
			self.previous_positions.append((self.x, self.y, self.z))
			if len(self.previous_positions) > trail_length: # limit size for performance reasons
				self.previous_positions.pop(0)

		else:
			self.x = self.originalPosX
			self.y = self.originalPosY
			self.z = self.originalPosZ

	def set_velocity(self, mod, angle):
		self.velocityModule = mod
		self.velocityAngle = angle

	def reset_body(self):
		self.velocityModule = self.originalVelocityModule
		self.velocityAngle = self.originalVelocityAngle
		self.x = self.originalPosX
		self.y = self.originalPosY
		self.accelerationModule = 0
		self.accelerationAngle = 0

	def reset_trail(self):
		self.previous_positions.clear()
		if self.is_comet:
			for i in range(len(self.previous_positions)):
				self.previous_positions[i] = (self.x, self.y)

	def propulsion(self, value):
		self.propulsion_force += value

	def reaction_wheels(self, value):
		self.reaction_wheels_force += value

	def destroy(self):
		self.x = 0
		self.y = 0
		self.velocityAngle = 0
		return self

	def generate_collision_list(self, body_list):
		for i in range(len(body_list) - 1):
			self.collisions_in_period.append(0)

#—————————————————————————————————————————————————————————————————————————————————————————————————
#—————————————————————————————————————————————————————————————————————————————————————————————————


class Camera():
	def __init__(self,
		x: float = screen_width / 2,
		y: float = screen_height / 2,
		zoom: float = 1.0
		):

		self.x = x
		self.y = y
		self.zoom = zoom
		self.zoom_in = False
		self.rotation_y = 0 # math.pi / 2 to start at 90°

	def reset(self):
		self.x = screen_width / 2
		self.y = screen_height / 2
		self.zoom = 1
		self.rotation_y = 0