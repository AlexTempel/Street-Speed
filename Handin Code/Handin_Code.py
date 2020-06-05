import pygame
import math
pygame.init()

#Setting Up display
display_width = 1800
display_height = 900
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('STREET SPEED')
#End setting up display

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed=False
carImg = pygame.image.load('Right.png')

car_width = 50
car_height = 50

def car(x,y):
    gameDisplay.blit(carImg, (x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_display(text, width, height,size):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (width,height)
    gameDisplay.blit(TextSurf, TextRect)

#Spawn Point
x = (125)
y = (750)

#Misc Variables
x_change = 0
y_change = 0
timer = 0
timep = 0
minutet = 0
timea = 0
moved = False
laps = 0
pointable = True
timepoint = 0
numlaps = 3
go_speed = 5
started = False
while not started:
    
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True          
    
        #Movement Keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x_change -= go_speed
                    carImg = pygame.image.load('Left.png')
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_change += go_speed
                    carImg = pygame.image.load('Right.png')
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y_change -= go_speed                    
                    carImg = pygame.image.load('Forward.png')
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y_change += go_speed
                    carImg = pygame.image.load('Backwards.png')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                x_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                y_change = 0
        #End of Movement Keys

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
    #Internal Track Boundaries
    if 650 > y > 150 and 1575 < x < 1600:
        x = 1600
    if 650 > y > 150 and 150 < x < 175:
        x = 150
    if 1600 > x > 200 and  675 < y < 700:
        y = 700
    if 1600 > x > 200 and 150 < y < 175:
        y = 150
#End of Boundaries

#Laps
    if 200 < x < 240 and 700 < y and pointable == True:
        laps += 1
        pointable = False
        #print(str(laps))

    gameDisplay.fill(white)

#Drawing Track
    pygame.draw.rect(gameDisplay, black, (200,200,1400,500))
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

    car(x,y)

    #Timer
    if x_change != 0 or y_change != 0 or moved == True:
        moved = True
        timel = timep
        timea += 1
        timer += 1
        timep = math.floor(timer/60)
        if timep >= 60:
            minutet += 1
            timer += -3600
        #if timep != timel:
        #    print(str(minutet),':',str(timep))
      
#Lap Counter
    if laps < 1:
        message_display('1/' + str(numlaps), int(display_width/2), int((display_height/2)+ 150), 100)
    elif laps >= 1:
        message_display(str(laps) + '/' + str(numlaps), int(display_width/2), int((display_height/2)+ 150), 100)

#Time Counter
    if minutet >= 10 and timep >= 10:
        message_display(str(minutet) + ':' + str(timep), int(display_width/2), int(display_height/2), 115)
    elif minutet < 10 and timep >= 10:
        message_display('0' + str(minutet) + ':' + str(timep), int(display_width/2), int(display_height/2), 115)
    elif minutet < 10 and timep < 10:
        message_display('0' + str(minutet) + ':' + '0' + str(timep), int(display_width/2), int(display_height/2), 115)
    elif minutet >= 10 and timep < 10:
        message_display(str(minutet) + ':' + '0' + str(timep), int(display_width/2), int(display_height/2), 115)

    if pointable == False:
        timepoint += 1

    if timepoint >= 420:
        pointable = True
        timepoint = 0
            
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
