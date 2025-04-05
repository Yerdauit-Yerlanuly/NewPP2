import pygame
import tkinter as tk
from tkinter import colorchooser

#Инициализация
pygame.init()
clock = pygame.time.Clock()

#Константы, переменные
WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
currentColor = BLACK
radius = 15
mode = "brush" #brush, eraser, rect, circle
startPos, lastPos = None, None #Для рисования фигур
done = False
showInstructions = True

#Настройки
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
screen.fill(WHITE)

def chooseColor(): #Функция для выбора цвета
    global currentColor
    root = tk.Tk() #Создает скрытое окно tkinter
    root.withdraw() #Cкрывает основное окно tkinter
    colorCode = colorchooser.askcolor(title="Choose color")[0] #Открывает диалоговое окно выбора цвета и берем только 1 элемент(кортеж rgb)
    if colorCode:
        currentColor = (int(colorCode[0]), int(colorCode[1]), int(colorCode[2]))

def drawSmoothLine(screen, start, end, width, color): #Функция для гладкого рисования
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

def drawInstructions(): #Функция отрисовки инструкции
    screen.fill(WHITE)
    font = pygame.font.Font(None, 24)
    instructions = [
        "Welcome to Paint!",
        "Press B - Brush mode",
        "Press E - Eraser mode",
        "Press R - Rectangle mode",
        "Press C - Circle mode",
        "Press P - Choose color",
        "Left Click, '+' - Increase brush size",
        "Right Click, '-' - Decrease brush size",
        "Press ENTER to start drawing!"
    ]

    yOffset = 100
    for line in instructions:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, yOffset))
        yOffset += 30

    pygame.display.flip()

# Главный цикл
while not done:
    if showInstructions:
        drawInstructions() #Рисуем инструкцию

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        elif event.type == pygame.KEYDOWN: #Проверяем на нажатие кнопки
            print(event.key)

            if event.key == pygame.K_ESCAPE: #Если ESC
                done = True
            elif showInstructions and event.key == pygame.K_RETURN: #Если ENTER
                showInstructions = False
                screen.fill(WHITE)

            #Переключаем инструменты
            elif event.key == pygame.K_b:
                mode = "brush"
            elif event.key == pygame.K_e:
                mode = "eraser"
            elif event.key == pygame.K_r:
                mode = "rect"
            elif event.key == pygame.K_c:
                mode = "circle"
            elif event.key == pygame.K_p:
                chooseColor()
            elif event.key == 1073741911: #Kнопка +
                radius += 1 #+ увеличивает радиус
            elif event.key == 1073741910: #Кнопка -
                radius -= 1 #- уменьшает радиус
        
        #Нажатие на мышки
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #ЛКМ увеличивает радиус
                radius += 1
            elif event.button == 3: #ПКМ уменьшает радиус
                radius -= 1

            #Обновляем позиции
            startPos = event.pos
            lastPos = event.pos

        #Если мышка нажата и двигается
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            if lastPos:
                if mode == "brush": #Рисуем кистью
                    drawSmoothLine(screen, lastPos, event.pos, radius, currentColor)
                elif mode == "eraser": #Стираем ластиком
                    drawSmoothLine(screen, lastPos, event.pos, radius, WHITE)
                
                lastPos = event.pos #Обновляем позицию
        
        #Если мышка БЫЛА зажатой
        elif event.type == pygame.MOUSEBUTTONUP:
            if mode in ("rect", "circle") and startPos:
                endPos = event.pos
                rect = pygame.Rect(startPos, (endPos[0] - startPos[0], endPos[1] - startPos[1])) #Создаем квадрат

                if mode == "rect":
                    pygame.draw.rect(screen, currentColor, rect, radius) #Рисуем квадрат внутри создванного квадрата
                elif mode == "circle":
                    pygame.draw.ellipse(screen, currentColor, rect, radius) #Рисуем круг внутри созданного квадрата

                startPos = None

            lastPos = None
    
    pygame.display.flip() #Обновляем экран
    clock.tick(60) #60 фпс

pygame.quit()