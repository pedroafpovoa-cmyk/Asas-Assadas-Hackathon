import pygame
import sys
import random

pygame.init()

LARGURA, ALTURA = 1000, 650
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo dos 7 Erros - Cibersegurança Premium")

# Fontes
fonte_pqi = pygame.font.SysFont("Arial", 14)
fonte_lista = pygame.font.SysFont("Arial", 11) # Fonte bem pequena para a lista lateral
fonte_med = pygame.font.SysFont("Arial", 18)
fonte_negrito = pygame.font.SysFont("Arial", 18, bold=True)
fonte_titulo = pygame.font.SysFont("Arial", 24, bold=True)

# Cores
BRANCO = (255, 255, 255)
CINZA_CLARO = (245, 245, 245)
CINZA_MEDIO = (220, 220, 220)
CINZA_ESCURO = (180, 180, 180)
AZUL_NAVEGADOR = (235, 235, 235)
AZUL_SITE = (25, 118, 210)
PRETO = (30, 30, 30)
VERDE_SUCESSO = (46, 125, 50)
VERMELHO_ALERTA = (211, 47, 47)
AMARELO_ALERTA = (251, 192, 45)

# --- CONFIGURAÇÃO DA MOSCA (VÍRUS LENTO) ---
mosca_pos = [random.randint(200, 800), random.randint(200, 500)]
# Velocidade reduzida para se mover de forma cadenciada (simulando 12-24 fps de animação)
mosca_vel = [random.choice([-1.2, 1.2]), random.choice([-1.2, 1.2])]
mosca_raio = 12
mosca_viva = True

# --- CONFIGURAÇÃO DO POP-UP DE COOKIES ---
cookies_visivel = False
cookies_clicado = False
tempo_surgimento_cookies = random.randint(3000, 7000) 
rect_cookies = pygame.Rect(300, 250, 400, 160)

# --- NOMES DOS ERROS PARA A LISTA INFERIOR ---
nomes_erros = {
    0: "URL falsa (g00gle)",
    1: "Selo 'Verificado' falso na barra",
    2: "Anúncio falso (Mina de Ouro)",
    3: "Botão 'X' falso no anúncio",
    4: "Erro ortográfico ('voçê')",
    5: "Botão Download Malicioso",
    6: "Vírus da Mosca Removido"
}

# --- ÁREAS CLICÁVEIS ---
erros = [
    pygame.Rect(232, 43, 145, 16),   # 0. URL errada
    pygame.Rect(148, 43, 16, 16),    # 1. Ícone "CORRETO" falso
    pygame.Rect(800, 125, 145, 200), # 2. Anúncio
    pygame.Rect(925, 110, 12, 12),   # 3. Botão "X" falso
    pygame.Rect(185, 272, 110, 18),  # 4. Erro de português
    pygame.Rect(452, 452, 150, 30),  # 5. Botão de Download
    pygame.Rect(0, 0, 0, 0),         # 6. Reservado para a mosca
]

encontrados = []
relogio = pygame.time.Clock()

# Controle de tempo para a variação de frames da mosca
ultimo_frame_mosca = 0

