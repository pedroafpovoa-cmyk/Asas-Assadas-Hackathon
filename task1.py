import pygame
import string
import random
import unicodedata

# Inicialização de Fontes
pygame.font.init()
fonte = pygame.font.SysFont(None, 36)          # Usada para Título, Senha e Botão
fonte_pequena = pygame.font.SysFont(None, 24)  # Usada para requisitos e dicas

# --- GEOMETRIA ADAPTADA E CENTRALIZADA (Para 800x600) ---

# Centro do eixo X é 400 (LARGURA // 2)

# Caixa de senha (600px de largura): X = 400 - (600 // 2) = 100. Y = 90 (Logo abaixo do título)
caixa = pygame.Rect(100, 90, 600, 50)       

# Botão Verificar (200px de largura): X = 400 - (200 // 2) = 300. Y = 160 (Logo abaixo da caixa)
botao = pygame.Rect(300, 160, 200, 50)     

# Blocos de dicas empilhados no canto inferior direito
# Alinhados em X = 480, Y começando em 270 para não embolar
bloquinho_dica = pygame.Rect(480, 270, 280, 95) # Em cima: Capitais/Países
bloquinho_ave = pygame.Rect(480, 385, 280, 95)  # Em baixo: Aves

cor_inativa = (220, 220, 220)
cor_ativa = (255, 255, 255)

# Variáveis de Estado do Jogo
ativa = False
senha = ""
indice_cursor = 0
tempo_cursor = 0
mostrar_cursor = True
mensagem = ""
cor_mensagem = (255, 255, 255)

# Controle de Conclusão e Saída
concluido = False
tempo_conclusao = 0

# --- Funções Auxiliares de Dados ---
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

# Carrega as listas de arquivos externos
capitais_dict = carregar_capitais("capitais.txt")
aves = carregar_lista("aves.txt")

capital_secreta = ""
pais_dica = ""
ave_dica = ""

def sortear_dica_capital():
    global capital_secreta, pais_dica
    if capitais_dict:
        capital_normalizada, pais = random.choice(list(capitais_dict.items()))
        pais_dica = pais
    else:
        pais_dica = "Arquivo não encontrado"

def sortear_dica_ave():
    global ave_dica
    if aves:
        ave_dica = random.choice(aves).capitalize()
    else:
        ave_dica = "Arquivo não encontrado"

# Sorteios Iniciais
sortear_dica_capital()
sortear_dica_ave()

# --- Validadores da Senha ---
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
        erros.append("Senha inválida: tamanho incorreto.")
    if not verificar_especiais(texto):
        erros.append("Senha precisa de 5 caracteres especiais.")
    if not verificar_capital(texto):
        erros.append("A senha não contém nenhuma capital válida!")
    if not verificar_ave(texto):
        erros.append("Inclua uma ave que não voa válida.")
    if not verificar_numeros(texto):
        erros.append("A senha deve conter exatamente 7 números.")
    return erros


