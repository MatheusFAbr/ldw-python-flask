animes_favoritos = []

def adicionar_anime(anime):
    animes_favoritos.append(anime)

def listar_animes():
    return animes_favoritos

def remover_anime(index):
    if 0 <= index < len(animes_favoritos):
        animes_favoritos.pop(index)
