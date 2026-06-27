import pygame
import string
import random  # Importado para sortear a dica aleatória

pygame.init()

LARGURA = 900
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini Game - Criador de Senhas")

fonte = pygame.font.SysFont(None, 36)
fonte_pequena = pygame.font.SysFont(None, 28)

caixa = pygame.Rect(100, 100, 700, 50)
botao = pygame.Rect(350, 200, 200, 60)

# Novo retângulo para o bloquinho de dicas no canto inferior direito
bloquinho_dica = pygame.Rect(550, 420, 280, 100)

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


# Modificada para tratar o formato "Cidade: País"
def carregar_capitais(arquivo):
    dicionario_capitais = {}
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha and ":" in linha:
                # Separa a capital e o país, removendo espaços extras
                capital, pais = linha.split(":")
                dicionario_capitais[capital.strip().lower()] = pais.strip()
    return dicionario_capitais


# Carrega as estruturas de dados
capitais_dict = carregar_capitais("capitais.txt")
aves = carregar_lista("aves.txt")

# Sorteia uma capital secreta e pega o seu respectivo país para a dica
capital_secreta, pais_dica = random.choice(list(capitais_dict.items()))


def verificar_tamanho(texto):
    return 6 <= len(texto) <= 40


def verificar_especiais(texto):
    quantidade = 0
    for caractere in texto:
        if caractere in string.punctuation:
            quantidade += 1
    return quantidade >= 5


# Agora verifica se a senha contém especificamente a capital sorteada na dica
def verificar_capital(texto):
    return capital_secreta in texto.lower()


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
        erros.append("A capital não corresponde à dica!")

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
                    mensagem = "SENHA VÁLIDA!"
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
        "- Use a capital correspondente à dica",
        "- Uma ave que não voa",
        "- Exatamente 7 números",
    ]

    y = 300
    for linha in regras:
        superficie = fonte_pequena.render(linha, True, (255, 255, 255))
        tela.blit(superficie, (70, y))
        y += 30

    # --- DESENHO DO BLOQUINHO DE DICA ---
    # Fundo do bloquinho (um azul um pouco mais claro para destacar)
    pygame.draw.rect(tela, (45, 90, 135), bloquinho_dica)
    pygame.draw.rect(
        tela, (255, 255, 255), bloquinho_dica, 2
    )  # Borda branca

    # Textos da dica
    texto_dica_titulo = fonte_pequena.render(
        "DICA DE CAPITAL:", True, (255, 215, 0)
    )  # Dourado
    texto_dica_conteudo = fonte_pequena.render(
        f"País: {pais_dica}", True, (255, 255, 255)
    )

    tela.blit(texto_dica_titulo, (bloquinho_dica.x + 15, bloquinho_dica.y + 20))
    tela.blit(
        texto_dica_conteudo, (bloquinho_dica.x + 15, bloquinho_dica.y + 55)
    )
    # ------------------------------------

    if mensagem != "":
        resultado = fonte_pequena.render(mensagem, True, cor_mensagem)
        tela.blit(resultado, (70, 520))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()