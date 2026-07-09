import pygame
import sys
import configuracoes  
import task1  # Importa o seu minijogo

# Inicialização Básica
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Menu Reformulado")
relogio = pygame.time.Clock()

# Carrega fundo
try:
    imagem_fundo = pygame.image.load("Tela_inicial.png").convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))
except pygame.error:
    imagem_fundo = pygame.Surface((LARGURA, ALTURA))
    imagem_fundo.fill((30, 30, 40))

# --- DIMENSÕES DOS BOTÕES REFORMULADAS ---
# PLAY e QUIT ficaram mais largos e altos (300x65)
# SETTINGS agora é um retângulo horizontal (120x50) posicionado no topo direito
botao_settings = pygame.Rect(LARGURA - 120 - 20, 20, 120, 50)
botao_play = pygame.Rect(LARGURA // 2 - 150, ALTURA - 180, 300, 65)
botao_quit = pygame.Rect(LARGURA // 2 - 150, ALTURA - 95, 300, 65)

# Carregamento e redimensionamento automático dos PNGs baseado nos novos tamanhos
try:
    img_play = pygame.image.load("botao_play.png").convert_alpha()
    img_play = pygame.transform.scale(img_play, (botao_play.width, botao_play.height))
except pygame.error:
    img_play = None

try:
    img_settings = pygame.image.load("botao_settings.png").convert_alpha()
    img_settings = pygame.transform.scale(img_settings, (botao_settings.width, botao_settings.height))
except pygame.error:
    img_settings = None

try:
    img_quit = pygame.image.load("botao_quit.png").convert_alpha()
    img_quit = pygame.transform.scale(img_quit, (botao_quit.width, botao_quit.height))
except pygame.error:
    img_quit = None


# Cores e Fontes (Usadas caso o PNG não exista)
COR_HACK = (20, 50, 70)
COR_TEXTO = (255, 255, 255)
COR_PLAY = (50, 180, 100)
COR_PLAY_HOVER = (80, 210, 130)
COR_SAIR = (200, 60, 60)
COR_SAIR_HOVER = (230, 90, 90)
COR_GEAR = (100, 110, 120)
COR_GEAR_HOVER = (140, 150, 160)

fonte_titulo = pygame.font.SysFont("Arial", 64, bold=True)
# Aumentei um pouco a fonte do menu para acompanhar os botões maiores
fonte_menu = pygame.font.SysFont("Arial", 32, bold=True)
fonte_engrenagem = pygame.font.SysFont("Arial", 32, bold=True)

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
    
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
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

    # --- RENDERIZAÇÃO E LÓGICA DE ESTADOS ---
    if estado_jogo == "MENU":
        tela.blit(imagem_fundo, (0, 0))
        desenhar_texto("HackTasks", fonte_titulo, COR_HACK, LARGURA // 2, 130)
        
        # --- DESENHO DO BOTÃO PLAY ---
        if img_play:
            tela.blit(img_play, (botao_play.x, botao_play.y))
        else:
            cor_atual_play = COR_PLAY_HOVER if botao_play.collidepoint(pos_mouse) else COR_PLAY
            pygame.draw.rect(tela, cor_atual_play, botao_play, border_radius=8)
            desenhar_texto("PLAY", fonte_menu, COR_TEXTO, botao_play.centerx, botao_play.centery)
            
        # --- DESENHO DO BOTÃO QUIT ---
        if img_quit:
            tela.blit(img_quit, (botao_quit.x, botao_quit.y))
        else:
            cor_atual_quit = COR_SAIR_HOVER if botao_quit.collidepoint(pos_mouse) else COR_SAIR
            pygame.draw.rect(tela, cor_atual_quit, botao_quit, border_radius=8)
            desenhar_texto("QUIT", fonte_menu, COR_TEXTO, botao_quit.centerx, botao_quit.centery)
            
        # --- DESENHO DO BOTÃO SETTINGS ---
        if img_settings:
            tela.blit(img_settings, (botao_settings.x, botao_settings.y))
        else:
            cor_atual_settings = COR_GEAR_HOVER if botao_settings.collidepoint(pos_mouse) else COR_GEAR
            pygame.draw.rect(tela, cor_atual_settings, botao_settings, border_radius=8)
            desenhar_texto("SETTINGS ⚙", fonte_engrenagem, COR_TEXTO, botao_settings.centerx, botao_settings.centery)

    elif estado_jogo == "JOGANDO":
        if primeiro_frame_jogo:
            eventos_finais = [e for e in lista_eventos if e.type != pygame.MOUSEBUTTONDOWN]
            primeiro_frame_jogo = False  
        else:
            eventos_finais = lista_eventos  
        
        estado_jogo = task1.gerenciar_task1(tela, eventos_finais, LARGURA, ALTURA)

    elif estado_jogo == "CONFIGURACOES":
        estado_jogo = configuracoes.gerenciar_configuracoes(tela, evento_clique, pos_mouse, LARGURA, ALTURA)

    pygame.display.flip()
    relogio.tick(60)