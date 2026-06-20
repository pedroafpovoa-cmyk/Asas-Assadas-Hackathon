<<<<<<< HEAD
import pygame

import Tela_inicial

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

=======
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

>>>>>>> 52d371d3c8fccc6fba9ce2832645e2bd4a2e0e46
pygame.quit()