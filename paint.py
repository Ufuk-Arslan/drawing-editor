'''
CmpE 496 HCI - HW1 - Drawing Editor

Authors:        UFUK ARSLAN - OĞUZ ARSLAN
Student Nos:    2017400219 - 2017405180
Date:           12.03.2022 
'''

from tkinter import *
import math

# Global constants for shape and operation names
rectangle = "rectangle"
square = "square"
circle = "circle"
line = "line"

draw = "draw"
move = "move"
delete = "delete"

shape_buttons = {}
operation_buttons = {}

# Keeps track of selected shape among (line, rectangle, square, circle)
shape = line

# Keeps track of selected operation among (draw, edit, delete)
operation = draw

# Keep track of the point mouse button 1 was clicked
x1, y1 = None, None

# Keep track of the point mouse button 1 was released
x2, y2 = None, None


# ------ EVENT HANDLER FUNCTIONS ---------------------------------------- #

def mouse_left_down(event=None):
    # Set x and y coordinates when mouse is clicked
    global x1
    global y1
    x1 = event.x
    y1 = event.y

def mouse_left_up(event=None):
    # Set x and y coordinates when mouse is released
    global x2
    global y2
    x2 = event.x
    y2 = event.y
    # when mouse button is released, perform the corresponding operation
    if operation == draw:
        if shape == line:
            draw_line(event)
        elif shape == rectangle:
            draw_rectangle(event)
        elif shape == square:
            draw_square(event)
        elif shape == circle:
            draw_circle(event)
    elif operation == delete or operation == move:
        closest_items = event.widget.find_closest(x1, y1)
        if len(closest_items) == 0: return
        item = closest_items[0]
        if operation == delete: event.widget.delete(item)
        if operation == move: event.widget.move(item, x2-x1, y2-y1)
    
def motion(event=None):
    # When a motion happens in the canvas, all the items are colored black
    for item in event.widget.find_all():
        if event.widget.type(item) == "line":
            event.widget.itemconfigure(item, fill="black")
        else:
            event.widget.itemconfigure(item, outline="black")
    if operation != delete and operation != move: return
    closest_items = event.widget.find_closest(event.x, event.y)
    if len(closest_items) == 0: return
    # If we are going to perform a delete operation the closest item is colored red
    if operation == delete:
        if event.widget.type(closest_items[0]) == "line":
            event.widget.itemconfigure(closest_items[0], fill="red")
        else:
            event.widget.itemconfigure(closest_items[0], outline="red")
    # If we are going to perform a move operation the closest item is colored cyan
    else:
        if event.widget.type(closest_items[0]) == "line":
            event.widget.itemconfigure(closest_items[0], fill="cyan")
        else:
            event.widget.itemconfigure(closest_items[0], outline="cyan")
    
    

# ------ DRAWING FUNCTIONS -------------------------------------------------- #

# Draw a line between (x1,y1) and (x2,y2)
def draw_line(event=None):
    if None not in (x1, y1, x2, y2):
        if operation == draw:
            event.widget.create_line(x1, y1, x2, y2, smooth=TRUE)

# Draw a rectangle with top-left corner at(x1,y1) and bottom-right corner at (x2,y2)
def draw_rectangle(event=None):
    if None not in (x1, y1, x2, y2):
        event.widget.create_rectangle(x1, y1, x2, y2)

# Draw a square  with top-left corner at (x1,y1) and length of an edge is x2-y2
def draw_square(event=None):
    x_length, y_length = max(x2 - x1, x1 - x2), max(y2 - y1, y1 - y2)
    length = min(x_length, y_length)
    direction = 1 if y2 >= y1 else -1

    x3 = x2 if y_length >= x_length else x1 + direction*length
    y3 = y2 if x_length > y_length else y1 + direction*length
        
    if None not in (x1, y1, x2, y2, x3, y3):
        event.widget.create_rectangle(x1, y1, x3, y3)

