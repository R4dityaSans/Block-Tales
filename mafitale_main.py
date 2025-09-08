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
mafioso_hp = 100
MAFIOSO_MAX_HP = 100
mafioso_direction = 1  # 1 = right, -1 = left
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
    def __init__(self, actor, spawn_time, weapon_name):
        self.actor = Actor(actor.image)
        self.actor.x = actor.x
        self.actor.y = actor.y
        self.spawn_time = spawn_time
        self.alpha = 255
        self.fading = False
        self.hp = 100
        self.max_hp = 100
        self.direction = 1  # 1: right, -1: left
        self.weapon_name = weapon_name
        self.next_attack_time = time.time() + random.uniform(1, 2)
        self.attacking = False
        self.attack_alpha = 0
        self.attack_timer = 0
        self.hit_this_slash = False
        self.target = None

    def update(self, dt):
        # Find target if enemy exists
        if enemy_mademans:
            self.target = min(enemy_mademans, key=lambda em: abs(em.actor.x - self.actor.x))
            # Move towards target if not in range
            if abs(self.actor.x - self.target.actor.x) > 40:
                self.direction = 1 if self.target.actor.x > self.actor.x else -1
                self.actor.x += self.direction * 2
            else:
                # In range, stop and attack
                now = time.time()
                if now >= self.next_attack_time and not self.attacking:
                    self.attacking = True
                    self.attack_alpha = 0
                    self.attack_timer = now
                    self.next_attack_time = now + random.uniform(1, 2)
                    sounds.sword_slash.play()  # Use sword slash for all for now
                    self.hit_this_slash = False
                # Attack animation
                if self.attacking:
                    elapsed = now - self.attack_timer
                    if elapsed < 0.2:
                        self.attack_alpha = min(1, elapsed / 0.2)
                    elif elapsed < 0.4:
                        self.attack_alpha = max(0, 1 - (elapsed - 0.2) / 0.2)
                    else:
                        self.attacking = False
                        self.attack_alpha = 0
        else:
            # No target, idle
            pass

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

class EnemyMademan:
    def __init__(self, x, y):
        self.actor = Actor("mademan")
        self.actor.x = x
        self.actor.y = y
        self.direction = -1  # Always starts moving left
        self.speed = 2
        self.next_attack_time = time.time() + random.uniform(1, 3)
        self.attacking = False
        self.attack_alpha = 0
        self.attack_timer = 0
        self.hp = 100
        self.max_hp = 100
        self.hit_this_slash = False
        self.target = mafioso

    def update(self, dt):
        # Move towards target if not in range
        if abs(self.actor.x - self.target.x) > 40:
            self.direction = 1 if self.target.x > self.actor.x else -1
            self.actor.x += self.direction * self.speed
        else:
            # In range, stop and attack
            now = time.time()
            if now >= self.next_attack_time and not self.attacking:
                self.attacking = True
                self.attack_alpha = 0
                self.attack_timer = now
                self.next_attack_time = now + random.uniform(1, 3)
                sounds.sword_slash.play()
                self.hit_this_slash = False
            # Attack animation
            if self.attacking:
                elapsed = now - self.attack_timer
                if elapsed < 0.2:
                    self.attack_alpha = min(1, elapsed / 0.2)
                elif elapsed < 0.4:
                    self.attack_alpha = max(0, 1 - (elapsed - 0.2) / 0.2)
                else:
                    self.attacking = False
                    self.attack_alpha = 0

enemy_mademans = []

def spawn_goons():
    if len(spawned_goons) >= 2:
        return
    positions = [
        mafioso.x - mafioso.width - 10,  # left
        mafioso.x + mafioso.width + 10   # right
    ]
    weapons = ["police_baton", "woodennail", "crowbar", "sword"]
    goon_map = {
        caporegime: "police_baton",
        contractee: "woodennail",
        soldier: "crowbar",
        consigliere: "sword"
    }
    for i, pos in enumerate(positions):
        goon_type = goon_types[i]
        new_goon = SpawnedGoon(goon_type, time.time(), goon_map[goon_type])
        new_goon.actor.x = pos
        new_goon.actor.y = mafioso.y
        spawned_goons.append(new_goon)
    sounds.here_we_go_folks.play()

def spawn_enemy_mademan():
    x = WIDTH - mademan.width // 2 - 10
    y = mafioso.y
    enemy_mademans.append(EnemyMademan(x, y))

