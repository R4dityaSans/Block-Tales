import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pgzrun
import random
import time

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
#Mafioso Goons character--------------------------------------
caporegime = Actor("caporegime_head")
contractee = Actor("contractee_head")   
soldier = Actor("soldier_head")
consigliere = Actor("consigliere_head")
goon_types = [
    caporegime,
    contractee,
    soldier,
    consigliere
]
spawned_goons = []
GOON_LIFESPAN = 10      # seconds before fade out starts
GOON_FADEOUT = 1        # seconds for fade out
#Weapons--------------------------------------
crowbar = Actor("crowbar")
sword = Actor("sword") 
police_baton = Actor("police_baton")
woodennail = Actor("woodennail")
debt_sign = Actor("debt_sign")
radio = Actor("radio")
radio_active = False
radio_timer = 0
radio_alpha = 0
RADIO_FADE_DURATION = 0.5  # seconds for fade in/out (adjust if needed)
RADIO_SOUND_LENGTH = sounds.radio_sound.length if hasattr(sounds.radio_sound, 'length') else 2  # fallback to 2s

# Attack states
attacking = False
ATTACK_IDLE = 0
ATTACK_FADEIN_SWORD = 1
ATTACK_SLASH = 2
ATTACK_FADEOUT = 3

attack_state = ATTACK_IDLE
attack_timer = 0
sword_alpha = 0
hitbox_alpha = 0

FADEIN_DURATION = 0.2
SLASH_DURATION = 0.15
FADEOUT_DURATION = 0.2
#enemy character--------------------------------------
mademan = Actor("mademan")
mademan.x = WIDTH // 2
mademan.y = HEIGHT // 2


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

class SpawnedGoon:
    def __init__(self, actor, spawn_time):
        self.actor = actor
        self.spawn_time = spawn_time
        self.alpha = 255
        self.fading = False

def spawn_goons():
    if len(spawned_goons) >= 2:
        return
    positions = [
        mafioso.x - mafioso.width - 10,  # left
        mafioso.x + mafioso.width + 10   # right
    ]
    for pos in positions:
        goon_type = random.choice(goon_types)
        new_goon = Actor(goon_type.image)
        new_goon.x = pos
        new_goon.y = mafioso.y
        spawned_goons.append(SpawnedGoon(new_goon, time.time()))
    sounds.here_we_go_folks.play()

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
    # Draw sword and hitbox with alpha if attacking
    if attack_state != ATTACK_IDLE:
        # Sword fade in/out
        sword.x = mafioso.x + mafioso.width // 2 + 10
        sword.y = mafioso.y
        sword.image = "sword"
        sword._surf.set_alpha(int(sword_alpha * 255))
        sword.draw()
        sword._surf.set_alpha(255)  # Reset

        # Hitbox fade in/out
        if attack_state == ATTACK_SLASH or attack_state == ATTACK_FADEOUT:
            screen.surface.set_alpha(int(hitbox_alpha * 255))
            hitbox_rect = Rect((sword.x, sword.y - 20), (40, 40))
            screen.draw.filled_rect(hitbox_rect, (255, 0, 0))
            screen.surface.set_alpha(255)
        
    # Draw radio with fade in/out
    if radio_active:
        radio.x = mafioso.x
        radio.y = mafioso.y - mafioso.height
        radio._surf.set_alpha(int(radio_alpha * 255))
        radio.draw()
        radio._surf.set_alpha(255)

    # Draw spawned goons with alpha
    for goon in spawned_goons:
        goon.actor._surf.set_alpha(int(goon.alpha))
        goon.actor.draw()
        goon.actor._surf.set_alpha(255)

def update(dt):
    global jumping, attack_state, attack_timer, sword_alpha, hitbox_alpha, radio_active, radio_timer, radio_alpha
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

    # Attack sequence
    if keyboard.f and attack_state == ATTACK_IDLE:
        attack_state = ATTACK_FADEIN_SWORD
        attack_timer = time.time()
        sword_alpha = 0
        hitbox_alpha = 0
        sounds.sword_equip.play()

    if attack_state == ATTACK_FADEIN_SWORD:
        elapsed = time.time() - attack_timer
        sword_alpha = min(1, elapsed / FADEIN_DURATION)
        if elapsed >= FADEIN_DURATION:
            attack_state = ATTACK_SLASH
            attack_timer = time.time()
            sounds.sword_slash.play()
            hitbox_alpha = 0

    elif attack_state == ATTACK_SLASH:
        elapsed = time.time() - attack_timer
        hitbox_alpha = min(1, elapsed / SLASH_DURATION)
        sword_alpha = 1
        if elapsed >= SLASH_DURATION:
            attack_state = ATTACK_FADEOUT
            attack_timer = time.time()

    elif attack_state == ATTACK_FADEOUT:
        elapsed = time.time() - attack_timer
        sword_alpha = max(0, 1 - elapsed / FADEOUT_DURATION)
        hitbox_alpha = max(0, 1 - elapsed / FADEOUT_DURATION)
        if elapsed >= FADEOUT_DURATION:
            attack_state = ATTACK_IDLE
            sword_alpha = 0
            hitbox_alpha = 0

    # Radio ability
    if keyboard.r and not radio_active and len(spawned_goons) < 2:
        radio_active = True
        radio_timer = time.time()
        radio_alpha = 0
        sounds.radio_sound.play()

    # Handle radio fade in/out and movement lock
    if radio_active:
        elapsed = time.time() - radio_timer
        # Fade in
        if elapsed < RADIO_FADE_DURATION:
            radio_alpha = min(1, elapsed / RADIO_FADE_DURATION)
            can_move = False
        # Hold
        elif elapsed < RADIO_SOUND_LENGTH - RADIO_FADE_DURATION:
            radio_alpha = 1
            can_move = False
        # Fade out
        elif elapsed < RADIO_SOUND_LENGTH:
            radio_alpha = max(0, 1 - (elapsed - (RADIO_SOUND_LENGTH - RADIO_FADE_DURATION)) / RADIO_FADE_DURATION)
            can_move = False
        else:
            radio_active = False
            radio_alpha = 0
            can_move = True
            # Spawn goons after radio finishes
            if len(spawned_goons) < 2:
                spawn_goons()
        # Prevent movement while radio is active
    else:
        can_move = True

    # Calculate next position only if can_move
    next_x = mafioso.x
    if can_move:
        if keyboard.left or keyboard.a:
            next_x -= move_speed
        if keyboard.right or keyboard.d:
            next_x += move_speed

        # Prevent moving off the left/right edge
        half_width = mafioso.width // 2
        if half_width <= next_x <= WIDTH - half_width:
            mafioso.x = next_x

    # Update goon lifespan and fade out
    now = time.time()
    for goon in spawned_goons[:]:
        elapsed = now - goon.spawn_time
        if elapsed > GOON_LIFESPAN:
            goon.fading = True
            fade_elapsed = elapsed - GOON_LIFESPAN
            goon.alpha = max(0, 255 - int((fade_elapsed / GOON_FADEOUT) * 255))
            if goon.alpha == 0:
                spawned_goons.remove(goon)

    # Gravity
    mafioso.y += mafioso.vy
    mafioso.vy += gravity

    # Stop falling if on ground
    if is_on_ground() and mafioso.vy > 0:
        mafioso.vy = 0
        # Snap to ground
        mafioso.y = (int((mafioso.y + mafioso.height // 2) // dirt_bg.height) * dirt_bg.height) - mafioso.height // 2








pgzrun.go()