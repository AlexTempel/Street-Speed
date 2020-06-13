import pygame
import math
pygame.init()

#Setting Up display
display_width = 1800
display_height = 900
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('STREET SPEED') #Window Name

black = (0,0,0) 
white = (255,255,255)
green = (0,255,0)
lessgreen = (20,200,20)
red = (255,0,0)

clock = pygame.time.Clock()
crashed=False
carImg = pygame.image.load('streetcar_right.png')

car_width = 50
car_height = 50

def car(x,y): #Change the cars position with only the coordinates
    gameDisplay.blit(carImg, (x,y))

def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def message_display(text, width, height, size, colour): #Display text on the screen
    largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, largeText, colour)
    TextRect.center = (width,height)
    gameDisplay.blit(TextSurf, TextRect)

#Spawn Point
x = (125)
y = (750)

#Misc Variables
x_change = 0 #How much the car changes position horizontally
y_change = 0 #How much the car changes position vertically
timer = 0 #Timer to rollover for the minutes
timep = 0 #Timer in seconds every 60 frames
minutet = 0 #How many minutes have passed
timea = 0 #Absolute timer that counts up every frame
moved = False #To make sure that the player has moved befor counting the time
laps = 0 #Counting how many laps have passed
pointable = True #To make sure you don't go back and forth over the finish line and get more laps
numlaps = 3 #How many laps you have to do to finish
go_speed = 5 #How fast the car moves
started = False #To start the counter after the player has moved
drift = 1800 #Variable to hold the position of the starting car moving across the screen
top_button = True #To see which start button is selected
options = False #To see if the options menu is open
otselect = 1 #To see which option option is selected
oselected = 0 #To see which option you've selected
endgame = False #To see if the end screen is open
star = False #To see if the player has gotten the star
door = True #The door preventing the player from going backwards

#Function to create the track easily
def track(startingx, startingy, rectwidth, rectheight): #The topleft corner coordinates and the width and length of the rectangle
    global x
    global y
    pygame.draw.rect(gameDisplay, black, (startingx, startingy, rectwidth, rectheight)) #Drawing the rectangle
    #Borders
    if (startingx - car_width + 25) > x > (startingx - car_width) and (startingy + rectheight) > y > (startingy - car_height): 
        x = (startingx - car_width)
    elif (startingx + rectwidth - 25) < x < (startingx + rectwidth) and (startingy + rectheight) > y > (startingy - car_height):
        x = (startingx + rectwidth)
    elif (startingy - car_height + 25)> y > (startingy - car_height) and (startingx - car_width) < x < (startingx + rectwidth):
        y = (startingy - car_height)
    elif (startingy + rectheight - car_height - 25) < y < (startingy + rectheight) and (startingx - car_width) < x < (startingx + rectwidth):
        y = (startingy + rectheight)


