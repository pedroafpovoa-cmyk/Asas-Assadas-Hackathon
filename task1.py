import pygame
import string

pygame.init()

LARGURA = 900
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini Game - Criador de Senhas")

fonte = pygame.font.SysFont(None, 36)
fonte_pequena = pygame.font.SysFont(None, 28)

caixa = pygame.Rect(100, 100, 700, 50)
botao = pygame.Rect(350, 200, 200, 60)

cor_inativa = (220, 220, 220)
cor_ativa = (255, 255, 255)

ativa = False
senha = ""

mensagem = ""
cor_mensagem = (255, 255, 255)


def carregar_lista(arquivo):

    lista = []

    with open(arquivo, "r", encoding="utf-8") as f:

        for linha in f:

            linha = linha.strip().lower()

            if linha != "":
                lista.append(linha)

    return lista


capitais = carregar_lista("capitais.txt")
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

    texto = texto.lower()

    for capital in capitais:

        if capital in texto:
            return True

    return False


def verificar_ave(texto):

    texto = texto.lower()

    for ave in aves:

        if ave in texto:
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
        erros.append("Inclua uma capital válida.")

    if not verificar_ave(texto):
        erros.append("Inclua uma ave que não voa.")

    if not verificar_numeros(texto):
        erros.append("A senha deve conter exatamente 7 números.")

    return erros


clock = pygame.time.Clock()

rodando = True

while rodando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:

            if caixa.collidepoint(evento.pos):
                ativa = True

            else:
                ativa = False

            if botao.collidepoint(evento.pos):

                erros = verificar_senha(senha)

                if len(erros) == 0:
                    mensagem = "SENHA VALIDA!"
                    cor_mensagem = (0, 255, 0)

                else:
                    mensagem = erros[0]
                    cor_mensagem = (255, 80, 80)

        if evento.type == pygame.KEYDOWN and ativa:

            if evento.key == pygame.K_BACKSPACE:

                senha = senha[:-1]

            else:

                if len(senha) < 40:
                    senha += evento.unicode

    tela.fill((30, 60, 90))

    titulo = fonte.render("CRIADOR DE SENHAS", True, (255, 255, 255))
    tela.blit(titulo, (250, 30))

    cor = cor_ativa if ativa else cor_inativa

    pygame.draw.rect(tela, cor, caixa)
    pygame.draw.rect(tela, (0, 0, 0), caixa, 2)

    texto = fonte.render(senha, True, (0, 0, 0))
    tela.blit(texto, (caixa.x + 10, caixa.y + 10))

    pygame.draw.rect(tela, (50, 180, 80), botao)

    texto_botao = fonte.render("VERIFICAR", True, (255, 255, 255))
    tela.blit(texto_botao, (botao.x + 25, botao.y + 15))

    regras = [
        "Regras:",
        "- Entre 6 e 40 caracteres",
        "- Pelo menos 5 caracteres especiais",
        "- Uma capital da Europa Ocidental ou da antiga Iugoslavia",
        "- Uma ave que não voa",
        "- Exatamente 7 números"
    ]

    y = 300

    for linha in regras:

        superficie = fonte_pequena.render(linha, True, (255, 255, 255))
        tela.blit(superficie, (70, y))
        y += 30

    if mensagem != "":

        resultado = fonte_pequena.render(mensagem, True, cor_mensagem)
        tela.blit(resultado, (70, 520))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()