import pygame, time, sys, random, psycopg2

# Параметры подключения
conn = psycopg2.connect(
    host = "localhost",
    port = 5432,            #Стандартный порт PostgreSQL
    database = "snake",     #Имя базы данных
    user = "postgres",      #Имя пользователя
    password = "61154365"           #Пароль
)

# Создание курсора
cursor = conn.cursor()

#Инициализация
pygame.init()
pygame.mixer.init()
fps = pygame.time.Clock()

#Переменные
change = ""
exist = ""
username = ""
warning = ""
width = 600
height = 600
speed = 5
apples = 0
score = 0
threshold = score - score % 3 #Для отслеживания яблок
level = 1
milliseconds = 4000 #Изначальное значение для таймера 4 секунд
done = False
active = False
setName = True
paused = False

#Панель и музыка
screen = pygame.display.set_mode((width, height))
image = pygame.image.load("snake/register.png")
image = pygame.transform.scale(image, (600, 600))
pygame.display.set_caption("Snake")
pygame.mixer.music.load("snake/back.mp3")
pygame.mixer.music.play(-1)

#Фонты и тексты
font = pygame.font.SysFont("Verdana", 50)
smallFont = pygame.font.SysFont("Verdana", 30)
smallerFont = pygame.font.SysFont("Verdana", 20)
over = font.render("Game Over", True, (0, 0, 0))
win = font.render("Congrats! You passed", True, (0, 0, 0))
win2 = font.render("the game!!!", True, (0, 0, 0))

