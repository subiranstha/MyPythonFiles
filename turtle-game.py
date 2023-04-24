#importin moudules turtle, random and Threading
import turtle
import random
import threading


BLUE,WHITE,GREEN = range(3)# 0, 1, 2 value for BLUE, WHITE, GREEN respectively for the state of squre
x_axis = 0 # next square x-axis value
y_axis = 0 # next square y-axis value
y =int(turtle.numinput('number of grid','Please Provide the grid size',minval=3,maxval=8))# Grid square Size 
level = int(turtle.numinput('Level','Please Provide the level',minval=1,maxval=3)) # level of speed of square to beclicked
speedLevel = 0.0 # speed of square

#Condition for the mapping level and square speed 
if(level==1):
    speedLevel = 2.0
elif(level==2):
    speedLevel = 1.5
else:
    speedLevel = 1.0

COLOR_STATE = BLUE # initializing the COLOR_STATE = 0 (BLUE) 

turtle.penup() # penup() function so that turle doesn't draw while setting new position
sample = turtle.Turtle() # Creating new Turtle object (sample) for Start Button and Counting the number of square on the screen
sample.hideturtle() # Hiding the turtle sample so no pointer is seen in the screen
pen = sample.getpen() # Creating instance pen to get pen for sample object
sample1 = turtle.Turtle() # Creating New turtle object (sample1) for score of the user
sample1.hideturtle() # Hiding the turtle sample1 so the pointer is not seen in the screen
score_pen = sample1.getpen() # Creating the score_pen to get pen for sample object
t = turtle.stamp # t for the stamping the square
startStatus = True # Boolean variable to start the square hunt game after clicking the start button
score = 0 # To record the score of the user
num = 1 # to record the number of square that has been displayed
turtle.setup(750,800) # to set up the windows size for the square hunt game
turtle.hideturtle() # to hide the turtle so pointer is not seen in the screen
turtle.speed(0) # for maxmizing the speed for creating the grid
turtle.setposition(-350,-375) # position the start point for creating grild
turtle.pendown() # To draw the while moving the turtle 
turtle.pensize(5) # defining the size for pen

# drawing the outer square for the grid
for x in range(4):
    turtle.forward(700)# move 700 pixels forward from the previous point
    if(x < 3):
        turtle.left(90) # change the angle to 90 degree left of the turtle

new_state = False # to control glitch created when click and next square happen in same time
z = float("{:.2f}".format(700/y)) # defining the length for smaller inside square grid
turtle.register_shape('new_square',((0,z-20),(z-20,z-20),(z-20,0),(0,0))) # registering the new_square with size for the turtle hunt
turtle.setposition(-350,-375) # setting postion for the turtle
turtle.setheading(0) # setting angle for the turtle

# for creating the inside vertical line for the grid
for x in range (y - 1):
    turtle.forward(z)
    turtle.setheading(90)
    turtle.forward(700)
    turtle.sety(-375)
    turtle.setheading(0)

turtle.setposition(-350,-375)
turtle.setheading(90)

# for creating inside horizontal line for the grid
for x in range (y - 1):
    turtle.forward(z)
    turtle.setheading(0)
    turtle.forward(700)
    turtle.setx(-350)
    turtle.setheading(90)
turtle.penup()# to remove the mark while setting new position
turtle.setposition(-350,345) # setting position for the title of the game
turtle.write("Square Hunt",move=False,align="left",font=("Arial",15,"normal"))# writing the title of the game in the screen
pen.penup() # to remove while mark while setting new position
pen.setposition(-70,330) # setting new position for the start button
pen.speed(0) # setting an angle of the pen
pen.pendown() # to draw the while moving the pen
pen.pen(fillcolor='red',pencolor='black') # setting the fillcolor and pen color while moving
pen.begin_fill() # to begin fill when the pen moves
pen.forward(150) # moving the pen forward 
pen.left(90) # changing the angle 90 degree left
pen.forward(50) # moving the pen forward
pen.left(90) # Changing the angle 90 degree left 
pen.forward(150)
pen.left(90)
pen.forward(50)
pen.penup()
pen.setposition(0,345) # setting position so that to write start inside the button 
pen.write("Start",move=False,align="Center",font=("Arial",15,"normal")) # writing inside the button
pen.end_fill() # to end fill that of the pen
score_pen.penup() # so that the score_pen doesn't draw while moving
score_pen.setposition(350,345)  # setting position of the score_pen to record the score of the users while playing the game
score_pen.write("Score ="+ str(score),move=False,align="right",font=("Arial",15,"normal")) # to Write the score of the user starting from 0

