import pygame
import math
import random
pygame.init()

#Setting Up display
display_width = 1800
display_height = 900
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('STREET SPEED') #Window Name

#Colour tuples
black = (0,0,0) 
white = (255,255,255)
green = (0,255,0)
lessgreen = (20,200,20)
red = (255,0,0)

clock = pygame.time.Clock()
crashed=False
carImg = pygame.image.load('streetcar_right.png') #Starting image for the car

#Window Icon
gameIcon = pygame.image.load('streeticon.png')
pygame.display.set_icon(gameIcon)

car_width = 50
car_height = 50

def car(x,y): #Change the cars position with only the coordinates
    gameDisplay.blit(carImg, (x,y))

def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

#Display text on the screen
def message_display(text, width, height, size, colour): #Input the string, the position of the text, the font size, and the colour of the text
    largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, largeText, colour)
    TextRect.center = (width,height)
    gameDisplay.blit(TextSurf, TextRect)

#Spawn Point
coords = [125,750] #Array to hold the coordinates

#Misc Variables
xychange = [0,0] #Array to hold the change in coordinates
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
speedboost = False #If true the car goes faster
times = 0 #Time to countdown the speed
slowdown = False #If true car goes slower
thingcounter = 0 #General counting variable
funmode = False #Extra setting

rancol = [0,0,0] #Array for generating random colours

#Function to create the track easily
def track(startingx, startingy, rectwidth, rectheight): #The topleft corner coordinates and the width and length of the rectangle
    if funmode == False:
        pygame.draw.rect(gameDisplay, black, (startingx, startingy, rectwidth, rectheight)) #Drawing the rectangle
    elif funmode == True:
        pygame.draw.rect(gameDisplay, rancol, (startingx, startingy, rectwidth, rectheight)) #Drawing the rectangle
    #Borders
    if (startingx - car_width + 25) > coords[0] > (startingx - car_width) and (startingy + rectheight) > coords[1] > (startingy - car_height): 
        coords[0] = (startingx - car_width)
    elif (startingx + rectwidth - 25) < coords[0] < (startingx + rectwidth) and (startingy + rectheight) > coords[1] > (startingy - car_height):
        coords[0] = (startingx + rectwidth)
    elif (startingy - car_height + 25)> coords[1] > (startingy - car_height) and (startingx - car_width) < coords[0] < (startingx + rectwidth):
        coords[1] = (startingy - car_height)
    elif (startingy + rectheight - car_height - 25) < coords[1] < (startingy + rectheight) and (startingx - car_width) < coords[0] < (startingx + rectwidth):
        coords[1] = (startingy + rectheight)

#Function to add speed boosts
def fast(cornerx,cornery): #Input the coordinates of topleft corner
    global speedboost
    if star == False and speedboost == False and slowdown == False:
        gameDisplay.blit(pygame.image.load('speed.png'),(cornerx,cornery))
        if (cornerx + 40) >= coords[0] >= (cornerx - car_width) and (cornery + 30) >= coords[1] >= (cornery - car_height):
            speedboost = True
            
#Function to add slowdown
def slow(cornerx,cornery): #Input the coordinates of the topleft corner
    global slowdown
    if slowdown == False and speedboost == False:
        gameDisplay.blit(pygame.image.load('slow.png'),(cornerx,cornery))
        if (cornerx + 40) >= coords[0] >= (cornerx - car_width) and (cornery + 40) >= coords[1] >= (cornery - car_height):
            slowdown = True

