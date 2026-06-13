Capitais_Paises = {
    "Lisboa": "Portugal",
    "Madri": "Espanha",
    "Paris": "França",
    "Bruxelas": "Bélgica",
    "Amsterdã": "Países Baixos",
    "Luxemburgo": "Luxemburgo",
    "Berlim": "Alemanha",
    "Viena": "Áustria",
    "Berna": "Suíça",
    "Vaduz": "Liechtenstein",
    "Mônaco": "Mônaco",
    "Belgrado": "Sérvia",
    "Zagreb": "Croácia",
    "Liubliana": "Eslovênia",
    "Sarajevo": "Bósnia e Herzegovina",
    "Escópia": "Macedônia do Norte",
    "Podgorica": "Montenegro"
}

dados = {
    "Lisboa": "Portugal",
    "Madri": "Espanha",
    "Paris": "França",
    "Bruxelas": "Bélgica",
    "Amsterdã": "Países Baixos",
    "Luxemburgo": "Luxemburgo",
    "Berlim": "Alemanha",
    "Viena": "Áustria",
    "Berna": "Suíça",
    "Vaduz": "Liechtenstein",
    "Mônaco": "Mônaco",
    "Belgrado": "Sérvia",
    "Zagreb": "Croácia",
    "Liubliana": "Eslovênia",
    "Sarajevo": "Bósnia e Herzegovina",
    "Escópia": "Macedônia do Norte",
    "Podgorica": "Montenegro"
}

with open("capitais.txt", "w", encoding="utf-8") as arquivo:
    for capital, pais in dados.items():
        arquivo.write(f"{capital}: {pais}\n")