# next_square function to show the next squre 
def next_square():
    global COLOR_STATE,x_axis,y_axis,speedLevel,num,t,new_state # to use the global variable 
    new_state = True 
    turtle.penup()
    if(num <= 10): # so that number of square displayed by game doesn't exceed 10
        if(COLOR_STATE != BLUE and COLOR_STATE !=GREEN): # while the color_state is WHITE i.e (neither BLUE or GREEN)
            COLOR_STATE = BLUE # stating the color_state BLUE
            x_axis = random.randrange(1,y) # Picking x value at random from 1 to y(i.e number of grid)
            y_axis = random.randrange(1,y) # Picking y value at random from 1 to y(i.e number of grid)
            threading.Timer(speedLevel,next_square).start() # Using the threading.Timer for scheduling call for the next_square()
            draw_hide_square(x_axis,y_axis) # calling the Function draw_hide_square
        else: # when the color_state is not WHITE i.e(either BLUE or GREEN)
            COLOR_STATE = WHITE # stating the color_state WHITE
            draw_hide_square(x_axis,y_axis) # calling the function draw_hide_square
            threading.Timer(0,next_square).start() # Using the threading.Timer for scheduling call for the next_square()
    else: # when the num value exceed 10 
        pen.clear() # clearing all the things written by the pen instance
        turtle.clearstamp(t) # clearing the stamp
        pen.write("Finished",move=False,align="Center",font=("Arial",15,"normal"))# Writing the finished in the screen to show the user the game is finished
        turtle.clearstamp(t) # Clearing the stamp so now square is shown a the end of the game
    new_state = False
    
# handle_click when the user click on the screen 
def handle_click(x,y): 
    global COLOR_STATE,x_axis,y_axis,t,score,startStatus,t,new_state,num # using global variables
    turtle.penup() # when turtle moves the turtle doesn't show any draws
    if(startStatus == True): # so that the game doesn't start until the user click on the start button
        print(x,y)
        if(x >= -70 and y >= 330 and x <= -70 + 150 and y <= 330+50): # when the user click on the area of button game starts
            startStatus = False # stating the startStatus to False so that games start
            next_square()
    else:# activates only  when users clicks on the start button i.e startStatus must be False
        if(x >= (x_axis*z)-350 and y >= ((y_axis-1)*z)-375 and x <= ((x_axis+1)*z)-350 and y <= ((y_axis)*z)-375 and COLOR_STATE != GREEN): # conditon for the user when the user click on the right square
            COLOR_STATE = GREEN # stating the color to green so that multiple click doesn't affect the score
            score = score + 1 # adding the score when the users click on the right square
            score_pen.clear() # Clearing all the thing written or drawn by score pen
            score_pen.write("Score ="+ str(score),move=False,align="right",font=("Arial",15,"normal")) # writing the new score on the screen
            turtle.pen(fillcolor='Green',pencolor= 'Green') # changing the color of turtle to Green 
            turtle.clearstamp(t) # removing the previous stamp
            t = turtle.stamp() # rewriting the stamp with new color
        elif(x >= -350 and y >= -375 and x <= -350 + 700 and y <= -375 + 700 and COLOR_STATE !=GREEN): # condition when the user click on the wrong square (which is inside the grid)
            COLOR_STATE = GREEN # changing the status to Green so that the multiple click doesn't affect the score
            if(score>0): # condition so that Score cannot go negative
                score = score - 1 # subtracting the from the previous Score
                score_pen.clear() # Clearing all the things drawn or written by score_pen
                score_pen.write("Score ="+ str(score),move=False,align="right",font=("Arial",15,"normal")) # writing hte new score on the screen
    if(new_state): # for handing the next_square and handle_click when occur in same time
        turtle.clearstamp(t) # clearing the stamp
        new_state = False # stating the new_state to false
        print('new state',num)   
         
# to draw new square or to removing the existing square
def draw_hide_square(x_axis,y_axis):
    global COLOR_STATE,t,pen,num # Using the global variables
    pen.clear() # Clearing all the things written or drawn by the pen
    pen.penup() 
    pen.setposition(0,345)
    pen.write("["+str(num)+"]",move=False,align="center",font=("Arial",15,"normal")) # Showing the number square shown by the game
    turtle.penup()
    turtle.setposition(-350,-375) # setting the positon of the turtle
    turtle.shape('new_square') # setting up the square
    turtle.setposition(x_axis*z -350+10,y_axis*z -375-10) # setting the square position
    turtle.setheading(0) # setting up the heading of the squre
    turtle.pen(fillcolor='Blue',pencolor='Blue') # turtle color and fill color setting to square
    if(COLOR_STATE == WHITE): # when the color_state is WHITE
        turtle.clearstamp(t) # Clearing the current square
    else:
        turtle.clearstamp(t) # Clearign the current Square
        num = num + 1 # Adding the number for the square
        t =turtle.stamp() # showing the square
        
   
turtle.listen() # listening to the click
turtle.onscreenclick(handle_click) # when there is the click on the screen then handle click is called
turtle.mainloop() # for interactive use of turtle