#Start Screen
while not started:
    thingcounter += 1 #Counts the amount of frames
    if thingcounter == 12: #Once x frames have passed it enables a colour change
        rancol[0] = random.randint(0,255) #Changes the red value 
        rancol[1] = random.randint(0,255) #Changes the green value
        rancol[2] = random.randint(0,255) #Changes the blue value
        thingcounter = 0 #Resets the frame counter

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
    if funmode == False:
        message_display('STREET SPEED', 900, 150, 100, black) #Title
    elif funmode == True:
        message_display('STREET SPEED', 900, 150, 100, rancol)
    gameDisplay.blit(pygame.image.load('pixel_car.png'),(drift,200)) #Draws the car

    #Buttons
    #colours in the button that's selected
    if top_button == True: 
        pygame.draw.rect(gameDisplay, green, (825, 550, 275, 125))
    elif top_button == False:
            pygame.draw.rect(gameDisplay, green, (825, 725, 275, 125))

    #Draws the buttons
    if funmode == False:
        pygame.draw.rect(gameDisplay, black, (825, 550, 275, 125), 3)
        pygame.draw.rect(gameDisplay, black, (825, 725, 275, 125), 3)
        message_display('START', 962, 612, 25, black)
        message_display('OPTIONS', 962, 787, 25, black)
    elif funmode == True:
        pygame.draw.rect(gameDisplay, rancol, (825, 550, 275, 125), 3)
        pygame.draw.rect(gameDisplay, rancol, (825, 725, 275, 125), 3)
        message_display('START', 962, 612, 25, rancol)
        message_display('OPTIONS', 962, 787, 25, rancol)

    #Options menu
    while options == True:
        thingcounter += 1 #Counts the amount of frames
        if thingcounter == 8: #Once x frames have passed it enables a colour change
            rancol[0] = random.randint(0,255) #Changes the red value 
            rancol[1] = random.randint(0,255) #Changes the green value
            rancol[2] = random.randint(0,255) #Changes the blue value
            thingcounter = 0 #Resets the frame counter        
          
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN: #Moves the selected button up and down
                if event.key == pygame.K_UP and otselect > 1 and oselected == 0:
                     otselect += -1
                elif event.key == pygame.K_DOWN and otselect < 4 and oselected == 0:
                     otselect += 1

                #When pressing enter it selects the option
                if event.key == pygame.K_RETURN and otselect == 1 and oselected == 0:
                    oselected = 1
                elif event.key == pygame.K_RETURN and otselect == 2 and oselected == 0:
                    oselected = 2
                elif event.key == pygame.K_RETURN and otselect == 3 and oselected == 0:
                    oselected = 3
                elif event.key == pygame.K_RETURN and otselect == 4:
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
                #Fun
                elif event.key == pygame.K_DOWN and oselected == 3 and funmode == False:
                    funmode = True
                elif event.key == pygame.K_DOWN and oselected == 3 and funmode == True:
                    funmode = False
                elif event.key == pygame.K_UP and oselected == 3 and funmode == False:
                    funmode = True
                elif event.key == pygame.K_UP and oselected == 3 and funmode == True:
                    funmode = False

                #Deselects the option
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_LEFT and oselected != 0:
                    oselected = 0

        gameDisplay.fill(white)
        if funmode == False:
            message_display('OPTIONS', 300, 100, 100, black) #Title for the options screen
        elif funmode == True:
            message_display('OPTIONS', 300, 100, 100, rancol)

        gameDisplay.blit(pygame.image.load('gears.png'), (50,550)) #Little image for the options screen

        #The laps button when selected
        if oselected == 1:
            pygame.draw.rect(gameDisplay, lessgreen, (100,250,300,75))
            message_display('Laps', 150, 275, 40, white)
            if funmode == False:
                message_display('Speed', 165, 375, 40, black)
                message_display('Fun', 140, 450, 40, black)
                message_display('Back', 135, 515, 25, black)
            elif funmode == True:
                message_display('Speed', 165, 375, 40, rancol)
                message_display('Fun', 140, 450, 40, rancol)
                message_display('Back', 135, 515, 25, rancol)
            #Up and down buttons
            pygame.draw.polygon(gameDisplay, white, [[300,280], [320,255], [340,280]])
            pygame.draw.polygon(gameDisplay, white, [[300,295], [320,320], [340,295]])

        #The speed button when selected
        elif oselected == 2:
            pygame.draw.rect(gameDisplay, lessgreen, (100,350,300,75))
            message_display('Speed', 165, 375, 40, white)
            if funmode == False:
                message_display('Laps', 150, 275, 40, black)
                message_display('Fun', 140, 450, 40, black)
                message_display('Back', 135, 515, 25, black)
            elif funmode == True:
                message_display('Laps', 150, 275, 40, rancol)
                message_display('Fun', 140, 450, 40, rancol)
                message_display('Back', 135, 515, 25, rancol)
            #Up and down buttons
            pygame.draw.polygon(gameDisplay, white, [[300,380], [320,355], [340,380]])
            pygame.draw.polygon(gameDisplay, white, [[300,395], [320,420], [340,395]])

        #The fun button when selected
        elif oselected == 3:
            pygame.draw.rect(gameDisplay, lessgreen, (100,420,300,75))
            message_display('Fun', 140, 450, 40, white)
            if funmode == False:
                message_display('Laps', 150, 275, 40, black)
                message_display('Speed', 165, 375, 40, black)
                message_display('Back', 135, 515, 25, black)
            elif funmode == True:
                message_display('Laps', 150, 275, 40, rancol)
                message_display('Speed', 165, 375, 40, rancol)
                message_display('Back', 135, 515, 25, rancol)

        #Buttons when hovered
        if otselect == 1 and oselected == 0:
            if funmode == False:
                pygame.draw.rect(gameDisplay, black, (100,250,300,75))
                message_display('Speed', 165, 375, 40, black)
                message_display('Fun', 140, 450, 40, black)
                message_display('Back', 135, 515, 25, black)
            if funmode == True:
                pygame.draw.rect(gameDisplay, rancol, (100,250,300,75))
                message_display('Speed', 165, 375, 40, rancol)
                message_display('Fun', 140, 450, 40, rancol)
                message_display('Back', 135, 515, 25, rancol)
            message_display('Laps', 150, 275, 40, white)


        elif otselect == 2 and oselected == 0:
            if funmode == False:
                pygame.draw.rect(gameDisplay, black, (100, 350, 300, 75))
                message_display('Laps', 150, 275, 40, black)
                message_display('Fun', 140, 450, 40, black)
                message_display('Back', 135, 515, 25, black)
            elif funmode == True:
                pygame.draw.rect(gameDisplay, rancol, (100, 350, 300, 75))
                message_display('Laps', 150, 275, 40, rancol)
                message_display('Fun', 140, 450, 40, rancol)
                message_display('Back', 135, 515, 25, rancol)
            message_display('Speed', 165, 375, 40, white)

        elif otselect == 3 and oselected == 0:            
            if funmode == False:
                pygame.draw.rect(gameDisplay, black, (100, 420, 300, 75))
                message_display('Back', 135, 515, 25, black)
                message_display('Speed', 165, 375, 40, black)
                message_display('Laps', 150, 275, 40, black)
            elif funmode == True:
                pygame.draw.rect(gameDisplay, rancol, (100, 420, 300, 75))
                message_display('Back', 135, 515, 25, rancol)
                message_display('Speed', 165, 375, 40, rancol)
                message_display('Laps', 150, 275, 40, rancol)
            message_display('Fun', 140, 450, 40, white)

        elif otselect == 4 and oselected == 0:
            message_display('Back', 135, 515, 25, white)
            if funmode == False:
                pygame.draw.rect(gameDisplay, black, (100, 500, 75, 25))
                message_display('Speed', 165, 375, 40, black)
                message_display('Laps', 150, 275, 40, black)
                message_display('Fun', 140, 450, 40, black)
            elif funmode == True:
                pygame.draw.rect(gameDisplay, rancol, (100, 500, 75, 25))
                message_display('Speed', 165, 375, 40, rancol)
                message_display('Laps', 150, 275, 40, rancol)
                message_display('Fun', 140, 450, 40, rancol)

        #The values for the buttons
        if otselect == 1 or oselected == 1:
            message_display(str(numlaps), 375, 275, 40, white)
            if funmode == False:
                message_display(str(go_speed), 375, 375, 40, black)
                message_display('No', 360, 450, 40, black)
            elif funmode == True:
                message_display('Yes', 360, 450, 40, rancol)
                message_display(str(go_speed), 375, 375, 40, rancol)

        elif otselect == 2 or oselected == 2:
            message_display(str(go_speed), 375, 375, 40, white)
            if funmode == False:
                message_display(str(numlaps), 375, 275, 40, black)
                message_display('No', 360, 450, 40, black)
            elif funmode == True:
                message_display('Yes', 360, 450, 40, rancol)
                message_display(str(numlaps), 375, 275, 40, rancol)

        elif otselect == 3:
            if funmode == False:
                message_display(str(numlaps), 375, 275, 40, black)
                message_display(str(go_speed), 375, 375, 40, black)
                message_display('No', 360, 450, 40, white)
            elif funmode == True:
                message_display(str(numlaps), 375, 275, 40, rancol)
                message_display(str(go_speed), 375, 375, 40, rancol)
                message_display('Yes', 360, 450, 40, white)

        elif otselect == 4:
            message_display('Back', 135, 515, 25, white)
            if funmode == False:
                message_display(str(numlaps), 375, 275, 40, black)
                message_display(str(go_speed), 375, 375, 40, black)
                message_display('No', 360, 450, 40, black)
            elif funmode == True:
                message_display(str(numlaps), 375, 275, 40, rancol)
                message_display(str(go_speed), 375, 375, 40, rancol)
                message_display('Yes', 360, 450, 40, rancol)

        pygame.display.update()
        clock.tick(60)

    pygame.display.update()
    clock.tick(60)

