import pygame
import sys
import random

pygame.init()

# =========================
# Configurações da janela
# =========================
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Invasão de Pop-ups")

# Fontes
fonte = pygame.font.SysFont(None, 36)
fonte_x = pygame.font.SysFont(None, 30)
fonte_gameover = pygame.font.SysFont(None, 72)

# =========================
# Imagem
# =========================
try:
    imagem = pygame.image.load("pop-up.png").convert_alpha()
    imagem = pygame.transform.scale(imagem, (250, 180))
except pygame.error as erro:
    print(f"Erro ao carregar a imagem: {erro}")
    pygame.quit()
    sys.exit()

# =========================
# Classe para Gerenciar Múltiplos Pop-ups
# =========================
class Popup:
    def __init__(self, tempo_atual):
        self.inicio = tempo_atual
        self.mostrar_x_real = False
        # Posição aleatória para não cobrirem uns aos cores perfeitamente
        x = random.randint(50, LARGURA - 350)
        y = random.randint(50, ALTURA - 250)
        self.rect = pygame.Rect(x, y, 300, 220)

    def atualizar(self, tempo_atual):
        if tempo_atual - self.inicio >= 10000:
            self.mostrar_x_real = True

# Inicialização do Jogo
popups = []
ultimo_popup = pygame.time.get_ticks()
tempo_proximo_popup = random.randint(45000, 60000)
clock = pygame.time.Clock()
rodando = True
game_over = False

while rodando:
    agora = pygame.time.get_ticks()

    # =========================
    # Eventos
    # =========================
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if game_over:
                # Se der Game Over, qualquer clique fecha o jogo
                rodando = False
                break

            # Verifica os pop-ups de trás para frente (do topo para o fundo)
            popup_clicado = False
            for p in reversed(popups):
                # Definição dos botões baseados na posição individual do pop-up
                # X Falso: Canto Superior Direito
                rect_x_falso = pygame.Rect(p.rect.right - 35, p.rect.top + 5, 30, 30)
                # X Real: Canto Superior Esquerdo
                rect_x_real = pygame.Rect(p.rect.left + 5, p.rect.top + 5, 30, 30)

                # Clicou no X Falso (Direito)
                if rect_x_falso.collidepoint(evento.pos):
                    print("X falso clicado! +3 Pop-ups!")
                    for _ in range(3):
                        popups.append(Popup(agora))
                    popup_clicado = True
                    break

                # Clicou no X Real (Esquerdo) - Só funciona se já tiver aparecido
                elif p.mostrar_x_real and rect_x_real.collidepoint(evento.pos):
                    popups.remove(p)
                    popup_clicado = True
                    break
                
                # Se clicou dentro do corpo do pop-up, bloqueia o clique para o que está atrás
                elif p.rect.collidepoint(evento.pos):
                    popup_clicado = True
                    break

    # =========================
    # Lógica do Jogo
    # =========================
    if not game_over:
        # Atualiza o estado de tempo de cada pop-up ativo
        for p in popups:
            p.atualizar(agora)

        # Sistema de spawn automático por tempo
        if agora - ultimo_popup >= tempo_proximo_popup:
            popups.append(Popup(agora))
            ultimo_popup = agora
            tempo_proximo_popup = random.randint(45000, 60000)

        # Condição de Game Over (10 ou mais pop-ups)
        if len(popups) >= 10:
            game_over = True

    # =========================
    # Renderização / Desenho
    # =========================
    tela.fill((30, 30, 30))

    # Texto de Fundo
    texto = fonte.render(f"Pop-ups ativos: {len(popups)}/10", True, (255, 255, 255))
    tela.blit(texto, (20, 30))

    # Desenha os pop-ups (da base para o topo)
    for p in popups:
        # Fundo do pop-up
        pygame.draw.rect(tela, (220, 220, 220), p.rect)
        pygame.draw.rect(tela, (0, 0, 0), p.rect, 3)

        # Desenhar Imagem Centralizada dentro dele
        img_x = p.rect.x + (p.rect.width - imagem.get_width()) // 2
        img_y = p.rect.y + (p.rect.height - imagem.get_height()) // 2 + 15
        tela.blit(imagem, (img_x, img_y))

        # Botão X Falso (Sempre visível no Canto Superior Direito)
        rect_x_falso = pygame.Rect(p.rect.right - 35, p.rect.top + 5, 30, 30)
        pygame.draw.rect(tela, (200, 50, 50), rect_x_falso)
        txt_falso = fonte_x.render("X", True, (255, 255, 255))
        tela.blit(txt_falso, txt_falso.get_rect(center=rect_x_falso.center))

        # Botão X Real (Aparece após 10s no Canto Superior Esquerdo)
        if p.mostrar_x_real:
            rect_x_real = pygame.Rect(p.rect.left + 5, p.rect.top + 5, 30, 30)
            pygame.draw.rect(tela, (50, 150, 50), rect_x_real) # Cor verde para diferenciar no teste (opcional)
            txt_real = fonte_x.render("X", True, (255, 255, 255))
            tela.blit(txt_real, txt_real.get_rect(center=rect_x_real.center))

    # Tela de Game Over
    if game_over:
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))

        txt_go = fonte_gameover.render("GAME OVER", True, (255, 50, 50))
        txt_sub = fonte.render("Muito pop-ups na tela! Clique para sair.", True, (255, 255, 255))
        
        tela.blit(txt_go, txt_go.get_rect(center=(LARGURA//2, ALTURA//2 - 30)))
        tela.blit(txt_sub, txt_sub.get_rect(center=(LARGURA//2, ALTURA//2 + 30)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()