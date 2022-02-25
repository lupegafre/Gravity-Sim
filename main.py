import pygame
from classes import *
from vars import *
from functions import *
from bodies import *

import random


class Game(): # remove this class?
    def __init__(self,
        draw_info_screen: bool = True, 
        draw_screen_lines: bool = True, 
        draw_labels: bool = True, 
        draw_body_lines: bool = True, 
        draw_vectors: bool = True, 
        draw_trails: bool = True
        ):

        pygame.init()
        pygame.display.set_caption('Gravity Sim')
        # pygame.display.set_icon(icon)

        self.title_font = pygame.font.SysFont("monospace", 50)
        self.font = pygame.font.SysFont("monospace", 15)

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.current_framerate = framerate
        self.current_timescale = timescale

        self.current_scale = scale
        self.current_diameter_scale = diameter_scale

        # VARIABLES
        self.draw_info_screen = draw_info_screen
        self.draw_screen_lines = draw_screen_lines
        self.draw_labels = draw_labels
        self.draw_body_lines = draw_body_lines
        self.draw_vectors = draw_vectors
        self.draw_trails = draw_trails

        self.current_vector_scale = vector_scale

        self.background_layers = 3
        self.background = []
        for i in range(self.background_layers):
            self.background.append(starry_background(1000, i)) 

        self.camera = Camera() # testing camera zoom in different start coords
        self.current_body_index = 0
        self.focus_camera_on_body = False
        self.is_lmb_pressed = False
        self.is_rmb_pressed = False
        self.mouse_original_x = 0
        self.mouse_original_y = 0
        self.body_original_x = 0
        self.body_original_y = 0

        self.ui_running = True
        self.game_running = True  
        self.timeElapsed = 0

        self.debug_offset_x = 486
        self.debug_offset_y = 150

        self.to_destroy = []

        self.center_of_mass = (0, 0)

        self.debug_counter = 0

        # LOAD BODY TEMPLATE
        self.templates = [solar_system, moons, earths, tim, test_system, test_system_2, test_system_3, test_system_4, test_system_5] 
        self.template_index = -1

        self.celestialBodyList = []
        self.originalCelestialBodyList = []

        self.render_order = []

        self.populate_procedural_generation()
        self.initialize_simulation()

        # self.set_orbital_velocities()

        self.debug_list = []

        self.main_loop()

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def initialize_simulation(self):
        # CREATE AND ADD BODIES TO LIST
        for body_info in reversed(self.templates[self.template_index]): # reversed to keep first in templates first in sim
            a,b,c,d,e,f,g,h,i,j = body_info  # ugly fix
            self.celestialBodyList.insert(0, CelestialBody(a,b,c,d,e,f,g,h,i,j))
        self.originalCelestialBodyList = self.celestialBodyList.copy()

        # GENERATE COLLISION LIST FOR EACH BODY
        for body in self.celestialBodyList: # there must be a better way of doing this
            body.generate_collision_list(self.celestialBodyList)


        self.labelList = []
        for i, body in enumerate(self.celestialBodyList):

            # GENERATE GRAVITY LIST
            tempList = self.celestialBodyList.copy()
            tempList.pop(i)
            body.set_circle_of_influence(tempList)

            # LABEL LIST FOR EACH BODY, improve
            subList = []
            for i in range(5):
                subList.append(self.font.render(get_body_info(body, i), 1, white))
            self.labelList.append(subList)  

        # DEBUG
        self.celestialBodyList[0].can_move = False
        for body in self.celestialBodyList:
            body.can_move = True

        self.celestialBodyList[1].debug_verbose = False

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def populate_procedural_generation(self):
        for i in range(number_of_proc_gen_bodies):
            name, mass, diameter, vX, vY, x, y, color, is_comet = proc_gen_body(i)
            self.celestialBodyList.append(CelestialBody(name, mass, diameter, vX, vY, x, y, color))   