#Start Screen
while not started:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    #Selecting which button
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN: #Pressing down to move the selected button down
                top_button = False
            elif event.key == pygame.K_UP: #Pressing up to move the selected button down
                top_button = True
            #Pressing the buttons
            if event.key == pygame.K_RETURN and top_button == True:
                started = True
            elif event.key == pygame.K_RETURN and top_button == False:
                options = True

    #Move the car across the screen
    drift += -go_speed #moves the car across the screen depending upon the selected speed
    if drift <= -800: #moves the car backaround after going across the end of the screen
        drift = 1800

    gameDisplay.fill(white) #Deletes previous screen
    message_display('STREET SPEED', 900, 150, 100, black) #Title
    gameDisplay.blit(pygame.image.load('pixel_car.png'),(drift,200)) #Draws the car

    #Buttons
    #colours in the button that's selected
    if top_button == True: 
        pygame.draw.rect(gameDisplay, green, (825, 550, 275, 125))
    elif top_button == False:
            pygame.draw.rect(gameDisplay, green, (825, 725, 275, 125))

    #Draws the buttons
    pygame.draw.rect(gameDisplay, black, (825, 550, 275, 125), 3)
    pygame.draw.rect(gameDisplay, black, (825, 725, 275, 125), 3)
    message_display('START', 962, 612, 25, black)
    message_display('OPTIONS', 962, 787, 25, black)

    #Options menu
    while options == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN: #Moves the selected button up and down
                if event.key == pygame.K_UP and otselect > 1 and oselected == 0:
                     otselect += -1
                elif event.key == pygame.K_DOWN and otselect < 3 and oselected == 0:
                     otselect += 1

                #When pressing enter it selects the option
                if event.key == pygame.K_RETURN and otselect == 1 and oselected == 0:
                    oselected = 1
                elif event.key == pygame.K_RETURN and otselect == 2 and oselected == 0:
                    oselected = 2
                elif event.key == pygame.K_RETURN and otselect == 3:
                    options = False

                #Adjusts the Options
                #Number of laps
                if event.key == pygame.K_DOWN and oselected == 1 and numlaps > 1:
                    numlaps += -1
                elif event.key == pygame.K_UP and oselected == 1 and numlaps < 5:
                    numlaps += 1
                #Speed
                elif event.key == pygame.K_DOWN and oselected == 2 and go_speed > 1:
                    go_speed += -1
                elif event.key == pygame.K_UP and oselected == 2 and go_speed < 9:
                    go_speed += 1

                #Deselects the option
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_LEFT and oselected != 0:
                    oselected = 0

        gameDisplay.fill(white)
        message_display('OPTIONS', 300, 100, 100, black) #Title for the options screen
        gameDisplay.blit(pygame.image.load('gears.png'), (50,550)) #Little image for the options screen

        #The laps button when selected
        if oselected == 1:
            pygame.draw.rect(gameDisplay, lessgreen, (100,250,300,75))
            message_display('Laps', 150, 275, 40, white)
            message_display('Speed', 165, 425, 40, black)
            message_display('Back', 135, 515, 25, black)
            #Up and down buttons
            pygame.draw.polygon(gameDisplay, white, [[300,280], [320,255], [340,280]])
            pygame.draw.polygon(gameDisplay, white, [[300,295], [320,320], [340,295]])

        #The speed button when selected
        elif oselected == 2:
            pygame.draw.rect(gameDisplay, lessgreen, (100,400,300,75))
            message_display('Laps', 150, 275, 40, black)
            message_display('Speed', 165, 425, 40, white)
            message_display('Back', 135, 515, 25, black)
            #Up and down buttons
            pygame.draw.polygon(gameDisplay, white, [[300,430], [320,405], [340,430]])
            pygame.draw.polygon(gameDisplay, white, [[300,445], [320,470], [340,445]])

        #Buttons when hovered
        if otselect == 1 and oselected == 0:
            pygame.draw.rect(gameDisplay, black, (100,250,300,75))
            message_display('Laps', 150, 275, 40, white)
            message_display('Speed', 165, 425, 40, black)
            message_display('Back', 135, 515, 25, black)

        elif otselect == 2 and oselected == 0:
            pygame.draw.rect(gameDisplay, black, (100, 400, 300, 75))
            message_display('Speed', 165, 425, 40, white)
            message_display('Laps', 150, 275, 40, black)
            message_display('Back', 135, 515, 25, black)

        elif otselect == 3 and oselected == 0:
            pygame.draw.rect(gameDisplay, black, (100, 500, 75, 25))
            message_display('Back', 135, 515, 25, white)
            message_display('Speed', 165, 425, 40, black)
            message_display('Laps', 150, 275, 40, black)

        #The values for the buttons
        if otselect == 1 or oselected == 1:
            message_display(str(numlaps), 375, 275, 40, white)
            message_display(str(go_speed), 375, 425, 40, black)

        elif otselect == 2 or oselected == 2:
            message_display(str(numlaps), 375, 275, 40, black)
            message_display(str(go_speed), 375, 425, 40, white)

        elif otselect == 3:
            message_display(str(numlaps), 375, 275, 40, black)
            message_display(str(go_speed), 375, 425, 40, black)


        pygame.display.update()
        clock.tick(60)

    pygame.display.update()
    clock.tick(60)

while not crashed and endgame == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True          
    
        #Movement Keys
        if event.type == pygame.KEYDOWN:
            #Moving left when pressing left
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x_change -= go_speed
                    carImg = pygame.image.load('streetcar_left.png') #Loading an image so that it points left
            #Moving to the right when pressing right
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_change += go_speed
                    carImg = pygame.image.load('streetcar_right.png') #Loading an image so that it points right
            #Moving up when pressing up
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y_change -= go_speed                    
                    carImg = pygame.image.load('streetcar_forwards.png') #Loading an image so that it points up
            #Moving up when pressing down
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y_change += go_speed
                    carImg = pygame.image.load('streetcar_backwards.png') #Loading an image so that it points down
        #When letting go of the keys to stop moving
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                x_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                y_change = 0
        #End of Movement Keys

    #Changing the coordinates
    x += x_change
    y += y_change

#Boundaries for Car
    #Outisde of the Screen Boundaries
    if x < 0:
        x = 0
    if x > display_width - car_width:
        x = (display_width - car_width)
    if y < 0:
        y = 0
    if y > display_height - car_height:
        y = (display_height - car_height)
#End of Boundaries