#Класс стены
class Wall:
    def __init__(self, snakeBody, range): #Конструктор
        self.size = 20
        self.rect = self.spawn(snakeBody, range)

    def spawn(self, snakeBody, range): #Функция для спавна
        while True:
            self.x = random.randint(range[0], range[1] // self.size - 1) * self.size
            self.y = random.randint(range[2] // self.size, range[3] // self.size - 1) * self.size
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
    def __init__(self, level, apples): #Конструктор
        self.size = 20
        self.body = [pygame.Rect(300 - i * self.size, 300, self.size, self.size)
                     for i in range(3 + apples)] #Создаем квадраты(тело и голова змеи)
        
        self.direction = pygame.Vector2(1, 0) #Направление змеи(вправо)
        self.nextDirection = self.direction #Чтобы избежать багов

        self.walls = [] #создаем список стен
        self.addWalls() #Вызываем метод для создания стен
        self.createWalls(level) #Вызываем метод для создания стен пользователям сохранившую игру
        self.apple = Apple(self.body, self.walls) #Создаем объект яблоко
        

    def createWalls(self, level): #Функция для спавна стен пользователям сохранившую игру
        for i in range(level - 1):
            self.walls.append(Wall(self.body + [wall.rect for wall in self.walls], [0, width, 0, height // 2 - 40]))
            self.walls.append(Wall(self.body + [wall.rect for wall in self.walls], [0, width, height // 2 + 40, height]))

    def addWalls(self): #Функция для спавна стен
        self.walls.append(Wall(self.body + [wall.rect for wall in self.walls], [0, width, 0, height // 2 - 40]))
        self.walls.append(Wall(self.body + [wall.rect for wall in self.walls], [0, width, height // 2 + 40, height]))

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
                
                levelUp = pygame.mixer.Sound("snake/level-up.mp3") #Включаем музыку
                levelUp.play()

                #Добавляем уровень и скорость
                level += 1
                speed += 1

                if milliseconds >= 2000: #Каждый раз когда увеличивается уровень уменьшаем значение в таймере
                    milliseconds -= 100
                #В итоге добавляем скорость, уменьшаем время для таймера и переходим на следующий уровень, если количество яблок превысила предел яблок кратных 3(3, 9, 12, ...)
            else:
                eat = pygame.mixer.Sound("snake/eating.mp3")
                eat.play()

            time.sleep(0.1)

            self.apple = Apple(self.body, self.walls) #Создаем новый объект яблоки
        else:
            self.body.pop() #Удаляем тело в последнем фрейме, чтобы все выглядело нормально

        return True

while setName: #Цикл для авторизации
    screen.blit(image, (0, 0)) #Заполняет экран изображением
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            setName = False
            done = True

        #Если мышка зажата
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 140 <= event.pos[0] <= 460 and 300 <= event.pos[1] <= 350:
                active = True

                if username: #Если никнейм есть
                    setName = False
                else:
                    warning = "Please enter your name"

            if 140 <= event.pos[0] <= 460 and 380 <= event.pos[1] <= 440:
                if username:
                    setName = False
                else:
                    warning = "Please enter your name"

        #Если кнопка нажата и рект активна
        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE: #Если нажата кнопка бэкспейс
                username = username[:-1]
            elif event.key == pygame.K_RETURN: #Если нажат Ентер
                if username:
                    setName = False

                #Выбираем запись где ник равно юзернейму
                cursor.execute("""
                    SELECT * FROM "user"
                    WHERE name = %s
                """, (username,))

                exist = cursor.fetchall() #Получение записей

                #Выбираем запись где ник раывно юзернейму и мод равно сейвед
                cursor.execute("""
                    SELECT level, speed, apples FROM "user"
                    WHERE name = %s and mode = 'saved'
                """, (username,))

                row = cursor.fetchone() #Получение записи

                #Выбираем счет где ник равно юзернейму
                cursor.execute("""
                    SELECT score FROM "user_score"
                    WHERE name = %s
                """, (username,))

                row1 = cursor.fetchone() #Получение записи
                if row:
                    #Извлекаем значения для переменнех
                    level = row[0]
                    speed = row[1]
                    apples = row[2]
                    score = row1[0]
                    milliseconds -= level * 100
            else:
                if len(username) < 15: #юзернейм должен содержать не больше 15 символов
                    username += event.unicode #Возврщает символьное представление клавиши
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                warning = "Please enter your name"
        
    #Рендерим текст
    pauseInstruction = smallerFont.render("Click P to pause the game", True, (0, 0, 0))
    usernameRender = smallFont.render(username, True, (0, 0, 0))
    screen.blit(usernameRender, (150, 310))
    screen.blit(pauseInstruction, (180, 450))

    #Предупреждение
    if not username:
        warningMessage = smallerFont.render(warning, True, (255, 0, 0))
        screen.blit(warningMessage, ((width - warningMessage.get_width()) // 2, 350))

    pygame.display.update()
    fps.tick(60)


#Создаем объект
S1 = Snake(level, apples)

#Создаем пользователькое событие
appleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(appleTimer, milliseconds) #Таймер на 4 секунды

while not done:
    #Если это следующий уровень, то меняем задний фон
    if level % 2 == 0:
        screen.fill((152, 251, 152))
    else:
        screen.fill((152, 255, 100))
        
    if paused: #Если игру поставили на паузу
        #Рендерим текст
        resume = smallFont.render("Resume", True, (230, 230, 230))
        save = smallFont.render("Save the Game", True, (230, 230, 230))
        pause = font.render("Paused", True, (0, 0, 0))

        #Создаем  квадраты
        rect = pygame.Rect(100, 100, 400, 400)
        boxForResume = pygame.Rect(220, 240, resume.get_width() + 20, resume.get_height() + 20)
        boxForSave = pygame.Rect(180, 345, save.get_width() + 20, save.get_height() + 20)

        #Заполняем экран
        screen.fill((255, 255, 255), rect)
        screen.fill((255, 0, 0), boxForResume)
        screen.fill((225, 225, 0), boxForSave)
        screen.blit(pause, (300 - pause.get_width() // 2, 120))
        screen.blit(resume, (230, 250))
        screen.blit(save, (190, 355))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boxForResume.collidepoint(event.pos): #Если нажата кнопка востановления игры
                    paused = not paused
                elif boxForSave.collidepoint(event.pos): #Если нажата кнопка сохранения игры
                    if exist: #Если пользователь существует в бд
                        #Обновляем его данные
                        cursor.execute("""
                            UPDATE "user"
                            SET level = %s, speed = %s, apples = %s, mode = 'saved'
                            WHERE name = %s
                        """, (level, speed, apples, username))

                        conn.commit() #Коммитим изменения

                        #Обновляем данные в другой таблице тоже
                        cursor.execute("""
                            UPDATE "user_score"
                            SET score = %s
                            WHERE name = %s
                        """, (score, username))

                        conn.commit() #Коммитим изменения
                    else: #Если пользователь не существует
                        #Добавляе новую запись
                        cursor.execute("""
                            INSERT INTO "user" (name, level, speed, apples, mode)
                            VALUES (%s, %s, %s, %s, 'saved')
                        """, (username, level, speed, apples))

                        conn.commit() #Коммитим изменения

                        #Добавляем новую запись в другую таблицу
                        cursor.execute("""
                            INSERT INTO "user_score" (name, score)
                            VALUES (%s, %s)
                        """, (username, score))

                        conn.commit() #Коммитим изменения

                    done = True
    else: #Если игра не на паузе
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = True

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

                if event.key == pygame.K_p:
                    paused = not paused
                
            if event.type == appleTimer:
                S1.apple = Apple(S1.body, S1.walls)

        if not S1.move(): #Проверяем может ли объект так ходить
            #Включаем музыку
            pygame.mixer.music.stop()
            gameOver = pygame.mixer.Sound("snake/gameOver.mp3")
            gameOver.play()

            if exist: #Если пользователь существует в бд
                #Обновляем данные
                cursor.execute("""
                    UPDATE "user"
                    SET level = %s, speed = %s, apples = %s, mode = 'finished'
                    WHERE name = %s
                """, (level, speed, apples, username))

                conn.commit() #Коммитим

                #Обновляем в другой таблице
                cursor.execute("""
                    UPDATE "user_score"
                    SET score = %s
                    WHERE name = %s
                """, (score, username))

                conn.commit() #Коммитим
            else: #Если пользователь не существует
                #Добавляем новую запись
                cursor.execute("""
                    INSERT INTO "user" (name, speed, level, apples, mode)
                    VALUES (%s, %s, %s, %s, 'finished');
                """, (username, speed, level, apples))

                conn.commit() #Коммитим

                #Добавляем новую запись в другую таблицу
                cursor.execute("""
                    INSERT INTO "user_score" (name, score)
                    VALUES (%s, %s)
                """, (username, score))

                conn.commit() #Коммитм

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
            time.sleep(2)

            screen.blit(win, (30, 200))
            screen.blit(win2, (130, 260))
            pygame.display.flip()

            if exist: #Если пользователь существует в бд
                #Обновляем данные
                cursor.execute("""
                    UPDATE "user"
                    SET level = %s, speed = %s, apples = %s, mode = 'finished'
                    WHERE name = %s
                """, (level, speed, apples, username))

                conn.commit() #Коммитм

                #Обновляем в другой
                cursor.execute("""
                    UPDATE "user_score"
                    SET score = %s
                    WHERE name = %s
                """, (score, username))

                conn.commit() #Коммитим
            else: #Если не существует
                cursor.execute("""
                    INSERT INTO "user" (name, level, speed, apples, mode)
                    VALUES (%s, %s, %s, %s, 'finished')
                """, (username, level, speed, apples))

                conn.commit() #Коммититм

                #Добавляем новую запись в другую таблицу
                cursor.execute("""
                    INSERT INTO "user_score" (name, score)
                    VALUES (%s, %s)
                """, (username, score))

                conn.commit() #Коммитим

            time.sleep(3)

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

# Закрываем соединение
cursor.close()
conn.close()

pygame.quit()