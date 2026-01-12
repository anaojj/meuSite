# ================================
# IMPORTAÇÕES
# ================================

# Importa Flask e funções essenciais
from flask import Flask, render_template, request, redirect, session

# Importa funções do backend (lógica separada)
from backend import (
    carregar_produtos,
    verificar_promocao,
    carregar_promocoes,
    salvar_promocoes,
    carregar_admin,
    salvar_admin
)


# ================================
# CRIA A APLICAÇÃO FLASK
# ================================

# Cria a aplicação Flask
# ⚠️ Nenhuma rota pode existir antes disso
app = Flask(__name__)

# Chave secreta usada pelo Flask para sessões
# (login, segurança, cookies, etc)
app.secret_key = "gm_acessorios_super_secreto"


# ================================
# ROTA HOME (PÁGINA INICIAL)
# ================================
@app.route("/")
def home():

    # Verifica se existe promoção ativa
    promocao = verificar_promocao()

    # Renderiza a página inicial
    return render_template("index.html", promocao=promocao)


# ================================
# ROTA PRODUTOS
# ================================
@app.route("/produtos")
def produtos():

    # Carrega os produtos do JSON
    produtos = carregar_produtos()

    # Renderiza a página de produtos
    return render_template("produtos.html", produtos=produtos)


# ================================
# ROTA ADMIN - CRIAÇÃO ÚNICA
# ================================
@app.route("/admin/criar", methods=["GET", "POST"])
def admin_criar():

    # Carrega dados do admin
    admin = carregar_admin()

    # Impede criar novamente
    if admin["criado"]:
        return "Admin já criado. Use o login.", 403

    # Se o formulário foi enviado
    if request.method == "POST":

        # Salva os dados informados
        admin["usuario"] = request.form.get("usuario")
        admin["senha"] = request.form.get("senha")
        admin["telefone"] = request.form.get("telefone")

        # Marca como criado
        admin["criado"] = True

        # Salva no JSON
        salvar_admin(admin)

        # Redireciona para o login
        return redirect("/admin/login")

    # Exibe formulário de criação
    return render_template("admin_criar.html")


# ================================
# ROTA ADMIN - LOGIN
# ================================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    # Carrega dados do admin
    admin = carregar_admin()

    # Se estiver bloqueado, força redefinição
    if admin["bloqueado"]:
        return redirect("/admin/reset")

    # Se o formulário foi enviado
    if request.method == "POST":

        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        # Verifica login e senha
        if usuario == admin["usuario"] and senha == admin["senha"]:

            # Login correto → zera tentativas
            admin["tentativas"] = 0
            salvar_admin(admin)

            # Marca admin como logado
            session["admin_logado"] = True

            return redirect("/admin/promocoes")

        else:
            # Login errado → incrementa tentativas
            admin["tentativas"] += 1

            # Bloqueia após 3 tentativas
            if admin["tentativas"] >= 3:
                admin["bloqueado"] = True

            salvar_admin(admin)

            return render_template(
                "admin_login.html",
                erro="Usuário ou senha inválidos"
            )

    # Exibe tela de login
    return render_template("admin_login.html")


# ================================
# ROTA ADMIN - PROMOÇÕES
# ================================
@app.route("/admin/promocoes", methods=["GET", "POST"])
def admin_promocoes():

    # Protege a rota (login obrigatório)
    if not session.get("admin_logado"):
        return redirect("/admin/login")

    # Se o formulário foi enviado
    if request.method == "POST":

        # Carrega promoções atuais
        dados = carregar_promocoes()

        # ----------------------------
        # PROMOÇÃO DA SEMANA
        # ----------------------------
        dados["promocao"]["ativo"] = "promo_ativo" in request.form
        dados["promocao"]["titulo"] = request.form.get("promo_titulo")
        dados["promocao"]["descricao"] = request.form.get("promo_descricao")

        # ----------------------------
        # PROMOÇÃO FIM DE SEMANA
        # ----------------------------
        dados["promofds"]["ativo"] = "fds_ativo" in request.form
        dados["promofds"]["titulo"] = request.form.get("fds_titulo")
        dados["promofds"]["descricao"] = request.form.get("fds_descricao")

        # Salva alterações
        salvar_promocoes(dados)

        return redirect("/admin/promocoes")

    # GET → exibe painel
    dados = carregar_promocoes()
    return render_template("admin_promocoes.html", dados=dados)


# ================================
# ROTA ADMIN - RESET / DESBLOQUEIO
# ================================
@app.route("/admin/reset", methods=["GET", "POST"])
def admin_reset():

    admin = carregar_admin()

    # Se o formulário foi enviado
    if request.method == "POST":

        telefone = request.form.get("telefone")
        nova_senha = request.form.get("senha")

        # Confirma telefone
        if telefone == admin["telefone"]:

            # Atualiza senha e desbloqueia
            admin["senha"] = nova_senha
            admin["tentativas"] = 0
            admin["bloqueado"] = False

            salvar_admin(admin)

            return redirect("/admin/login")

        else:
            return render_template(
                "admin_reset.html",
                erro="Telefone incorreto"
            )

    return render_template("admin_reset.html")


# ================================
# ROTA ADMIN - LOGOUT
# ================================
@app.route("/admin/logout")
def admin_logout():

    # Remove login da sessão
    session.pop("admin_logado", None)

    # Redireciona para login
    return redirect("/admin/login")


# ================================
# EXECUÇÃO DO SERVIDOR
# ================================
if __name__ == "__main__":

    # Inicia o servidor Flask
    app.run(debug=True)
