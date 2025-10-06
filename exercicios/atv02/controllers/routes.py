import requests
from flask import render_template, request, redirect, url_for, flash
from models.anime_model import adicionar_anime, listar_animes, remover_anime

def init_app(app):

    @app.route('/')
    def home():
        return render_template('index.html')

    # Catálogo de animes (API)
    @app.route('/animes')
    def lista_animes():
        url = "https://api.jikan.moe/v4/top/anime?limit=15"
        response = requests.get(url).json()
        animes = response["data"]
        return render_template("anime_list.html", animes=animes)

    # Detalhes do anime
    @app.route('/anime/<int:anime_id>')
    def detalhes_anime(anime_id):
        url = f"https://api.jikan.moe/v4/anime/{anime_id}"
        response = requests.get(url).json()
        anime = response["data"]
        anime_data = {
            "title": anime["title"],
            "synopsis": anime["synopsis"],
            "episodes": anime["episodes"],
            "score": anime["score"],
            "image": anime["images"]["jpg"]["image_url"],
            "url": anime["url"]
        }
        return render_template("anime_detail.html", anime=anime_data)

    # Busca por nome
    @app.route('/buscar', methods=['GET', 'POST'])
    def buscar_anime():
        animes = []
        if request.method == 'POST':
            termo = request.form.get('termo')
            if termo:
                url = f"https://api.jikan.moe/v4/anime?q={termo}&limit=12"
                response = requests.get(url).json()
                animes = response["data"]
        return render_template("anime_search.html", animes=animes)

    # Cadastro local
    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro_anime():
        if request.method == 'POST':
            titulo = request.form.get("titulo")
            genero = request.form.get("genero")
            nota = request.form.get("nota")
            if titulo and genero and nota:
                adicionar_anime({"titulo": titulo, "genero": genero, "nota": nota})
                flash("Anime cadastrado com sucesso!", "success")
                return redirect(url_for('listar_cadastros'))
            else:
                flash("Preencha todos os campos!", "danger")
        return render_template("anime_cadastro.html")

    # Listar favoritos
    @app.route('/favoritos')
    def listar_cadastros():
        animes = listar_animes()
        return render_template("anime_listar_cad.html", animes=animes)

    # Remover favorito
    @app.route('/remover/<int:index>')
    def remover(index):
        remover_anime(index)
        flash("Anime removido com sucesso!", "warning")
        return redirect(url_for('listar_cadastros'))
