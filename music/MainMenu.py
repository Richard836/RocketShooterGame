import pygame, PlayGame, time

class GameMenu:
    def __init__(self):
        # Constructor: Initialize Pygame and screen optimization and create objects
        pygame.init()
        pygame.mixer.init()
        self.PlayMusic = pygame.mixer.music  #create variable for music to pass down
        self.PlayMusic.load("music/MainMenuMusic.mp3")
        self.gameVolume = 1  #default volume 100%
        self.PlayMusic.play(-1)  # play menu theme
        self.PlayMusic.set_volume(self.gameVolume) #set volume to gamevolume initialization
        self.running = True    #Game is runninga
        self.InMenu = True   #If were in game
        self.InOptions = False

        #run timer
        self.clock = pygame.time.Clock()

        #screen initialization
        self.info = pygame.display.Info()    #access users display info
        self.screen_width = self.info.current_w   #max screen width
        self.screen_height = self.info.current_h  #max screen height

        # Background Space image
        self.Background = pygame.image.load('Images/SpaceBackground.png')
        self.Background = pygame.transform.scale(self.Background, (1537, 865))

        # Set up the window
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Space Shooter")

###########################Everything else runs inside this function that Runs the Game################################################################################
    def run(self, game, callPlay):
        while self.running == True:
            events = pygame.event.get()  #universal event so it can carry and not have to be remade in each method

            for event in events:
                if event.type == pygame.QUIT:   #always check to see if top right red 'x' is clicked, if yes then exit the loop
                    self.running = False

            pos = pygame.mouse.get_pos()  # get mous position (x, y)
            if self.InMenu == True:
                self.screen.blit(self.Background, (0, 0))  #draw background constantly until condition false
                game.MainMenu(game, callPlay, pos, events) #Go instantly to menu otherwise NO MENUS BUTTONS OR FUNCTIONS will work (good for going to PlayGame)
            else:
                callPlay.runGame(game, callPlay)

            pygame.display.update() #update the screen
            self.clock.tick(100) #FPS limiter so cpu doesn't get overloaded

#######################################This is the main menu itself that loads other functions####################################################################
    def MainMenu(self, game, callPlay, pos, events):
        if self.InOptions == False:
            game.MenuButtons(pos)  #load buttons
            game.titleImages()  #display images needed for title screen
            game.MenuSelection(game, callPlay, pos, events)    #detects which menu option selected
        elif self.InOptions == True:
            game.OptionsMenu(game, callPlay, pos, events)  #keep loading options menu

################################Create Main Menu buttons with shadow effects###########################################################################
    def MenuButtons(self, pos):
        buttonx = 350  # set x size of buttons
        buttony = 150  # set y size of buttons

        #Play Button
        PlayButtonShadow = pygame.Rect(((self.screen_width - buttonx)/2) - 5, ((self.screen_height - buttony)/5) - 5, buttonx + 10, buttony + 10)
        PlayButton = pygame.Rect((self.screen_width - buttonx)/2, (self.screen_height - buttony)/5, buttonx, buttony)
        pygame.draw.rect(self.screen, (0, 0, 0), PlayButtonShadow)
        pygame.draw.rect(self.screen, (71, 224, 255), PlayButton)

        #Options Button
        OptionsButtonShadow = pygame.Rect(((self.screen_width - buttonx)/2) - 5,((self.screen_height - buttony)/2) - 5, buttonx + 10, buttony + 10)
        OptionsButton = pygame.Rect((self.screen_width - buttonx)/2, (self.screen_height - buttony)/2, buttonx, buttony)
        pygame.draw.rect(self.screen, (0, 0, 0), OptionsButtonShadow)
        pygame.draw.rect(self.screen, (71, 224, 255), OptionsButton)

        #Exit Button
        ExitButtonShadow = pygame.Rect(((self.screen_width - buttonx)/2) - 5,((self.screen_height - buttony)/1.2) - 5, buttonx + 10, buttony + 10)
        ExitButton = pygame.Rect((self.screen_width - buttonx)/2, (self.screen_height - buttony)/1.2, buttonx, buttony)
        pygame.draw.rect(self.screen, (0, 0, 0), ExitButtonShadow)
        pygame.draw.rect(self.screen, (71, 224, 255), ExitButton)

        #Hover over CURRENT selection (TURN BOX RED)
        if (pos[0] >= 595 and pos[0] <= 945) and (pos[1] >= 140 and pos[1] <= 290):
            pygame.draw.rect(self.screen, (255, 0, 0), PlayButton)
        elif (pos[0] >= 595 and pos[0] <= 945) and (pos[1] >= 355 and pos[1] <= 505):
            pygame.draw.rect(self.screen, (255, 0, 0), OptionsButton)
        elif (pos[0] >= 595 and pos[0] <= 945) and (pos[1] >= 595 and pos[1] <= 745):
            pygame.draw.rect(self.screen, (255, 0, 0), ExitButton)

