import turtle
import random

# Game settings
w = 500           # Screen width
h = 500           # Screen height
food_size = 20    # Size of the food
delay = 100       # Delay in milliseconds between movements (controls speed)
running = True  # Flag to indicate if the game is running

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
    global snake, snake_dir, food_position, pen, running
    # Initial snake body coordinates
    snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    snake_dir = "up"  # Start moving upwards
    food_position = get_random_food_position()  # Get new random position for the food
    food.goto(food_position)  # Move the food to its new position

    running = True  # After resetting, allow the game to continue

    move_snake()  # Start snake movement

def move_snake():
    """
    Handles the movement of the snake based on its direction. The snake's 
    position is updated, collisions are checked (with itself or food), 
    and the game continues unless paused.
    """
    global snake_dir, paused, running

    if not running:  # Stop movement if the game is resetting
        return

    if paused:
        turtle.ontimer(move_snake, delay)
        return

    # Calculate new head position
    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_dir][0]
    new_head[1] += offsets[snake_dir][1]

    if new_head in snake[:-1]:  # If the snake collides with itself
        running = False  # Stop the game loop
        reset()  # Restart the game
        return
    else:
        snake.append(new_head)

        if not food_collision():
            snake.pop(0)  # Remove tail if not eating

        # Handle screen boundary wrapping
        if snake[-1][0] > w / 2:
            snake[-1][0] -= w
        elif snake[-1][0] < -w / 2:
            snake[-1][0] += w
        elif snake[-1][1] > h / 2:
            snake[-1][1] -= h
        elif snake[-1][1] < -h / 2:
            snake[-1][1] += h

        pen.clearstamps()  # Clear previous stamps

        # Draw the snake
        for segment in snake:
            pen.goto(segment[0], segment[1])
            pen.stamp()

        screen.update()  # Refresh the screen

    turtle.ontimer(move_snake, delay)

def food_collision():
    global food_position
    if get_distance(snake[-1], food_position) < food_size:
        food_position = get_random_food_position()
        food.goto(food_position)
        return True
    return False

def get_random_food_position():
    x = random.randint(-w//2 + food_size, w//2 - food_size)
    y = random.randint(-h//2 + food_size, h//2 - food_size)
    return (x, y)

def get_distance(pos1, pos2):
    return ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) ** 0.5

def go_up():
    global snake_dir
    if snake_dir != "down":
        snake_dir = "up"

def go_right():
    global snake_dir
    if snake_dir != "left":
        snake_dir = "right"

def go_down():
    global snake_dir
    if snake_dir != "up":
        snake_dir = "down"

def go_left():
    global snake_dir
    if snake_dir != "right":
        snake_dir = "left"

def toggle_pause():
    global paused
    paused = not paused

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
screen.setup(w, h)
screen.title("Snake Gameeeeeeeeeeeeeeeee")
screen.bgcolor("orange")
screen.tracer(0)

# Setup the pen for drawing the snake
pen = turtle.Turtle("square")
pen.penup()

# Setup the food turtle
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.shapesize(food_size / 20)
food.penup()

# Setup keyboard controls
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(toggle_pause, "p")

# Draw the border around the screen
draw_border()

# Start the game
reset()
turtle.done()

