import pygame
import sys
import random

pygame.init()

LARGURA, ALTURA = 1000, 650
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo dos 7 Erros. Cibersegurança")

# Fontes
fonte_pqi = pygame.font.SysFont("Arial", 14)
fonte_lista = pygame.font.SysFont("Arial", 11)
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

# --- ESTADOS DO JOGO ---
estado_jogo = "JOGANDO" # Pode ser: "JOGANDO", "GAME_OVER", "VITORIA"
motivo_derrota = ""

# --- CONFIGURAÇÃO DO POP-UP DE COOKIES ---
cookies_visivel = False
cookies_clicado = False
tempo_surgimento_cookies = random.randint(3000, 6000) 
rect_cookies = pygame.Rect(300, 250, 400, 160)
rect_btn_evitar_cookies = pygame.Rect(350, 360, 130, 30)
rect_btn_aceitar_cookies = pygame.Rect(520, 360, 130, 30)

# --- ELEMENTOS DO FORMULÁRIO DE LOGIN ---
rect_btn_logar = pygame.Rect(815, 510, 115, 28)

# --- NOMES DOS ERROS PARA A LISTA DISCRETA ---
nomes_erros = {
    0: "URL falsa (g00gle)",
    1: "Selo 'Verificado' falso na barra",
    2: "Anúncio falso (Mina de Ouro)",
    3: "Botão 'X' falso no anúncio",
    4: "Erro ortográfico ('voçê')",
    5: "Botão Download Malicioso",
    6: "Identificou o Painel de Login Falso"
}

# --- ÁREAS CLICÁVEIS DOS 7 ERROS ---
erros = [
    pygame.Rect(232, 43, 145, 16),   # 0. URL errada
    pygame.Rect(148, 43, 16, 16),    # 1. Ícone "CORRETO" falso
    pygame.Rect(800, 125, 145, 160), # 2. Anúncio "Mina de Ouro" (Ajustado tamanho)
    pygame.Rect(925, 110, 12, 12),   # 3. Botão "X" falso do anúncio
    pygame.Rect(185, 272, 110, 18),  # 4. Erro de português
    pygame.Rect(452, 452, 150, 30),  # 5. Botão de Download
    pygame.Rect(800, 340, 145, 160), # 6. Caixa inteira do formulário de Login Falso
]

encontrados = []
relogio = pygame.time.Clock()

def reiniciar_jogo():
    global encontrados, cookies_visivel, cookies_clicado, tempo_surgimento_cookies, estado_jogo, motivo_derrota
    encontrados = []
    cookies_visivel = False
    cookies_clicado = False
    tempo_surgimento_cookies = pygame.time.get_ticks() + random.randint(3000, 6000)
    estado_jogo = "JOGANDO"
    motivo_derrota = ""