##############################Load Title Image and Create Text for buttons with shadow effects#############################################################################
    def titleImages(self):
        font = pygame.font.SysFont("arial", 80)  # None = default font

        #Title image
        Title = pygame.image.load('Images/SpaceShooterTitle.png')
        Title = pygame.transform.scale(Title, (800, 600))
        self.screen.blit(Title, ((self.screen_width - 800) / 2, -230))

        #Start Text
        StartShadow = font.render("Start", True, (0, 0, 0))
        Start = font.render("Start", True, (0, 200, 0))
        self.screen.blit(StartShadow, (695, 165))
        self.screen.blit(Start, (697, 167))

        #Options Text
        OptionsShadow = font.render("Options", True, (0, 0, 0))
        Options = font.render("Options", True, (0, 200, 0))
        self.screen.blit(OptionsShadow, (655, 375))
        self.screen.blit(Options, (657, 377))

        #Exit Text
        ExitShadow = font.render("Exit", True, (0, 0, 0))
        Exit = font.render("Exit", True, (0, 200, 0))
        self.screen.blit(ExitShadow, (705, 618))
        self.screen.blit(Exit, (707, 620))

#################################Handle Main Menu button Selection##########################################################################
    def MenuSelection(self, game, callPlay, pos, events):
        font = pygame.font.SysFont("arial", 50)

        #Current mouse position for testing (top-left screen)
        mouse = font.render(str(pos), True, (0, 200, 0))
        self.screen.blit(mouse, (0, 0)) #display x,y coordinates of mouse

        #Current MusicVol (top-right screen)
        MusicVolText = font.render("Music: " + str(int(self.gameVolume*100)) + "%", True, (0, 200, 0))
        self.screen.blit(MusicVolText, (self.screen_width - 240, 0))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (pos[0] >= 595 and pos[0] <= 945) and (pos[1] >= 140 and pos[1] <= 290):  # if you clicked EXIT button in menu
                    self.PlayButton(game, callPlay)
                elif (pos[0] >= 595 and pos[0] <= 945) and (pos[1] >= 355 and pos[1] <= 505):
                    self.InOptions = True
                    self.screen.blit(game.Background, (0, 0))  # re-draw background
                    game.OptionsMenu(game, callPlay, pos, events)
                elif (pos[0] >= 595 and pos[0] <= 945) and (pos[1] >= 595 and pos[1] <= 745): #if you clicked EXIT button in menu
                    game.ExitGame()

################################If the Play button is clicked run this###########################################################################
    def PlayButton(self, game, callPlay):
        self.InMenu = False
        self.PlayMusic.stop()   #stop music
        self.PlayMusic.load("music/GameMusic.mp3")
        self.PlayMusic.set_volume(self.gameVolume)
        self.PlayMusic.play(-1)     #play new music
        callPlay.initialize(self.screen_width, self.screen_height, self.gameVolume)
        callPlay.runGame(game, callPlay)

