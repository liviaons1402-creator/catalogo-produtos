from flask import Flask, render_template, redirect, request, url_for
import sqlite3
import base64

app = Flask(__name__)

def conexao():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    
    return render_template("admin/index.html")




@app.route("/listar_categorias")
def listarCategoria():
    conn = conexao()
    categoria = conn.execute("select * from categoria")
    return render_template("admin/listar_categoria.html", categorias=categoria)


@app.route("/listar_produtos")
def listarProdutos():
    conn = conexao()
    produto = conn.execute(
        """SELECT produto.*, categoria.nome AS nome_categoria
                              FROM produto
                              LEFT JOIN categoria ON produto.id_categoria = categoria.id"""
    ).fetchall()
    conn.close()
    return render_template("admin/listar_produtos.html", produto=produto)


@app.route("/cadastrar_categorias", methods=["GET", "POST"])
def cadastrarCategoria():

    if request.method == "POST":
        nome_categoria = request.form.get("nome_categoria")
        descricao = request.form.get("descricao")
        ativo = request.form.get("ativo")
        imagem = request.files.get("imagem")
        imagem_base64 = base64.b64encode(imagem.read()).decode("utf-8")
        if nome_categoria:
            conn = conexao()
            conn.execute(
                """INSERT INTO categoria (nome, descricao, 
             ativo, imagem )
              VALUES (?, ?, ?, ?)""",
                (nome_categoria, descricao, ativo, imagem_base64),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("listarCategoria"))

    return render_template("admin/cadastrar_categoria.html")


@app.route("/cadastrar_produto", methods=["GET", "POST"])
def cadastrarProduto():
    conn = conexao()
    if request.method == "POST":
        nome_produto = request.form.get("nome_produto")
        preco = request.form.get("preco")
        id_categoria = request.form.get("categoria")
        ativo = request.form.get("ativo")
        imagem = request.files.get("imagem")
        imagem_base64 = (
            base64.b64encode(imagem.read()).decode("utf-8") if imagem else ""
        )
        if nome_produto:
            conn.execute(
                "INSERT INTO produto (nome, preco, ativo, imagem, id_categoria) VALUES (?,?,?,?,?)",
                (nome_produto, preco, ativo, imagem_base64, id_categoria),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("listarProdutos"))
    categorias = conn.execute("SELECT * FROM categoria").fetchall()

    produto = conn.execute("SELECT * FROM produto").fetchall()

    conn.close()

    return render_template(
        "admin/cadastrar_produtos.html", produto=produto, categorias=categorias
    )


@app.route("/editarcategoria/<int:id>", methods=["GET", "POST"])
def editarCategoria(id):
    conn = conexao()
    categoria = conn.execute("select * from categoria where id=?", (id,)).fetchone()

    if request.method == "POST":
        nome_categoria = request.form.get("nome_categoria")
        descricao = request.form.get("descricao")
        ativo = request.form.get("ativo")
        imagem = request.files.get("imagem")
        imagem_base64 = base64.b64encode(imagem.read()).decode("utf-8")
        if nome_categoria:
            conn = conexao()
            if imagem:
                conn.execute(
                    """UPDATE categoria SET nome=?, descricao=?,
                              ativo=?,
                              imagem=? WHERE id=?""",
                    (
                        nome_categoria,
                        descricao,
                        ativo,
                        imagem_base64,
                        id,
                    ),
                )
            else:
                conn.execute(
                    """UPDATE categoria SET nome=?, descricao=?,
                              ativo=? WHERE id=?""",
                    (
                        nome_categoria,
                        descricao,
                        ativo,
                        id,
                    ),
                )

            conn.commit()
            conn.close()
            return redirect(url_for("listarCategoria"))

    return render_template("admin/editar_categoria.html", categoria=categoria)

