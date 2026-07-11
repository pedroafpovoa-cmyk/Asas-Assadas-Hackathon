import pygame
import string
import random
import unicodedata

# --- FUNÇÕES DE VALIDAÇÃO E DADOS ---
def normalizar_texto(texto):
    texto_minusculo = texto.strip().lower()
    processado = unicodedata.normalize('NFKD', texto_minusculo)
    return "".join([c for c in processado if not unicodedata.combining(c)])

def carregar_lista(arquivo):
    lista = []
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha != "":
                    lista.append(normalizar_texto(linha))
    except FileNotFoundError:
        print(f"Aviso: Arquivo {arquivo} não encontrado.")
    return lista

def carregar_capitais(arquivo):
    dicionario_capitais = {}
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha and ":" in linha and not linha.startswith("["):
                    capital, pais = linha.split(":", 1)
                    dicionario_capitais[normalizar_texto(capital)] = pais.strip()
    except FileNotFoundError:
        print(f"Aviso: Arquivo {arquivo} não encontrado.")
    return dicionario_capitais

capitais_dict = carregar_capitais("capitais.txt")
aves = carregar_lista("aves.txt")

def verificar_tamanho(texto):
    return 6 <= len(texto) <= 40

def verificar_especiais(texto):
    quantidade = 0
    for caractere in texto:
        if caractere in string.punctuation:
            quantidade += 1
    return quantidade >= 5

def verificar_capital(texto):
    texto_usuario = normalizar_texto(texto)
    for capital in capitais_dict.keys():
        if capital in texto_usuario:
            return True
    return False

def verificar_ave(texto):
    texto_usuario = normalizar_texto(texto)
    for ave in aves:
        if ave in texto_usuario:
            return True
    return False

def verificar_numeros(texto):
    quantidade = 0
    for caractere in texto:
        if caractere.isdigit():
            quantidade += 1
    return quantidade == 7

def verificar_senha(texto):
    erros = []
    if not verificar_tamanho(texto):
        erros.append("Senha deve ter entre 6 e 40 caracteres.")
    if not verificar_especiais(texto):
        erros.append("Senha deve possuir pelo menos 5 caracteres especiais.")
    if not verificar_capital(texto):
        erros.append("A senha não contém nenhuma capital válida!")
    if not verificar_ave(texto):
        erros.append("Inclua uma ave que não voe válida.")
    if not verificar_numeros(texto):
        erros.append("A senha deve conter exatamente 7 números.")
    return erros

# --- VARIÁVEIS GLOBAIS DE ESTADO ---
caixa = pygame.Rect(100, 100, 700, 50)
botao = pygame.Rect(350, 180, 200, 50)

cor_inativa = (220, 220, 220)
cor_ativa = (255, 255, 255)

ativa = False
senha = ""
indice_cursor = 0
tempo_cursor = 0
mostrar_cursor = True
mensagem = ""
cor_mensagem = (255, 255, 255)

concluido = False
tempo_conclusao = 0

fontes_carregadas = False
fonte = None
fonte_pequena = None

