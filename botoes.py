import pygame

class Botao():
    def __init__(self, pos_x, pos_y, largura, altura, cor_fundo, texto, cor_texto, fonte, tamanho_fonte):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.largura = largura
        self.altura = altura
        self.cor_fundo = cor_fundo
        self.texto = texto
        self.cor_texto = cor_texto
        self.fonte = fonte
        self.tamanho_fonte = tamanho_fonte

    def definir_cor_fundo(self, cor_fundo):

        self.cor_fundo = cor_fundo

    pygame.font.init()

    def desenhar_botao(self, tela):

        pygame.draw.rect(tela, self.cor_fundo, (self.pos_x,
                     self.pos_y, self.largura, self.altura))
        fonte = pygame.font.SysFont(self.fonte, self.tamanho_fonte)
        texto = fonte.render(self.texto, True, self.cor_texto)

class Botao():
    def __init__(self, pos_x, pos_y, largura, altura, cor_fundo, texto, cor_texto, fonte, tamanho_fonte):

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.largura = largura
        self.altura = altura
        self.cor_fundo = cor_fundo
        self.texto = texto
        self.cor_texto = cor_texto
        self.fonte = fonte
        self.tamanho_fonte = tamanho_fonte

    def definir_cor_fundo(self, cor_fundo):

        self.cor_fundo = cor_fundo

    pygame.font.init()

    def desenhar_botao(self, tela):

        pygame.draw.rect(tela, self.cor_fundo, (self.pos_x,
                     self.pos_y, self.largura, self.altura))
        fonte = pygame.font.SysFont(self.fonte, self.tamanho_fonte)
        texto = fonte.render(self.texto, True, self.cor_texto)
        tela.blit(texto, (self.pos_x + 10, self.pos_y + 10))