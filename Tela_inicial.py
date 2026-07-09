import pygame
import sys
import random
import configuracoes  
import task1  # Importa o seu minijogo

# ==============================================================================
# CLASSE: GERENCIADOR GLOBAL DE POP-UPS
# ==============================================================================
class PopupGlobal:
    def __init__(self, largura_tela, altura_tela):
        self.LARGURA = largura_tela
        self.ALTURA = altura_tela
        self.fonte_x = pygame.font.SysFont(None, 30)
        
        # Carrega a imagem do anúncio
        try:
            self.imagem = pygame.image.load("pop-up.png").convert_alpha()
            self.imagem = pygame.transform.scale(self.imagem, (300, 250))
        except pygame.error:
            # Fallback seguro caso a imagem não exista no diretório
            self.imagem = pygame.Surface((300, 250))
            self.imagem.fill((150, 150, 150))

        self.popup_ativo = False
        self.mostrar_x_real = False
        self.botao_x = pygame.Rect(0, 0, 0, 0)
        self.inicio_popup = 0
        self.ultimo_popup = pygame.time.get_ticks()
        
        # Intervalo aleatório de surgimento (45 a 60 segundos)
        self.tempo_proximo_popup = random.randint(45000, 60000)

    def atualizar(self):
        agora = pygame.time.get_ticks()

        # Gatilho para abrir o pop-up
        if not self.popup_ativo and agora - self.ultimo_popup >= self.tempo_proximo_popup:
            self.popup_ativo = True
            self.mostrar_x_real = False
            self.inicio_popup = agora

        # Após 10 segundos, o X real aparece
        if self.popup_ativo and agora - self.inicio_popup >= 10000:
            self.mostrar_x_real = True

    def processar_evento(self, evento):
        """Retorna True se o clique foi absorvido pelo Pop-up."""
        if not self.popup_ativo:
            return False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.botao_x.collidepoint(evento.pos):
                if self.mostrar_x_real:
                    self.popup_ativo = False
                    self.ultimo_popup = pygame.time.get_ticks()
                    self.tempo_proximo_popup = random.randint(45000, 60000)
                else:
                    print("X falso clicado!")
                return True  # Absorve o clique
            
            # Bloqueia qualquer clique que ocorra dentro do corpo do pop-up
            popup_rect = pygame.Rect((self.LARGURA - 400) // 2, (self.ALTURA - 300) // 2, 400, 300)
            if popup_rect.collidepoint(evento.pos):
                return True
                
        return False

    def desenhar(self, tela):
        if not self.popup_ativo:
            return

        # Fundo escurecido
        overlay = pygame.Surface((self.LARGURA, self.ALTURA))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))

        # Janela do Pop-up centralizada de forma dinâmica
        popup_rect = pygame.Rect((self.LARGURA - 400) // 2, (self.ALTURA - 300) // 2, 400, 300)
        pygame.draw.rect(tela, (220, 220, 220), popup_rect)
        pygame.draw.rect(tela, (0, 0, 0), popup_rect, 3)

        # Definindo as posições do botão X
        if self.mostrar_x_real:
            self.botao_x = pygame.Rect(popup_rect.right - 80, popup_rect.top + 80, 30, 30)
        else:
            self.botao_x = pygame.Rect(popup_rect.right - 35, popup_rect.top + 5, 30, 30)

        pygame.draw.rect(tela, (200, 50, 50), self.botao_x)
        texto_x = self.fonte_x.render("X", True, (255, 255, 255))
        tela.blit(texto_x, texto_x.get_rect(center=self.botao_x.center))

        # Imagem do anúncio centralizada
        x = popup_rect.x + (popup_rect.width - self.imagem.get_width()) // 2
        y = popup_rect.y + (popup_rect.height - self.imagem.get_height()) // 2
        tela.blit(self.imagem, (x, y))


# Inicialização Básica
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Menu Reformulado com Pop-ups")
relogio = pygame.time.Clock()

# Instancia o Gerenciador de Pop-ups Global
popups_globais = PopupGlobal(LARGURA, ALTURA)

# Carrega fundo
try:
    imagem_fundo = pygame.image.load("Tela_inicial.png").convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))
except pygame.error:
    imagem_fundo = pygame.Surface((LARGURA, ALTURA))
    imagem_fundo.fill((30, 30, 40))

# Cores e Fontes
COR_HACK = (20, 50, 70)
COR_TEXTO = (255, 255, 255)
COR_PLAY = (50, 180, 100)
COR_PLAY_HOVER = (80, 210, 130)
COR_SAIR = (200, 60, 60)
COR_SAIR_HOVER = (230, 90, 90)
COR_GEAR = (100, 110, 120)
COR_GEAR_HOVER = (140, 150, 160)

