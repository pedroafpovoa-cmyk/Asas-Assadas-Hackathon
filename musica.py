import pygame

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("In The End (Linkin Park).mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

Executando = True
while Executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            Executando = False

pygame.quit()