while not crashed and endgame == False:
    thingcounter += 1 #Counts the amount of frames
    if thingcounter == 15: #Once x frames have passed it enables a colour change
        rancol[0] = random.randint(0,255) #Changes the red value 
        rancol[1] = random.randint(0,255) #Changes the green value
        rancol[2] = random.randint(0,255) #Changes the blue value
        thingcounter = 0 #Resets the frame counter    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True          
    
        #Movement Keys
        if event.type == pygame.KEYDOWN:
            #Moving left when pressing left
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    xychange[0] -= go_speed
                    carImg = pygame.image.load('streetcar_left.png') #Loading an image so that it points left
            #Moving to the right when pressing right
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    xychange[0] += go_speed
                    carImg = pygame.image.load('streetcar_right.png') #Loading an image so that it points right
            #Moving up when pressing up
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    xychange[1] -= go_speed                    
                    carImg = pygame.image.load('streetcar_forwards.png') #Loading an image so that it points up
            #Moving up when pressing down
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    xychange[1] += go_speed
                    carImg = pygame.image.load('streetcar_backwards.png') #Loading an image so that it points down
        #When letting go of the keys to stop moving
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                xychange[0] = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                xychange[1] = 0
        #End of Movement Keys

    #Changing the coordinates
    if speedboost == True:
        coords[0] += (xychange[0] * 2)
        coords[1] += (xychange[1] * 2)
    elif slowdown == True:
        coords[0] += math.floor(xychange[0] / 2)
        coords[1] += math.floor(xychange[1] / 2)
    else:
        coords[0] += xychange[0]
        coords[1] += xychange[1]

