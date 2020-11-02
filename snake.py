import pygame, random, pathlib

width = 600
height = 450
rect = 15

path = pathlib.Path(__file__).resolve().parent

gameover = False
cursor = 0
difficulty = None
score = 0

difficulties = {
    "Easy" : 10,
    "Medium" : 15,
    "Hard" : 20,
}

go_options = [
    "Play Again",
    "Quit",
]

pygame.init()

clock = pygame.time.Clock()
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

background = pygame.image.load(str(path) + "/lib/background.jpg")
background = pygame.transform.scale(background, (width, height))
font = str(path) + "/lib/font.ttf"

red = pygame.Color(255, 0, 0)
green = pygame.Color("green")
white = pygame.Color(255, 255, 255)
grey = pygame.Color(50, 50, 50)
yellow = pygame.Color("yellow")
black = pygame.Color(0, 0, 0)
background_color = pygame.Color(0, 20, 0)
purple = pygame.Color("purple")

class Snake:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = "right"
        self.tail = []
        self.color = 255
    
    def show(self):
        self.eat()
        self.move()

        # Head
        if self.x > width/rect-1: self.x = 0
        elif self.x < 0: self.x = width/rect
        elif self.y > height/rect-1: self.y = 0
        elif self.y < 0: self.y = height/rect
        pygame.draw.rect(display, (0, self.color, 0), (int(self.x*rect), int(self.y*rect), rect, rect))
        
        # Body
        g = self.color
        for part in self.tail:
            if g > 105:
                g -= 10
            if self.x == part[0] and self.y == part[1]:
                global gameover
                gameover = True
            else:
                pygame.draw.rect(display, (0, g, 0), (int(part[0]*rect), int(part[1]*rect), rect, rect))

    def eat(self):
        global score
        
        self.tail.insert(0, (self.x, self.y))

        if food.x == self.x and food.y == self.y:
            food.isEaten = True
            score += 1
        elif badfood.x == self.x and badfood.y == self.y:
            badfood.isEaten = True
            self.tail = self.tail[:-2]
            if score > 0:
                score -= 1
        else:
            self.tail = self.tail[:-1]

    def move(self):
        if self.direction == "right": self.x += 1
        elif self.direction == "left": self.x -= 1
        elif self.direction == "up": self.y -= 1
        elif self.direction == "down": self.y += 1

class Food:
    def __init__(self):
        self.x = None
        self.y = None
        self.isEaten = False
    
    def show(self):
        if self.isEaten == False and self.x != None and self.y != None:
            pygame.draw.ellipse(display, red, (self.x*rect, self.y*rect, rect, rect))
        else:
            self.new()

    def new(self):
        while True:
            self.x = random.randint(0, int(width/rect - 1))
            self.y = random.randint(0, int(height/rect - 1))
            if self.x != badfood.x and self.y != badfood.y and badfood.isEaten == False:
                self.isEaten = False
                break

class BadFood:
    def __init__(self):
        self.x = None
        self.y = None
        self.isEaten = False
    
    def show(self):
        if self.isEaten == False and self.x != None and self.y != None:
            pygame.draw.ellipse(display, purple, (self.x*rect, self.y*rect, rect, rect))
        else:
            self.new()

    def new(self):
        while True:
            self.x = random.randint(0, int(width/rect - 1))
            self.y = random.randint(0, int(height/rect - 1))
            if self.x != food.x and self.y != food.y and food.isEaten == False:
                self.isEaten = False
                break

def show_fps(surface, font_size, visible, color, xy):
    fps_font = pygame.font.Font(font, font_size)
    fps = fps_font.render(str(int(clock.get_fps())), visible, color)
    surface.blit(fps, (xy[0], xy[1]))

def draw_grid(surface, spacebtwn, color):
    for x in range(1, int(height/spacebtwn)):
        pygame.draw.line(surface, color, (0, x*rect), (width, x*rect))
    for y in range(1, int(width/spacebtwn)):
        pygame.draw.line(surface, color, (y*rect, 0), (y*rect, height))

