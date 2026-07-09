# settings.py
import pygame

# Cores e fontes específicas das configurações
COR_FUNDO = (50, 40, 60)
COR_TEXTO = (255, 255, 255)
COR_MUTED = (150, 150, 160)
COR_INTERATIVA = (70, 80, 95)
COR_HOVER = (100, 115, 135)
COR_VOLTAR = (200, 70, 70)
COR_VOLTAR_HOVER = (230, 95, 95)

# Variáveis globais para guardar o estado das opções
volume = 50
tela_cheia = False

def iniciar_fontes():
    global fonte_titulo, fonte_label, fonte_valor
    fonte_titulo = pygame.font.SysFont("Arial", 48, bold=True)
    fonte_label = pygame.font.SysFont("Arial", 28, bold=True)
    fonte_valor = pygame.font.SysFont("Arial", 24)

def desenhar_texto(tela, texto, fonte, cor, x, y, alinhar="center"):
    superficie = fonte.render(texto, True, cor)
    if alinhar == "left":
        retangulo = superficie.get_rect(topleft=(x, y))
    else:
        retangulo = superficie.get_rect(center=(x, y))
    tela.blit(superficie, retangulo)

# Esta função roda a cada frame quando o estado_jogo for "CONFIGURACOES"
def gerenciar_configuracoes(tela, evento, pos_mouse, largura, altura):
    global volume, tela_cheia
    
    # Executa a inicialização de fontes apenas uma vez
    if 'fonte_titulo' not in globals():
        iniciar_fontes()

    # --- DEFINIÇÃO DOS BOTÕES ---
    btn_vol_menos = pygame.Rect(450, 220, 45, 45)
    btn_vol_mais = pygame.Rect(580, 220, 45, 45)
    btn_tela = pygame.Rect(450, 320, 175, 45)
    btn_voltar = pygame.Rect(largura // 2 - 100, altura - 100, 200, 50)

    # --- PROCESSA O EVENTO CASO ELE EXISTA ---
    if evento and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if btn_vol_menos.collidepoint(pos_mouse):
            volume = max(0, volume - 10)
        elif btn_vol_mais.collidepoint(pos_mouse):
            volume = min(100, volume + 10)
        elif btn_tela.collidepoint(pos_mouse):
            tela_cheia = not tela_cheia
            if tela_cheia:
                tela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
            else:
                tela = pygame.display.set_mode((largura, altura))
        elif btn_voltar.collidepoint(pos_mouse):
            return "MENU" # Sinaliza que o jogador quer voltar

    # --- DESENHO NA TELA ---
    tela.fill(COR_FUNDO)
    desenhar_texto(tela, "CONFIGURAÇÕES", fonte_titulo, COR_TEXTO, largura // 2, 80)
    
    # Volume
    desenhar_texto(tela, "Volume do Jogo:", fonte_label, COR_MUTED, 180, 225, alinhar="left")
    cor_menos = COR_HOVER if btn_vol_menos.collidepoint(pos_mouse) else COR_INTERATIVA
    cor_mais = COR_HOVER if btn_vol_mais.collidepoint(pos_mouse) else COR_INTERATIVA
    pygame.draw.rect(tela, cor_menos, btn_vol_menos, border_radius=6)
    pygame.draw.rect(tela, cor_mais, btn_vol_mais, border_radius=6)
    desenhar_texto(tela, "-", fonte_label, COR_TEXTO, btn_vol_menos.centerx, btn_vol_menos.centery - 2)
    desenhar_texto(tela, "+", fonte_label, COR_TEXTO, btn_vol_mais.centerx, btn_vol_mais.centery - 2)
    desenhar_texto(tela, f"{volume}%", fonte_valor, COR_TEXTO, 535, 242)
    
    # Modo de Tela
    desenhar_texto(tela, "Modo de Tela:", fonte_label, COR_MUTED, 180, 325, alinhar="left")
    cor_btn_tela = COR_HOVER if btn_tela.collidepoint(pos_mouse) else COR_INTERATIVA
    pygame.draw.rect(tela, cor_btn_tela, btn_tela, border_radius=6)
    texto_tela = "Tela Cheia" if tela_cheia else "Janela"
    desenhar_texto(tela, texto_tela, fonte_valor, COR_TEXTO, btn_tela.centerx, btn_tela.centery)
    
    # Voltar
    cor_btn_voltar = COR_VOLTAR_HOVER if btn_voltar.collidepoint(pos_mouse) else COR_VOLTAR
    pygame.draw.rect(tela, cor_btn_voltar, btn_voltar, border_radius=8)
    desenhar_texto(tela, "SALVAR E VOLTAR", fonte_valor, COR_TEXTO, btn_voltar.centerx, btn_voltar.centery)

    return "CONFIGURACOES" # Continua na tela de configurações