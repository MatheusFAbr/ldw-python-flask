import requests
from flask import render_template, request, redirect, url_for, flash
from models import db
from models.anime_model import AnimeFavorite
from models.user_model import User

def init_app(app):

    @app.route('/')
    def home():
        return render_template('index.html')

    # Catálogo de animes (API)
    @app.route('/animes')
    def lista_animes():
        url = "https://api.jikan.moe/v4/top/anime?limit=15"
        response = requests.get(url).json()
        animes = response.get("data", [])
        return render_template("anime_list.html", animes=animes)

    # Detalhes do anime (API)
    @app.route('/anime/<int:anime_id>')
    def detalhes_anime(anime_id):
        url = f"https://api.jikan.moe/v4/anime/{anime_id}"
        response = requests.get(url).json()
        anime = response.get("data", {})
        anime_data = {
            "title": anime.get("title"),
            "synopsis": anime.get("synopsis"),
            "episodes": anime.get("episodes"),
            "score": anime.get("score"),
            "image": anime.get("images", {}).get("jpg", {}).get("image_url"),
            "url": anime.get("url")
        }
        return render_template("anime_detail.html", anime=anime_data)

    # Busca por nome (API)
    @app.route('/buscar', methods=['GET', 'POST'])
    def buscar_anime():
        animes = []
        if request.method == 'POST':
            termo = request.form.get('termo')
            if termo:
                url = f"https://api.jikan.moe/v4/anime?q={termo}&limit=12"
                response = requests.get(url).json()
                animes = response.get("data", [])
        return render_template("anime_search.html", animes=animes)

    # Cadastro local (DB)
    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro_anime():
        if request.method == 'POST':
            titulo = request.form.get("titulo")
            genero = request.form.get("genero")
            nota = request.form.get("nota")
            image = request.form.get("image") or None

            if titulo and genero and nota:
                # Ensure at least one default user exists
                user = User.query.first()
                if not user:
                    user = User(name='default')
                    db.session.add(user)
                    db.session.commit()

                try:
                    nota_val = float(nota)
                except:
                    nota_val = None

                fav = AnimeFavorite(titulo=titulo, genero=genero, nota=nota_val, image=image, user_id=user.id)
                db.session.add(fav)
                db.session.commit()
                flash("Anime cadastrado com sucesso!", "success")
                return redirect(url_for('listar_cadastros'))
            else:
                flash("Preencha todos os campos!", "danger")
        return render_template("anime_cadastro.html")

    # Listar favoritos (paginação)
    @app.route('/favoritos')
    def listar_cadastros():
        page = request.args.get('page', 1, type=int)
        per_page = 5
        pagination = AnimeFavorite.query.order_by(AnimeFavorite.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        animes = pagination.items
        return render_template("anime_listar_cad.html", animes=animes, pagination=pagination)

    # Editar favorito
    @app.route('/editar/<int:anime_id>', methods=['GET', 'POST'])
    def editar(anime_id):
        anime = AnimeFavorite.query.get_or_404(anime_id)
        if request.method == 'POST':
            anime.titulo = request.form.get('titulo') or anime.titulo
            anime.genero = request.form.get('genero') or anime.genero
            nota = request.form.get('nota')
            if nota:
                try:
                    anime.nota = float(nota)
                except:
                    pass
            anime.image = request.form.get('image') or anime.image
            db.session.commit()
            flash('Anime atualizado com sucesso!', 'success')
            return redirect(url_for('listar_cadastros'))
        return render_template('anime_edit.html', anime=anime)

    # Remover favorito
    @app.route('/remover/<int:anime_id>')
    def remover(anime_id):
        anime = AnimeFavorite.query.get_or_404(anime_id)
        db.session.delete(anime)
        db.session.commit()
        flash("Anime removido com sucesso!", "warning")
        return redirect(url_for('listar_cadastros'))
