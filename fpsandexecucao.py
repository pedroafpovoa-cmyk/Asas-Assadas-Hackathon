import pygame

import botoes

pygame.init()
largura = 800
altura = 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Hackathon - Asas Assadas")
clock = pygame.time.Clock()
FPS = 60

Executando = True
while Executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            Executando = False
pygame.quit()