@app.route("/editarProduto/<int:id>", methods=["GET", "POST"])
def editarProduto(id):
    conn = conexao()
    produto = conn.execute(
        "SELECT * FROM produto WHERE id = ?", (id,)
    ).fetchone()

    if request.method == "POST":
        nome_produto = request.form.get("nome_produto")
        preco = request.form.get("preco")
        ativo = request.form.get("ativo")
        imagem = request.files.get("imagem")

        if nome_produto:
            if imagem and imagem.filename:
                imagem_base64 = base64.b64encode(imagem.read()).decode("utf-8")
                conn.execute(
                    """UPDATE produto
                       SET nome = ?, preco = ?, ativo = ?, imagem = ?
                       WHERE id = ?""",
                    (
                        nome_produto,
                        preco,
                        ativo,
                        imagem_base64,
                        id,
                    ),
                )
            else:
                conn.execute(
                    """UPDATE produto
                       SET nome = ?, preco = ?, ativo = ?
                       WHERE id = ?""",
                    (
                        nome_produto,
                        preco,
                        ativo,
                        id,
                    ),
                )

            conn.commit()
            conn.close()
            return redirect(url_for("listarProdutos"))

            conn.close()
    return render_template("admin/editar_produto.html", produto=produto)



@app.route("/excluir_categoria/<int:id>", methods=["GET", "POST"])
def excluirCategoria(id):
    conn = conexao()
    categoria = conn.execute(
        """SELECT * FROM categoria
          WHERE id = ?""",
        (id,),
    ).fetchone()

    if request.method == "POST":
        conn.execute("DELETE FROM categoria WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for("listarCategoria"))

    return render_template("admin/excluir_categoria.html", categoria=categoria)

@app.route("/excluir_produto/<int:id>", methods=["GET", "POST"])
def excluirProduto(id):
    conn = conexao()
    produto = conn.execute(
        """SELECT * FROM produto
          WHERE id = ?""",
        (id,),
    ).fetchone()

    if request.method == "POST":
        conn.execute("DELETE FROM produto WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for("listarProdutos"))

    return render_template("admin/excluir_Produto.html", produto=produto)

@app.route("/home")
def home():
    conn = conexao()
    produto = conn.execute(
        """SELECT produto.*, categoria.nome AS nome_categoria
           FROM produto
           LEFT JOIN categoria ON produto.id_categoria = categoria.id
           ORDER BY produto.preco ASC
           LIMIT 4"""
    ).fetchall()
    categoria = conn.execute("SELECT * FROM categoria ORDER BY nome").fetchall()
    conn.close()

    return render_template("site/index.html", produto=produto, categoria=categoria)

@app.route("/categorias")
def categorias():
    conn = conexao()
    categoria = conn.execute("select * from categoria")
        
    return render_template("site/categorias.html", categorias=categoria)

@app.route("/produtos")
def produtos():
    conn = conexao()
    busca = request.args.get("q", "").strip()
    categoria_selecionada = request.args.get("categoria", type=int)
    ordem = request.args.get("ordem", "menor-preco")
    consulta = """SELECT produto.*, categoria.nome AS nome_categoria
                  FROM produto
                  LEFT JOIN categoria ON produto.id_categoria = categoria.id
                  WHERE 1 = 1"""
    parametros = []

    if busca:
        consulta += " AND (produto.nome LIKE ? OR categoria.nome LIKE ?)"
        parametros.extend((f"%{busca}%", f"%{busca}%"))

    if categoria_selecionada is not None:
        consulta += " AND produto.id_categoria = ?"
        parametros.append(categoria_selecionada)

    ordenacoes = {
        "menor-preco": "produto.preco ASC",
        "maior-preco": "produto.preco DESC",
        "nome": "produto.nome COLLATE NOCASE ASC",
    }
    if ordem not in ordenacoes:
        ordem = "menor-preco"
    consulta += f" ORDER BY {ordenacoes[ordem]}"

    produto = conn.execute(consulta, parametros).fetchall()
    categorias = conn.execute("SELECT * FROM categoria ORDER BY nome").fetchall()
    conn.close()

    return render_template(
        "site/produtos.html",
        produto=produto,
        categorias=categorias,
        busca=busca,
        categoria_selecionada=categoria_selecionada,
        ordem=ordem,
    )

@app.route("/verCategoria/<int:id>",methods=["GET", "POST"])
def verCategoria(id):
    conn = conexao()
    cursor = conn.cursor()
    categoria = conn.execute(
            """SELECT * FROM categoria
              WHERE id = ?""",
            (id,),
        ).fetchone()
    produto = cursor.execute(
        "SELECT * FROM produto WHERE id_categoria = ?",
        (id,)
    ).fetchall()
    conn.close()
        
    return render_template("site/verCategoria.html", categorias=categoria,produto=produto)
    



app.run(debug=True, port=5005)
