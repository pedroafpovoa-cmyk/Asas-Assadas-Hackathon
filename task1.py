import pygame
import string
import random
import unicodedata

pygame.init()

LARGURA = 900
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini Game - Criador de Senhas")

fonte = pygame.font.SysFont(None, 36)
fonte_pequena = pygame.font.SysFont(None, 28)

caixa = pygame.Rect(100, 100, 700, 50)
botao = pygame.Rect(350, 180, 200, 50)  # Ajustado levemente a posição para dar espaço aos blocos

# Retângulos para os blocos de dicas no canto inferior direito
bloquinho_ave = pygame.Rect(550, 310, 280, 95)   # Novo bloco (em cima)
bloquinho_dica = pygame.Rect(550, 420, 280, 100) # Bloco de capitais (em baixo)

cor_inativa = (220, 220, 220)
cor_ativa = (255, 255, 255)

ativa = False
senha = ""
indice_cursor = 0

tempo_cursor = 0
mostrar_cursor = True

mensagem = ""
cor_mensagem = (255, 255, 255)


# Função auxiliar para remover acentos e deixar em minúsculo
def normalizar_texto(texto):
    texto_minusculo = texto.strip().lower()
    # Remove acentos usando decomposição unicode
    processado = unicodedata.normalize('NFKD', texto_minusculo)
    return "".join([c for c in processado if not unicodedata.combining(c)])


def carregar_lista(arquivo):
    lista = []
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha != "":
                    # Guarda o texto normalizado (sem acento e minúsculo) para a checagem rápida
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
                    # A chave do dicionário será a capital SEM acento para facilitar a busca genérica
                    dicionario_capitais[normalizar_texto(capital)] = pais.strip()
    except FileNotFoundError:
        print(f"Aviso: Arquivo {arquivo} não encontrado.")
    return dicionario_capitais


# Carrega as estruturas de dados
capitais_dict = carregar_capitais("capitais.txt")
aves = carregar_lista("aves.txt")

# Variáveis para as dicas visuais
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
        # Sorteia uma ave da lista (ela está guardada normalizada, mas serve como string de dica)
        ave_dica = random.choice(aves).capitalize()
    else:
        ave_dica = "Arquivo não encontrado"


# Sorteia as primeiras dicas do jogo
sortear_dica_capital()
sortear_dica_ave()


def verificar_tamanho(texto):
    return 6 <= len(texto) <= 40


def verificar_especiais(texto):
    quantidade = 0
    for caractere in texto:
        if caractere in string.punctuation:
            quantidade += 1
    return quantidade >= 5


# AGORA ACEITA QUALQUER CAPITAL DO ARQUIVO (E IGNORA ACENTOS)
def verificar_capital(texto):
    texto_usuario = normalizar_texto(texto)
    # Procura se alguma das chaves (capitais sem acento) está contida no texto do usuário
    for capital in capitais_dict.keys():
        if capital in texto_usuario:
            return True
    return False


# VERIFICA SE QUALQUER AVE ESTÁ NA SENHA (E IGNORA ACENTOS)
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
        erros.append("Inclua uma ave que não voa válida.")
    if not verificar_numeros(texto):
        erros.append("A senha deve conter exatamente 7 números.")
    return erros


clock = pygame.time.Clock()
rodando = True