while True:
    tempo_atual = pygame.time.get_ticks()

    if not cookies_visivel and not cookies_clicado and tempo_atual >= tempo_surgimento_cookies:
        cookies_visivel = True

    # Movimentação simulada da mosca (atualiza a posição em intervalos maiores para parecer 15-20 FPS)
    if mosca_viva and 6 not in encontrados:
        if tempo_atual - ultimo_frame_mosca > 50: # Atualiza a cada 50ms (aprox. 20 FPS de movimento)
            mosca_pos[0] += mosca_vel[0] * 2.5
            mosca_pos[1] += mosca_vel[1] * 2.5
            ultimo_frame_mosca = tempo_atual

        # Rebater nas bordas da tela do site
        if mosca_pos[0] <= 55 or mosca_pos[0] >= 945:
            mosca_vel[0] *= -1
            mosca_vel[0] += random.choice([-0.2, 0.2]) # Pequena variação ao rebater
        if mosca_pos[1] <= 85 or mosca_pos[1] >= 555:
            mosca_vel[1] *= -1
            mosca_vel[1] += random.choice([-0.2, 0.2])

        # Limitar variações exageradas de velocidade
        mosca_vel[0] = max(-2, min(2, mosca_vel[0]))
        mosca_vel[1] = max(-2, min(2, mosca_vel[1]))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if cookies_visivel:
                if rect_cookies.collidepoint(pos):
                    cookies_visivel = False
                    cookies_clicado = True
                continue 

            # Clique na Mosca
            if mosca_viva and 6 not in encontrados:
                distancia = ((pos[0] - mosca_pos[0])**2 + (pos[1] - mosca_pos[1])**2)**0.5
                if distancia <= mosca_raio + 8: 
                    mosca_viva = False
                    encontrados.append(6)

            # Clique nos outros erros
            for i, erro in enumerate(erros):
                if i != 6:
                    if erro.collidepoint(pos) and i not in encontrados:
                        encontrados.append(i)

    # --- RENDERIZAÇÃO ---
    tela.fill(CINZA_CLARO)
    
    lbl_titulo = fonte_titulo.render("Encontre os 7 Sinais de Alerta (Segurança Web)", True, PRETO)
    tela.blit(lbl_titulo, (40, 8))

    # --- BARRA DO GOOGLE CHROME ---
    pygame.draw.rect(tela, AZUL_NAVEGADOR, (40, 35, 920, 35))
    pygame.draw.circle(tela, CINZA_ESCURO, (60, 52), 10, 2)   
    pygame.draw.circle(tela, CINZA_ESCURO, (85, 52), 10, 2)   
    pygame.draw.circle(tela, CINZA_ESCURO, (110, 52), 10, 2)  
    
    pygame.draw.rect(tela, BRANCO, (140, 40, 800, 24), 0, 12)
    pygame.draw.rect(tela, CINZA_MEDIO, (140, 40, 800, 24), 1, 12)
    
    # Selo falso verificado
    pygame.draw.circle(tela, VERDE_SUCESSO, (156, 51), 8)
    txt_check = fonte_pqi.render("v", True, BRANCO)
    tela.blit(txt_check, (153, 43))
    
    # URL
    txt_url = fonte_pqi.render("https://www.g00gle-security-update.com/login", True, (100, 100, 100))
    tela.blit(txt_url, (175, 43))

    # --- CONTEÚDO DO SITE ---
    pygame.draw.rect(tela, BRANCO, (40, 70, 920, 500))
    pygame.draw.rect(tela, CINZA_MEDIO, (40, 70, 920, 500), 2)
    
    pygame.draw.rect(tela, AZUL_SITE, (42, 72, 916, 40))
    txt_logo = fonte_negrito.render("Portal Interativo Anti-Vírus Gratuito", True, BRANCO)
    tela.blit(txt_logo, (60, 82))
    
    txt_artigo_titulo = fonte_negrito.render("AVISO: Atualize seus componentes de segurança imediatamente", True, VERMELHO_ALERTA)
    tela.blit(txt_artigo_titulo, (65, 140))
    
    linhas_texto = [
        "O sistema identificou arquivos corrompidos que podem danificar sua máquina.",
        "Para garantir que voçê navegue sem anúncios irritantes, atualize sua proteção.",
        "Atenção: ignore avisos de cookies ou extensões externas durante esse processo.",
        "O download começará em segundo plano assim que aceitar as permissões da página."
    ]
    
    y_txt = 180
    for linha in linhas_texto:
        txt_render = fonte_med.render(linha, True, PRETO)
        tela.blit(txt_render, (65, y_txt))
        y_txt += 30

    # Botão de Download
    pygame.draw.rect(tela, VERDE_SUCESSO, (450, 450, 155, 32), 0, 5)
    txt_btn = fonte_negrito.render("DOWNLOAD GRÁTIS", True, BRANCO)
    tela.blit(txt_btn, (458, 456))

    # --- ANÚNCIOS LATERAIS ---
    pygame.draw.rect(tela, (255, 245, 230), (800, 125, 145, 200))
    pygame.draw.rect(tela, AMARELO_ALERTA, (800, 125, 145, 200), 2)
    
    txt_anuncio1 = fonte_negrito.render("MINA DE OURO!", True, VERMELHO_ALERTA)
    txt_anuncio2 = fonte_pqi.render("Clique e receba já!", True, PRETO)
    txt_anuncio3 = fonte_negrito.render("GANHE 1 MILHÃO!", True, AZUL_SITE)
    tela.blit(txt_anuncio1, (810, 145))
    tela.blit(txt_anuncio2, (820, 175))
    tela.blit(txt_anuncio3, (806, 250))
    
    # "X" Falso
    pygame.draw.rect(tela, CINZA_MEDIO, (923, 128, 16, 16))
    txt_x = fonte_pqi.render("x", True, PRETO)
    tela.blit(txt_x, (928, 127))

    # --- DESENHO DA MOSCA (Se estiver viva) ---
    if mosca_viva and 6 not in encontrados:
        pygame.draw.circle(tela, PRETO, (int(mosca_pos[0]), int(mosca_pos[1])), mosca_raio)
        pygame.draw.circle(tela, CINZA_ESCURO, (int(mosca_pos[0]) - 8, int(mosca_pos[1]) - 6), 6)
        pygame.draw.circle(tela, CINZA_ESCURO, (int(mosca_pos[0]) + 8, int(mosca_pos[1]) - 6), 6)
        pygame.draw.circle(tela, VERMELHO_ALERTA, (int(mosca_pos[0]) - 3, int(mosca_pos[1]) - 4), 2)
        pygame.draw.circle(tela, VERMELHO_ALERTA, (int(mosca_pos[0]) + 3, int(mosca_pos[1]) - 4), 2)

    # Nota: A seção "MARCAÇÃO DOS ERROS" (os retângulos verdes) foi COMPLETAMENTE removida daqui!

    # --- POP-UP DE COOKIES ---
    if cookies_visivel:
        pygame.draw.rect(tela, BRANCO, rect_cookies, 0, 10)
        pygame.draw.rect(tela, PRETO, rect_cookies, 3, 10)
        
        txt_c1 = fonte_negrito.render("Este site rastreia cookies de terceiros", True, PRETO)
        txt_c2 = fonte_pqi.render("Permitir que parceiros comerciais coletem seu histórico de", True, PRETO)
        txt_c3 = fonte_pqi.render("busca para exibir anúncios baseados em dados sensíveis?", True, PRETO)
        tela.blit(txt_c1, (320, 270))
        tela.blit(txt_c2, (315, 305))
        tela.blit(txt_c3, (315, 325))
        
        pygame.draw.rect(tela, VERMELHO_ALERTA, (350, 360, 130, 30), 0, 5)
        txt_b1 = fonte_pqi.render("EVITAR COOKIES", True, BRANCO)
        tela.blit(txt_b1, (362, 368))
        
        pygame.draw.rect(tela, CINZA_ESCURO, (520, 360, 130, 30), 0, 5)
        txt_b2 = fonte_pqi.render("ACEITAR TODOS", True, PRETO)
        tela.blit(txt_b2, (542, 368))

    # --- PAINEL INFERIOR ---
    pygame.draw.rect(tela, CINZA_MEDIO, (0, 590, LARGURA, 60))
    placar = fonte_negrito.render(f"Ameaças Detectadas: {len(encontrados)} / 7", True, AZUL_SITE)
    tela.blit(placar, (40, 608))

    # --- LISTA DISCRETA DE ERROS ENCONTRADOS (Canto inferior direito) ---
    y_lista = 595
    x_lista = 760
    
    # Renderiza um cabeçalho bem pequeno para a lista
    if encontrados:
        lbl_lista_tit = fonte_lista.render("Histórico de Limpeza:", True, PRETO)
        tela.blit(lbl_lista_tit, (x_lista, y_lista))
        y_lista += 12
        
    for idx in encontrados:
        txt_item = fonte_lista.render(f"✔ {nomes_erros[idx]}", True, VERDE_SUCESSO)
        tela.blit(txt_item, (x_lista, y_lista))
        y_lista += 11  # Espaçamento bem curto entre itens

    # Tela de Vitória
    if len(encontrados) == 7:
        msg_vitoria = fonte_titulo.render("Excelente! O navegador está 100% seguro!", True, VERDE_SUCESSO)
        tela.blit(msg_vitoria, (320, 603))

    pygame.display.flip()
    relogio.tick(60)