###############################If Option button is clicked go to Option menu##########################################################################
    def OptionsMenu(self, game, callPlay, pos, events):
        font = pygame.font.SysFont("arial", 50)  # None = default font

        # Current mouse position for testing
        mouse = font.render(str(pos), True, (0, 200, 0))
        self.screen.blit(mouse, (0, 0))  # display x,y coordinates of mouse

        # Current MusicVol (top-right screen)
        MusicVolText = font.render("Music: " + str(int(self.gameVolume * 100)) + "%", True, (0, 200, 0))
        self.screen.blit(MusicVolText, (self.screen_width - 240, 0))

        game.optionsButtons(pos) #load buttons for options menu
        game.optionsText() #load text for options menu

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if (pos[0] >= 395 and pos[0] <= 745) and (pos[1] >= 60 and pos[1] <= 210) and self.gameVolume < 1.0: #Increase Music Vol
                    self.gameVolume += 0.1
                    self.PlayMusic.set_volume(self.gameVolume)
                elif (pos[0] >= 790 and pos[0] <= 1140) and (pos[1] >= 60 and pos[1] <= 210) and self.gameVolume > 0.0: #Decrease Music Vol
                    self.gameVolume -= 0.1
                    self.PlayMusic.set_volume(self.gameVolume)
                elif (pos[0] >= 395 and pos[0] <= 745) and (pos[1] >= 355 and pos[1] <= 505):  #Set Music On
                    self.gameVolume = 1.0
                    self.PlayMusic.set_volume(self.gameVolume)
                    self.PlayMusic.play(-1)
                elif (pos[0] >= 790 and pos[0] <= 1140) and (pos[1] >= 355 and pos[1] <= 505):  #Set Music Off
                    self.gameVolume = 0.0
                    self.PlayMusic.set_volume(self.gameVolume)
                    self.PlayMusic.stop()
                elif (pos[0] >= 595 and pos[0] <= 945) and (pos[1] >= 650 and pos[1] <= 800):  #if you clicked go back to Main Menu
                    self.InOptions = False
                    self.screen.blit(self.Background, (0, 0))  # draw background constantly until condition false
                    game.MainMenu(game, callPlay, pos, events)


    ##############################Load layout for options menu#############################################################################
    def optionsButtons(self, pos):
        buttonx = 350  # set x size of buttons
        buttony = 150  # set y size of buttons

        #volUpButton
        volUpButtonShadow = pygame.Rect(((self.screen_width - buttonx)/3) - 5, ((self.screen_height - buttony)/12) - 5, buttonx + 10, buttony + 10)
        volUpButton = pygame.Rect((self.screen_width - buttonx)/3, (self.screen_height - buttony)/12, buttonx, buttony)
        pygame.draw.rect(self.screen, (0, 0, 0), volUpButtonShadow)
        pygame.draw.rect(self.screen, (71, 224, 255), volUpButton)

        #volDownButton
        volUpDownShadow = pygame.Rect(((self.screen_width - buttonx)/1.5) - 5, ((self.screen_height - buttony)/12) - 5, buttonx + 10, buttony + 10)
        volDownButton = pygame.Rect((self.screen_width - buttonx)/1.5, (self.screen_height - buttony)/12, buttonx, buttony)
        pygame.draw.rect(self.screen, (0, 0, 0), volUpDownShadow)
        pygame.draw.rect(self.screen, (71, 224, 255), volDownButton)

        #MusicOnButton
        MusicOnButtonShadow = pygame.Rect(((self.screen_width - buttonx)/3) - 5,((self.screen_height - buttony)/2) - 5, buttonx + 10, buttony + 10)
        MusicOnButton = pygame.Rect((self.screen_width - buttonx)/3, (self.screen_height - buttony)/2, buttonx, buttony)
        pygame.draw.rect(self.screen, (0, 0, 0), MusicOnButtonShadow)
        pygame.draw.rect(self.screen, (71, 224, 255), MusicOnButton)

        #MusicOff
        MusicOffButtonShadow = pygame.Rect(((self.screen_width - buttonx)/1.5) - 5, ((self.screen_height - buttony)/2) - 5, buttonx + 10, buttony + 10)
        MusicOffButton = pygame.Rect((self.screen_width - buttonx)/1.5, (self.screen_height - buttony)/2, buttonx, buttony)
        pygame.draw.rect(self.screen, (0, 0, 0), MusicOffButtonShadow)
        pygame.draw.rect(self.screen, (71, 224, 255), MusicOffButton)

        #BackToMenuButton
        BackToMenuButtonShadow = pygame.Rect(((self.screen_width - buttonx)/2) - 5,((self.screen_height - buttony)/1.1) - 5, buttonx + 10, buttony + 10)
        BackToMenuButton = pygame.Rect((self.screen_width - buttonx)/2, (self.screen_height - buttony)/1.1, buttonx,buttony)
        pygame.draw.rect(self.screen, (0, 0, 0), BackToMenuButtonShadow)
        pygame.draw.rect(self.screen, (71, 224, 255), BackToMenuButton)

        #Hover over CURRENT selection (TURN BOX RED)
        if (pos[0] >= 395 and pos[0] <= 745) and (pos[1] >= 60 and pos[1] <= 210):
            pygame.draw.rect(self.screen, (255, 0, 0), volUpButton)
        elif (pos[0] >= 790 and pos[0] <= 1140) and (pos[1] >= 60 and pos[1] <= 210):
            pygame.draw.rect(self.screen, (255, 0, 0), volDownButton)
        elif (pos[0] >= 395 and pos[0] <= 745) and (pos[1] >= 355 and pos[1] <= 505):
            pygame.draw.rect(self.screen, (255, 0, 0), MusicOnButton)
        elif (pos[0] >= 790 and pos[0] <= 1140) and (pos[1] >= 355 and pos[1] <= 505):
            pygame.draw.rect(self.screen, (255, 0, 0), MusicOffButton)
        elif (pos[0] >= 595 and pos[0] <= 945) and (pos[1] >= 650 and pos[1] <= 800):
            pygame.draw.rect(self.screen, (255, 0, 0), BackToMenuButton)


    def optionsText(self):
        font = pygame.font.SysFont("arial", 80)  # None = default font

        #VolUP Text
        VolUpTextShaddow = font.render("Vol +", True, (0, 0, 0))
        VolUpText = font.render("Vol +", True, (0, 200, 0))
        self.screen.blit(VolUpTextShaddow, (500, 85))
        self.screen.blit(VolUpText, (500, 88))

        #VolDown Text
        VolDownTextShaddow = font.render("Vol -", True, (0, 0, 0))
        VolDownText = font.render("Vol -", True, (0, 200, 0))
        self.screen.blit(VolDownTextShaddow, (900, 85))
        self.screen.blit(VolDownText, (900, 88))

        #MusicOn Text
        MusicOnTextShadow = font.render("Music On", True, (0, 0, 0))
        MusicOnText = font.render("Music On", True, (0, 200, 0))
        self.screen.blit(MusicOnTextShadow, (430, 378))
        self.screen.blit(MusicOnText, (430, 381))

        #MusicOff Text
        MusicOffTextShadow = font.render("Music Off", True, (0, 0, 0))
        MusicOffText = font.render("Music Off", True, (0, 200, 0))
        self.screen.blit(MusicOffTextShadow, (830, 378))
        self.screen.blit(MusicOffText, (830, 381))

        #Back Text
        BackTextShadow = font.render("Back", True, (0, 0, 0))
        BackText = font.render("Back", True, (0, 200, 0))
        self.screen.blit(BackTextShadow, (695, 675))
        self.screen.blit(BackText, (697, 678))

#####################################QUIT GAME######################################################################
    def ExitGame(self):     #simple EXIT GAME
        pygame.quit()

#####################################GAME OVER SCREEN LOAD######################################################################
    def GameOverScreen(self, game, callPlay):
        GameOver = pygame.image.load("Images/GameOverText.png")
        GameOver = pygame.transform.scale(GameOver, (1000, 600))

        Waiting = True
        while Waiting:
            game.screen.blit(GameOver, ((self.screen_width - 1000)/2, (self.screen_height - 600)/2))
            self.PlayMusic.stop()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    break
                if event.type == pygame.KEYDOWN:
                    self.InMenu = True
                    self.PlayMusic.load("music/MainMenuMusic.mp3")
                    self.PlayMusic.set_volume(self.gameVolume)
                    self.PlayMusic.play(-1)  # play menu theme
                    Waiting = False
                    break

#################################Runs everything based on INIT pygame##########################################################################
# Run the game
if __name__ == "__main__":
    game = GameMenu()   #set variable equal to class
    callPlay = PlayGame.Play()
    game.run(game, callPlay) #run the game

