<<<<<<< HEAD
import pygame

import botoes

import musica

pygame.init()
largura = 800
altura = 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Hack Tasks")
clock = pygame.time.Clock()
FPS = 60

imagem_fundo = pygame.image.load("Tela_menu.png.png").convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))
tela.blit(imagem_fundo, (0, 0))
pygame.display.flip()

Executando = True
while Executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            Executando = False

=======
import pygame

import botoes

import musica

pygame.init()
largura = 800
altura = 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Hack Tasks")
clock = pygame.time.Clock()
FPS = 60

imagem_fundo = pygame.image.load("Tela_menu.png.png").convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))
tela.blit(imagem_fundo, (0, 0))
pygame.display.flip()

Executando = True
while Executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            Executando = False
            ll
>>>>>>> 52d371d3c8fccc6fba9ce2832645e2bd4a2e0e46
