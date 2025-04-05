import pygame, random, time, sys
from pygame.locals import *

#Инициализация
pygame.init()
pygame.mixer.init()
fps = pygame.time.Clock()

#Цвета
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Переменные
width = 400
height = 600
speedForEnemy = 5
speedForCoin = 3
speedForCar = 5
score = 0
coin = 0

#Создаем шрифт и надпись
font = pygame.font.SysFont("Verdana", 60)
fontSmall = pygame.font.SysFont("Verdana", 20)
over = font.render("Game Over", True, (0, 0, 0))

back = pygame.image.load("src/racer/AnimatedStreet.png")

#Создаем Панель
screen = pygame.display.set_mode((width, height))
screen.fill(WHITE)
pygame.display.set_caption("Racer")

pygame.mixer.music.load("src/racer/background.wav") #Загружаем музыку 
pygame.mixer.music.play(-1)  # -1 означает бесконечное повторение

#Функция для того, чтобы монета и машина не появлялись на одной и той же координате
def randomCoin(enemyRect):
    while True:
        x = random.randint(40, width - 40)
        new_rect = pygame.Rect(x, 0, 60, 60)  #Размер монеты

        if not new_rect.colliderect(enemyRect):  #Проверяем пересечение с врагом
            return x

#Создаем класс Врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self): #Конструктор
        super().__init__()
        self.image = pygame.image.load("src/racer/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, width - 40), 0) #Рандомные координаты

    def move(self): #Функция для передвижения
        global score
        self.rect.move_ip(0, speedForEnemy)

        #Проверка на то, прошла ли машина полный путь сверху вниз
        if (self.rect.bottom > 600):
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, width - 40), 0)

#Класс для монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self, enemyRect): #Конструктор
        super().__init__()
        self.image = pygame.image.load("src/racer/coin.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (randomCoin(enemyRect), 0) #Вызываем функцию сверху

    def move(self): #Функция для передвижения
        self.rect.move_ip(0, speedForCoin)

        #Проверка на то, прошла ли монета полный путь сверху вниз
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, width - 40), 0)

#Класс для Игрока
class Player(pygame.sprite.Sprite):
    def __init__(self): #Конструктор
        super().__init__()
        self.image = pygame.image.load("src/racer/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520) #Начальные координаты
    
    def move(self): #Функция для передвижения
        pressedKey = pygame.key.get_pressed()

        #Проверка на нажатую кнопку
        if self.rect.left > 0:
            if pressedKey[K_LEFT] or pressedKey[K_a]:
                self.rect.move_ip(-(speedForCar), 0)
        
        if self.rect.right < width:
            if pressedKey[K_RIGHT] or pressedKey[K_d]:
                self.rect.move_ip(speedForCar, 0)

#Создаем объекты классов
P1 = Player()
E1 = Enemy()
C1 = Coin(E1.rect)

#Группируем объекты
enemies = pygame.sprite.Group()
enemies.add(E1)

coinsGroup = pygame.sprite.Group()
coinsGroup.add(C1)

allSprites = pygame.sprite.Group()
allSprites.add(P1)
allSprites.add(E1)
allSprites.add(C1)

#Создаем пользовательское событие и ставим таймер, который каждые 2 секунд зовет его
incSpeed = pygame.USEREVENT + 1 # + 1 значит уникальный айди номером 1
pygame.time.set_timer(incSpeed, 2000)

done = False

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

        if event.type == incSpeed: #Пользовательское событие
            if speedForEnemy < 18: #Лимит на скорость
                speedForEnemy += 1
                speedForCoin += 1
                speedForCar += 0.5

    screen.blit(back, (0, 0)) #Рисуем дорогу

    #Рендерим тексты
    scores = fontSmall.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(scores, (10, 10))
    coins = fontSmall.render("Coins: " + str(coin), True, (0, 0, 0))
    screen.blit(coins, (300, 10))

    #Проходимся по всем спрайтам в группе
    for entity in allSprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, coinsGroup): #Проверка на взаимодействие между игрока с монетой
        coinMusic = pygame.mixer.Sound("src/racer/coin.mp3")
        coinMusic.set_volume(0.1)
        coinMusic.play()

        coin += 1

        # Удаляем текущую монету
        for c in coinsGroup:
            c.kill()

        # Создаём новую монету
        newСoin = Coin(E1.rect)
        coinsGroup.add(newСoin)
        allSprites.add(newСoin)

    #Проверка на столкновение
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.load("src/racer/crash.wav")
        pygame.mixer.music.play()

        time.sleep(0.5)

        screen.fill(RED) #Выводим красный экран
        screen.blit(over, (30, 250)) #С надписью Game Over

        pygame.display.update() #Обновляем экран

        #Удаляем всех спрайтов
        for entity in allSprites:
            entity.kill()

        time.sleep(2)

        pygame.quit()
        sys.exit() #Выходим из системы

    pygame.display.update() #Обновляем экран
    fps.tick(60) #60 фпс

pygame.quit()