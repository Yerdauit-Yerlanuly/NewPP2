import pygame

#Функция для того, чтобы выбрать фонт для текста 
def makeFont(fonts, size):
    available = pygame.font.get_fonts()

    choices = map(lambda x:x.lower().replace(' ', ''), fonts)

    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
        
    return pygame.font.Font(None, size)
    
#Для кэширования фонт текста 
cachedFonts = {}
def getFont(fontPref, size):
    global cachedFonts

    key = str(fontPref) + '|' + str(size)
    font = cachedFonts.get(key, None)

    if font == None:
        font = makeFont(fontPref, size)
        cachedFonts[key] = font

    return font

#Для кэширования текстового изображения, чтобы оно не рендерилось бесконечно при повторяющемся тексте
cachedText = {}
def createText(text, fonts, size, color):
    global cachedText

    key = '|'.join(map(str, (fonts, size, color, text)))
    image = cachedText.get(key, None)

    if image == None:
        font = getFont(fonts, size)
        image = font.render(text, True, color)
        cachedText[key] = image

    return image

pygame.init() #Инициализация
pygame.mixer.init() #Инициализация
clock = pygame.time.Clock() #Для фпс

songs = ["mp3/alpha-bal.mp3", "mp3/ninety-one-jurek.mp3", "mp3/city-of-stars.mp3"]
current = 0

pygame.mixer.music.load(songs[current])

done = False
pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Создаёт пользовательское событие, которое срабатывает при завершении трека

fontPref = ["Comic Sans MS"]

#Создаем текстовое изображение с помощью функции сверху
text = createText("Welcome to Music Player", fontPref, 18, (0, 0, 0))
controls = createText("Music Player Controls:", fontPref, 18, (0, 0, 0))
space = createText("Spacebar – Play/Pause the music", fontPref, 18, (0, 0, 0))
right = createText("Right Arrow / 'D' – Play the next track", fontPref, 18, (0, 0, 0))
left = createText("Left Arrow / 'A' – Play the previous track", fontPref, 18, (0, 0, 0))

#создаем скрин
screen = pygame.display.set_mode((380, 450))
img = pygame.image.load("img/iconForMusicPlayer.png")
img = pygame.transform.scale(img, (300, 300))

while not done:
    screen.fill((255, 255, 255)) #Заполняем экран

    for event in pygame.event.get():
        #Обработка событий 
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy(): #Проверяет играет ли какая та музыка
                    pygame.mixer.music.pause() #Ставит на паузу
                else:
                    if pygame.mixer.music.get_pos() > 0: #Проверяет, проигрывается ли музыка(возвращает позицию в миллисекундах)
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.play()

            #Обработчик для кнопки D и стрелки на право
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                songs = songs[1:] + [songs[current]]
                pygame.mixer.music.load(songs[current])
                pygame.mixer.music.play()

            #Обработчик для кнопки A и стрелки на лево
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                songs = [songs[-1]] + songs[:2]
                pygame.mixer.music.load(songs[current])
                pygame.mixer.music.play()

        #Обработчик для пользовательского события. Переключает на след. трек
        if event.type == pygame.USEREVENT:
            songs = songs[1:] + [songs[current]]
            pygame.mixer.music.load(songs[current])
            pygame.mixer.music.play()

    #Рисуем изображения, текстовое изображение
    screen.blit(img, (40, text.get_height()))
    screen.blit(text, ((380 - text.get_width()) / 2, 0))
    screen.blit(controls, (10, text.get_height() + img.get_height()))
    screen.blit(space, (20, text.get_height() + img.get_height() + controls.get_height()))
    screen.blit(right, (20, text.get_height() + img.get_height() + controls.get_height() + space.get_height()))
    screen.blit(left, (20, text.get_height() + img.get_height() + controls.get_height() + space.get_height() + right.get_height()))

    pygame.display.flip() #Для того чтобы было видно все изменения
    clock.tick(60) #60 фпс

pygame.quit()