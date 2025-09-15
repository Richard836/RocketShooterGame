import pygame, MainMenu, random

class Play:
    def __init__(self):
        self.lasers = []
        self.laser_cooldown = 0
        self.last_shot = 0

        self.asteroids = []
        self.asteroids_cooldown = 0
        self.last_spawn = 0
        self.asteroidSpeed = 0

        self.screen_width = 0
        self.screen_height = 0
        self.playerx_size = 0
        self.playery_size = 0
        self.playerx = 0
        self.playery = 0
        self.playerspeed = 0
        self.lives = 0
        self.score = 0
        self.scoreGoal = 0
        self.gameVolume = 0.0

    def initialize(self, screen_width, screen_height, gameVolume):  #Player variable initialization does this once EVERY RUN
        self.lasers = []
        self.laser_cooldown = 250
        self.last_shot = 0

        self.asteroids = []
        self.asteroids_cooldown = 2000
        self.last_spawn = 0
        self.asteroidSpeed = 3

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.playerx_size = 150
        self.playery_size = 100
        self.playerx = (screen_width - self.playerx_size)/2
        self.playery = screen_height - self.playery_size
        self.playerspeed = 10
        self.lives = 3
        self.score = 0
        self.scoreGoal = 300
        self.gameVolume = gameVolume

################################LOAD LIVES AND HANDLE LOSS###########################################################################
    def Lives(self, game, lives):
        font = pygame.font.SysFont("arial", 80)  # None = default font
        Lives = font.render("Lives = " + str(lives), True, (0, 200, 0))
        game.screen.blit(Lives, (game.screen_width - 300, 0))

################################LOAD SCORE AND HANDLE GAIN###########################################################################
    def Score(self, game):
        font = pygame.font.SysFont("arial", 80)  # None = default font
        Score = font.render("Score = " + str(self.score), True, (0, 200, 0))
        game.screen.blit(Score, (0, 0))

################################RUN THE MAIN GAME METHOD###########################################################################
    def runGame(self, game, callPlay):
        game.screen.blit(game.Background, (0, 0))  #re-draw background
        callPlay.asteroid(game, callPlay)
        callPlay.updateLasers(game)
        callPlay.Lives(game, self.lives) #show lives
        callPlay.Score(game) #show score
        callPlay.Player(game, callPlay) # load player method from MainMenu
        callPlay.HitDetection()

###################################ALL PLAYER CONTROLS AND SPRITE########################################################################
    def Player(self, game, callPlay):
        Player = pygame.image.load('Images/RocketSprite.png')
        Player = pygame.transform.scale(Player, (self.playerx_size, self.playery_size))
        game.screen.blit(Player, (self.playerx, self.playery))

        keys = pygame.key.get_pressed()  # check key status and set it to 'keys' variable

        #PLAYER CONTROLS
        if keys[pygame.K_w]:  # go up (Linear)
            self.playery -= self.playerspeed
            if keys[pygame.K_w] and keys[pygame.K_a]: #go up-left (diagonal)
                self.playerx -= self.playerspeed
            if keys[pygame.K_w] and keys[pygame.K_d]: #go up-right (diagonal)
                self.playerx += self.playerspeed

        elif keys[pygame.K_s]:  # go down
            self.playery += self.playerspeed
            if keys[pygame.K_s] and keys[pygame.K_a]: #go down-left (diagonal)
                self.playerx -= self.playerspeed
            if keys[pygame.K_s] and keys[pygame.K_d]: #go down-right (diagonal)
                self.playerx += self.playerspeed

        elif keys[pygame.K_a]:  # go left
            self.playerx -= self.playerspeed
            if keys[pygame.K_a] and keys[pygame.K_w]: #go left-up (diagonal)
                self.playery -= self.playerspeed
            if keys[pygame.K_s] and keys[pygame.K_s]: #go left-down (diagonal)
                self.playery += self.playerspeed

        elif keys[pygame.K_d]:  # go right
            self.playerx += self.playerspeed
            if keys[pygame.K_d] and keys[pygame.K_w]: #go right-up (diagonal)
                self.playery -= self.playerspeed
            if keys[pygame.K_d] and keys[pygame.K_s]: #go right-down (diagonal)
                self.playery += self.playerspeed

        #PLAYER BOUNDARIES
        if self.playerx > game.screen_width - self.playerx_size - 1:  #right boundary
            self.playerx = game.screen_width - self.playerx_size
        if self.playerx < 0:                                         #left boundary
            self.playerx = 0
        if self.playery > game.screen_height - self.playery_size - 1: #bottom boundary
            self.playery = game.screen_height - self.playery_size
        if self.playery < 0:                                         #top boundary
            self.playery = 0

        if keys[pygame.K_SPACE]:
            callPlay.shootLaser()

