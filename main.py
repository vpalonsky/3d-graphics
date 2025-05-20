import pygame
from math import cos, sin, pi

W_WIDTH = 900
W_HEIGHT = 600
FPS = 30
BACKGROUND_COLOR = "black"
GRAPHICS_COLOR = "white"

CUBE_CENTER = (W_WIDTH/2, W_HEIGHT/2, 0)
CUBE_SIDE_L = 50
ROTATE_X = 1
ROTATE_Y = 2
ROTATE_Z = 3
Mx = lambda alpha : [[1, 0, 0], [0, cos(alpha), -sin(alpha)], [0, sin(alpha), cos(alpha)]]
My = lambda beta : [[cos(beta), 0, sin(beta)], [0, 1, 0], [-sin(beta), 0, cos(beta)]]
Mz = lambda theta : [[cos(theta), -sin(theta), 0], [sin(theta), cos(theta), 0], [0, 0, 1]]

CAMERA_ANGLE = [0, 0, 0]
CAMERA_POS = [0, 0, -50]
DISPLAY_SURFACE_POS = [0, 0, 100]
Mx_ = lambda alpha : [[1, 0, 0], [0, cos(alpha), sin(alpha)], [0, -sin(alpha), cos(alpha)]]
My_ = lambda beta : [[cos(beta), 0, -sin(beta)], [0, 1, 0], [sin(beta), 0, cos(beta)]]
Mz_ = lambda theta : [[cos(theta), sin(theta), 0], [-sin(theta), cos(theta), 0], [0, 0, 1]]

MOVE_CAMERA_UP = 1
MOVE_CAMERA_DOWN = 2
MOVE_CAMERA_LEFT = 3
MOVE_CAMERA_RIGHT = 4

pygame.init()
surface = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 16)

def initialize_cube(cube_points):
	pos_x = int(CUBE_SIDE_L/2)
	neg_x = int(-CUBE_SIDE_L/2)
	pos_y = int(CUBE_SIDE_L/2)
	neg_y = int(-CUBE_SIDE_L/2)
	pos_z = int(CUBE_SIDE_L/2)
	neg_z = int(-CUBE_SIDE_L/2)

	for y in range(neg_y, pos_y+1):
		cube_points.append((y, pos_x, neg_z))
		cube_points.append((y, neg_x, neg_z))
		cube_points.append((y, pos_x, pos_z))
		cube_points.append((y, neg_x, pos_z))
	for x in range(neg_x, pos_x+1):
		cube_points.append((neg_y, x, neg_z))
		cube_points.append((pos_y, x, neg_z))
		cube_points.append((neg_y, x, pos_z))
		cube_points.append((pos_y, x, pos_z))
	for z in range(neg_z, pos_z+1):
		cube_points.append((neg_y, pos_x, z))
		cube_points.append((pos_y, pos_x, z))
		cube_points.append((neg_y, neg_x, z))
		cube_points.append((pos_y, neg_x, z))

def rotate_figure(points, M):
	for p in range(len(points)):
		point = points[p]
		new_point = rotate_point(point, M)

		points[p] = new_point

def rotate_point(point, M):
	new_point = [0, 0, 0]
	for i in range(len(M)):
		sum = 0
		for j in range(len(M[i])):
			sum += point[j] * M[i][j]
		new_point[i] = sum
	return (new_point[0], new_point[1], new_point[2])

def apply_perspective(points):
	for p in range(len(points)):
		point = points[p]

		ac = (point[0]-CAMERA_POS[0], point[1]-CAMERA_POS[1], point[2]-CAMERA_POS[2])
		d = rotate_point(rotate_point(rotate_point(ac, Mz(CAMERA_ANGLE[2])), My(CAMERA_ANGLE[1])), Mx(CAMERA_ANGLE[0]))
		if d[2]==0: d = (d[0], d[1], 0.001)
		new_point = (DISPLAY_SURFACE_POS[2]/d[2]*d[0]+DISPLAY_SURFACE_POS[0], DISPLAY_SURFACE_POS[2]/d[2]*d[1]+DISPLAY_SURFACE_POS[1], point[2])

		points[p] = new_point

def main():
	running = True
	move_camera = None
	rotate = None

	cube_points = []
	initialize_cube(cube_points)

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				if event.key == pygame.K_UP:
					move_camera = MOVE_CAMERA_UP
				if event.key == pygame.K_DOWN:
					move_camera = MOVE_CAMERA_DOWN
				if event.key == pygame.K_RIGHT:
					move_camera = MOVE_CAMERA_RIGHT
				if event.key == pygame.K_LEFT:
					move_camera = MOVE_CAMERA_LEFT
				if event.key == pygame.K_w:
					rotate = -ROTATE_X
				if event.key == pygame.K_s:
					rotate = ROTATE_X
				if event.key == pygame.K_d:
					rotate = -ROTATE_Y
				if event.key == pygame.K_a:
					rotate = ROTATE_Y
				if event.key == pygame.K_g:
					rotate = ROTATE_Z
				if event.key == pygame.K_h:
					rotate = -ROTATE_Z
			if event.type == pygame.KEYUP:
				move_camera = None
				rotate = None

		surface.fill(BACKGROUND_COLOR)

		if move_camera == MOVE_CAMERA_UP:
			CAMERA_POS[2] += 5*cos(2*pi-CAMERA_ANGLE[1])
			CAMERA_POS[0] += 5*sin(2*pi-CAMERA_ANGLE[1])
		if move_camera == MOVE_CAMERA_DOWN:
			CAMERA_POS[2] -= 5*cos(2*pi-CAMERA_ANGLE[1])
			CAMERA_POS[0] -= 5*sin(2*pi-CAMERA_ANGLE[1])
		if move_camera == MOVE_CAMERA_RIGHT:
			CAMERA_POS[2] -= 5*sin(2*pi-CAMERA_ANGLE[1])
			CAMERA_POS[0] += 5*cos(2*pi-CAMERA_ANGLE[1])
		if move_camera == MOVE_CAMERA_LEFT:
			CAMERA_POS[2] += 5*sin(2*pi-CAMERA_ANGLE[1])
			CAMERA_POS[0] -= 5*cos(2*pi-CAMERA_ANGLE[1])

		if rotate == ROTATE_X:
			# rotate_figure(cube_points, Mx(1/(2*pi)))
			CAMERA_ANGLE[0]+=pi/180
		if rotate == -ROTATE_X:
			# rotate_figure(cube_points, Mx(-1/(2*pi)))
			CAMERA_ANGLE[0]-=pi/180
		if rotate == ROTATE_Y:
			# rotate_figure(cube_points, My(1/(2*pi)))
			CAMERA_ANGLE[1]+=pi/180
		if rotate == -ROTATE_Y:
			# rotate_figure(cube_points, My(-1/(2*pi)))
			CAMERA_ANGLE[1]-=pi/180
		if rotate == ROTATE_Z:
			# rotate_figure(cube_points, Mz(1/(2*pi)))
			CAMERA_ANGLE[2]+=pi/180
		if rotate == -ROTATE_Z:
			# rotate_figure(cube_points, Mz(-1/(2*pi)))
			CAMERA_ANGLE[2]-=pi/180

		new_cube_points = [cube_point for cube_point in cube_points]
		apply_perspective(new_cube_points)

		for point in new_cube_points:
			x = point[0]+CUBE_CENTER[0]
			y = point[1]+CUBE_CENTER[1]
			pygame.draw.circle(surface, GRAPHICS_COLOR, (x, y), 1)

		pygame.display.flip()

		clock.tick(FPS)

	pygame.quit()

main()