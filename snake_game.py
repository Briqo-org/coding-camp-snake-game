import turtle
import random

# Game settings
w = 500           # Screen width
h = 500           # Screen height
food_size = 20    # Size of the food
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
    global snake, snake_dir, food_position
    snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    snake_dir = "up"
    food_position = get_random_food_position()
    food.goto(food_position)
    move_snake()

def move_snake():
    global snake_dir, paused

    if paused:
        turtle.ontimer(move_snake, delay)
        return

    # Calculate new head position
    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_dir][0]
    new_head[1] += offsets[snake_dir][1]

    if new_head in snake[:-1]:  # Collision with self
        reset()
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

# Start the game
reset()
turtle.done()