#—————————————————————————————————————————————————————————————————————————————————————————————————
  

    def renderizer(self):
        render_order = self.celestialBodyList.copy()
        # render_order = reversed(sorted(render_order, key=lambda body: body.z * math.cos(self.camera.rotation_y)))
        # should it be (body.x * math.sin(self.camera.rotation_y) + body.z * math.cos(self.camera.rotation_y))????
        render_order = reversed(sorted(render_order, key=lambda body: (body.x * math.sin(self.camera.rotation_y) + body.z * math.cos(self.camera.rotation_y))))
        for b in render_order: # should take cam rotation into account
            self.draw_body(b)

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_body(self, body): # nothing is working, FIX

        xx = body.x #  * self.camera.zoom?
        xz = body.z #  * self.camera.zoom?
        mod = math.sqrt(xx ** 2 + xz ** 2)
        ang = math.atan2(xz, xx)
        x = mod * math.cos(ang + self.camera.rotation_y)
        y = (body.y + self.camera.y) * self.camera.zoom


        # DRAW TRAILS, completely borked
        # is it possible to render part of it in front and the rest behind something?
        if self.draw_trails: # HUGE performance hit
            if len(body.previous_positions) >= 2:

                camera_positions = []

                for pos in body.previous_positions:
                    trail_mod = math.sqrt(pos[0] ** 2 + pos[2] ** 2)
                    trail_ang = math.atan2(pos[2], pos[0])
                    trail_x = trail_mod * math.cos(trail_ang + self.camera.rotation_y)

                    trail_y = (pos[1] + self.camera.y) * self.camera.zoom
                    camera_positions.append(((trail_x + self.camera.x) * self.camera.zoom, trail_y))

                pygame.draw.lines(self.screen, body.color, False, camera_positions, 2)


        # DRAW COMET TAIL, probably completely broken
        current_fadeaway = 1
        for i in range(len(body.comet_trail_positions)):
            current_color = (body.color[0] * current_fadeaway, body.color[1] * current_fadeaway, body.color[2] * current_fadeaway)
            x = (body.comet_trail_positions[i][0] + self.camera.x) * self.camera.zoom
            y = (body.comet_trail_positions[i][1] + self.camera.y) * self.camera.zoom
            r = (body.diameter * current_fadeaway / 2000) * self.camera.zoom
            pygame.draw.circle(self.screen, current_color, (x, y), r)
            current_fadeaway *= fadeaway

        body_radius = ((body.diameter / 2) / self.current_diameter_scale)
        r = body_radius * lerp(1, 0.1, mod * math.sin(ang + self.camera.rotation_y) / 1000)

        pygame.draw.circle(self.screen, body.color, ((x + self.camera.x) * self.camera.zoom, y), r * self.camera.zoom)

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_body_labels(self, body, i): # repeating code, improve later
        if self.draw_info_screen:
            if self.draw_labels == 0: # don't draw
                pass
            elif self.draw_labels == 1: # draw all
                if len(self.celestialBodyList) <= 10: # don't draw if more than 10 objetcs
                    labelWrap = -40 / self.camera.zoom
                    for j in range(5):
                        self.labelList[i][j] = self.font.render(get_body_info(body, j), 1, white)

                        mod = math.sqrt(body.x ** 2 + body.z ** 2)
                        ang = math.atan2(body.z, body.x)
                        x = mod * math.cos(ang + self.camera.rotation_y)
                        x += (body.diameter / 2) / self.current_diameter_scale

                        y = (body.y + labelWrap + self.camera.y) * self.camera.zoom
                        self.screen.blit(self.labelList[i][j], ((x + self.camera.x + 5) * self.camera.zoom, y))
                        labelWrap += 14 / self.camera.zoom
            elif self.draw_labels == 2: # draw on hover, broken
                if mouse_hover(self.mouseX, self.mouseY, body, self.camera.x, self.camera.y, self.camera.zoom):
                    labelWrap = -40
                    for j in range(5):
                        self.labelList[i][j] = self.font.render(get_body_info(body, j), 1, white)

                        mod = math.sqrt(body.x ** 2 + body.z ** 2)
                        ang = math.atan2(body.z, body.x)
                        x = mod * math.cos(ang + self.camera.rotation_y)
                        x += (body.diameter / 2) / self.current_diameter_scale

                        y = (body.y + labelWrap + self.camera.y) * self.camera.zoom
                        self.screen.blit(self.labelList[i][j], ((x + self.camera.x + 5) * self.camera.zoom, y))
                        labelWrap += 14

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_body_vectors(self, body): # very wrong, not 3D
        if self.draw_vectors:    # still need arrowheads
            
            vx, vy = vector_components(body, 'Velocity')
            vx *= 10 * self.current_vector_scale / 3
            vy *= 10 * self.current_vector_scale / 3
            ax, ay = vector_components(body, 'Acceleration')
            ax *= 10 * self.current_vector_scale * 50
            ay *= 10 * self.current_vector_scale * 50

            # finish 3D
            mod = math.sqrt(body.x ** 2 + body.z ** 2)
            ang = math.atan2(body.z, body.x)
            x = mod * math.cos(ang + self.camera.rotation_y)
            x += (body.diameter / 2) / self.current_diameter_scale


            xi = (x + self.camera.x) * self.camera.zoom
            yi = (body.y + self.camera.y) * self.camera.zoom

            xf = (ax + x + self.camera.x) * self.camera.zoom
            yf = (ay + body.y + self.camera.y) * self.camera.zoom
            pygame.draw.line(self.screen, red, (xi, yi), (xf, yf))

            xf = (vx + x + self.camera.x) * self.camera.zoom
            yf = (vy + body.y + self.camera.y) * self.camera.zoom
            pygame.draw.line(self.screen, green, (xi, yi), (xf, yf))

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_body_distance_lines(self, body):
        if self.draw_body_lines and self.draw_info_screen:
            for body in self.celestialBodyList[self.current_body_index].circleOfInfluence:
                d = distance(self.celestialBodyList[self.current_body_index], body, False)
                line_color = white
                if d >= 200000:
                    line_color = white
                elif d < 200000 and d >= 100000:
                    line_color = green
                elif d < 100000 and d >= 60000:
                    line_color = yellow
                elif d < 60000:
                    line_color = red

                xi = (self.celestialBodyList[self.current_body_index].x + self.camera.x) * self.camera.zoom
                yi = (self.celestialBodyList[self.current_body_index].y + self.camera.y) * self.camera.zoom
                xf = (body.x + self.camera.x) * self.camera.zoom
                yf = (body.y + self.camera.y) * self.camera.zoom
                pygame.draw.line(self.screen, line_color, (xi, yi), (xf, yf))

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def set_orbital_velocities(self): 
        # angle only works for up down left right, for now
        # should automatically set angle, maybe favoring clockwise orbits
        angle = math.pi / 2
        for body in self.celestialBodyList:
            if body.name != self.celestialBodyList[0].name:
                body.set_velocity(orbital_velocity(self.celestialBodyList[0].mass, distance(body, self.celestialBodyList[0])) / 10, angle)
                angle -= math.pi / 2

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_background(self): # not efficient AT ALL ==> O(n²)
        for i in range(self.background_layers): # layers need better centering and sizing
            dimmer = lerp(0.7, 1, math.sin(self.timeElapsed * random.triangular(0.5, 1.5, 1)))
            if i == 0:
                color = (dimmer * 255, dimmer * 255, dimmer * 255)
            elif i == 1:
                color = (dimmer * 105, 0, 0)
            elif i == 2:
                color = (0, dimmer * 155, 0)
            elif i == 3:
                color = (0, 0, dimmer * 155)
            elif i == 4:
                color = (dimmer * 255, dimmer * 255, 0)
            else:
                color = (255, 255, 255)
            for star in self.background[i]:
                # dimmer = lerp(0.7, 1, math.sin(self.timeElapsed * random.triangular(0.5, 1.5, 1)))
                # color = (dimmer * 255, dimmer * 255, dimmer * 255)
                parallax_factor = lerp(0.7, 0.3, (i + 1) / 5)
                x = (star[0] + self.camera.x) * self.camera.zoom * parallax_factor + self.debug_offset_x
                y = (star[1] + self.camera.y) * self.camera.zoom * parallax_factor + self.debug_offset_y

                r = (star[2]) * self.camera.zoom * parallax_factor
                if r < 1:
                    r = 1
                pygame.draw.circle(self.screen, color, (x, y), r)
            # print(f'X{self.debug_offset_x}   Y{self.debug_offset_y}')

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_grid(self): 
        if self.draw_info_screen: # repeating code, improve
            if self.draw_screen_lines == 1: # HUGE performance hit, skip every other line when zoomed out
                # add numbers to indicate distance, like cartesian plane

                # VERTICAL
                step_x = grid_width * self.camera.zoom # rename to just step
                grid_start_x = (boundary[0] + self.camera.x) * self.camera.zoom
                grid_end_x = grid_start_x
                grid_start_y = (boundary[2] + self.camera.y) * self.camera.zoom
                grid_end_y = (boundary[3] + self.camera.y) * self.camera.zoom
                number_lines = (boundary[1] - boundary[0]) / grid_width

                num_position = -num

                for i in range(int(number_lines)):
                    if i % 2 == 0:
                        pygame.draw.line(self.screen, light_gray, (grid_start_x, grid_start_y), ((grid_end_x, grid_end_y)))
                    grid_start_x += step_x
                    grid_end_x = grid_start_x
                    
                    if num_position % 100 == 0: # draw 100 increments
                        # not perfect but good enough
                        self.screen.blit(self.font.render(f'{num_position}', 1, white), (grid_start_x - 47 * self.camera.zoom, (grid_start_y + grid_end_y) / 2))
                    num_position += grid_width

                # HORIZONTAL
                step_y = grid_width * self.camera.zoom
                grid_start_x = (boundary[0] + self.camera.x) * self.camera.zoom
                grid_end_x = (boundary[1] + self.camera.x) * self.camera.zoom
                grid_start_y = (boundary[2] + self.camera.y) * self.camera.zoom
                grid_end_y = grid_start_y
                number_lines = (boundary[3] - boundary[2]) / grid_width

                num_position = num

                for j in range(int(number_lines)):
                    if j % 2 == 0:
                        pygame.draw.line(self.screen, light_gray, (grid_start_x, grid_start_y), ((grid_end_x, grid_end_y)))
                    grid_start_y += step_y
                    grid_end_y = grid_start_y

                    if num_position % 100 == 0: # draw 100 increments
                        # not perfect but good enough
                        self.screen.blit(self.font.render(f'{num_position}', 1, white), (5 + (grid_start_x + grid_end_x) / 2, grid_start_y - 65 * self.camera.zoom))
                    num_position -= grid_width

            elif self.draw_screen_lines == 2:
                pygame.draw.line(self.screen, light_gray, (screen_width / 2, 0), ((screen_width / 2, screen_height)))
                pygame.draw.line(self.screen, light_gray, (0, screen_height / 2), ((screen_width, screen_height / 2)))
                pygame.draw.line(self.screen, light_gray, (0, 0), ((screen_width, screen_height)))
                pygame.draw.line(self.screen, light_gray, (0, screen_height), ((screen_width, 0)))

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_buttons(self):
        pygame.draw.rect(self.screen, white, button_rect)

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def draw_engine_ui(self):
        # DRAW UNIVERSE BOUNDARIES
        min_x = (boundary[0] + self.camera.x) * self.camera.zoom
        max_x = (boundary[1] + self.camera.x) * self.camera.zoom
        min_y = (boundary[2] + self.camera.y) * self.camera.zoom
        max_y = (boundary[3] + self.camera.y) * self.camera.zoom
        pygame.draw.line(self.screen, red, (min_x, min_y), (min_x, max_y), 7)
        pygame.draw.line(self.screen, red, (max_x, min_y), (max_x, max_y), 7)
        pygame.draw.line(self.screen, red, (min_x, min_y), (max_x, min_y), 7)
        pygame.draw.line(self.screen, red, (min_x, max_y), (max_x, max_y), 7)

        # DRAW BOUNDARY LENGTHS
        length = (boundary[1] - boundary[0]) * scale / 1000
        stringuy = f'{length:.2E} km'
        self.screen.blit(self.font.render(stringuy, 1, white), (((min_x + max_x) / 2) - (len(stringuy) * 4.5), min_y - 20))
        self.screen.blit(self.font.render(stringuy, 1, white), (((min_x + max_x) / 2) - (len(stringuy) * 4.5), max_y + 5))
        # pygame does not rotate text :(, so y text will stay horizontal
        length = (boundary[3] - boundary[2]) * scale / 1000
        stringuy = f'{length:.2E} km'
        self.screen.blit(self.font.render(stringuy, 1, white), (min_x - (len(stringuy) * 9.5), ((min_y + max_y) / 2) - 8.5))
        self.screen.blit(self.font.render(stringuy, 1, white), (max_x + 5, ((max_y + min_y) / 2) - 8.5))

        # CREATE UI AREA
        pygame.draw.rect(self.screen, black, ui_background)
        pygame.draw.line(self.screen, white, (0, screen_height - ui_height), ((screen_width, screen_height - ui_height)), 3)

        # CURRENT CAMERA COORDINATES (screen center)
        cameraCoordsLabel = self.font.render(f'camX{self.camera.x:.3f} camY{self.camera.y:.3f} zoom{self.camera.zoom:.3f} rotY{math.degrees(self.camera.rotation_y):.3f}°', 1, white)
        self.screen.blit(cameraCoordsLabel, (screen_width - 550, screen_height - 40))

        # ENGINE INFO
        framerateTitleLabel = self.font.render('Framerate (current / target)', 1, white)
        self.screen.blit(framerateTitleLabel, (screen_width - 90, screen_height - 40))
        framerateLabel = self.font.render(f'{round(self.clock.get_fps())} / {self.current_framerate}', 1, white)
        self.screen.blit(framerateLabel, (screen_width - 90, screen_height - 20))

        # timescaleLabel = self.font.render(str(round(self.current_timescale)), 1, white)
        # self.screen.blit(timescaleLabel, (screen_width - 30, screen_height - 40))
        timeElapsedLabel = self.font.render(f'{round(self.timeElapsed)} seconds    {str(round(self.current_timescale))} sec / sec', 1, white)
        self.screen.blit(timeElapsedLabel, (10, screen_height - 20))

        scaleLabel = self.font.render(f'1 pixel : {(self.current_scale / self.camera.zoom) / 1000:.0f} kilometers', 1, white)
        self.screen.blit(scaleLabel, (10, screen_height - 40))

        # UI
        grid_text = 'none'
        if self.draw_screen_lines == 1:
            grid_text = 'full'
        elif self.draw_screen_lines == 2:
            grid_text = 'angle'
        gridLabel = self.font.render(f'(g)rid type: {grid_text}', 1, white)
        self.screen.blit(gridLabel, (300, screen_height - 20))

        # change shortcut
        linesLabel = self.font.render(f'distance (k) lines: {self.draw_body_lines}', 1, white)
        self.screen.blit(linesLabel, (300, screen_height - 40))

        lines_text = 'never'
        if self.draw_labels == 1:
            lines_text = 'always'
        elif self.draw_labels == 2:
            lines_text = 'on hover'
        linesLabel = self.font.render(f'show (l)abels: {lines_text}', 1, white)
        self.screen.blit(linesLabel, (300, screen_height - 60))

        #  DRAW FOCUS LABEL
        if not self.focus_camera_on_body:
            bodyFocusName = f'Focus: {self.celestialBodyList[self.current_body_index].name}'
        else:
            bodyFocusName = f'Focused on: {self.celestialBodyList[self.current_body_index].name}'
        bodyFocusLabel = self.font.render(bodyFocusName, 1, white)
        self.screen.blit(bodyFocusLabel, ((screen_width / 2) - len(bodyFocusName) * 4.5, screen_height - 20))

        # DRAW DISTANCE LABEL
        for body in self.celestialBodyList:
            if mouse_hover(self.mouseX, self.mouseY, body, self.camera.x, self.camera.y, self.camera.zoom):
                distanceLabelText = f'{round(distance(self.celestialBodyList[self.current_body_index], body) / 1000)} km'
                distanceLabel = self.font.render(distanceLabelText, 1, white)
                self.screen.blit(distanceLabel, ((screen_width / 2) - (len(distanceLabelText) * 4.5), screen_height - 40))

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def event_handler(self):
        keys = pygame.key.get_pressed()

        key_value = 1
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            key_value = 10
                  

        if keys[pygame.K_KP_PERIOD]:
            self.current_timescale *= -1
        if keys[pygame.K_KP_PLUS]:
            self.current_timescale += key_value
        if keys[pygame.K_KP_MINUS]:
            self.current_timescale -= key_value
        if keys[pygame.K_KP_ENTER]:
            self.current_timescale = timescale

        # if keys[pygame.K_i]:
        #     self.debug_offset_y -= 1
        # if keys[pygame.K_k]:
        #     self.debug_offset_y += 1
        # if keys[pygame.K_l]:
        #     self.debug_offset_x += 1
        # if keys[pygame.K_j]:
        #     self.debug_offset_x -= 1

        if keys[pygame.K_p]:
            self.camera.rotation_y += 1 / (2 * math.pi * 20)
            # if self.camera.rotation_y > math.pi:
                # self.camera.rotation_y = -math.pi
        if keys[pygame.K_o]:
            self.camera.rotation_y -= 1 / (2 * math.pi * 20)
            # if self.camera.rotation_y <= -math.pi:
                # self.camera.rotation_y = math.pi       

        if keys[pygame.K_UP]:
            pass
        elif keys[pygame.K_DOWN]:
            pass

        if keys[pygame.K_ESCAPE]:
            print('Quitting')
            pygame.quit()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.pan_camera(0, key_value * 4)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.pan_camera(0, -key_value * 4)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pan_camera(-key_value * 4, 0)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.pan_camera(key_value * 4, 0)

        if keys[pygame.K_e]:
            self.zoom_camera(0.01 * key_value)
        elif keys[pygame.K_q]:
            self.zoom_camera(-0.01 * key_value)


        if pygame.mouse.get_pressed()[0]:
            if not self.is_lmb_pressed:
                self.is_lmb_pressed = True
                self.mouse_original_x = self.mouseX
                self.mouse_original_y = self.mouseY
            else:
                self.pan_camera(-(self.mouse_original_x - self.mouseX) * 1, -(self.mouse_original_y - self.mouseY) * 1)
                self.mouse_original_x = self.mouseX
                self.mouse_original_y = self.mouseY
        else:
            self.is_lmb_pressed = False

        if pygame.mouse.get_pressed()[2]: # rmb for rotation
            if not self.is_rmb_pressed:
                self.is_rmb_pressed = True
                self.mouse_original_x = self.mouseX
                self.mouse_original_y = self.mouseY
            else:
                self.camera.rotation_y += (self.mouseX - self.mouse_original_x) / 700
                self.mouse_original_x = self.mouseX
                self.mouse_original_y = self.mouseY
        else:
            self.is_rmb_pressed = False


        for event in pygame.event.get(): # use if keys[] instead (like in Pong)
            if self.game_running:

                if event.type == pygame.MOUSEWHEEL:
                    if event.y == 1:
                        self.zoom_camera(0.01)
                    elif event.y == -1:
                        self.zoom_camera(-0.01)

                if event.type == pygame.KEYDOWN:
                    key = event.key
                    modifier = event.mod

                    key_value = 1
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        key_value = 10

                    if event.key == pygame.K_t:
                        self.template_index += 1
                        if self.template_index >= len(self.templates):
                            self.template_index = 0   
                        self.timeElapsed = 0
                        self.current_timescale = timescale
                        self.camera.reset()
                        self.celestialBodyList.clear()
                        self.to_destroy.clear()
                        self.populate_procedural_generation()
                        self.initialize_simulation()
                        self.originalCelestialBodyList = self.celestialBodyList.copy()
                        for body in self.celestialBodyList: # there must be a better way of doing this
                            body.generate_collision_list(self.celestialBodyList)
                        for body in self.celestialBodyList:
                            body.reset_body()
                            body.reset_trail()
                        self.debug_counter = 0

                    if event.key == pygame.K_PERIOD:                       
                        self.current_body_index += 1
                        if self.current_body_index >= len(self.celestialBodyList):
                            self.current_body_index = 0
                    if event.key == pygame.K_COMMA:                       
                        self.current_body_index -= 1
                        if self.current_body_index < 0:
                            self.current_body_index = len(self.celestialBodyList) - 1
                    if event.key == pygame.K_SEMICOLON:
                        self.focus_camera_on_body = not self.focus_camera_on_body

                    if event.key == pygame.K_DELETE:
                        self.celestialBodyList.pop(self.current_body_index)

                    if event.key == pygame.K_l:
                        self.draw_labels += 1
                        if self.draw_labels > 2:
                            self.draw_labels = 1
                    if event.key == pygame.K_k:
                        self.draw_body_lines = not self.draw_body_lines
                    if event.key == pygame.K_g:
                        self.draw_screen_lines += 1
                        if self.draw_screen_lines > 2:
                            self.draw_screen_lines = 0

                    # if event.key == pygame.K_o:
                    #     self.draw_info_screen = not self.draw_info_screen

                    if event.key == pygame.K_SPACE:
                        if self.current_timescale != 0:
                            self.current_timescale = 0
                        else:
                            self.current_timescale = timescale
                    if event.key == pygame.K_KP_PERIOD:
                        self.current_timescale *= -1
                    if event.key == pygame.K_KP_PLUS:
                        if event.mod & (pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT):
                            self.current_timescale += 10
                        else:
                            self.current_timescale += 1
                    if event.key == pygame.K_KP_MINUS:
                        if event.mod & (pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT):
                            self.current_timescale -= 10
                        else:
                            self.current_timescale -= 1
                    if event.key == pygame.K_KP_ENTER:
                        self.current_timescale = timescale

                    if event.key == pygame.K_r:
                        self.timeElapsed = 0
                        self.current_timescale = timescale
                        self.camera.reset()
                        self.celestialBodyList.clear()
                        self.to_destroy.clear()
                        self.populate_procedural_generation()
                        self.initialize_simulation()                      
                        for body in self.celestialBodyList:
                            body.reset_body()
                            body.reset_trail()  
                        self.debug_counter = 0

                    if event.key == pygame.K_y:
                        self.draw_trails = not self.draw_trails

                    if event.key == pygame.K_v:
                        self.draw_vectors = not self.draw_vectors

                    if event.key == pygame.K_n:
                        self.camera.rotation_y += math.pi / 4
                    if event.key == pygame.K_b:
                        self.camera.rotation_y -= math.pi / 4

                    # if event.key == pygame.K_b:
                    #     self.background_layers += 1
                    #     self.background.clear()
                    #     for i in range(self.background_layers):
                    #         self.background.append(starry_background(1000, i)) 
                    #     print(self.background_layers)
                    # elif event.key == pygame.K_v:
                    #     self.b+ackground_layers -= 1
                    #     self.background.clear()
                    #     for i in range(self.background_layers):
                    #         self.background.append(starry_background(1000, i)) 
                    #     print(self.background_layers)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_index = mouse_click(self.mouseX, self.mouseY)
                    if button_index == 1:
                        self.current_vector_scale += 5

            elif self.ui_running:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_index = mouse_click(self.mouseX, self.mouseY)
                    if button_index == 2:
                        current_template_index += 1
                        if current_template_index > len(temp):
                            current_template_index = 0
                    elif button_index == 3:
                        current_template_index -= 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('Quitting')
                    self.game_running = False
                    self.ui_running = False

            if event.type == pygame.QUIT:
                print('Quitting')
                self.game_running = False
                self.ui_running = False

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def boundary_check(self, body):
        vx, vy = vector_components(body)
        ang = math.atan2(vy, -vx)
        if body.x - (body.diameter / 2) / self.current_diameter_scale < boundary[0]:
            body.x = boundary[0] + (body.diameter / 2) / self.current_diameter_scale
            body.velocityAngle = ang
        elif body.x + (body.diameter / 2) / self.current_diameter_scale > boundary[1]:
            body.x = boundary[1] - (body.diameter / 2) / self.current_diameter_scale
            body.velocityAngle = ang

        vx, vy = vector_components(body)
        ang = math.atan2(-vy, vx)
        if body.y - (body.diameter / 2) / self.current_diameter_scale < boundary[2]:
            body.y = boundary[2] + (body.diameter / 2) / self.current_diameter_scale
            body.velocityAngle = ang
        elif body.y + (body.diameter / 2) / self.current_diameter_scale > boundary[3]:
            body.y = boundary[3] - (body.diameter / 2) / self.current_diameter_scale
            body.velocityAngle = ang

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def collision_check(self, body): 
    # still has issues
        for other_body in [x for x in self.celestialBodyList if x.name != body.name]:
            body_collision_index = self.celestialBodyList.index(other_body) - 1
            other_body_collision_index = self.celestialBodyList.index(body) - 1

            # d = distance(other_body, body, False) # regular 2d distance (XY plane)
            d = threeD_distance(other_body, body, False) # implementing 3d (XYZ)
            sum_of_radii = ((other_body.diameter / 2) / self.current_diameter_scale) + ((body.diameter / 2) / self.current_diameter_scale)       

            if d <= sum_of_radii: # NEVER colliding with 3d distance
                if body.collisions_in_period[body_collision_index] < collisions_for_destruction and other_body.collisions_in_period[other_body_collision_index] < 4:
                    dx = other_body.x - body.x
                    dy = other_body.y - body.y
                    collisionTangentAngle = math.atan2(dy, dx)

                    dz = other_body.z - body.z

                    body.velocityAngle = 2 * collisionTangentAngle + body.velocityAngle
                    other_body.velocityAngle = 2 * collisionTangentAngle + other_body.velocityAngle

                    body.velocityModule, other_body.velocityModule = elastic_collision(body.velocityModule, body.mass, other_body.velocityModule, other_body.mass)

                    unstuck_angle = 0.5 * math.pi + collisionTangentAngle
    
                    if body.can_move: # if not working?
                        body.x -= math.cos(unstuck_angle)
                        body.y += math.sin(unstuck_angle)
                    if other_body.can_move: # if not working?
                        other_body.x -= math.cos(unstuck_angle)
                        other_body.y += math.sin(unstuck_angle)

                    body.collisions_in_period[body_collision_index] += 1
                    other_body.collisions_in_period[other_body_collision_index] += 1

                else: # destroy if velocity too low instead of collisions_in_period?
                    if other_body.mass <= body.mass and other_body.destructible:
                        body.mass += other_body.mass
                        # add volume to self, not just add radius
                        body.diameter = ((((body.diameter / 2) ** 3) + ((other_body.diameter / 2) ** 3)) ** (1/3)) * 2
                        self.to_destroy.append(other_body.destroy())
                    elif body.destructible:
                        other_body.mass += body.mass
                        # add volume to self, not just add radius
                        other_body.diameter = ((((body.diameter / 2) ** 3) + ((other_body.diameter / 2) ** 3)) ** (1/3)) * 2
                        self.to_destroy.append(body.destroy())
            else:
                body.collisions_in_period[body_collision_index] = 0
                other_body.collisions_in_period[other_body_collision_index] = 0

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def destroy_bodies(self):
        self.to_destroy = list(set(self.to_destroy)) # uniques only
        for body in reversed(self.to_destroy):
            index = self.celestialBodyList.index(body)
            self.celestialBodyList.pop(index)

        if len(self.to_destroy) == 1:
            print(f'Destroyed {len(self.to_destroy)} body')
        elif len(self.to_destroy) > 1:
            print(f'Destroyed {len(self.to_destroy)} bodies')
        self.to_destroy.clear()

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def update_center_of_mass(self):
        center_x = 0
        center_y = 0
        total_mass = 0
        for body in self.celestialBodyList:
            center_x += body.x * body.mass
            center_y += body.y * body.mass
            total_mass += body.mass
        center_x /= total_mass
        center_y /= total_mass

        cross_size = 20 / self.camera.zoom

        xi = (center_x - cross_size + self.camera.x) * self.camera.zoom
        yi = (center_y - cross_size + self.camera.y) * self.camera.zoom
        xf = (center_x + cross_size + self.camera.x) * self.camera.zoom
        yf = (center_y + cross_size + self.camera.y) * self.camera.zoom
        pygame.draw.line(self.screen, white, (xi, yi), (xf, yf))

        xi = (center_x - cross_size + self.camera.x) * self.camera.zoom
        yi = (center_y + cross_size + self.camera.y) * self.camera.zoom
        xf = (center_x + cross_size + self.camera.x) * self.camera.zoom
        yf = (center_y - cross_size + self.camera.y) * self.camera.zoom
        pygame.draw.line(self.screen, white, (xi, yi), (xf, yf))

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def pan_camera(self, x, y):
        if not self.focus_camera_on_body: # unnecessary if?

            # PAN CAMERA
            self.camera.x += x / self.camera.zoom
            self.camera.y += y / self.camera.zoom

            # LIMIT CAMERA POSITION TO BOUNDARIES
            if self.camera.x < boundary[0]:
                self.camera.x = boundary[0]
            elif self.camera.x > boundary[1] + screen_width / self.camera.zoom:  # wrong
                self.camera.x = boundary[1] + screen_width / self.camera.zoom
            if self.camera.y < boundary[2]:
                self.camera.y = boundary[2]
            elif self.camera.y > boundary[3] + screen_height / self.camera.zoom: # wrong
                self.camera.y = boundary[3] + screen_height / self.camera.zoom

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def zoom_camera(self, increment):
        if increment > 0:
            if self.camera.zoom + increment <= max_zoom:
                self.camera.zoom += increment
            else:
                self.camera.zoom = max_zoom
        elif increment < 0:
            if self.camera.zoom + increment > min_zoom:
                self.camera.zoom += increment
            else:
                self.camera.zoom = min_zoom
        else:
            print('No zoom change')

        # CAMERA MUST ALWAYS BE INSIDE BOUNDARIES (pan_camera () applies boundary limits)
        self.pan_camera(0, 0)

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def ui_loop(self):
        while self.ui_running:
            self.clock.tick(self.current_framerate) # shouldn't this argument be (timescale / framerate)?

            self.screen.fill(black)

            self.mouseX, self.mouseY = pygame.mouse.get_pos()

            self.screen.blit(self.title_font.render('GRAVITY SIM', 1, white), ((screen_width / 2) - 150, 10))            
    
            self.screen.blit(self.font.render('Template:', 1, white), ((screen_width / 2) - 100, 100))
            selected_template = 'Solar System'          
            self.screen.blit(self.font.render(selected_template, 1, white), ((screen_width / 2) + 30, 100))
            pygame.draw.rect(self.screen, white, button_plus_template_rect)
            pygame.draw.rect(self.screen, white, button_minus_template_rect)

            self.event_handler()

            pygame.display.flip()

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def main_loop(self):
        frame = 1
        while self.game_running: 
            self.clock.tick(self.current_framerate)

            self.screen.fill(black)

            self.mouseX, self.mouseY = pygame.mouse.get_pos()

            self.draw_background()

            self.draw_grid()

            for step in range(int(self.current_timescale * physics_step)): # O(n²)
                for i, body in enumerate(self.celestialBodyList):
                    body.update_acceleration()
                    body.update_position(self.current_timescale)                            
                    body.update_velocity(self.current_timescale) # maybe remove / merge this
                    self.collision_check(body)

            
            for i, body in enumerate(self.celestialBodyList):

                self.boundary_check(body)

                # body.update_acceleration()
                # body.update_velocity(self.current_timescale)
                # body.update_position(self.current_timescale)                            
                # self.collision_check(body)

                self.draw_body_labels(body, i)

                self.draw_body_vectors(body)

                self.draw_body_distance_lines(body)
                
                # broken
                # if mouse_hover(self.mouseX, self.mouseY, body, self.camera.x, self.camera.y):
                #     distanceLabelText = f'{round(distance(self.celestialBodyList[self.current_body_index], body) / 1000)} km'
                #     distanceLabel = self.font.render(distanceLabelText, 1, white)
                #     self.screen.blit(distanceLabel, ((screen_width / 2) - (len(distanceLabelText) * 4.5), screen_height - 40))

            self.renderizer()           

            # self.camera.rotation_y += 0.001
            
            self.update_center_of_mass()   

            self.draw_engine_ui()
            
            # self.draw_buttons()
            
            self.camera_position()

            self.destroy_bodies()

            self.event_handler()

            self.timeElapsed += self.current_timescale / self.current_framerate
            frame +=1

            pygame.display.flip()

        pygame.quit()

#—————————————————————————————————————————————————————————————————————————————————————————————————


    def camera_position(self):  # rename / merge with other camera functions
        # not perfectly centered when moving really fast
        # might be related to function order in code
        if self.focus_camera_on_body:
            current_body = self.celestialBodyList[self.current_body_index]
            self.camera.x = ((screen_width / 2) / self.camera.zoom - current_body.x)
            self.camera.y = ((screen_height / 2) / self.camera.zoom - current_body.y)

#—————————————————————————————————————————————————————————————————————————————————————————————————
#—————————————————————————————————————————————————————————————————————————————————————————————————


if __name__=="__main__":
    game = Game(True, 1, 2, False, False, True)
    # game.ui_loop()
    # game.main_loop()
