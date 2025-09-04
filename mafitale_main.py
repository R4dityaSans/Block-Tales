import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pgzrun
import random

dirt_bg = Actor("dirt_bg")
sky_bg = Actor("bluesky_bg")
grass_dirt_bg = Actor("grass_dirt_bg")
clouds_bg = Actor("clouds_bg")

move_speed = 5
size_w = 20 # Lebar dari bidang dalam sel
size_h = 12 # Tinggi dari bidang dalam sel
WIDTH = dirt_bg.width * size_w
HEIGHT = dirt_bg.height * size_h
#character--------------------------------------
mafioso = Actor("mafioso_head")
mafioso.x = WIDTH // 2
mafioso.y = HEIGHT // 2
gravity = 1
jump_power = -15
mafioso.vy = 0
jumping = False
#maps------------------------------------------
outside_map =  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

def is_on_ground():
    # Check if mafioso is standing on tile 2 (grass_dirt)
    tile_x = int(mafioso.x // dirt_bg.width)
    tile_y = int((mafioso.y + mafioso.height // 2) // dirt_bg.height)
    if 0 <= tile_y < len(outside_map) and 0 <= tile_x < len(outside_map[0]):
        return outside_map[tile_y][tile_x] == 2
    return False

def map_draw():
    for i in range(len(outside_map)):
        for j in range(len(outside_map[0])):
            tile = outside_map[i][j]
            if tile == 0:
                dirt_bg.left = dirt_bg.width * j
                dirt_bg.top = dirt_bg.height * i
                dirt_bg.draw()
            if tile == 1:
                sky_bg.left = dirt_bg.width * j
                sky_bg.top = dirt_bg.height * i
                sky_bg.draw()
            if tile == 2:
                grass_dirt_bg.left = dirt_bg.width * j
                grass_dirt_bg.top = dirt_bg.height * i
                grass_dirt_bg.draw()
            if tile == 3:
                clouds_bg.left = dirt_bg.width * j
                clouds_bg.top = dirt_bg.height * i
                clouds_bg.draw()


def draw():
    map_draw()
    mafioso.draw()

def update(dt):
    global jumping
     # Calculate next position
    next_x = mafioso.x
    if keyboard.left or keyboard.a:
        next_x -= move_speed
    if keyboard.right or keyboard.d:
        next_x += move_speed

    # Prevent moving off the left/right edge
    half_width = mafioso.width // 2
    if half_width <= next_x <= WIDTH - half_width:
        mafioso.x = next_x

    # Jump only if on ground and not already jumping
    if is_on_ground():
        if keyboard.space and not jumping:
            mafioso.vy = jump_power
            sounds.youre_mine.play()  # Play sound once per jump
            jumping = True
        elif not keyboard.space:
            jumping = False  # Reset flag when space is released

    # Gravity
    mafioso.y += mafioso.vy
    mafioso.vy += gravity

    # Stop falling if on ground
    if is_on_ground() and mafioso.vy > 0:
        mafioso.vy = 0
        # Snap to ground
        mafioso.y = (int((mafioso.y + mafioso.height // 2) // dirt_bg.height) * dirt_bg.height) - mafioso.height // 2








pgzrun.go()