while rodando:
    dt = clock.tick(60)

    tempo_cursor += dt
    if tempo_cursor >= 500:
        mostrar_cursor = not mostrar_cursor
        tempo_cursor = 0

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if caixa.collidepoint(evento.pos):
                ativa = True
                indice_cursor = len(senha)
            else:
                ativa = False

            # Clique no bloco de dicas de capitais
            if bloquinho_dica.collidepoint(evento.pos):
                sortear_dica_capital()
                mensagem = ""

            # Clique no bloco de dicas de aves
            if bloquinho_ave.collidepoint(evento.pos):
                sortear_dica_ave()
                mensagem = ""

            if botao.collidepoint(evento.pos):
                erros = verificar_senha(senha)
                if len(erros) == 0:
                    mensagem = "SENHA VÁLIDA!"
                    cor_mensagem = (0, 255, 0)
                else:
                    mensagem = erros[0]
                    cor_mensagem = (255, 80, 80)

        if evento.type == pygame.KEYDOWN and ativa:
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

            elif evento.key not in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_TAB, pygame.K_ESCAPE):
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

    tela.fill((120, 60, 90))

    titulo = fonte.render("          CRIADOR DE SENHAS", True, (255, 255, 255))
    tela.blit(titulo, (250, 30))

    cor = cor_ativa if ativa else cor_inativa
    pygame.draw.rect(tela, cor, caixa)
    pygame.draw.rect(tela, (0, 0, 0), caixa, 2)

    texto_antes_cursor = senha[:indice_cursor]
    superficie_antes = fonte.render(texto_antes_cursor, True, (0, 0, 0))
    largura_antes = superficie_antes.get_width()

    texto_completo = fonte.render(senha, True, (0, 0, 0))
    tela.blit(texto_completo, (caixa.x + 10, caixa.y + 11))

    if ativa and mostrar_cursor:
        x_cursor = caixa.x + 10 + largura_antes
        pygame.draw.line(
            tela,
            (0, 0, 0),
            (x_cursor, caixa.y + 10),
            (x_cursor, caixa.y + 40),
            2,
        )

    pygame.draw.rect(tela, (50, 180, 80), botao)
    texto_botao = fonte.render("VERIFICAR", True, (255, 255, 255))
    tela.blit(texto_botao, (botao.x + 25, botao.y + 10))

    regras = [
        "Regras:",
        "- Entre 6 e 40 caracteres",
        "- Pelo menos 5 caracteres especiais",
        "- Coloque uma capital da Europa Ocidental",
        "- Uma ave que não voe",
        "- Exatamente 7 números",
    ]

    y = 280
    for linha in regras:
        superficie = fonte_pequena.render(linha, True, (255, 255, 255))
        tela.blit(superficie, (70, y))
        y += 30

    pygame.draw.rect(tela, (45, 90, 135), bloquinho_ave)
    pygame.draw.rect(tela, (255, 255, 255), bloquinho_ave, 2)

    texto_ave_titulo = fonte_pequena.render("Exemplo de ave:", True, (0, 255, 255))  # Cor Ciano
    texto_ave_conteudo = fonte_pequena.render(f"Ave: {ave_dica}", True, (255, 255, 255))
    texto_ave_clique = fonte_pequena.render("(Clique para mudar)", True, (180, 200, 220))

    tela.blit(texto_ave_titulo, (bloquinho_ave.x + 15, bloquinho_ave.y + 10))
    tela.blit(texto_ave_conteudo, (bloquinho_ave.x + 15, bloquinho_ave.y + 37))
    tela.blit(texto_ave_clique, (bloquinho_ave.x + 15, bloquinho_ave.y + 64))

    pygame.draw.rect(tela, (45, 90, 135), bloquinho_dica)
    pygame.draw.rect(tela, (255, 255, 255), bloquinho_dica, 2)

    texto_dica_titulo = fonte_pequena.render("DICA DE CAPITAL:", True, (255, 215, 0))
    texto_dica_conteudo = fonte_pequena.render(f"País: {pais_dica}", True, (255, 255, 255))
    texto_dica_clique = fonte_pequena.render("(Clique para mudar)", True, (180, 200, 220))

    tela.blit(texto_dica_titulo, (bloquinho_dica.x + 15, bloquinho_dica.y + 12))
    tela.blit(texto_dica_conteudo, (bloquinho_dica.x + 15, bloquinho_dica.y + 42))
    tela.blit(texto_dica_clique, (bloquinho_dica.x + 15, bloquinho_dica.y + 72))

    if mensagem != "":
        resultado = fonte_pequena.render(mensagem, True, cor_mensagem)
        tela.blit(resultado, (70, 520))

    pygame.display.flip()

pygame.quit()