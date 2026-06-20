<<<<<<< HEAD
import pygame
import botoes

pygame.init()
largura = 800
altura = 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Capyvaras Powerfull Cotton Fight")
clock = pygame.time.Clock()
FPS = 60

Executando = True
while Executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
=======
import pygame
import botoes

pygame.init()
largura = 800
altura = 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Capyvaras Powerfull Cotton Fight")
clock = pygame.time.Clock()
FPS = 60

Executando = True
while Executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
>>>>>>> 52d371d3c8fccc6fba9ce2832645e2bd4a2e0e46
            Executando = False