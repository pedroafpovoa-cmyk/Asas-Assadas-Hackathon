import pygame
import sys
import random

pygame.init()

# --- RESOLUÇÃO ---
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo dos Erros: Cibersegurança")

# Fontes
fonte_pqi = pygame.font.SysFont("Arial", 13)
fonte_lista = pygame.font.SysFont("Arial", 11)
fonte_med = pygame.font.SysFont("Arial", 15)
fonte_negrito = pygame.font.SysFont("Arial", 16, bold=True)
fonte_titulo = pygame.font.SysFont("Arial", 20, bold=True)
fonte_gameover = pygame.font.SysFont("Arial", 50, bold=True)

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
LARANJA_ALERTA = (230, 81, 0)

# --- ESTADOS DO JOGO ---
estado_jogo = "JOGANDO"
motivo_derrota = ""

# --- CONFIGURAÇÃO DO POP-UP DE COOKIES ---
cookies_visivel = False
cookies_clicado = False
tempo_surgimento_cookies = random.randint(3000, 6000) 
rect_cookies = pygame.Rect(190, 220, 420, 160)
rect_btn_evitar_cookies = pygame.Rect(240, 330, 140, 30)
rect_btn_aceitar_cookies = pygame.Rect(420, 330, 140, 30)

# --- ELEMENTOS DO FORMULÁRIO DE LOGIN (DURAÇÃO E ESCRITA) ---
rect_campo_email = pygame.Rect(630, 365, 125, 22)
rect_campo_senha = pygame.Rect(630, 415, 125, 22)
rect_btn_logar = pygame.Rect(635, 470, 115, 28)

texto_email = ""
texto_senha = ""
campo_ativo = None  # Pode ser "email" ou "senha"

# --- NOMES DOS ERROS MAPEADOS (AGORA SÃO 6 ALERTAS PARA ENCONTRAR) ---
nomes_erros = {
    0: "URL falsa (g00gle)",
    1: "Selo 'Seguro' falso (Laranja)",
    2: "Anúncio falso (Mina de Ouro)",
    3: "Botão 'X' falso no anúncio",
    5: "Botão Download Malicioso",
    6: "Recusou Cookies Suspeitos"
}

# --- ÁREAS CLICÁVEIS RECALCULADAS ---
erros = {
    0: pygame.Rect(175, 40, 350, 24),    # URL Falsa
    1: pygame.Rect(148, 43, 16, 16),     # Selo falso laranja
    2: pygame.Rect(620, 140, 145, 145),  # Anúncio "Mina de Ouro"
    3: pygame.Rect(743, 128, 16, 16),    # Botão "X" falso do anúncio
    5: pygame.Rect(300, 450, 200, 40),   # Botão de Download Ampliado
}

encontrados = []
relogio = pygame.time.Clock()

def reiniciar_jogo():
    global encontrados, cookies_visivel, cookies_clicado, tempo_surgimento_cookies, estado_jogo, motivo_derrota
    global texto_email, texto_senha, campo_ativo
    encontrados = []
    cookies_visivel = False
    cookies_clicado = False
    tempo_surgimento_cookies = pygame.time.get_ticks() + random.randint(3000, 6000)
    estado_jogo = "JOGANDO"
    motivo_derrota = ""
    texto_email = ""
    texto_senha = ""
    campo_ativo = None

