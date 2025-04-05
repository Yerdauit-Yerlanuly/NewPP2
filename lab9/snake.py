import pygame, time, sys, random

#Класс стены
class Wall:
    def __init__(self, snakeBody): #Конструктор
        self.size = 20
        self.rect = self.spawn(snakeBody)

    def spawn(self, snakeBody): #Функция для спавна
        while True:
            self.x = random.randint(0, width // self.size - 1) * self.size
            self.y = random.randint(0, height // self.size - 1) * self.size
            wall = pygame.Rect(self.x, self.y, self.size, self.size)

            if wall not in snakeBody:
                return wall
            
    def draw(self, screen): #Функция для прорисовки
        global level
        if level % 2 == 0:
            pygame.draw.rect(screen, (135, 135, 135), self.rect)
        else:
            pygame.draw.rect(screen, (95, 95, 95), self.rect)

#Класс яблоко
class Apple:
    def __init__(self, snakeBody, walls): #Конструктор
        self.size = 20
        self.rect = self.spawn(snakeBody, walls)

    def spawn(self, snakeBody, walls): #Функция для спавна яблока на рандомном месте
        while True:
            self.x = random.randint(0, width // self.size - 1) * self.size
            self.y = random.randint(0, height // self.size - 1) * self.size
            apple = pygame.Rect(self.x, self.y, self.size, self.size) #Создаем квадрат для яблоки

            if apple not in snakeBody and all(not apple.colliderect(wall.rect) for wall in walls): #Проверка находиться ли яблоко под змейкой или под стеной
                return apple
            
    def draw(self, screen): #Функция для прорисовки
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

#Класс Змейки
class Snake:
    def __init__(self): #Конструктор
        self.size = 20
        self.body = [pygame.Rect(300 - i * self.size, 300 - i * self.size, self.size, self.size)
                     for i in range(3)] #Создаем квадраты(тело и голова змеи)
        
        self.direction = pygame.Vector2(1, 0) #Направление змеи(вправо)
        self.nextDirection = self.direction #Чтобы избежать багов

        self.walls = [] #создаем список стен
        self.addWalls() #Вызываем метод для создания стен
        self.apple = Apple(self.body, self.walls) #Создаем объект яблоко
        
    def addWalls(self): #Функция для спавна стен
        self.walls.append(Wall(self.body + [wall.rect for wall in self.walls]))
        self.walls.append(Wall(self.body + [wall.rect for wall in self.walls]))

    def draw(self, screen): #Функция для прорисовки
        pygame.draw.rect(screen, (0, 128, 0), self.body[0]) #Рисуем голову

        for segment in self.body[1:]: #Рисуем остальную часть тела
            pygame.draw.rect(screen, (45, 200, 45), segment)

        for wall in self.walls: #Рисуем стены
            wall.draw(screen)

        self.apple.draw(screen)
        
    def move(self): #Функция для движения
        global speed, apples, level, threshold, score, milliseconds
        self.direction = self.nextDirection #Чтобы избежать багов

        #Копируем основную голову и меняем координаты новой головы
        head = self.body[0].copy()
        head.x += self.direction.x * self.size
        head.y += self.direction.y * self.size

        #Если голова вышло за пределами границ
        if head.x < 0 or head.x >= width or head.y < 0 or head.y >= height:
            return False
        
        #Если голова врезалась об свое тело
        if head in self.body:
            return False
        
        #Если голова врезалась об стену
        for wall in self.walls:
            if head.colliderect(wall.rect):
                return False

        self.body.insert(0, head) #Добавляем новую голову в первую позицию

        #Если змейка съела яблоко
        if head == self.apple.rect:
            pygame.time.set_timer(appleTimer, milliseconds) #Возобновляем таймер после того, как наша змейка съела яблоко

            weight = random.randint(1, 3) #Вес яблоки
            score += weight #Рандомное число, которое мы генерируем и добавляем - это вес яблоки
            apples += 1 #Для отслежиания в целом сколько яблок было съедено

            if score >= threshold + 3: #Для отслеживания предела
                self.addWalls() #Добавляем стены
                threshold += 3
                
                levelUp = pygame.mixer.Sound("src/snake/level-up.mp3") #Включаем музыку
                levelUp.play()

                #Добавляем уровень и скорость
                level += 1
                speed += 1

                if milliseconds >= 2000: #Каждый раз когда увеличивается уровень уменьшаем значение в таймере
                    milliseconds -= 100
                #В итоге добавляем скорость, уменьшаем время для таймера и переходим на следующий уровень, если количество яблок превысила предел яблок кратных 3(3, 9, 12, ...)
            else:
                eat = pygame.mixer.Sound("src/snake/eating.mp3")
                eat.play()

            time.sleep(0.1)

            self.apple = Apple(self.body, self.walls) #Создаем новый объект яблоки
        else:
            self.body.pop() #Удаляем тело в последнем фрейме, чтобы все выглядело нормально

        return True

#Инициализация
pygame.init()
pygame.mixer.init()
fps = pygame.time.Clock()

#Переменные
width = 600
height = 600
speed = 5
apples = 0
score = 0
threshold = 0 #Для отслеживания яблок
level = 1
done = False
milliseconds = 4000 #Изначальное значение для таймера 4 секунд

#Панель и музыка
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
pygame.mixer.music.load("src/snake/back.mp3")
pygame.mixer.music.play(-1)

#Фонты и тексты
font = pygame.font.SysFont("Verdana", 50)
smallFont = pygame.font.SysFont("Verdana", 30)
over = font.render("Game Over", True, (0, 0, 0))
win = font.render("Congrats! You passed", True, (0, 0, 0))
win2 = font.render("the game!!!", True, (0, 0, 0))


#Создаем объект
S1 = Snake()

#Создаем пользователькое событие
appleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(appleTimer, milliseconds) #Таймер на 3 секунд

while not done:
    #Если это следующий уровень, то меняем задний фон
    if level % 2 == 0:
        screen.fill((152, 251, 152))
    else:
        screen.fill((152, 255, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:  #Проверяем, было ли нажато какое-либо клавиша
           
            #Проверяем, нажал ли игрок клавишу влево и не движется ли змейка направо
            if event.key == pygame.K_LEFT and not S1.direction.x == 1:
                S1.nextDirection = pygame.Vector2(-1, 0)  #Двигаемся влево

            #Проверяем, нажал ли игрок клавишу вправо и не движется ли змейка влево
            if event.key == pygame.K_RIGHT and not S1.direction.x == -1:
                S1.nextDirection = pygame.Vector2(1, 0)  #Двигаемся вправо

            #Проверяем, нажал ли игрок клавишу вверх и не движется ли змейка вниз
            if event.key == pygame.K_UP and not S1.direction.y == 1:
                S1.nextDirection = pygame.Vector2(0, -1)  #Двигаемся вверх

            #Проверяем, нажал ли игрок клавишу вниз и не движется ли змейка вверх
            if event.key == pygame.K_DOWN and not S1.direction.y == -1:
                S1.nextDirection = pygame.Vector2(0, 1)  #Двигаемся вниз
        
        if event.type == appleTimer:
            S1.apple = Apple(S1.body, S1.walls)

    if not S1.move(): #Проверяем может ли объект так ходить
        #Включаем музыку
        pygame.mixer.music.stop()
        gameOver = pygame.mixer.Sound("src/snake/gameOver.mp3")
        gameOver.play()

        time.sleep(0.5)

        #Заполняем экран красным цветом и добавляем надпись
        screen.fill((255, 0, 0))
        screen.blit(over, (150, 250))

        pygame.display.flip()

        time.sleep(1)

        #Выходим из игры
        sys.exit()
        pygame.quit()

    #Чтобы пройти игру польностью, надо дойти до 15 уровня
    if level == 15:
        time.sleep(0.5)

        screen.blit(win, (30, 200))
        screen.blit(win2, (130, 260))
        pygame.display.flip()

        time.sleep(1)

        sys.exit()
        pygame.quit()

    S1.draw(screen) #Прорисовываем объект

    #Рендерим текст
    scoreText = smallFont.render("Score: " + str(score), True, (0, 0, 0))
    scoredLevel = smallFont.render("Level: " + str(level), True, (0, 0, 0))
    screen.blit(scoreText, (20, 20))
    screen.blit(scoredLevel, (450, 20))

    pygame.display.flip() #Обновляем экран
    fps.tick(speed) #Фрейм используется как скорость

pygame.quit()