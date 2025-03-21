import pygame

pygame.init() #Инициализация

width = 500
height = 400
screen = pygame.display.set_mode((width, height)) #Размер экрана
clock = pygame.time.Clock() #Для фпс

circle_x, circle_y = width // 2, height // 2 #Позиция

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and circle_y - 25 - 20 >= 0:
                circle_y -= 20
            if event.key == pygame.K_DOWN and circle_y + 25 + 20 <= height:
                circle_y += 20
            if event.key == pygame.K_LEFT and circle_x - 25 - 20 >= 0:
                circle_x -= 20
            if event.key == pygame.K_RIGHT and circle_x + 25 + 20 <= width:
                circle_x += 20

    screen.fill((255, 255, 255)) #Закрашиваем экран
    pygame.draw.circle(screen, (255, 0, 0), (circle_x, circle_y), 25) #Рисуем шар
    pygame.display.update() #Обновляем экран

    clock.tick(60) #60 фпс

pygame.quit()