import pgzrun
import random
import mathstropy 

#message to players
print('    ') 
print('___________________________________________')
print("Welcome to the Really Cool Space Game!")
print("You have been hired tp protect your planet from different kinds of dangers.")
print("Your goal is to collect small pieces of space junk, and destroy larger debris.")
print("Also, evil satellites are attacking your planet, and you must destroy them.")
print("Collect a piece of space junk to recive 1 point.")
print("Destroy a piece of debris to recieve 5 points.")
print("Destroy an evil satellite to recieve 10 points.")
print("Score 50 points to win.")
print("Be careful not to let the satellites or debris to touch you, or you will lose points.")
print("Use the arrow keys to move, and the spacebar to shoot.")
print("Good Luck!")
user_name = input("Please enter your user name: ")
#define screen
WIDTH = 1000
HEIGHT = 600
SCOREBOX_HEIGHT = 50  # change to height of scoreboard

# count score
score = 5  # start off with zero points

#number of lasers on screen
lasers_on_screen = 0

#laser messages
laser_hit_deb = 0
laser_hit_sat = 0

#decides weather to shoot a laser
shouldShoot = 1

#initiate debris timers
explosion_timer = 0

# sprite speeds
junk_speed = 5
sat_speed = 3
debris_speed = 5
laser_speed = -5

BACKGROUND_IMG = "char_space_game_background"  # change to your file name
PLAYER_IMG = "char_spaceship"  # change to your file name
JUNK_IMG = "space_junk"  # change to your file name
SATELLITE_IMG = "evil_satelite"  # change to your file name 
DEBRIS_IMG = "space_debris"
LASER_IMG = "laser_red"
GAME_OVER_SCREEN_IMG = 'game_over_screen'
WINNING_SCREEN_IMG = 'winning_screen'

#INITIALIZE SPRITES
# sprite_name = Actor("file_name", rect_pos = (x, y))
player = Actor(PLAYER_IMG)
player.midright = (WIDTH - 10, HEIGHT/2)  # rect_position = (x, y)

# initialize junk sprites
junks = []  # list to keep track of junks
for i in range(6):
    junk = Actor(JUNK_IMG)  # create a junk sprite
    x_pos = random.randint(-500, -50)
    y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
    junk.pos = (x_pos, y_pos)  # rect_position = (x, y)
    junks.append(junk)

# initialize satellite
satellite = Actor(SATELLITE_IMG)  # create sprite
x_sat = random.randint(-500, -50)
y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
satellite.topright = (x_sat, y_sat)  # rect_position

# initialize debris
debris = Actor(DEBRIS_IMG)
x_deb = random.randint(-500, -50)
y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
debris.topright = (x_deb, y_deb)

#initilize lasers
lasers = []

#background music
sounds.spacelife.play(-1)
        
    
def draw():
    global WIDTH, HEIGHT
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0,0))
    player.draw()  # draw player sprite on screen
    for junk in junks:
        junk.draw()  # draw junk sprite on screen
    satellite.draw()
    debris.draw()
    for laser in lasers:
        laser.draw()

    # show text on screen
    show_score = "Score: " + str(score)  # remember to convert score to a string
    screen.draw.text(show_score, topleft=(750, 15), fontsize=35, color="white")
    

    show_name = 'Player:  ' + user_name
    screen.draw.text(show_name, topleft=(450, 15), fontsize=35, color="white")

    if score < 0:
        screen.blit(GAME_OVER_SCREEN_IMG, (0,0))
        game_over = 'GAME OVER'
        screen.draw.text(game_over, center=(500, 300), fontsize=100, color="black")
        sounds.spacelife.stop()
        sounds.collect_pep.stop()
    if score > 50:
        screen.blit(WINNING_SCREEN_IMG, (0,0))
        sounds.spacelife.stop()
        sounds.collect_pep.stop()
        