# --- FUNÇÃO GERENCIADORA ---
def gerenciar_final_task(tela, lista_eventos, LARGURA, ALTURA):
    global ativa, senha, indice_cursor, tempo_cursor, mostrar_cursor, mensagem, cor_mensagem
    global concluido, tempo_conclusao, fontes_carregadas, fonte, fonte_pequena

    if not fontes_carregadas:
        pygame.font.init()
        fonte = pygame.font.SysFont(None, 36)
        fonte_pequena = pygame.font.SysFont(None, 28)
        fontes_carregadas = True

    # 1. Lógica do temporizador após vencer
    if concluido:
        if pygame.time.get_ticks() - tempo_conclusao >= 3000:
            # Reseta as variáveis caso queira jogar de novo e manda de volta pro MENU (Fim do jogo)
            senha = ""
            indice_cursor = 0
            mensagem = ""
            concluido = False
            ativa = False
            return "MENU" # Venceu o jogo inteiro! Volta pro menu inicial.

    # Lógica do cursor piscando
    tempo_cursor += 16 # Aproximadamente o tempo de 1 frame a 60 FPS
    if tempo_cursor >= 500:
        mostrar_cursor = not mostrar_cursor
        tempo_cursor = 0

    # 2. Processamento de Eventos
    for evento in lista_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if caixa.collidepoint(evento.pos):
                ativa = True
                indice_cursor = len(senha)
            else:
                ativa = False

            if botao.collidepoint(evento.pos) and not concluido:
                erros = verificar_senha(senha)
                if len(erros) == 0:
                    mensagem = "SENHA VÁLIDA! JOGO CONCLUÍDO!"
                    cor_mensagem = (0, 255, 0)
                    concluido = True
                    tempo_conclusao = pygame.time.get_ticks() # Marca a hora que venceu
                    
                    try:
                        with open("senha_salva.txt", "w", encoding="utf-8") as f:
                            f.write(senha.strip())
                    except Exception as e:
                        print(f"Erro ao salvar: {e}")
                else:
                    mensagem = erros[0]
                    cor_mensagem = (255, 80, 80)
                    concluido = False

        if evento.type == pygame.KEYDOWN and ativa and not concluido:
            if evento.key == pygame.K_ESCAPE:
                mensagem = "Tentou fugir pelo ESC? Sem chances."
                cor_mensagem = (255, 80, 80)
                continue

            if evento.key == pygame.K_BACKSPACE:
                if indice_cursor > 0:
                    senha = senha[: indice_cursor - 1] + senha[indice_cursor:]
                    indice_cursor -= 1
                    mostrar_cursor = True
                    tempo_cursor = 0

            elif evento.key == pygame.K_DELETE:
                if indice_cursor < len(senha):
                    senha = senha[:indice_cursor] + senha[indice_cursor + 1 :]
                    mostrar_cursor = True
                    tempo_cursor = 0

            elif evento.key == pygame.K_LEFT:
                if indice_cursor > 0:
                    indice_cursor -= 1
                    mostrar_cursor = True
                    tempo_cursor = 0

            elif evento.key == pygame.K_RIGHT:
                if indice_cursor < len(senha):
                    indice_cursor += 1
                    mostrar_cursor = True
                    tempo_cursor = 0

            elif evento.key not in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_TAB):
                if evento.unicode and evento.unicode.isprintable():
                    if len(senha) < 40:
                        senha = (
                            senha[:indice_cursor]
                            + evento.unicode
                            + senha[indice_cursor:]
                        )
                        indice_cursor += 1
                        mostrar_cursor = True
                        tempo_cursor = 0
                        
    # 3. Renderização na Tela
    tela.fill((120, 60, 90))

    titulo = fonte.render("              SENHA INICIAL", True, (255, 255, 255))
    tela.blit(titulo, (250, 30))

    cor = cor_ativa if ativa else cor_inativa
    pygame.draw.rect(tela, cor, caixa)
    pygame.draw.rect(tela, (0, 0, 0), caixa, 2)

    texto_antes_cursor = senha[:indice_cursor]
    superficie_antes = fonte.render(texto_antes_cursor, True, (0, 0, 0))
    largura_antes = superficie_antes.get_width()

    texto_completo = fonte.render(senha, True, (0, 0, 0))
    tela.blit(texto_completo, (caixa.x + 10, caixa.y + 11))

    if ativa and mostrar_cursor and not concluido:
        x_cursor = caixa.x + 10 + largura_antes
        pygame.draw.line(tela, (0, 0, 0), (x_cursor, caixa.y + 10), (x_cursor, caixa.y + 40), 2)

    pygame.draw.rect(tela, (50, 180, 80), botao)
    texto_botao = fonte.render(" VERIFICAR", True, (255, 255, 255))
    tela.blit(texto_botao, (botao.x + 24, botao.y + 10))

    texto_instrucao = fonte_pequena.render("Coloque sua senha inicial.", True, (255, 255, 255))
    tela.blit(texto_instrucao, (70, 280))

    if mensagem != "":
        resultado = fonte_pequena.render(mensagem, True, cor_mensagem)
        tela.blit(resultado, (70, 520))

    # Mantém o jogo no estado FINAL_TASK enquanto estiver jogando
    return "FINAL_TASK"