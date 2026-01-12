# ================================
# IMPORTAÇÕES
# ================================

# Biblioteca para trabalhar com JSON
import json

# Biblioteca para trabalhar com datas
from datetime import datetime


# ================================
# CAMINHOS DOS ARQUIVOS
# ================================

# Caminho do arquivo de produtos
CAMINHO_PRODUTOS = "data/produtos.json"

# Caminho do arquivo de promoções
CAMINHO_PROMOCOES = "data/promocoes.json"

# Caminho do arquivo do admin
CAMINHO_ADMIN = "data/admin.json"


# ================================
# PRODUTOS
# ================================
def carregar_produtos():
    """
    Lê o arquivo produtos.json e retorna os produtos
    """

    with open(CAMINHO_PRODUTOS, encoding="utf-8") as f:
        return json.load(f)


# ================================
# PROMOÇÕES
# ================================
def carregar_promocoes():
    """
    Lê o arquivo promocoes.json e retorna os dados
    """

    with open(CAMINHO_PROMOCOES, encoding="utf-8") as f:
        return json.load(f)


def salvar_promocoes(dados):
    """
    Salva os dados de promoções no arquivo JSON
    """

    with open(CAMINHO_PROMOCOES, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def verificar_promocao():
    """
    Decide qual promoção deve aparecer no site:
    - Promoção de fim de semana
    - Promoção da semana
    - Ou nenhuma
    """

    dados = carregar_promocoes()

    # Descobre o dia da semana (0 = segunda, 6 = domingo)
    dia = datetime.now().weekday()

    # Se for sábado ou domingo
    if dia >= 5 and dados["promofds"]["ativo"]:
        return dados["promofds"]

    # Se for dia de semana
    if dados["promocao"]["ativo"]:
        return dados["promocao"]

    # Se nenhuma promoção estiver ativa
    return None


# ================================
# ADMIN (LOGIN)
# ================================
def carregar_admin():
    """
    Lê os dados do admin.
    Se o arquivo não existir, cria um padrão.
    """

    try:
        with open(CAMINHO_ADMIN, encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        # Estrutura inicial do admin
        admin_padrao = {
            "criado": False,
            "usuario": "",
            "senha": "",
            "telefone": "",
            "tentativas": 0,
            "bloqueado": False
        }

        # Salva o arquivo pela primeira vez
        salvar_admin(admin_padrao)

        return admin_padrao


def salvar_admin(dados):
    """
    Salva os dados do admin no arquivo JSON
    """

    with open(CAMINHO_ADMIN, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