def draw_hp_bar(x, y, hp, max_hp, width=40, height=8, color=(0,200,0)):
    # Draw background
    screen.draw.filled_rect(Rect((x, y), (width, height)), (60,60,60))
    # Draw HP
    hp_width = int(width * hp / max_hp)
    screen.draw.filled_rect(Rect((x, y), (hp_width, height)), color)
    # Draw border
    screen.draw.rect(Rect((x, y), (width, height)), (255,255,255))

def draw():
    map_draw()
    mafioso.draw()
    # Draw Mafioso HP bar
    draw_hp_bar(mafioso.x-20, mafioso.y-mafioso.height-20, mafioso_hp, MAFIOSO_MAX_HP)

    # Draw sword and hitbox with alpha if attacking
    if attack_state != ATTACK_IDLE:
        # Sword fade in/out
        if mafioso_direction == 1:
            sword.x = mafioso.x + mafioso.width // 2 + 10
        else:
            sword.x = mafioso.x - mafioso.width // 2 - 10
        sword.y = mafioso.y
        sword.image = "sword"
        sword._surf.set_alpha(int(sword_alpha * 255))
        sword.draw()
        sword._surf.set_alpha(255)  # Reset

        # Hitbox fade in/out
        if attack_state == ATTACK_SLASH or attack_state == ATTACK_FADEOUT:
            if mafioso_direction == 1:
                hitbox_rect = Rect((sword.x, sword.y - 20), (40, 40))
            else:
                hitbox_rect = Rect((sword.x - 40, sword.y - 20), (40, 40))
            screen.surface.set_alpha(int(hitbox_alpha * 255))
            screen.draw.filled_rect(hitbox_rect, (255, 0, 0))
            screen.surface.set_alpha(255)
        
    # Draw radio with fade in/out
    if radio_active:
        radio.x = mafioso.x
        radio.y = mafioso.y - mafioso.height
        radio._surf.set_alpha(int(radio_alpha * 255))
        radio.draw()
        radio._surf.set_alpha(255)

    # Draw goons and their attack hitboxes
    for goon in spawned_goons:
        goon.actor.draw()
        draw_hp_bar(goon.actor.x-20, goon.actor.y-goon.actor.height-20, goon.hp, goon.max_hp, color=(0,0,200))
        if goon.attacking and goon.attack_alpha > 0:
            if goon.direction == 1:
                hitbox_rect = Rect((goon.actor.x + goon.actor.width // 2 + 10, goon.actor.y - 20), (40, 40))
            else:
                hitbox_rect = Rect((goon.actor.x - goon.actor.width // 2 - 50, goon.actor.y - 20), (40, 40))
            screen.surface.set_alpha(int(goon.attack_alpha * 128))
            screen.draw.filled_rect(hitbox_rect, (255, 0, 0))
            screen.surface.set_alpha(255)
    # Draw enemy mademans and their attack hitboxes
    for em in enemy_mademans:
        em.actor.draw()
        draw_hp_bar(em.actor.x-20, em.actor.y-em.actor.height-20, em.hp, em.max_hp, color=(200,0,0))
        if em.attacking and em.attack_alpha > 0:
            if em.direction == 1:
                hitbox_rect = Rect((em.actor.x + em.actor.width // 2 + 10, em.actor.y - 20), (40, 40))
            else:
                hitbox_rect = Rect((em.actor.x - em.actor.width // 2 - 50, em.actor.y - 20), (40, 40))
            screen.surface.set_alpha(int(em.attack_alpha * 128))
            screen.draw.filled_rect(hitbox_rect, (255, 0, 0))
            screen.surface.set_alpha(255)

def update(dt): #-----------------------------------------------------------------------------------
    global jumping, attack_state, attack_timer, sword_alpha, hitbox_alpha, radio_active, radio_timer, radio_alpha, mafioso_hp, mafioso_direction
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
        # Reset hit_this_slash for all enemies
        for em in enemy_mademans:
            em.hit_this_slash = False

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

    # Update goons
    now = time.time()
    for goon in spawned_goons[:]:
        goon.update(dt)
        # Despawn logic: if no enemies and lifespan > 10s
        if not enemy_mademans:
            elapsed = now - goon.spawn_time
            if elapsed > GOON_LIFESPAN:
                spawned_goons.remove(goon)
                continue  # Skip further checks for this goon

        # Attack collision (deal 5 damage to enemy, only once per slash)
        if goon.attacking and goon.attack_alpha > 0 and goon.target:
            if goon.direction == 1:
                hitbox = Rect((goon.actor.x + goon.actor.width // 2 + 10, goon.actor.y - 20), (40, 40))
            else:
                hitbox = Rect((goon.actor.x - goon.actor.width // 2 - 50, goon.actor.y - 20), (40, 40))
            target_rect = Rect(
                (goon.target.actor.x - goon.target.actor.width // 2, goon.target.actor.y - goon.target.actor.height // 2),
                (goon.target.actor.width, goon.target.actor.height)
            )
            if hitbox.colliderect(target_rect) and not goon.hit_this_slash:
                goon.target.hp = max(0, goon.target.hp - 5)
                goon.hit_this_slash = True

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

    # Track direction for hitbox
    if can_move:
        if keyboard.left or keyboard.a:
            mafioso_direction = -1
        elif keyboard.right or keyboard.d:
            mafioso_direction = 1

    # Update goon lifespan and fade out (keep only for fading visuals, not despawn)
    for goon in spawned_goons[:]:
        elapsed = now - goon.spawn_time
        if elapsed > GOON_LIFESPAN and not enemy_mademans:
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

    # Spawn mademan enemy with U key
    if keyboard.u:
        spawn_enemy_mademan()

    # Update enemies
    for em in enemy_mademans:
        # Find closest opponent (mafioso or any goon)
        targets = [mafioso] + [g.actor for g in spawned_goons]
        closest = min(targets, key=lambda t: abs(em.actor.x - t.x))
        em.target = closest
        em.update(dt)

        # Attack collision (deal 5 damage to target, only once per slash)
        if em.attacking and em.attack_alpha > 0:
            if em.direction == 1:
                hitbox = Rect((em.actor.x + em.actor.width // 2 + 10, em.actor.y - 20), (40, 40))
            else:
                hitbox = Rect((em.actor.x - em.actor.width // 2 - 50, em.actor.y - 20), (40, 40))
            if isinstance(em.target, Actor):
                target_rect = Rect((em.target.x - em.target.width // 2, em.target.y - em.target.height // 2), (em.target.width, em.target.height))
                # Damage mafioso or goon
                if hitbox.colliderect(target_rect) and not em.hit_this_slash:
                    if em.target == mafioso:
                        mafioso_hp = max(0, mafioso_hp - 5)
                    else:
                        # Find the goon object and reduce its HP
                        for goon in spawned_goons:
                            if goon.actor == em.target:
                                goon.hp = max(0, goon.hp - 5)
                    em.hit_this_slash = True

    # Sword attack collision (deal 10 damage to mademan, only once per slash)
    if attack_state == ATTACK_SLASH:
        if mafioso_direction == 1:
            sword_hitbox = Rect((mafioso.x + mafioso.width // 2 + 10, mafioso.y - 20), (40, 40))
        else:
            sword_hitbox = Rect((mafioso.x - mafioso.width // 2 - 50, mafioso.y - 20), (40, 40))
        for em in enemy_mademans:
            mademan_rect = Rect(
                (em.actor.x - em.actor.width // 2, em.actor.y - em.actor.height // 2),
                (em.actor.width, em.actor.height)
            )
            if sword_hitbox.colliderect(mademan_rect) and not em.hit_this_slash:
                if em.hp > 0:
                    em.hp = max(0, em.hp - 10)
                    em.hit_this_slash = True


    # Mademan attack collision (deal 5 damage to Mafioso)
    for em in enemy_mademans:
        if em.attacking and em.attack_alpha > 0:
            punch_hitbox = Rect((em.actor.x + em.actor.width // 2, em.actor.y - 20), (40, 40))
            mafioso_rect = Rect((mafioso.x - mafioso.width // 2, mafioso.y - mafioso.height // 2), (mafioso.width, mafioso.height))
            if punch_hitbox.colliderect(mafioso_rect):
                if mafioso_hp > 0:
                    mafioso_hp = max(0, mafioso_hp - 5)

    # Remove dead goons and enemies
    spawned_goons[:] = [g for g in spawned_goons if g.hp > 0]
    enemy_mademans[:] = [e for e in enemy_mademans if e.hp > 0]




pgzrun.go()