# Draw a circle that the center is center of mass of (x1,y1) and (x2,y2),
# radius is the half of the distance between (x1,y1) and (x2,y2)
def draw_circle(event=None):
    r = math.sqrt(pow(y2-y1, 2) + pow(x2-x1, 2)) / 2
    x0 = (x1 + x2) / 2
    y0 = (y1 + y2) / 2
    
    x3 = x0 - r
    y3 = y0 - r
    x4 = x0 + r
    y4 = y0 + r
    
    if None not in (x3, y3, x4, y4):
        event.widget.create_oval(x3, y3, x4, y4)

# ------ PROGRAM SETUP FUNCTIONS ------------------------------------------------ #
def setButtonsToDefault():
    global shape_buttons
    global operation_buttons
    for button in shape_buttons.keys(): shape_buttons[button].configure(bg="white")
    for button in operation_buttons.keys(): operation_buttons[button].configure(bg="white")

# Sets the global shape variable
def onShapeSelectionClick(input):
    global shape
    global operation
    global shape_buttons
    setButtonsToDefault()
    shape_buttons[input].configure(bg="#8cb8ff")
    shape = input
    operation = draw
    
# Sets the global operation variable
def onOperationSelectionClick(input):
    global operation
    global operation_buttons
    setButtonsToDefault()
    operation_buttons[input].configure(bg="#8cb8ff")
    operation = input

# Initialize the GUI
root = Tk()
root.title(string='CmpE 496 HCI - Drawing Editor')

main_frame = LabelFrame(root, width = 1000, height = 100)
main_frame.pack(side = TOP)

shape_buttons_frame = LabelFrame(main_frame, cursor = "target")
shape_buttons_frame.pack(side = LEFT)

operation_buttons_frame = LabelFrame(main_frame, cursor = "target")
operation_buttons_frame.pack(side = RIGHT)

canvas_frame = LabelFrame(root, cursor = "tcross")
canvas_frame.pack(side = TOP)

drawing_area = Canvas(canvas_frame, width=1000, height=500)
drawing_area.pack()

rectangle_image = PhotoImage(file = r"rectangle.png").subsample(20, 20)
square_image = PhotoImage(file = r"square.png").subsample(20, 20)
circle_image = PhotoImage(file = r"circle.png").subsample(20, 20)
line_image = PhotoImage(file = r"line.png").subsample(20, 20)
move_image = PhotoImage(file = r"move.png").subsample(20, 20)
delete_image = PhotoImage(file = r"delete.png").subsample(20, 20)

shape_buttons[rectangle] = Button(shape_buttons_frame, text = " Rectangle", padx=15, bg="white", pady=5, image = rectangle_image, compound = LEFT, command=lambda: onShapeSelectionClick(rectangle))
shape_buttons[rectangle].pack(side = LEFT)
shape_buttons[square] = Button(shape_buttons_frame, text = " Square", padx=15, pady=5, bg="white", image = square_image, compound = LEFT, command=lambda: onShapeSelectionClick(square))
shape_buttons[square].pack(side = LEFT)
shape_buttons[circle] = Button(shape_buttons_frame, text = " Circle", padx=15, pady=5, bg="white", image = circle_image, compound = LEFT, command=lambda: onShapeSelectionClick(circle))
shape_buttons[circle].pack(side = LEFT)
shape_buttons[line] = Button(shape_buttons_frame, text = " Line", padx=15, pady=5, bg="#8cb8ff", image = line_image, compound = LEFT, command=lambda: onShapeSelectionClick(line))
shape_buttons[line].pack(side = LEFT)
operation_buttons[delete] = Button(operation_buttons_frame, text = " Delete", padx=15, pady=5, bg="white", image = delete_image, compound = LEFT, command=lambda: onOperationSelectionClick(delete))
operation_buttons[delete].pack(side = RIGHT)
operation_buttons[move] = Button(operation_buttons_frame, text = " Move", padx=15, pady=5, bg="white", image = move_image, compound = LEFT, command=lambda: onOperationSelectionClick(move))
operation_buttons[move].pack(side = RIGHT)

drawing_area.bind("<ButtonPress-1>", mouse_left_down)
drawing_area.bind("<ButtonRelease-1>", mouse_left_up)
drawing_area.bind("<Motion>", motion)

root.mainloop()
