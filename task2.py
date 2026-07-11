import pygame
import random

# =========================
# Classe Individual do Pop-up
# =========================
class Popup:
    def __init__(self, tempo_atual, largura_tela, altura_tela):
        self.inicio = tempo_atual
        self.mostrar_x_real = False
        # Posição aleatória considerando os limites da tela
        x = random.randint(50, largura_tela - 350)
        y = random.randint(50, altura_tela - 250)
        self.rect = pygame.Rect(x, y, 300, 220)

    def atualizar(self, tempo_atual):
        if tempo_atual - self.inicio >= 10000:
            self.mostrar_x_real = True

# =========================
# Classe Gerenciadora de Pop-ups
# =========================
class GerenciadorPopups:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.popups = []
        self.ultimo_popup = pygame.time.get_ticks()
        self.tempo_proximo_popup = random.randint(15000, 20000)
        self.game_over = False

        # Fontes
        self.fonte = pygame.font.SysFont(None, 36)
        self.fonte_x = pygame.font.SysFont(None, 30)
        self.fonte_gameover = pygame.font.SysFont(None, 72)

        # Imagem
        try:
            imagem_bruta = pygame.image.load("pop-up.png").convert_alpha()
            self.imagem = pygame.transform.scale(imagem_bruta, (250, 180))
        except pygame.error as erro:
            print(f"Aviso: Erro ao carregar 'pop-up.png' ({erro}). Usando fundo cinza padrão.")
            self.imagem = pygame.Surface((250, 180))
            self.imagem.fill((150, 150, 150)) # Imagem de fallback

    def processar_evento(self, evento):
        """
        Processa os eventos de clique do mouse.
        Retorna:
            - "FECHAR_JOGO": se o limite de popups estourou e o usuário clicou na tela.
            - True: se o clique do mouse interagiu com o popup (bloqueando a tela atrás).
            - False: se o clique foi fora de todos os popups.
        """
        if self.game_over:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                return "FECHAR_JOGO"
            return True # Bloqueia outros cliques enquanto estiver no Game Over dos popups

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            agora = pygame.time.get_ticks()
            popup_clicado = False
            
            # Verifica os pop-ups de trás para frente (do topo para o fundo)
            for p in reversed(self.popups):
                rect_x_falso = pygame.Rect(p.rect.right - 35, p.rect.top + 5, 30, 30)
                rect_x_real = pygame.Rect(p.rect.left + 5, p.rect.top + 5, 30, 30)

                # Clicou no X Falso (Direito)
                if rect_x_falso.collidepoint(evento.pos):
                    print("X falso clicado! +3 Pop-ups!")
                    for _ in range(3):
                        self.popups.append(Popup(agora, self.largura, self.altura))
                    popup_clicado = True
                    break

                # Clicou no X Real (Esquerdo)
                elif p.mostrar_x_real and rect_x_real.collidepoint(evento.pos):
                    self.popups.remove(p)
                    popup_clicado = True
                    break
                
                # Clicou no corpo do pop-up
                elif p.rect.collidepoint(evento.pos):
                    popup_clicado = True
                    break

            # Se algum popup foi clicado, retorna True (isso impede que o jogo de trás também conte o clique)
            return popup_clicado 
        
        return False

    def atualizar(self):
        """Atualiza a lógica de tempo e surgimento dos popups."""
        if self.game_over:
            return

        agora = pygame.time.get_ticks()

        # Atualiza o estado de tempo de cada pop-up ativo
        for p in self.popups:
            p.atualizar(agora)

        # Sistema de spawn automático por tempo
        if agora - self.ultimo_popup >= self.tempo_proximo_popup:
            self.popups.append(Popup(agora, self.largura, self.altura))
            self.ultimo_popup = agora
            self.tempo_proximo_popup = random.randint(45000, 60000)

        # Condição de Game Over (10 ou mais pop-ups)
        if len(self.popups) >= 10:
            self.game_over = True

    def desenhar(self, tela):
        """Desenha os pop-ups na tela especificada."""
        # Fundo semitransparente atrás do texto para garantir que dê pra ler por cima de outras telas
        texto = self.fonte.render(f"Pop-ups ativos: {len(self.popups)}/10", True, (255, 255, 255))
        fundo_texto = pygame.Surface((texto.get_width() + 10, texto.get_height() + 10))
        fundo_texto.set_alpha(180)
        fundo_texto.fill((0, 0, 0))
        tela.blit(fundo_texto, (15, 25))
        tela.blit(texto, (20, 30))

        # Desenha os pop-ups (da base para o topo)
        for p in self.popups:
            # Fundo do pop-up
            pygame.draw.rect(tela, (220, 220, 220), p.rect)
            pygame.draw.rect(tela, (0, 0, 0), p.rect, 3)

            # Desenhar Imagem Centralizada
            img_x = p.rect.x + (p.rect.width - self.imagem.get_width()) // 2
            img_y = p.rect.y + (p.rect.height - self.imagem.get_height()) // 2 + 15
            tela.blit(self.imagem, (img_x, img_y))

            # Botão X Falso
            rect_x_falso = pygame.Rect(p.rect.right - 35, p.rect.top + 5, 30, 30)
            pygame.draw.rect(tela, (200, 50, 50), rect_x_falso)
            txt_falso = self.fonte_x.render("X", True, (255, 255, 255))
            tela.blit(txt_falso, txt_falso.get_rect(center=rect_x_falso.center))

            # Botão X Real
            if p.mostrar_x_real:
                rect_x_real = pygame.Rect(p.rect.left + 5, p.rect.top + 5, 30, 30)
                pygame.draw.rect(tela, (50, 150, 50), rect_x_real)
                txt_real = self.fonte_x.render("X", True, (255, 255, 255))
                tela.blit(txt_real, txt_real.get_rect(center=rect_x_real.center))

        # Tela de Game Over dos pop-ups
        if self.game_over:
            overlay = pygame.Surface((self.largura, self.altura))
            overlay.set_alpha(220)
            overlay.fill((0, 0, 0))
            tela.blit(overlay, (0, 0))

            txt_go = self.fonte_gameover.render("GAME OVER", True, (255, 50, 50))
            txt_sub = self.fonte.render("Muitos pop-ups na tela! Clique para sair.", True, (255, 255, 255))
            
            tela.blit(txt_go, txt_go.get_rect(center=(self.largura//2, self.altura//2 - 30)))
            tela.blit(txt_sub, txt_sub.get_rect(center=(self.largura//2, self.altura//2 + 30)))