################################LASERS CREATION AND MECHANICSd###########################################################################
    def shootLaser(self):
        laser_width = 10
        laser_height = 30
        now = pygame.time.get_ticks()  # current time in ms

        if now - self.last_shot >= self.laser_cooldown: #did required time between lasers pass?
            self.lasers.append(pygame.Rect(self.playerx + self.playerx_size/2, self.playery, laser_width, laser_height)) # Add a new laser
            self.last_shot = now
            pygame.mixer.init()
            sound_effect = pygame.mixer.Sound("music/LaserSound.mp3")
            sound_effect.set_volume(self.gameVolume) #sets volume of this to whatever music vol was set in other class
            sound_effect.play()


    def updateLasers(self, game):
        for laser in self.lasers[:]:
            laser.y -= 10   #laser moves up the screen
            pygame.draw.rect(game.screen, (0, 200, 0), laser) #draw the current laser

            if laser.y < 0:   #if off the screen remove it
                self.lasers.remove(laser)

################################ASTEROID CREATION AND MECHANICS###########################################################################
    def asteroid(self, game, callPlay):
        now = pygame.time.get_ticks()
        randomSpawnX = random.randint(30, self.screen_width - 150)   #random X spawn

        if now - self.last_spawn >= self.asteroids_cooldown:
            size = random.randint(30, 150)  #random asteroid size

            asteroid_img = pygame.image.load("Images/AsteroidSprite.png")  #new image created everytime
            asteroid_img = pygame.transform.scale(asteroid_img, (size, size))   #each asteroid scaled
            rect = asteroid_img.get_rect(topleft=(randomSpawnX, -size))    #get rect hitbox for each asteroid

            self.asteroids.append((asteroid_img, rect))    #add unique sized asteroid to list
            self.last_spawn = now   #update last spawn timer

        # update + draw asteroids
        for asteroid_img, rect in self.asteroids[:]:    #loop through the asteroid 2 parameter list (image, box)
            rect.y += self.asteroidSpeed  # move down
            game.screen.blit(asteroid_img, rect)    #draw

            if rect.y > self.screen_height:
                self.asteroids.remove((asteroid_img, rect))     #remove asteroid from list
                self.lives -= 1

                if self.lives <= 0: #If lives are 0 or less then go to game over
                    game.GameOverScreen(game, callPlay)

################################HIT DETECTION MECHANIC###########################################################################
    def HitDetection(self):
        for asteroid_img, asteroid_rect in self.asteroids[:]:   #loop through asteroids
            for laser in self.lasers[:]:    #loop through lasers
                if laser.colliderect(asteroid_rect):    #if any asteroid hitbox connects with a laser
                    w, h = asteroid_rect.size

                    if w >= 30 and w <= 69:    #depending on asteroid size award more points (smaller = more)
                        self.score += 70
                    elif w >= 70 and w <= 109:
                        self.score += 40
                    else:
                        self.score += 20

                    if self.score >= self.scoreGoal:  #check to see if current score reached current goal then increase asteroid speed
                        if self.asteroidSpeed <= 8:     #maximum asteroid speed of 10
                            self.asteroidSpeed += 1
                        if self.laser_cooldown >= 130:  #maximum laser cooldown of 130
                            self.laser_cooldown -= 10
                        self.scoreGoal += 300

                    if self.asteroids_cooldown >= 600:  #maximum asteroid cooldown spawn 600
                        self.asteroids_cooldown -= 10

                    self.lasers.remove(laser)   #remove laser from list
                    self.asteroids.remove((asteroid_img, asteroid_rect))    #remove asteroid
                    break