def select_difficulty():
    # Background Image
    display.blit(background, (0, 0))

    header_font = pygame.font.Font(font, 60)
    header = header_font.render("Select Difficulty", True, white)
    header_rect = header.get_rect()
    header_rect.midtop = (int(width/2), int(height/5))

    dif_font = pygame.font.Font(font, 25)
    for dif in difficulties:
        if cursor % len(difficulties) == list(difficulties.keys()).index(dif):
            dif_option = dif_font.render(dif, True, green)
        else: dif_option = dif_font.render(dif, True, white)

        dif_option_rect = dif_option.get_rect()
        dif_option_rect.center = (int(width/2), int(height/2) + list(difficulties.keys()).index(dif)*40)
        display.blit(dif_option, dif_option_rect)

    display.blit(header, header_rect)
    
def game_over():
    global difficulty
    
    # Background image
    display.blit(background, (0, 0))
    difficulty = None
    
    header_font = pygame.font.Font(font, 60)
    header = header_font.render("Game Over!", True, white)
    header_rect = header.get_rect()
    header_rect.midtop = (int(width/2), int(height/5))
    
    scr_font = pygame.font.Font(font, 20)
    scr = scr_font.render(f"Score: {score}", True, white)
    scr_rect = scr.get_rect()
    scr_rect.midtop = (int(width/2), int(height/4) + 45) 
    
    opt_font = pygame.font.Font(font, 25)
    for opt in go_options:
        if cursor % len(go_options) == go_options.index(opt):
            go_option = opt_font.render(opt, True, green)
        else: go_option = opt_font.render(opt, True, white)
        
        go_option_rect = go_option.get_rect()
        go_option_rect.center = (int(width/2), int(height/2) + go_options.index(opt)*40)
        display.blit(go_option, go_option_rect)
    
    display.blit(header, header_rect)
    display.blit(scr, scr_rect)
    
def replay():
    global difficulty
    global gameover
    global score

    difficulty = None
    gameover = False
    snake.x = 0
    snake.y = 0
    score = 0
    snake.direction = "right"
    snake.tail.clear()
    food.isEaten = True
    badfood.isEaten = True



snake = Snake()
food = Food()
badfood = BadFood()

# Game loop
while True:
    display.fill(background_color)

    if not gameover:
        if difficulty == None:
            select_difficulty()
        else:
            food.show()
            badfood.show()
            snake.show()
            draw_grid(display, rect, grey)
    else:
        game_over()
    
    # Keyboard handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            # Difficulty selection:
            if difficulty == None and gameover == False:
                if event.key == pygame.K_UP:
                    cursor -= 1
                if event.key == pygame.K_DOWN:
                    cursor += 1
                if event.key == pygame.K_RETURN:
                    for dif in difficulties:
                        if cursor%len(difficulties) == list(difficulties.keys()).index(dif):
                            difficulty = difficulties[dif]

            # Player movement:
            if difficulty != None and gameover == False:
                if event.key == pygame.K_LEFT and snake.direction != "right":
                    snake.direction = "left"
                if event.key == pygame.K_RIGHT and snake.direction != "left":
                    snake.direction = "right"
                if event.key == pygame.K_UP and snake.direction != "down":
                    snake.direction = "up"
                if event.key == pygame.K_DOWN and snake.direction != "up":
                    snake.direction = "down"
                    
            # Replay selection:
            if gameover == True:
                if event.key == pygame.K_UP:
                    cursor -= 1
                if event.key == pygame.K_DOWN:
                    cursor += 1
                if event.key == pygame.K_RETURN:
                    for opt in go_options:
                        if cursor%len(go_options) == go_options.index(opt):
                            if go_options[go_options.index(opt)] == "Play Again":
                                replay()
                            else:
                                pygame.quit()
                                exit()
    

    show_fps(display, 20, True, yellow, (10, 10))
    pygame.display.update()
    clock.tick(60 if difficulty == None else difficulty)
