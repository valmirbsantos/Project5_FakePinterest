# importar url_for que será utilizado nos codigos html, chamados pelo
#           render_template, para acessar o link do site, que utilizarão a
#           url definida no @appSite.route
from flask import render_template, url_for, redirect
from projeto5fakepinterest import appSite, database, bcrypt
from projeto5fakepinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
from projeto5fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename

@appSite.route('/', methods=["GET", "POST"])
def home():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('home.html', formlogin=formlogin)

@appSite.route('/criarconta', methods=["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha_crypt = bcrypt.generate_password_hash(formcriarconta.senha.data)
        # ---- incluir usuario no banco de dados
        usuario = Usuario(username=formcriarconta.username.data,
                          email=formcriarconta.email.data,
                          senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        # ----fazer login do usuario (remember=True, armazena nos cookies o user logado)
        login_user(usuario, remember=True)
        return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('criarconta.html', formnovousuario=formcriarconta)

@appSite.route('/perfil/<id_usuario>', methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        usuario = current_user
        # perfil do proprio usuario
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            # renomear o arquivo para eliminar caracteres que possam causar problemas
            nome_seguro = str(current_user.id) + '_' + secure_filename(arquivo.filename)
            #--- salvar o arquivo na pasta fotos_posts
            # codigo abaixo pega o caminho absoluto do proprio arquivo routs.py que
            #       é igual ao path do projeto flask (nesse caso o projeto5fakepinterest)
            path_projeto = os.path.abspath(os.path.dirname(__file__))
            path_arq = os.path.join(path_projeto,
                               appSite.config["UPLOAD_FOLDER"],
                               nome_seguro)
            arquivo.save(path_arq)
            # salvar o nome do arquivo no banco de dados do usuario
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
    else:
        usuario = Usuario.query.get(int(id_usuario))
        formfoto = None
    return render_template('perfil.html', usuario=usuario, formfoto=formfoto)

@appSite.route('/feed>')
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template('feed.html', fotos=fotos)

@appSite.route('/logout>')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