while True:
    tempo_atual = pygame.time.get_ticks()

    if estado_jogo == "JOGANDO" and not cookies_visivel and not cookies_clicado and tempo_atual >= tempo_surgimento_cookies:
        cookies_visivel = True

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Captura de cliques do Mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if estado_jogo == "JOGANDO":
                # Interação com campos de texto primeiro
                if rect_campo_email.collidepoint(pos):
                    campo_ativo = "email"
                elif rect_campo_senha.collidepoint(pos):
                    campo_ativo = "senha"
                else:
                    campo_ativo = None

                # Lógica dos Cookies
                if cookies_visivel:
                    if rect_btn_evitar_cookies.collidepoint(pos):
                        cookies_visivel = False
                        cookies_clicado = True
                        if 6 not in encontrados:
                            encontrados.append(6)
                        continue
                    elif rect_btn_aceitar_cookies.collidepoint(pos):
                        estado_jogo = "GAME_OVER"
                        motivo_derrota = "Você aceitou cookies de terceiros! Seus dados de navegação foram expostos."
                        continue 

                # Botão de Entrar (Causa Game Over independente do que foi digitado)
                if rect_btn_logar.collidepoint(pos):
                    estado_jogo = "GAME_OVER"
                    motivo_derrota = "Você tentou logar em um site suspeito! Suas credenciais foram roubadas."
                    continue

                # Identificação de erros mecânicos da tela
                for idx, erro_rect in erros.items():
                    if erro_rect.collidepoint(pos) and idx not in encontrados:
                        encontrados.append(idx)
                        
                # Condição de Vitória (Agora são 6 itens mapeados)
                if len(encontrados) == 6:
                    estado_jogo = "VITORIA"

        # Captura de Teclado (Para digitação e Restart)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                reiniciar_jogo()
            
            # Digitação nos inputs ativos
            if estado_jogo == "JOGANDO" and campo_ativo is not None:
                if evento.key == pygame.K_BACKSPACE:
                    if campo_ativo == "email":
                        texto_email = texto_email[:-1]
                    elif campo_ativo == "senha":
                        texto_senha = texto_senha[:-1]
                elif evento.key not in [pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_TAB]:
                    # Limita o tamanho dos caracteres para caber na caixa de texto
                    if campo_ativo == "email" and len(texto_email) < 16:
                        texto_email += evento.unicode
                    elif campo_ativo == "senha" and len(texto_senha) < 16:
                        texto_senha += evento.unicode

    # --- RENDERIZAÇÃO DA TELA DO JOGO ---
    tela.fill(CINZA_CLARO)
    
    # Título do Painel
    lbl_titulo = fonte_titulo.render("Encontre os Sinais de Alerta (Segurança Web)", True, PRETO)
    tela.blit(lbl_titulo, (40, 8))

    # Barra do Navegador
    pygame.draw.rect(tela, AZUL_NAVEGADOR, (40, 35, 720, 35))
    pygame.draw.circle(tela, CINZA_ESCURO, (60, 52), 10, 2)   
    pygame.draw.circle(tela, CINZA_ESCURO, (85, 52), 10, 2)   
    pygame.draw.circle(tela, CINZA_ESCURO, (110, 52), 10, 2)  
    
    pygame.draw.rect(tela, BRANCO, (140, 40, 600, 24), 0, 12)
    pygame.draw.rect(tela, CINZA_MEDIO, (140, 40, 600, 24), 1, 12)
    
    # Selo falso Laranja
    pygame.draw.circle(tela, LARANJA_ALERTA, (156, 51), 8)
    txt_check = fonte_pqi.render("!", True, BRANCO)
    tela.blit(txt_check, (153, 44))
    
    # URL Falsa
    txt_url = fonte_pqi.render("http://www.g00gle-security-antivirus.com/free-cleaner", True, PRETO)
    tela.blit(txt_url, (175, 44))
    
    # Corpo do site
    pygame.draw.rect(tela, BRANCO, (40, 70, 720, 450))
    pygame.draw.rect(tela, CINZA_MEDIO, (40, 70, 720, 450), 2)
    
    # Cabeçalho do site
    pygame.draw.rect(tela, AZUL_SITE, (42, 72, 716, 40))
    txt_logo = fonte_negrito.render("Portal Interativo Anti-Vírus Gratuito", True, BRANCO)
    tela.blit(txt_logo, (60, 82))
    
    # Texto Principal (CORRIGIDO: "você" agora está escrito corretamente)
    txt_artigo_titulo = fonte_negrito.render("AVISO: Atualize seus componentes de segurança imediatamente", True, VERMELHO_ALERTA)
    tela.blit(txt_artigo_titulo, (65, 140))
    
    linhas_texto = [
        "O sistema identificou arquivos corrompidos que podem danificar sua máquina.",
        "Para garantir que você navegue sem anúncios irritantes, atualize sua proteção.",
        "Atenção: ignore avisos de cookies ou extensões externas durante esse processo.",
        "O download começará em segundo plano assim que aceitar as permissões da página."
    ]
    
    y_txt = 180
    for linha in linhas_texto:
        txt_render = fonte_med.render(linha, True, PRETO)
        tela.blit(txt_render, (65, y_txt))
        y_txt += 26

    # Botão de Download
    pygame.draw.rect(tela, VERDE_SUCESSO, (300, 450, 200, 40), 0, 5)
    txt_btn = fonte_negrito.render("DOWNLOAD GRÁTIS", True, BRANCO)
    tela.blit(txt_btn, (322, 460))

    # Anúncio Lateral
    pygame.draw.rect(tela, (255, 245, 230), (620, 125, 145, 160))
    pygame.draw.rect(tela, AMARELO_ALERTA, (620, 125, 145, 160), 2)
    
    txt_anuncio1 = fonte_negrito.render("MINA DE OURO!", True, VERMELHO_ALERTA)
    txt_anuncio2 = fonte_pqi.render("Clique e receba já!", True, PRETO)
    txt_anuncio3 = fonte_negrito.render("GANHE 1 MILHÃO!", True, AZUL_SITE)
    tela.blit(txt_anuncio1, (630, 155))
    tela.blit(txt_anuncio2, (640, 185))
    tela.blit(txt_anuncio3, (626, 230))
    
    # "X" Falso do Anúncio
    pygame.draw.rect(tela, CINZA_MEDIO, (743, 128, 16, 16))
    txt_x = fonte_pqi.render("x", True, PRETO)
    tela.blit(txt_x, (748, 127))

    # --- FORMULÁRIO DE LOGIN INTERATIVO ---
    pygame.draw.rect(tela, (240, 245, 250), (620, 300, 145, 210))
    pygame.draw.rect(tela, CINZA_ESCURO, (620, 300, 145, 210), 2)
    
    txt_log_tit = fonte_negrito.render("ÁREA DE LOGIN", True, PRETO)
    tela.blit(txt_log_tit, (635, 310))
    
    # Campo de E-mail
    txt_email_lbl = fonte_pqi.render("E-mail:", True, PRETO)
    tela.blit(txt_email_lbl, (630, 345))
    pygame.draw.rect(tela, BRANCO, rect_campo_email)
    # Borda muda de cor caso esteja selecionada
    cor_borda_email = AZUL_SITE if campo_ativo == "email" else CINZA_MEDIO
    pygame.draw.rect(tela, cor_borda_email, rect_campo_email, 1)
    # Renderiza texto digitado no e-mail
    surf_txt_email = fonte_pqi.render(texto_email, True, PRETO)
    tela.blit(surf_txt_email, (634, 369))

    # Campo de Senha
    txt_senha_lbl = fonte_pqi.render("Senha do E-mail:", True, PRETO)
    tela.blit(txt_senha_lbl, (630, 395))
    pygame.draw.rect(tela, BRANCO, rect_campo_senha)
    cor_borda_senha = AZUL_SITE if campo_ativo == "senha" else CINZA_MEDIO
    pygame.draw.rect(tela, cor_borda_senha, rect_campo_senha, 1)
    # Renderiza bolinhas para a senha ocultada
    surf_txt_senha = fonte_pqi.render("*" * len(texto_senha), True, PRETO)
    tela.blit(surf_txt_senha, (634, 421))

    # Botão Entrar
    pygame.draw.rect(tela, AZUL_SITE, rect_btn_logar, 0, 3)
    txt_btn_entrar = fonte_pqi.render("ENTRAR", True, BRANCO)
    tela.blit(txt_btn_entrar, (670, 476))

    # Pop-up de Cookies
    if cookies_visivel:
        pygame.draw.rect(tela, BRANCO, rect_cookies, 0, 10)
        pygame.draw.rect(tela, PRETO, rect_cookies, 3, 10)
        
        txt_c1 = fonte_negrito.render("Este site rastreia cookies de terceiros", True, PRETO)
        txt_c2 = fonte_pqi.render("Permitir que parceiros comerciais coletem seu histórico de", True, PRETO)
        txt_c3 = fonte_pqi.render("busca para exibir anúncios baseados em dados sensíveis?", True, PRETO)
        tela.blit(txt_c1, (210, 240))
        tela.blit(txt_c2, (205, 275))
        tela.blit(txt_c3, (205, 295))

        pygame.draw.rect(tela, VERMELHO_ALERTA, rect_btn_evitar_cookies, 0, 5)
        txt_b1 = fonte_pqi.render("EVITAR COOKIES", True, BRANCO)
        tela.blit(txt_b1, (260, 338))

        pygame.draw.rect(tela, VERDE_SUCESSO, rect_btn_aceitar_cookies, 0, 5)
        txt_b2 = fonte_pqi.render("ACEITAR TODOS", True, BRANCO)
        tela.blit(txt_b2, (440, 338))

    # Placar Inferior de Jogo Ativo
    pygame.draw.rect(tela, CINZA_MEDIO, (0, 530, LARGURA, 70))
    placar = fonte_negrito.render(f"Ameaças Detectadas: {len(encontrados)} / 6", True, AZUL_SITE)
    tela.blit(placar, (40, 555))

    y_lista = 535
    x_lista = 560
    if encontrados:
        lbl_lista_tit = fonte_lista.render("Histórico de Limpeza:", True, PRETO)
        tela.blit(lbl_lista_tit, (x_lista, y_lista))
        y_lista += 12
    for idx in encontrados:
        txt_item = fonte_lista.render(f"✔ {nomes_erros[idx]}", True, VERDE_SUCESSO)
        tela.blit(txt_item, (x_lista, y_lista))
        y_lista += 11

    # --- TELA INTEGRAL DE VITORIA ---
    if estado_jogo == "VITORIA":
        pygame.draw.rect(tela, (0, 50, 0), (0, 530, LARGURA, 70))
        msg_vitoria = fonte_titulo.render("Excelente! O navegador está 100% limpo e seguro!", True, BRANCO)
        msg_restart = fonte_pqi.render("Pressione [R] para jogar novamente", True, AMARELO_ALERTA)
        tela.blit(msg_vitoria, (40, 542))
        tela.blit(msg_restart, (40, 572))

    # --- MODAL / FILTRO DE GAME OVER INTEGRAL ---
    elif estado_jogo == "GAME_OVER":
        filtro_vermelho = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        filtro_vermelho.fill((180, 20, 20, 230))  
        tela.blit(filtro_vermelho, (0, 0))
        
        pygame.draw.rect(tela, PRETO, (100, 150, 600, 300), 0, 15)
        pygame.draw.rect(tela, VERMELHO_ALERTA, (100, 150, 600, 300), 3, 15)
        
        lbl_go = fonte_gameover.render("GAME OVER", True, VERMELHO_ALERTA)
        lbl_falha = fonte_titulo.render("FALHA DE SEGURANÇA!", True, BRANCO)
        lbl_motivo = fonte_med.render(motivo_derrota, True, CINZA_CLARO)
        lbl_reiniciar = fonte_negrito.render("Pressione [R] para tentar novamente", True, AMARELO_ALERTA)
        
        tela.blit(lbl_go, (LARGURA // 2 - lbl_go.get_width() // 2, 180))
        tela.blit(lbl_falha, (LARGURA // 2 - lbl_falha.get_width() // 2, 250))
        tela.blit(lbl_motivo, (LARGURA // 2 - lbl_motivo.get_width() // 2, 300))
        tela.blit(lbl_reiniciar, (LARGURA // 2 - lbl_reiniciar.get_width() // 2, 380))

    pygame.display.flip()
    relogio.tick(60)