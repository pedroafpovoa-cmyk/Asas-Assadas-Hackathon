dados = {
    "Avestruz",
    "Ema",
    "Emu",
    "Casuar",
    "Kiwi",
    "Pinguim",
    "Cormorão-das-Galápagos",
    "Kakapo",
    "Takahe",
    "Weka",
    "Trilho",
    "Frango-d'água",
    "Mergulhão",
    "Pato-vapor",
    "Marreca"
}

with open("aves.txt", "w", encoding="utf-8") as arquivo:
    for ave in dados:
        arquivo.write(f"{ave}\n")