#Boundaries for Car
    #Outisde of the Screen Boundaries
    if coords[0] < 0:
        coords[0] = 0
    if coords[0] > display_width - car_width:
        coords[0] = (display_width - car_width)
    if coords[1] < 0:
        coords[1] = 0
    if coords[1] > display_height - car_height:
        coords[1] = (display_height - car_height)
#End of Boundaries

#Laps
    if 200 < coords[0] < 240 and 650 < coords[1] and pointable == True:
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

#Boosts
    fast(625,615)
    fast(1225,795)
    fast(1700,450)
    fast(1700,150)
    fast(1205,150)
    fast(415,550)

#Slowdowns
    slow(220,200)
    slow(1350,690)
    slow(925,740)
    slow(1550,515)
    slow(980,200)
    slow(480,200)
    slow(550,320)

#Reverse Door
    if 1800 > coords[0] > 1650 and 675 > coords[1] > 575: #If you pass the point the door opens so you can complete a lap and be able to score a point
        door = False
        pointable = True

    if door == True: #Door so you couldn't go backwards through the track
        track(80,475,70,50)
    elif door == False:
        track(1150,600,50,200)

#Star Points
    if 670 < coords[0] < 720 and 260 < coords[1] < 310: #Getting the star if you touch it
        star = True
    if star == False:
        gameDisplay.blit(pygame.image.load('star.png'), (670,260))
    