fonte_titulo = pygame.font.SysFont("Arial", 64, bold=True)
fonte_menu = pygame.font.SysFont("Arial", 28, bold=True)
fonte_engrenagem = pygame.font.SysFont("Arial", 36, bold=True)

estado_jogo = "MENU"
primeiro_frame_jogo = True  

def desenhar_texto(texto, fonte, cor, x, y):
    superficie_texto = fonte.render(texto, True, cor)
    retangulo_texto = superficie_texto.get_rect(center=(x, y))
    tela.blit(superficie_texto, retangulo_texto)

# Loop Principal
while True:
    pos_mouse = pygame.mouse.get_pos()
    evento_clique = None 
    lista_eventos = pygame.event.get()
    
    # 1. MODIFICAÇÃO: O cronômetro do pop-up só corre se estivermos JOGANDO
    if estado_jogo == "JOGANDO":
        popups_globais.atualizar()
    else:
        # Evita que o tempo acumulado no menu faça o pop-up explodir na tela assim que o jogo inicia
        popups_globais.ultimo_popup = pygame.time.get_ticks()
    
    eventos_filtrados_popup = []

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # 2. MODIFICAÇÃO: O pop-up só intercepta os cliques se o estado for JOGANDO
        if estado_jogo == "JOGANDO" and popups_globais.processar_evento(evento):
            continue  # Ignora e não repassa o clique para o jogo de fundo
            
        eventos_filtrados_popup.append(evento)

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            evento_clique = evento 
            if estado_jogo == "MENU":
                if botao_play.collidepoint(pos_mouse):
                    estado_jogo = "JOGANDO"
                    primeiro_frame_jogo = True  
                elif botao_settings.collidepoint(pos_mouse):
                    estado_jogo = "CONFIGURACOES"
                elif botao_quit.collidepoint(pos_mouse):
                    pygame.quit()
                    sys.exit()

    # --- RENDERIZAÇÃO E LÓGICA DE ESTADOS ---
    if estado_jogo == "MENU":
        tela.blit(imagem_fundo, (0, 0))
        desenhar_texto("HackTasks", fonte_titulo, COR_HACK, LARGURA // 2, 130)
        
        botao_settings = pygame.Rect(LARGURA - 55 - 20, 20, 55, 55)
        botao_play = pygame.Rect(LARGURA // 2 - 125, ALTURA - 160, 250, 50)
        botao_quit = pygame.Rect(LARGURA // 2 - 125, ALTURA - 95, 250, 50)
        
        cor_atual_play = COR_PLAY_HOVER if botao_play.collidepoint(pos_mouse) else COR_PLAY
        cor_atual_quit = COR_SAIR_HOVER if botao_quit.collidepoint(pos_mouse) else COR_SAIR
        cor_atual_settings = COR_GEAR_HOVER if botao_settings.collidepoint(pos_mouse) else COR_GEAR
        
        pygame.draw.rect(tela, cor_atual_play, botao_play, border_radius=8)
        pygame.draw.rect(tela, cor_atual_quit, botao_quit, border_radius=8)
        pygame.draw.rect(tela, cor_atual_settings, botao_settings, border_radius=8)
        
        desenhar_texto("PLAY", fonte_menu, COR_TEXTO, LARGURA // 2, ALTURA - 135)
        desenhar_texto("QUIT", fonte_menu, COR_TEXTO, LARGURA // 2, ALTURA - 70)
        desenhar_texto("⚙", fonte_engrenagem, COR_TEXTO, botao_settings.centerx, botao_settings.centery)

    elif estado_jogo == "JOGANDO":
        if primeiro_frame_jogo:
            eventos_finais = [e for e in eventos_filtrados_popup if e.type != pygame.MOUSEBUTTONDOWN]
            primeiro_frame_jogo = False  
        else:
            eventos_finais = eventos_filtrados_popup  
        
        estado_jogo = task1.gerenciar_task1(tela, eventos_finais, LARGURA, ALTURA)

    elif estado_jogo == "CONFIGURACOES":
        estado_jogo = configuracoes.gerenciar_configuracoes(tela, evento_clique, pos_mouse, LARGURA, ALTURA)

    # 3. MODIFICAÇÃO: Só desenha o pop-up por cima se estiver na fase "JOGANDO"
    if estado_jogo == "JOGANDO":
        popups_globais.desenhar(tela)

    pygame.display.flip()
    relogio.tick(60)