#MAIN GAME LOOP___________________________________________
def update():  # main update function
    global laser_hit_deb, laser_hit_sat, explosion_timer
    updatePlayer()  # calling our player update function
    updateJunk()  # calling junk update function 
    updateSatellite()
    updateDebris()
    updateLasers()
    if laser_hit_deb == 1:
        explosionTimer(debris, DEBRIS_IMG,10, laser_hit_deb)
        if explosion_timer > 10:
            laser_hit_deb =0
        
    if laser_hit_sat == 1:
        explosionTimer(satellite, SATELLITE_IMG, 10, laser_hit_sat)
        if explosion_timer >10:
            laser_hit_sat =0
    #game over screen


#UPDATE SPRITES_________________________________________________________________________________
def updatePlayer():
    global lasers_on_screen, shouldShoot
    # check for keyboard inputs
    if keyboard.up == 1:
        player.y += -5  # moving up is negative y-direction
    elif keyboard.down == 1:
        player.y += 5  # moving down is positive y-direction
    # prevent player from moving off screen - add boundaries
    if player.top < SCOREBOX_HEIGHT:
        player.top = SCOREBOX_HEIGHT
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
    # check for fired laser 
    if keyboard.space == 1 and lasers_on_screen<2 and shouldShoot == 1: #if space is pressed and there are fewer than 2 lasers on screen and no lasers have been fired
        lasers_on_screen += 1
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)
        shouldShoot = 0
    if keyboard.space!= 1:
        shouldShoot = 1
        

def updateJunk():
    global score
    for junk in junks:  # add for loop
        junk.x += junk_speed  # same as junk.x = junk.x + 3
    
        collision = player.colliderect(junk)  # declare collision variable

        if junk.left > WIDTH or collision == 1:  # make junk reappear if move off screen
            x_pos = random.randint(-500, -50) # start off screen
            y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)

        if collision == 1: # if collisions occurs 
            score += 1  # this is the same score = score + 1
            sounds.collect_pep.play()
            
def updateSatellite():
    global score
    if laser_hit_sat == 0:
        satellite.x += sat_speed  # or just put 3
    collision = player.colliderect(satellite)

    if satellite.left > WIDTH or collision == 1:
        x_sat = random.randint(-500, -50)
        y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)
        satellite.image = SATELLITE_IMG

    if collision == 1:
        score += -10

def updateDebris():
    global score, laser_hit_deb
    if laser_hit_deb == 0:
        debris.x += debris_speed  # or just put 3
    collision = player.colliderect(debris)

    if debris.left > WIDTH or collision == 1:
        x_deb = random.randint(-500, -50)
        y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
        debris.topright = (x_deb, y_deb)

    if collision == 1:
        score += -10
        
def updateLasers():
    global lasers, score, lasers_on_screen, laser_hit_deb, laser_hit_sat, explosion_timer

    satelliteTimer = 0
    debrisTimer = 0
    
    for laser in lasers:
        laser.x += laser_speed
        if laser.right < 0:  # if laser moves off the screen, remove it from our game list
            lasers.remove(laser)
            lasers_on_screen += (-1)
            
        if satellite.colliderect(laser) == 1:
            lasers.remove(laser)
            lasers_on_screen += (-1)
            score += 10
            sounds.explosion.play()
            explosion_timer = 0
            satellite.image = 'explosion00' #change image to explosion
            laser_hit_sat = 1 #tell main function that laser hit satellite

        if debris.colliderect(laser) == 1:
            lasers.remove(laser)
            lasers_on_screen += (-1)
            score += 5
            explosion_timer = 0
            sounds.explosion.play()
            debris.image = 'explosion00' #change image to explosion
            laser_hit_deb = 1 #tell main function that laser hit debris

    lasers = mathstropy.pgzero.listCleanup(lasers)  # this helps make sure our lists are working properly

#time how long an explosion should last
def explosionTimer(sprite, img, max_time, trigger):
    global explosion_timer
    explosion_timer +=1
    if explosion_timer > max_time:
        x_pos = random.randint(-500, -50)
        y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - sprite.height)
        sprite.topright = (x_pos, y_pos)
        sprite.image = img
        trigger = 0
        

# activating lasers 
player.laserActive = 1

def makeLaserActive():
    global player
    player.laserActive = 1

def fireLasers(sprite):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()
        lasers.append(sprite)
        lasers[len(lasers) - 1].status = 0


        
pgzrun.go()  # function that runs our game loop

