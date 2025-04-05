import pygame, math
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
mode = "brush" #brush, eraser, rect, circle, square, triangle, eTriangle, rhombus
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
        "Press S - Square mode",
        "Press T - Right Triangle mode",
        "Press Q - Equilateral Triangle mode",
        "Press H - Rhombus mode",
        "Press P - Choose color",
        "Left Click, '+' - Increase brush size",
        "Right Click, '-' - Decrease brush size",
        "Press ENTER to show or hide instructions"
    ]

    yOffset = 50
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
            if event.key == pygame.K_ESCAPE: #Если ESC
                done = True
            elif event.key == pygame.K_RETURN: #Если ENTER
                if showInstructions:
                    showInstructions = False
                else:
                    showInstructions = True
                
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
            elif event.key == pygame.K_s:
                mode = "square"
            elif event.key == pygame.K_t:
                mode = "triangle"
            elif event.key == pygame.K_q:
                mode = "eTriangle"
            elif event.key == pygame.K_h:
                mode = "rhombus"
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
            if mode in ("rect", "circle", "square", "triangle", "eTriangle", "rhombus") and startPos:
                rect = pygame.Rect(startPos, (lastPos[0] - startPos[0], lastPos[1] - startPos[1])) #Создаем квадрат

                if mode == "rect":
                    pygame.draw.rect(screen, currentColor, rect, radius) #Рисуем прямоугольник внутри создванного квадрата
                elif mode == "circle":
                    pygame.draw.ellipse(screen, currentColor, rect, radius) #Рисуем круг внутри созданного квадрата
                elif mode == "square":
                    minSide = min(lastPos[0] - startPos[0], lastPos[1] - startPos[1]) #Ищем меньшую сторону
                    sqr = pygame.Rect(startPos, (minSide, minSide))
                    pygame.draw.rect(screen, currentColor, sqr, radius)  #Рисуем квадрат
                elif mode == "triangle":
                    a = startPos #Левая верхняя точка
                    b = (startPos[0], lastPos[1]) #Левая нижняя точка
                    c = lastPos #Правая нижняя точка

                    pygame.draw.polygon(screen, currentColor, [a, b, c], radius) #Рисуем правильный треугольник
                elif mode == "eTriangle":
                    #Вычисляем длину стороны треугольника
                    length = lastPos[0] - startPos[0]

                    #Вычисляем высоту треугольника
                    height = (math.sqrt(3) / 2) * length

                    a = (startPos[0], lastPos[1]) #Левая нижняя
                    b = (startPos[0] + length, lastPos[1]) #Правая нижняя
                    c = (startPos[0] + length / 2, lastPos[1] - height) #Верхняя

                    pygame.draw.polygon(screen, currentColor, [a, b, c], radius) #Рисуем равностороний треугольник
                elif mode == "rhombus":
                    #Вычисляем ширину и высоту
                    width = lastPos[0] - startPos[0]
                    height = lastPos[1] - startPos[1]

                    a = (startPos[0] + width / 2, startPos[1]) #Верхняя
                    b = (startPos[0], startPos[1] + height / 2) #Левая
                    c = (startPos[0] + width / 2, lastPos[1]) #Нихняя
                    d = (lastPos[0], lastPos[1] - height / 2) #Правая

                    pygame.draw.polygon(screen, currentColor, [a, b, c, d], radius) #Рисуем ромб

                startPos = None

            lastPos = None
    
    pygame.display.flip() #Обновляем экран
    clock.tick(240) #60 фпс

pygame.quit()