# --- FUNÇÃO GERENCIADORA ---
def gerenciar_task1(tela, lista_eventos, LARGURA, ALTURA):
    global ativa, senha, indice_cursor, tempo_cursor, mostrar_cursor, mensagem, cor_mensagem, concluido, tempo_conclusao

    # 1. Lógica do temporizador após vencer
    if concluido:
        if pygame.time.get_ticks() - tempo_conclusao >= 3000:
            senha = ""
            indice_cursor = 0
            mensagem = ""
            concluido = False
            return "MENU"

    # Piscar do cursor
    tempo_cursor += 16
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

            if bloquinho_dica.collidepoint(evento.pos):
                sortear_dica_capital()
                mensagem = ""

            if bloquinho_ave.collidepoint(evento.pos):
                sortear_dica_ave()
                mensagem = ""

            if botao.collidepoint(evento.pos):
                erros = verificar_senha(senha)
                if len(erros) == 0:
                    mensagem = "SENHA VÁLIDA!"
                    cor_mensagem = (0, 255, 0)
                    if not concluido:
                        concluido = True
                        tempo_conclusao = pygame.time.get_ticks()
                        try:
                            with open("senha_salva.txt", "w", encoding="utf-8") as f:
                                f.write(senha.strip())
                        except Exception as e:
                            print(f"Erro ao salvar a senha: {e}")
                else:
                    mensagem = erros[0]
                    cor_mensagem = (255, 80, 80)
                    concluido = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "MENU"

            if ativa:
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

    # Título centralizado
    titulo = fonte.render("CRIADOR DE SENHAS", True, (255, 255, 255))
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 30))

    # Caixa de senha centralizada abaixo do título
    cor = cor_ativa if ativa else cor_inativa
    pygame.draw.rect(tela, cor, caixa)
    pygame.draw.rect(tela, (0, 0, 0), caixa, 2)

    # Texto interno da senha
    texto_antes_cursor = senha[:indice_cursor]
    superficie_antes = fonte.render(texto_antes_cursor, True, (0, 0, 0))
    largura_antes = superficie_antes.get_width()

    texto_completo = fonte.render(senha, True, (0, 0, 0))
    tela.blit(texto_completo, (caixa.x + 10, caixa.y + 11))

    if ativa and mostrar_cursor:
        x_cursor = caixa.x + 10 + largura_antes
        pygame.draw.line(tela, (0, 0, 0), (x_cursor, caixa.y + 10), (x_cursor, caixa.y + 40), 2)

    # Botão VERIFICAR alinhado centralizado abaixo da caixa de texto
    pygame.draw.rect(tela, (50, 180, 80), botao)
    texto_botao = fonte.render("VERIFICAR", True, (255, 255, 255))
    tela.blit(texto_botao, (botao.x + (botao.width // 2 - texto_botao.get_width() // 2), botao.y + 11))

    # --- REQUISITOS NO CANTO ESQUERDO DA TELA ---
    regras = [
        "Requisitos da Senha:",
        "- Entre 6 e 40 caracteres",
        "- Pelo menos 5 especiais",
        "- Uma capital da Europa Ocidental",
        "- Uma ave que não voa",
        "- Exatamente 7 números",
    ]

    # Renderiza organizadamente na esquerda (X = 50), começando abaixo do botão (Y = 270)
    y = 270
    for linha in regras:
        # Destaca o título da lista usando a fonte normal, o restante usa a pequena
        if linha == "Requisitos da Senha:":
            superficie = fonte.render(linha, True, (255, 255, 255))
            y_spacing = 35
        else:
            superficie = fonte_pequena.render(linha, True, (240, 240, 240))
            y_spacing = 30
            
        tela.blit(superficie, (50, y))
        y += y_spacing

    # --- BLOCOS DE DICAS EMPILHADOS (CANTO DIREITO) ---
    
    # Bloco de Cima: Capitais
    pygame.draw.rect(tela, (45, 90, 135), bloquinho_dica)
    pygame.draw.rect(tela, (255, 255, 255), bloquinho_dica, 2)

    texto_dica_titulo = fonte_pequena.render("DICA DE CAPITAL:", True, (255, 215, 0))
    texto_dica_conteudo = fonte_pequena.render(f"País: {pais_dica}", True, (255, 255, 255))
    texto_dica_clique = fonte_pequena.render("(Clique para mudar)", True, (180, 200, 220))

    tela.blit(texto_dica_titulo, (bloquinho_dica.x + 15, bloquinho_dica.y + 10))
    tela.blit(texto_dica_conteudo, (bloquinho_dica.x + 15, bloquinho_dica.y + 37))
    tela.blit(texto_dica_clique, (bloquinho_dica.x + 15, bloquinho_dica.y + 64))

    # Bloco de Baixo: Aves
    pygame.draw.rect(tela, (45, 90, 135), bloquinho_ave)
    pygame.draw.rect(tela, (255, 255, 255), bloquinho_ave, 2)

    texto_ave_titulo = fonte_pequena.render("Exemplo de ave:", True, (0, 255, 255))
    texto_ave_conteudo = fonte_pequena.render(f"Ave: {ave_dica}", True, (255, 255, 255))
    texto_ave_clique = fonte_pequena.render("(Clique para mudar)", True, (180, 200, 220))

    tela.blit(texto_ave_titulo, (bloquinho_ave.x + 15, bloquinho_ave.y + 10))
    tela.blit(texto_ave_conteudo, (bloquinho_ave.x + 15, bloquinho_ave.y + 37))
    tela.blit(texto_ave_clique, (bloquinho_ave.x + 15, bloquinho_ave.y + 64))

    # Mensagem de Feedback dinâmica (Centralizada entre o botão e os blocos inferiores)
    if mensagem != "":
        resultado = fonte_pequena.render(mensagem, True, cor_mensagem)
        tela.blit(resultado, (LARGURA // 2 - resultado.get_width() // 2, 230))

    return "JOGANDO"