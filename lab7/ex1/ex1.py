import pygame
import datetime

pygame.init()

screen = pygame.display.set_mode((840, 840))
pygame.display.set_caption("Mickey_Clock")
icon = pygame.image.load('mickey-mouse.png')
seconds_image = pygame.image.load('leftHandCopy.png')
minutes_image = pygame.image.load('rightHandCopy.png')
clock_image = pygame.image.load('body.jpg')
seconds_image = pygame.transform.scale(seconds_image, (500, 500))
minutes_image = pygame.transform.scale(minutes_image, (500, 500))
pygame.display.set_icon(icon)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Get the current time
    current_time = datetime.datetime.now()
    seconds = current_time.second
    minutes = current_time.minute


    screen.blit(clock_image, (0, 0))

    second_angle = -seconds * 6
    minute_angle = -minutes * 6

    rotated_seconds = pygame.transform.rotate(seconds_image, second_angle)
    sec_rect = rotated_seconds.get_rect(center=(420, 420))
    screen.blit(rotated_seconds, sec_rect)

    rotated_minutes = pygame.transform.rotate(minutes_image, minute_angle)
    min_rect = rotated_minutes.get_rect(center=(420, 420))
    screen.blit(rotated_minutes, min_rect)

    pygame.display.flip()

pygame.quit()
