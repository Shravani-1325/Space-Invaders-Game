# imports the pygame classes,methods and attributes into the current name space. 
import pygame  
import random
import math
from pygame import mixer

# Initialize all imported pygame modules.
pygame.init()

# It returns a Surface object, which we assign to the variable 'screen'.
screen = pygame.display.set_mode((800, 600))  

# Background Image
background = pygame.image.load(r"assets/bg.png")
#background = pygame.transform.scale(background, (800, 600))

# Background music
mixer.music.load(r"assets/space.mp3")
mixer.music.play(-1)

# window title for the game.
pygame.display.set_caption(r"assets/Space Invaders")  

# Loading the game icon 
game_icon = pygame.image.load('assets/ufo.png')  
pygame.display.set_icon(game_icon) 

# Setting player & its initial position
playerImg = pygame.image.load("assets/spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

# Setting Enemy & its initial position
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("assets/monster.png"))
    enemyX.append(random.randint(0, 736))  # Ensure enemy starts within the screen
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)  # Increased speed
    enemyY_change.append(40)

# Setting Bullet & its initial position
# Ready- You cant see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load("assets/bullet2.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10 
bullet_state = "Ready"

# Score 
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10


# Display Score
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))


# Game & Play button Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)
play_font = pygame.font.Font("freesansbold.ttf", 34)


# Load The Play Again Button Image
play_button_img = pygame.image.load("assets/play.png")
play_button_x = 390
play_button_y = 200


# Game over function
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text,(200, 100))
    
    # Draw the play button
    screen.blit(play_button_img, (play_button_x,play_button_y))
    
    # Displaying the text under the play button
    play_text = play_font.render ("Play Again", True, (255,255,255))
    screen.blit(play_text, (play_button_x - 55, play_button_y + 80))
       
game_over = False  # Game over flag (Initially False)

def restart_game():
    global score_value, enemyX, enemyY, bullet_state, bulletY, game_over
    score_value = 0
    bullet_state = "Ready"
    bulletY = 480
    game_over = False  # Reset the game over flag
    for i in range(no_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)


# player function
def player(x,y):
    screen.blit(playerImg, (x, y))  # Drawing the player image
    
    
# Enemy Function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # Drawing the enemy


# Bullet Function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg,(x + 16, y + 10))


# Collision Function
def isCollision(enemyX, enemyY, bulletX, bulletY):
                                        
   # distance btwn two cordinates: D= V(x2−x1)^2+(y2−y1)^2

    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
    



# Game Controls / All events control
running = True  
while running:
    
    # RGB: to update the background.    
    screen.blit(background,(0,0))
    

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: # event type is QUIT (when the user clicks the close button)
            running = False  # Exit the loop and close the game

        # If keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:  # Keydown is when pressing the button continous
            
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                
                if bullet_state is "Ready": 
                    bullet_Sound = mixer.Sound("assets/shoot.mp3")                  
                    bullet_Sound.play()
                    # get the current x coordinate of the spaceship                   
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)      
                
        if event.type == pygame.KEYUP:   # Keydown is when releasing the button continous
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                
        
        if game_over:
            mouse_pos = pygame.mouse.get_pos()
            screen.blit(play_button_img, (play_button_x, play_button_y))        

    if event.type == pygame.MOUSEBUTTONDOWN:
        if (play_button_x <= mouse_pos[0] <= play_button_x + play_button_img.get_width()) and \
           (play_button_y <= mouse_pos[1] <= play_button_y + play_button_img.get_height()):
            restart_game()
             
                
                
    # 5 = 5 + (-0.3) ->  5 - 0.1  
    # 5 = 5 + 0.3  
    
    # Boundaries of the player
    playerX += playerX_change
    
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736        
        
        
    # Boundaries of the enemy 
    for i in range(no_of_enemies):  
        
        # Game Over
        if enemyY[i] > 440:
            game_over = True  # Set game over flag
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
                 
        enemyX[i] += enemyX_change[i]     # Move enemy in X direction
    
        if enemyX[i] <= 0:  
            enemyX_change[i] = 4  # Move right when hitting left edge
            enemyY[i] += enemyY_change[i]  # Move enemy down
             
        elif enemyX[i] >= 736:  
            enemyX_change[i] = -4  # Mo ve left when hitting right edge
            enemyY[i] += enemyY_change[i]  # Move enemy down
 
            
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("assets/collision.mp3")
            explosion_Sound.play()
            bulletY = 480
            bullet_state =  "Ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            
        enemy(enemyX[i], enemyY[i], i) # calling the enemy function
            
        
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "Ready"
        
        
    if bullet_state is "Fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change 
        
   
     
    player(playerX, playerY) # calling player function
    show_score(textX,textY)
    
    
    pygame.display.update()

# Quit pygame properly after exiting the game loop.
pygame.quit()
