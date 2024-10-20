import turtle
import random

# Game settings
w = 500           # Screen width
h = 500           # Screen height
food_size = 10    # Size of the food
delay = 100       # Delay in milliseconds between movements (controls speed)

# Movement offsets for the snake based on direction
offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

paused = False  # Track if the game is paused

def reset():
    """
    Resets the game by initializing the snake, setting its direction to 'up', 
    placing food in a random position, and starting the snake's movement.
    """
    global snake, snake_dir, food_position, pen
    # Initial snake body coordinates
    snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    snake_dir = "up"  # Start moving upwards
    food_position = get_random_food_position()  # Get new random position for the food
    food.goto(food_position)  # Move the food to its new position
    move_snake()  # Start snake movement

def move_snake():
    """
    Handles the movement of the snake based on its direction. The snake's 
    position is updated, collisions are checked (with itself or food), 
    and the game continues unless paused.
    """
    global snake_dir, paused

    if paused:  # Skip movement if the game is paused
        turtle.ontimer(move_snake, delay)  # Continue checking in intervals
        return

    # Calculate new head position
    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_dir][0]
    new_head[1] = snake[-1][1] + offsets[snake_dir][1]

    if new_head in snake[:-1]:  # If the snake collides with itself
        reset()  # Restart the game
    else:
        snake.append(new_head)  # Add the new head position to the snake

        if not food_collision():  # If food isn't eaten
            snake.pop(0)  # Remove the tail to keep the snake the same length

        # Handle screen boundary wrapping (snake moves to opposite side)
        if snake[-1][0] > w / 2:
            snake[-1][0] -= w
        elif snake[-1][0] < -w / 2:
            snake[-1][0] += w
        elif snake[-1][1] > h / 2:
            snake[-1][1] -= h
        elif snake[-1][1] < -h / 2:
            snake[-1][1] += h

        pen.clearstamps()  # Clear the previous snake stamps

        # Draw the snake on the screen
        for segment in snake:
            pen.goto(segment[0], segment[1])
            pen.stamp()

        screen.update()  # Refresh the screen to show updates

    # Continue to move the snake after the delay
    turtle.ontimer(move_snake, delay)

def food_collision():
    """
    Checks if the snake's head has collided with the food. If so, the food 
    is relocated and returns True. Otherwise, returns False.
    """
    global food_position
    if get_distance(snake[-1], food_position) < 20:  # Collision threshold
        food_position = get_random_food_position()  # Get a new random position for food
        food.goto(food_position)  # Move the food to the new position
        return True
    return False

def get_random_food_position():
    """
    Generates a random position for the food within the screen boundaries.
    """
    x = random.randint(int(-w / 2 + food_size), int(w / 2 - food_size))
    y = random.randint(- int(h / 2 + food_size), int(h / 2 - food_size))
    return (x, y)

def get_distance(pos1, pos2):
    """
    Returns the Euclidean distance between two points.
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5

# Direction controls for the snake
def go_up():
    global snake_dir
    if snake_dir != "down":  # Prevent reversing direction
        snake_dir = "up"

def go_right():
    global snake_dir
    if snake_dir != "left":  # Prevent reversing direction
        snake_dir = "right"

def go_down():
    global snake_dir
    if snake_dir != "up":  # Prevent reversing direction
        snake_dir = "down"

def go_left():
    global snake_dir
    if snake_dir != "right":  # Prevent reversing direction
        snake_dir = "left"

def toggle_pause():
    """
    Pauses or unpauses the game.
    """
    global paused
    paused = not paused  # Toggle pause state

def draw_border():
    """
    Draws a black border around the screen to represent the boundaries
    where the snake wraps around.
    """
    border_pen = turtle.Turtle()  # Create a new turtle for drawing the border
    border_pen.hideturtle()  # Hide the turtle (we just want the drawing)
    border_pen.penup()
    border_pen.goto(-w / 2, h / 2)  # Go to the top-left corner of the screen
    border_pen.pendown()
    border_pen.pensize(3)  # Set the thickness of the border
    border_pen.color("black")  # Set the color to black

    # Draw the rectangular border
    for _ in range(2):
        border_pen.forward(w)  # Move right
        border_pen.right(90)
        border_pen.forward(h)  # Move down
        border_pen.right(90)

# Setup the screen
screen = turtle.Screen()
screen.setup(w, h)           # Set the screen width and height
screen.title("Snake Game")    # Set the window title
screen.bgcolor("blue")        # Set the background color
screen.tracer(0)              # Disable automatic screen updates for smoother animation

# Setup the pen for drawing the snake
pen = turtle.Turtle("square")
pen.penup()  # Disable drawing line

# Setup the food turtle
food = turtle.Turtle()
food.shape("square")
food.color("yellow")
food.shapesize(food_size / 20)  # Set the food size relative to the default turtle size
food.penup()  # Disable drawing line

# Setup keyboard controls for snake movement and pause
screen.listen()  # Listen for key presses
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(toggle_pause, "p")

# Draw the border around the screen
draw_border()

# Start the game
reset()  # Initialize the game state
turtle.done()  # Keep the window open