while True:
    tempo_atual = pygame.time.get_ticks()

    # Gatilho do Pop-up de Cookies
    if estado_jogo == "JOGANDO" and not cookies_visivel and not cookies_clicado and tempo_atual >= tempo_surgimento_cookies:
        cookies_visivel = True

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if estado_jogo == "JOGANDO":
                # Interações com o Pop-up de Cookies aberto
                if cookies_visivel:
                    if rect_btn_evitar_cookies.collidepoint(pos):
                        cookies_visivel = False
                        cookies_clicado = True
                    elif rect_btn_aceitar_cookies.collidepoint(pos):
                        estado_jogo = "GAME_OVER"
                        motivo_derrota = "Você aceitou cookies de terceiros! Seus dados de navegação foram expostos."
                    continue 

                # Verificação de clique no botão de Logar (Causa Derrota)
                if rect_btn_logar.collidepoint(pos):
                    estado_jogo = "GAME_OVER"
                    motivo_derrota = "Você tentou logar em um site suspeito onde não possui conta! Suas credenciais foram roubadas."
                    continue

                # Verificação dos 7 erros normais
                for i, erro in enumerate(erros):
                    if erro.collidepoint(pos) and i not in encontrados:
                        encontrados.append(i)
                        
                if len(encontrados) == 7:
                    estado_jogo = "VITORIA"

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                reiniciar_jogo()

    # --- RENDERIZAÇÃO ---
    tela.fill(CINZA_CLARO)
    
    # Título do Painel
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
    
    # Cabeçalho do site
    pygame.draw.rect(tela, AZUL_SITE, (42, 72, 916, 40))
    txt_logo = fonte_negrito.render("Portal Interativo Anti-Vírus Gratuito", True, BRANCO)
    tela.blit(txt_logo, (60, 82))
    
    # Texto Principal
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

    # --- ANÚNCIO LATERAL DE CIMA ---
    pygame.draw.rect(tela, (255, 245, 230), (800, 125, 145, 160))
    pygame.draw.rect(tela, AMARELO_ALERTA, (800, 125, 145, 160), 2)
    
    txt_anuncio1 = fonte_negrito.render("MINA DE OURO!", True, VERMELHO_ALERTA)
    txt_anuncio2 = fonte_pqi.render("Clique e receba já!", True, PRETO)
    txt_anuncio3 = fonte_negrito.render("GANHE 1 MILHÃO!", True, AZUL_SITE)
    tela.blit(txt_anuncio1, (810, 145))
    tela.blit(txt_anuncio2, (820, 175))
    tela.blit(txt_anuncio3, (806, 230))
    
    # "X" Falso do Anúncio
    pygame.draw.rect(tela, CINZA_MEDIO, (923, 128, 16, 16))
    txt_x = fonte_pqi.render("x", True, PRETO)
    tela.blit(txt_x, (928, 127))

    # --- NOVO ELEMENTO: FORMULÁRIO DE LOGIN SUSPEITO ---
    pygame.draw.rect(tela, (240, 245, 250), (800, 340, 145, 210))
    pygame.draw.rect(tela, CINZA_ESCURO, (800, 340, 145, 210), 2)
    
    txt_log_tit = fonte_negrito.render("ÁREA DE LOGIN", True, PRETO)
    tela.blit(txt_log_tit, (815, 350))
    
    # Campo E-mail
    txt_email_lbl = fonte_pqi.render("E-mail:", True, PRETO)
    tela.blit(txt_email_lbl, (810, 385))
    pygame.draw.rect(tela, BRANCO, (810, 405, 125, 22))
    pygame.draw.rect(tela, CINZA_MEDIO, (810, 405, 125, 22), 1)

    txt_senha_lbl = fonte_pqi.render("Senha do E-mail:", True, PRETO)
    tela.blit(txt_senha_lbl, (810, 435))
    pygame.draw.rect(tela, BRANCO, (810, 455, 125, 22))
    pygame.draw.rect(tela, CINZA_MEDIO, (810, 455, 125, 22), 1)

    pygame.draw.rect(tela, AZUL_SITE, rect_btn_logar, 0, 3)
    txt_btn_entrar = fonte_pqi.render("ENTRAR", True, BRANCO)
    tela.blit(txt_btn_entrar, (850, 516))

    if cookies_visivel:
        pygame.draw.rect(tela, BRANCO, rect_cookies, 0, 10)
        pygame.draw.rect(tela, PRETO, rect_cookies, 3, 10)
        
        txt_c1 = fonte_negrito.render("Este site rastreia cookies de terceiros", True, PRETO)
        txt_c2 = fonte_pqi.render("Permitir que parceiros comerciais coletem seu histórico de", True, PRETO)
        txt_c3 = fonte_pqi.render("busca para exibir anúncios baseados em dados sensíveis?", True, PRETO)
        tela.blit(txt_c1, (320, 270))
        tela.blit(txt_c2, (315, 305))
        tela.blit(txt_c3, (315, 325))

        pygame.draw.rect(tela, VERMELHO_ALERTA, rect_btn_evitar_cookies, 0, 5)
        txt_b1 = fonte_pqi.render("ACEITAR TODOS", True, BRANCO)
        tela.blit(txt_b1, (362, 368))

        pygame.draw.rect(tela, VERDE_SUCESSO, rect_btn_aceitar_cookies, 0, 5)
        txt_b2 = fonte_pqi.render("EVITAR COOKIES", True, BRANCO)
        tela.blit(txt_b2, (542, 368))

    pygame.draw.rect(tela, CINZA_MEDIO, (0, 590, LARGURA, 60))
    
    if estado_jogo == "JOGANDO":
        placar = fonte_negrito.render(f"Ameaças Detectadas: {len(encontrados)} / 7", True, AZUL_SITE)
        tela.blit(placar, (40, 608))

        y_lista = 595
        x_lista = 760
        if encontrados:
            lbl_lista_tit = fonte_lista.render("Histórico de Limpeza:", True, PRETO)
            tela.blit(lbl_lista_tit, (x_lista, y_lista))
            y_lista += 12
        for idx in encontrados:
            txt_item = fonte_lista.render(f"✔ {nomes_erros[idx]}", True, VERDE_SUCESSO)
            tela.blit(txt_item, (x_lista, y_lista))
            y_lista += 11


    elif estado_jogo == "GAME_OVER":

        pygame.draw.rect(tela, (50, 0, 0), (0, 590, LARGURA, 60))
        msg_perdeu = fonte_negrito.render("FALHA DE SEGURANÇA! " + motivo_derrota, True, BRANCO)
        msg_restart = fonte_pqi.render("Pressione [R] para tentar novamente", True, AMARELO_ALERTA)
        tela.blit(msg_perdeu, (40, 600))
        tela.blit(msg_restart, (40, 625))

    elif estado_jogo == "Parabéns por achar todos os erros!!!":
        pygame.draw.rect(tela, (0, 50, 0), (0, 590, LARGURA, 60))
        msg_vitoria = fonte_titulo.render("Excelente! O navegador está 100% limpo e seguro!", True, BRANCO)
        msg_restart = fonte_pqi.render("Pressione [R] para jogar novamente", True, AMARELO_ALERTA)
        tela.blit(msg_vitoria, (40, 598))
        tela.blit(msg_restart, (40, 628))

    pygame.display.flip()
    relogio.tick(60)
    
    #py -3.12 task3.py