#Finish Line
    if funmode == False:
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
    elif funmode == True:
        pygame.draw.rect(gameDisplay, rancol, (200,700,20,20))
        pygame.draw.rect(gameDisplay, rancol, (200,740,20,20))
        pygame.draw.rect(gameDisplay, rancol, (200,780,20,20))
        pygame.draw.rect(gameDisplay, rancol, (200,820,20,20))
        pygame.draw.rect(gameDisplay, rancol, (200,860,20,20))
        pygame.draw.rect(gameDisplay, rancol, (220,720,20,20))
        pygame.draw.rect(gameDisplay, rancol, (220,760,20,20))
        pygame.draw.rect(gameDisplay, rancol, (220,800,20,20))
        pygame.draw.rect(gameDisplay, rancol, (220,840,20,20))
        pygame.draw.rect(gameDisplay, rancol, (220,880,20,20))
        pygame.draw.rect(gameDisplay, rancol, (200,700,40,200), 1)

    car(coords[0],coords[1]) #Updating the car position

    #Timer
    if xychange[0] != 0 or xychange[1] != 0 or moved == True:
        moved = True #If you've moved you can start the timer
        timel = timep
        timea += 1
        timer += 1
        timep = math.floor(timer/60)
        if timep >= 60: #Rollover for the minutes
            minutet += 1
            timer += -3600
        if speedboost == True or slowdown == True: #Timer to count time after speed
            times += 1

    if times > 60: #Expires the speedboost after a second
        speedboost = False
        slowdown = False
        times = 0 #Resets the timer
      
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
    thingcounter += 1 #Counts the amount of frames
    if thingcounter == 9: #Once x frames have passed it enables a colour change
        rancol[0] = random.randint(0,255) #Changes the red value 
        rancol[1] = random.randint(0,255) #Changes the green value
        rancol[2] = random.randint(0,255) #Changes the blue value
        thingcounter = 0 #Resets the frame counter
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    gameDisplay.fill(white)
    if funmode == False:
        message_display('GAME OVER', 900, 150, 100, black) #End Title
    elif funmode == True:
        message_display('GAME OVER', 900, 150, 100, rancol)
    
    #Time for the end screen   
    if funmode == False: 
        if minutet >= 10 and timep >= 10: 
            message_display('Time ' + str(minutet) + ':' + str(timep), 900, 300, 70, black)
        elif minutet < 10 and timep >= 10:
            message_display('Time ' + '0' + str(minutet) + ':' + str(timep), 900, 300, 70, black)
        elif minutet < 10 and timep < 10:
            message_display('Time ' + '0' + str(minutet) + ':' + '0' + str(timep), 900, 300, 70, black)
        elif minutet >= 10 and timep < 10:
            message_display('Time ' + str(minutet) + ':' + '0' + str(timep), 900, 300, 70, black)
    elif funmode == True:
        if minutet >= 10 and timep >= 10: 
            message_display('Time ' + str(minutet) + ':' + str(timep), 900, 300, 70, rancol)
        elif minutet < 10 and timep >= 10:
            message_display('Time ' + '0' + str(minutet) + ':' + str(timep), 900, 300, 70, rancol)
        elif minutet < 10 and timep < 10:
            message_display('Time ' + '0' + str(minutet) + ':' + '0' + str(timep), 900, 300, 70, rancol)
        elif minutet >= 10 and timep < 10:
            message_display('Time ' + str(minutet) + ':' + '0' + str(timep), 900, 300, 70, rancol)

    if star == True: #Puts a star if you got it in the game
        gameDisplay.blit(pygame.image.load('big_star.png'), (650,375))
    else: #Puts finish line flags if you don't get the star
        gameDisplay.blit(pygame.image.load('End_Flags.png'), (650,375))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()