#Laps
    if 200 < x < 240 and 700 < y and pointable == True:
        laps += 1
        door = True
        if laps > numlaps:
            endgame = True
        pointable = False
        #print(str(laps))

    gameDisplay.fill(white) #Deleting the previous screen

#Timer Track
    track(0,0,1800,125)
#Main Track
    track(200,600,400,100)
    track(550,500,50,100)
    track(600,500,350,75)
    track(725,800,275,100)
    track(950,525,350,100)
    track(1000,700,200,200)
    track(1200,850,600,150)
    track(1500,275,100,215)
    track(1275,575,400,100)
    track(1200,200,400,100)
    track(950,250,100,300)
    track(1250,400,50,150)
    track(800,125,50,250)
    track(600,325,200,50)
    track(600,200,50,125)
    track(650,200,90,50)
    track(400,125,75,400)
    track(200,250,75,350)
    track(150,375,50,250)
    track(0,300,80,225)

#Reverse Door
    if 1800 > x > 1675 and 675 > y > 575: #If you pass the point the door opens so you can complete a lap and be able to score a point
        door = False
        pointable = True

    if door == True: #Door so you couldn't go backwards through the track
        track(80,475,70,50)

#Star Points
    if 670 < x < 720 and 260 < y < 310: #Getting the star if you touch it
        star = True
    if star == False:
        gameDisplay.blit(pygame.image.load('star.png'), (670,260))
    
#Finish Line
    pygame.draw.rect(gameDisplay, black, (200,700,20,20))
    pygame.draw.rect(gameDisplay, black, (200,740,20,20))
    pygame.draw.rect(gameDisplay, black, (200,780,20,20))
    pygame.draw.rect(gameDisplay, black, (200,820,20,20))
    pygame.draw.rect(gameDisplay, black, (200,860,20,20))
    pygame.draw.rect(gameDisplay, black, (220,720,20,20))
    pygame.draw.rect(gameDisplay, black, (220,760,20,20))
    pygame.draw.rect(gameDisplay, black, (220,800,20,20))
    pygame.draw.rect(gameDisplay, black, (220,840,20,20))
    pygame.draw.rect(gameDisplay, black, (220,880,20,20))
    pygame.draw.rect(gameDisplay, black, (200,700,40,200), 1)

    car(x,y) #Updating the car position

    #Timer
    if x_change != 0 or y_change != 0 or moved == True:
        moved = True #If you've moved you can start the timer
        timel = timep
        timea += 1
        timer += 1
        timep = math.floor(timer/60)
        if timep >= 60: #Rollover for the minutes
            minutet += 1
            timer += -3600
      
#Lap Counter
    if laps < 1: #Displaying the laps as 1 before you started
        message_display('1/' + str(numlaps), 100, 75, 100, white)
    elif laps >= 1: #Displaying the number of laps compared to the number of laps
        message_display(str(laps) + '/' + str(numlaps), 100, 75, 100, white)

#Time Counter
    if minutet >= 10 and timep >= 10: #Displays time that has passed
        message_display(str(minutet) + ':' + str(timep), 1650, 75, 100, white)
    elif minutet < 10 and timep >= 10: #Adds a 0 before the minute so that there's 4 digits
        message_display('0' + str(minutet) + ':' + str(timep), 1650, 75, 100, white)
    elif minutet < 10 and timep < 10: #Adds a 0 before the seconds and the minutes so there's 4 digits
        message_display('0' + str(minutet) + ':' + '0' + str(timep), 1650, 75, 100, white)
    elif minutet >= 10 and timep < 10: #Adds a 0 before the seconds so there's 4 digits
        message_display(str(minutet) + ':' + '0' + str(timep), 1650, 75, 100, white)
            
    pygame.display.update()
    clock.tick(60)

#Endscreen
while endgame == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    gameDisplay.fill(white)
    message_display('GAME OVER', 900, 150, 100, black) #End Title
    #Time for the end screen
    if minutet >= 10 and timep >= 10: 
        message_display('Time ' + str(minutet) + ':' + str(timep), 900, 300, 70, black)
    elif minutet < 10 and timep >= 10:
        message_display('Time ' + '0' + str(minutet) + ':' + str(timep), 900, 300, 70, black)
    elif minutet < 10 and timep < 10:
        message_display('Time ' + '0' + str(minutet) + ':' + '0' + str(timep), 900, 300, 70, black)
    elif minutet >= 10 and timep < 10:
        message_display('Time ' + str(minutet) + ':' + '0' + str(timep), 900, 300, 70, black)

    if star == True: #Puts a star if you got it in the game
        gameDisplay.blit(pygame.image.load('big_star.png'), (650,375))
    else: #Puts finish line flags if you don't get the star
        gameDisplay.blit(pygame.image.load('End_Flags.png'), (650,375))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
